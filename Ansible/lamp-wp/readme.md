ansible/lamp-wp/
 ├── inventories/
 │    ├── hosts.ini
 │    ├── hosts_vars/
 │    └── group_vars/
 │        └── all.yml
 ├── roles/
 │    ├── common/          # apt update, base packets, timezone, firewall
 │    ├── webserver/       # Apache, PHP 7.4.3, modules
 │    ├── mysql/           # MySQL 8.0.41, user, db
 │    └── wordpress/       # install WP, perms, wp-config
 ├── playbooks/
 │    ├── 01-common.yml
 │    ├── 02-webserver.yml
 │    ├── 03-database.yml
 │    └── 04-migration.yml
 ├── vault/
 │    └── secrets.yml (Encrypted)
 └── files/
      └── wordpress-6.9.4.tar.gz



```bash
wget https://wordpress.org/wordpress-6.9.4.tar.gz -O files/wordpress-6.9.4.tar.gz
```

Backup Wordpress > 04-migration.yml
```bash
rsync -avz root@vps:/var/www/html/ /var/www/html/

```


Restore Database  > 04-migration.yml
```bash
mysql -u root -p wordpress < backup.sql
```

Fix permissions  > 04-migration.yml
```bash
chown -R www-data:www-data /var/www/html
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;

```

update url in database  > 04-migration.yml
TODO add to Ansible
```sql
UPDATE wp_options SET option_value='http://192.168.200.5' WHERE option_name='siteurl';
UPDATE wp_options SET option_value='http://192.168.200.5' WHERE option_name='home';

```

Things to check
 1. Same PHP version
 2. Same MySql version
 3. Set permissions for www-data user/group
 4. Set correct URL in database
 5. check .htaccess files , backups often miss those 
 6. Plugins and motives need to be in backup if were installed manually. 


