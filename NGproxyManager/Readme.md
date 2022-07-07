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

Create a network, ie "scoobydoo":
```
docker network create scoobydoo
```
Then add the following to the docker-compose.yml file for both NPM and any other services running on this Docker host:
```
networks:
  default:
    external:
      name: scoobydoo
```      

## Docker Secrets

This image supports the use of Docker secrets to import from file and keep sensitive usernames or passwords from being passed or preserved in plaintext.

You can set any environment variable from a file by appending `__FILE` (double-underscore FILE) to the environmental variable name.
