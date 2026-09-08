<h1 align="center">
  biedronka-opener
  <br>
</h1>
<p align="center">
    <img src="./private/biedronka-512.png" alt="logo" width="128">
</p>

<h4 align="center">A Python script to automatically open biedronka promotional shakeomat and send loot notifications to Discord</h4>
<h3 align="center">DISCLAIMER!<br>This project is intended solely for educational purposes and does not encourage the penetration testing or reverse engineering of any applications.</h2>

<p align="center">
  <a href="#how-to-use">How to use</a> •
  <a href="#support">Support</a> •
  <a href="#support-the-developers">Support the Developers</a> •
  <a href="#license">License</a>
</p>

## How to use

INSTRUKCJA NIE ZROBIONA!! TO NIE DO TEGO!!

You must have [Docker](https://docs.docker.com/engine/install/debian/)

```bash
# Clone this repository
$ git clone https://github.com/fixedzik/x-kom-opener.git
```

```bash
# Fill your credentials file with your login, password and discord webhook
$ cd x-kom-opener
$ vim credentials
```

```bash
# Test your configuration
$ /usr/bin/docker compose build
$ /usr/bin/docker compose up
```

If no error occurs, it means that the script is working and can be connected to the system automation.

```bash
# Edit your crontab
$ crontab -e

# and paste this in the last line
0 8 * * * cd /root/x-kom-opener && /usr/bin/docker compose up >> /root/x-kom-opener/cron.log 2>&1
# (/root/x-kom-opener this is the path where I downloaded the repository)

# Restart crontab service
$ service cron restart # Debian/Ubuntu
$ rc-service crond restart # Alpine Linux
```

That's it! After all these steps, the script should run at 8:00am every day!

## Support

- Debian
- Ubuntu
- Alpine Linux
- Windows

## Support the Developers

<a href="https://supportme.fixed.ovh/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Support me!" style="height: 60px !important; width: 217px !important;" /></a>

## You may also like...

- [lamp-script](https://github.com/fixedzik/lamp-script) - Script to install the LAMP module in less than a minute!
- [eazbiuro-scraper](https://github.com/fixedzik/eazbiuro-scraper/tree/main) - A tool for extracting products from the eazbiuro.pl online store

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/fixedzik/biedronka-opener/blob/main/LICENSE) file for details.

---

> [fixed.ovh](https://fixed.ovh/) &nbsp;&middot;&nbsp;
> GitHub [@fixedzik](https://github.com/fixedzik)
