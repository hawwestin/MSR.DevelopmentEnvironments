# PHP deployment

The `webserver` role supports Ubuntu 22.04 and 24.04 and installs the PHP minor selected by `php_version`, defaulting to 8.4. It uses `ppa:ondrej/php` so those releases do not silently use different distro-default PHP versions. Ubuntu 20.04 is not supported by this PHP package source; upgrade the host before running this role. Set `php_version` in inventory to use another supported minor, such as `"8.4"` for application compatibility.

The role enables the matching Apache module and selects the same CLI alternative. To verify the deployed configuration:

```bash
php -v
php -m
apache2ctl -M | grep php
sudo systemctl is-active apache2
```

# manual runbook 
## X. Update OS
```bash
sudo do-release-upgrade

lsb_release -a 
uname -a
```
## 0. APT sources for 8+
This and other points are in ansible. This references are for SSH VPS that are not ansible driven. 
```bash
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update

sudo apt install php8.4 libapache2-mod-php8.4 php8.4-mysql php8.4-curl php8.4-xml php8.4-mbstring php8.4-gd php8.4-zip php8.4-intl -y
```

## 1. Wylaczenie modulu starej wersji (z Ubuntu 20.04)
```bash
sudo a2dismod php7.4
```
## 2. Wlaczenie modulu nowej wersji (domyslnej dla Ubuntu 22.04)
```bash
sudo a2enmod php8.4
```
## 3. Restart serwera, aby zastosowac zmiany
```bash
sudo systemctl restart apache2
```
## 4. Change terminal php version
```bash
sudo update-alternatives --set php /usr/bin/php8.4
```

## Y Revert
```bash
sudo a2dismod php8.4
sudo a2enmod php7.4
sudo systemctl restart apache2
sudo update-alternatives --set php /usr/bin/php7.4
```
