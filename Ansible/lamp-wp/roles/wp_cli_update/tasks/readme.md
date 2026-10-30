# Manual WordPress updates with WP-CLI

Use this runbook when you need to update a WordPress server manually over SSH.
Run the commands as a user with `sudo` access. Replace `/var/www/html` with the
document root of the WordPress site.

## 1. Set the WordPress path

```bash
export WEB_ROOT=/var/www/html
cd "$WEB_ROOT"
```

Confirm that this is the correct installation before proceeding:

```bash
sudo -u www-data -- wp --path="$WEB_ROOT" core version
```

## 2. Install WP-CLI if it is missing

The Ansible role installs WP-CLI at `/usr/local/bin/wp` only when it is absent.
Check for it first:

```bash
command -v wp
```

If the command is not found, install the PHAR in the same location as the role:

```bash
sudo curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
sudo chmod 0755 /usr/local/bin/wp
```

Verify the installation:

```bash
wp --info
```

## 3. Update WordPress core

```bash
sudo -u www-data -- wp --path="$WEB_ROOT" core update
```

## 4. Update the WordPress database

Run this after updating core:

```bash
sudo -u www-data -- wp --path="$WEB_ROOT" core update-db
```

## 5. Update plugins

Updates all plugins except Contact Form 7, matching the Ansible role:

```bash
sudo -u www-data -- wp --path="$WEB_ROOT" plugin update --all --exclude=contact-form-7
```

If WP-CLI reports that no plugins were updated, there may simply be no eligible
plugin updates available.

## 6. Update themes

```bash
sudo -u www-data -- wp --path="$WEB_ROOT" theme update --all
```

## 7. Verify the site versions

```bash
sudo -u www-data -- wp --path="$WEB_ROOT" core version
sudo -u www-data -- wp --path="$WEB_ROOT" plugin list --update=available
sudo -u www-data -- wp --path="$WEB_ROOT" theme list --update=available
```

## 8. Check the PHP versions

Check the default PHP CLI version. This is the PHP version used by WP-CLI:

```bash
php -v
readlink -f "$(command -v php)"
sudo update-alternatives --display php
```

For an Apache `mod_php` setup, check which PHP module is enabled:

```bash
sudo apache2ctl -M | grep php
ls -l /etc/apache2/mods-enabled/php*.load
```

To check the PHP version actually serving WordPress requests, sign in to
WordPress and open **Tools > Site Health > Info > Server**. Read the **PHP
version** value there. This is the web-server runtime; it can differ from the
CLI version shown by `php -v`.

## 9. Check clock synchronization and set the timezone

Check the server's local and UTC time, timezone, and NTP synchronization status:

```bash
date
date -u
timedatectl status
```

If the server uses `systemd-timesyncd`, inspect its synchronization details and
reported clock offset:

```bash
timedatectl timesync-status
```

If it uses Chrony instead, check the time source and estimated clock offset:

```bash
chronyc tracking
chronyc sources -v
```

Set the timezone to Warsaw time. It will use CET in winter and CEST during
daylight-saving time:

```bash
sudo timedatectl set-timezone Europe/Warsaw
timedatectl
date '+%Z %z %Y-%m-%d %H:%M:%S'
```

Use the IANA timezone for the server's actual location if it is not in Poland.
For example, `Europe/Berlin` also switches between CET and CEST automatically.