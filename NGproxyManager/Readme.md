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

Create a network, ie "ngingProxyManager":
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
