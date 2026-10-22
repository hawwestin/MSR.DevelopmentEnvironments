# PHP deployment

The `webserver` role installs the PHP minor selected by `php_version`, defaulting to 8.4. It uses `ppa:ondrej/php` so Ubuntu 22.04 and 24.04 do not silently use different distro-default PHP versions. Set `php_version` in inventory to use another supported minor, such as `"8.2"` for application compatibility.

The role enables the matching Apache module and selects the same CLI alternative. To verify the deployed configuration:

```bash
php -v
php -m
apache2ctl -M | grep php
sudo systemctl is-active apache2
```

# manual runbook 
## 0. APT sources for 8+
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update

sudo apt install php8.2 libapache2-mod-php8.2 php8.2-mysql php8.2-curl php8.2-xml php8.2-mbstring php8.2-gd php8.2-zip php8.2-intl -y



## 1. Wylaczenie modulu starej wersji (z Ubuntu 20.04)
sudo a2dismod php7.4

## 2. Wlaczenie modulu nowej wersji (domyslnej dla Ubuntu 22.04)
sudo a2enmod php8.2

## 3. Restart serwera, aby zastosowac zmiany
sudo systemctl restart apache2

## 4. Change terminal php version
sudo update-alternatives --set php /usr/bin/php8.2


## X. Update OS
sudo do-release-upgrade


## Y Revert
sudo a2dismod php8.2
sudo a2enmod php7.4
sudo systemctl restart apache2
sudo update-alternatives --set php /usr/bin/php7.4

