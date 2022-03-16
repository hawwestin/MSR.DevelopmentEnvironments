# Remote ready Elastic cluster
This directory holds a version of elastic with and without security enabled.

## WSL

By default running Elastic on WSL will cause an error preventing it from running `max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]` 
To fix it execute below command in powershell 
```
wsl -d docker-desktop
sysctl -w vm.max_map_count=262144
```
And for the persistence configuration
```
echo "vm.max_map_count=262144" >> /etc/sysctl.conf
```

## Compose yamls

`docker-compose.yml` Holds not secured configuration. For version below 8 it is valid and fastest way to set up and runing cluster.

`docker-compose.ssl.yml` Holds minimum security with password, transport layer ssl between nodes on 9300 port and https for 9200 port communication. To use this remember to use basic authorization user with password when you comunicate with elastic API directly. And do not forget to change HTTP 9200 to HTTPS in your favority tool 😉 Kiabana use https for 5601 port over generted wild card certificate. 

**Please be advise** that password for account need to be provided for all stack application like Kibana and Beats. Example generic password is provided via `.env` file for admin account `elastic`. After you log in to cluster you can change password to other build in users or create new one for kibana nad beats. 

## Configuration files 
**.env**
| Variable  | default  | description/Effect | 
|---|---|---|
| ELK_VERSION | 7.16.3 | Convinient way to use the same version accross all composes and update them once |
| COMPOSE_PROJECT_NAME | elk  | Stack name that will run Elastic search cluster. In case that this docker-compose will be executed in different directory as default project name is directory name if not provided. Its purpose is to holds volumes with certifcates in same namespace. |
| CERTS_DIR  | /usr/share/elasticsearch/config/certificates  | Path for volume mounting with generated certs. |
| ELASTIC_PASSWORD | PleaseChangeMe  | Default password for `elastic` user  |
| KIBANA_CERT_PASSWORD | PleaseChangeMe  | Default password for `elastic` user. As this and ELASTIC_PASSWORD can holds different values you have two variable keys to have this option. |