# General

References 
[Official project page](https://nginxproxymanager.com/)

## Default Administrator User

Email:    `admin@example.com`\
Password: `changeme`

Immediately after logging in with this default user you will be asked to modify your details and change your password.
# Best Practice: 
## Use a Docker network
For those who have a few of their upstream services running in Docker on the same Docker host as NPM, here's a trick to secure things a bit better. By creating a custom Docker network, you don't need to publish ports for your upstream services to all of the Docker host's interfaces.

Create docker network named "ngingProxyManager"
```
docker network create ngingProxyManager
```
Then add the following to the docker-compose.yml file for both NPM and any other services running on this Docker host:
```
networks:
  default:
    external:
      name: ngingProxyManager
```      
In other containers to attach to that network please add following to container
```
    networks:
      - ngproxy
```
And declare external network at the bottom. 
```
networks:
  ngproxy:
    external:
      name: ngproxy
```

## Docker Secrets

This image supports the use of Docker secrets to import from file and keep sensitive usernames or passwords from being passed or preserved in plaintext. Add folowing at the begining of docker-compose.yml file: 
```
secrets:
  # Secrets are single-line text files where the sole content is the secret
  # Paths in this example assume that secrets are kept in local folder called ".secrets"
  DB_ROOT_PWD:
    file: .secrets/db_root_pwd.txt
  MYSQL_PWD:
    file: .secrets/mysql_pwd.txt
```

You can set any environment variable from a file by appending `__FILE` (double-underscore FILE) to the environmental variable name.
```
    environment:
      MYSQL_ROOT_PASSWORD__FILE: /run/secrets/DB_ROOT_PWD
      MYSQL_PASSWORD__FILE: /run/secrets/MYSQL_PWD
```
# DNS configuration
Reverse proxy is a tool that can obscure IP address and port with user firendly and not changing name. 
## Cloudflare
For self hosting websites. Requirements
- You need to own domain name 

On dashboard go through wizzard of adding domain. At your domain name provider change pointing of name server records to cloudflare. \
On DNS panel of your new added domain add record with domain that points to your homelab IP. It is recommended to set full predefined sceuirty level.\
On your firewall / Router you need to point port 443 (80 is HTTP, and if you can you should avoid it) to Ip address of NginxProxyManager host. \
Now load in browser your domain address and you should see Congratulations page of successful configuration. Cheers!

You can add 'A' records or Cname of `service.yourdomain.com` directly on cloudflare dns tab. Second option is to create wildcard records `*.yourdomain.com` and points all possible domains to NginxProxyManager. \
In first scenario you need to manually add each time new record on DNS of cloud flare. But you will not acceidentaly expose site that should not be public. When somebody will try to access `null.yourdomain.com` he will hit a cloudflare error page or just browser not found message. \
In second scenario cloudflare will proxy everything and not existing domains need to be handled by Nginx. In such scenario you can point such ppl to custom domain for example on your main address `yourdomain.com` so in case of user error he will get sth from you. This should be monitored becouse all healthchecks will be green as some page responded 200 but this may be not the site that you expect. 

## Internal DNS from Pihole with Cname records. 
Local network domain name resolution can be handled by pihole. To apply such configuration you have to have reliable host serving DNS or a pair of them to fufill primary and secondary dns record in your router. Also you need to sync or manually apply changes to DNS records to both of them. 

### Internal domain name
If you does not plan to self host services you can configure pihole. In dns tab add a record that points your local domain for examle `home.lab` to IP address of nginxProxyManager host. You can chose whatever you like and fits your homelab spirit. 

Then on Cname Tab you provide name of service and reverse proxy. For example add records like 
`portainer.home.lab` that points to 'A' DNS record of `home.lab`.  Pihole has limitations that does not accept wildcards that will resolve all services on `*.home.lab` to provided DNS record. But still it is deacent solution for local environment. 

Last step is to use Reverse proxy. Add reverse proxy records on NginxProxyManager that point to psyhical address and port of given service with usage of DNS records added to Pihole. Now if you open such address it should go through nginx and load your service. Cheers!\
To add any other site you need to repeat adding Cname record in Pihole and then record in NginxProxyManager. 


### Public domain name over internal dns
Even if you does not plan to self host publicly any services you still may found out owning public domain name usefull. 
This approach is to obscure cloudflare dns with your own. This way instead of `home.lab` you can use `yourdomain.com`. Configuration is the same as for `home.lab` you can point both domain to same IP address and in Nginx record add two Domain names. This way you can distinguish self hosted and internal only sites and mixed. In case of lack of internet connection your domain will be handled back by pihole manually added records. But this can obscure any potential issues with cloudflare as for you those site will be working. 

# LetsEncrypt
Obtain new certificate for your domain. 
## Through DNS on cloudflare. 
During optaining certificate for 'A' record your DNS in cloudflare cannot be in `proxy` mode but in `DNS only` mode. So that letsencrypt can connect directly to you. After that you can switch it back to `proxy`. \
If you try to obtain wildcard certificate for `*.mydomain.com` you need to create CloudFlare API token with permission to `Edit zone DNS`. Generated PAT is displayed only once so don't lose it and copy it directly to letsencrypt window in NGINXproxyManger. After few seconds you should have new certificate for wildcard domains that you can secure your local homelab services. 

## With Pihole internall dns. 
You probably cannot buy such simple domain for `home.lab`. Therefore if your not self host but use some services only internally you can use selfsigned certificates. Alternatively you can generate certificate manually and apply it to nginx.\
Recommended option is to use your public domain wildcard SSL. In such scenario after you obtain certificate you can close outside network connection to home lab. Then in pihole you can use `service.yourdomain.com` and in Nginx proxy chose wildcard certificate for `*yourdomain.com`. 

# Access List control

!! Attention section work in progress. Due to unexpected results after enabling access control with enabled Proxy over Cloudflare section for IP based filtering I could not made to work. Probably need to be added list of CLoudFlare addresses to the list instead of your public IP address. 
to be tested
- Add ip filtering on cloudflare level to homelab public IP address. 
## User access 

It is limited access to provided list of basic authentication pair Username:Password. Helpful over pages without authentication. Before enabling it is recommended to pair Fail2Ban with ngingProxyManager logs and autmatic IP blocking on Cloudflare. 
Test of such pair connection on HomeLab RoadMap. 

## IP address based filtering

Ip address with /24 mask for your local homelab. Mask of /32 need to be used for single IP. For Example your public address.

