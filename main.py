from curl_cffi import requests
import time
import random
import os

ENV_FILE = ".env"
BASE_URL = "https://api.prod.biedronka.cloud/api/v7"
AUTH_URL = "https://konto.biedronka.pl/realms/loyalty/protocol/openid-connect/token"
USER_AGENT = "iOS/2.24.0"


def load_env():
    env_vars = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


def update_env(key, value):
    env_vars = load_env()
    env_vars[key] = value
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")


def send_discord_webhook(webhook_url, activated_offers):
    if not webhook_url or not activated_offers:
        return

    description = "\n".join([f"✅ **{offer}**" for offer in activated_offers])
    payload = {
        "embeds": [
            {
                "title": "🎉 Biedronka Offers Activated!",
                "description": description,
                "color": 15158332,
                "footer": {"text": "@fixedzik/biedronka-opener"}
            }
        ]
    }
    try:
        requests.post(webhook_url, json=payload, impersonate="safari_ios")
    except:
        pass


def get_fresh_tokens(session, refresh_token):
    print("Refreshing access token...")
    payload = {
        "client_id": "cma20",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT
    }

    response = session.post(AUTH_URL, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        new_access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token")

        if new_refresh_token and new_refresh_token != refresh_token:
            update_env("REFRESH_TOKEN", new_refresh_token)

        print("Access token generated.")
        return new_access_token

    print(f"Token refresh failed ({response.status_code})")
    return None


def fetch_and_activate_offers(session, access_token):
    base_headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "pl-PL",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    dashboard_url = f"{BASE_URL}/dashboards/dashboard/"
    print("Fetching dashboard...")

    dashboard_response = session.get(dashboard_url, headers=base_headers)
    if dashboard_response.status_code != 200:
        print(f"Dashboard fetch failed: {dashboard_response.status_code}")
        return []

    dashboard_data = dashboard_response.json()
    sections = dashboard_data.get("sections", [])

    carousel_ids = [s.get("param") for s in sections if s.get("type") == "Carousels" and s.get("param")]

    if not carousel_ids:
        print("Nie znaleziono żadnych karuzel.")
        return []

    activated_in_this_run = []

    for cid in carousel_ids:
        carousel_url = f"{BASE_URL}/promos/carousels/{cid}/"
        carousel_response = session.get(carousel_url, headers=base_headers)

        if carousel_response.status_code != 200:
            continue

        items = carousel_response.json().get("items", [])
        offers_to_activate = [item for item in items if "offer_id" in item]

        for offer in offers_to_activate:
            offer_id = offer.get("offer_id")
            offer_type = offer.get("offer_type", "SHAKEOMAT")

            print(f"Checking state: {offer_type} ({offer_id})")
            check_url = f"{BASE_URL}/offers/{offer_id}/check-activation/"
            session.get(check_url, headers=base_headers)

            time.sleep(random.uniform(1.0, 2.0))

            print(f"Activating: {offer_type} ({offer_id})")
            activate_url = f"{BASE_URL}/offers/{offer_id}/reveal-and-activate/"

            patch_headers = base_headers.copy()
            patch_headers["Content-Type"] = "application/json"

            activate_response = session.patch(activate_url, headers=patch_headers)

            if activate_response.status_code in [200, 204]:
                print("✅ Activation successful.")
                product_name = offer_type
                try:
                    data = activate_response.json()
                    product_name = data.get("name") or data.get("title") or offer_type
                except:
                    pass
                activated_in_this_run.append(product_name)
            elif activate_response.status_code in [400, 409]:
                print("⚠️ Offer already activated.")
            else:
                print(f"❌ Activation failed ({activate_response.status_code}) - {activate_response.text.strip()}")

            time.sleep(random.uniform(4.5, 6.0))

    print("Process finished.")
    return activated_in_this_run


if __name__ == "__main__":
    env_vars = load_env()
    current_refresh_token = env_vars.get("REFRESH_TOKEN")
    webhook_url = env_vars.get("DISCORD_WEBHOOK_URL")

    if not current_refresh_token:
        print("REFRESH_TOKEN not found in .env")
    else:
        session = requests.Session(impersonate="safari_ios")

        access_token = get_fresh_tokens(session, current_refresh_token)

        if access_token:
            all_activated_offers = []

            while True:
                new_offers = fetch_and_activate_offers(session, access_token)

                if new_offers:
                    all_activated_offers.extend(new_offers)
                    print("\nWaiting 90 seconds for next activation...\n")
                    time.sleep(90)
                else:
                    print("\nNo more new offers available. Exiting script.")
                    break

            if all_activated_offers and webhook_url:
                send_discord_webhook(webhook_url, all_activated_offers)