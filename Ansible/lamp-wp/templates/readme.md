# activete site and module

Honestly I don't know if wordpress need this. Need more testing with apache configuration and wordpress in deep dive some day. 

```bash
sudo a2enmod remoteip rewrite headers
sudo a2ensite wordpress.conf
sudo systemctl reload apache2
```

set RemoteIPTrustedProxy in wordpress configs/db to IP of HaProxy 