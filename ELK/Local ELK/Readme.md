# Local host Elastic stack
This directory holds a few version of elastic one node cluster security that can be configured for elastic search and kibana. 

## WSL

By default running Elastic on WSL will cause an error preventing it from running `max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]` 
To fix it execute below command in powershell 
```
wsl -d docker-desktop
sysctl -w vm.max_map_count=262144
```

## Compose yamls

`docker-compose.yml` Holds not secured configuration. For version below 8 it is valid and fastest way to set up and run local stack.

`docker-compose.9300-ssl.yml` Holds minimum security with password and transport layer between nodes on 9300 port. As this is one node instance it is rather an example of valid configraution. 
**Please be advise** that password for admin account `elastic` need to be provided for all stack application like Kibana and Beats. Example generic password is provided via `.env` file

`docker-compose.9200-ssl.yml` All benefits of 9300-ssl comose and https for 9200 port communication. After you use this please use basic security with password and user when you will comunicate with elastic API directly. And do not forget to change HTTP to HTTPS in your favority tool 😉

`docker-compose.5601-ssl.yml` All benefits of 9200-ssl compose and https for 5601 Kibana web port over generted wild card certificate. 

## Configuration files 
**.env**
| Variable  | default  | description/Effect | 
|---|---|---|
| ELK_VERSION | 7.16.3 | Convinient way to use the same version accross all composes and update them once |
| COMPOSE_PROJECT_NAME | elk  | Stack name that will run Elastic search cluster. In case that this docker-compose will be executed in different directory as default project name is directory name if not provided. Its purpose is to holds volumes with certifcates in same namespace. |
| CERTS_DIR  | /usr/share/elasticsearch/config/certificates  | Path for volume mounting with generated certs. |
| ELASTIC_PASSWORD | PleaseChangeMe  | Default password for `elastic` user  |
| KIBANA_CERT_PASSWORD | PleaseChangeMe  | Default password for `elastic` user. As this and ELASTIC_PASSWORD can holds different values you have two variable keys to have this option. |