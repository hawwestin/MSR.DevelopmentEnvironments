# SSL Certificates for HTTPS

## How to generate certificates 
File `create.sh` holds a command to execute docker-compose.certificates.yml with required parameters. 

## Configuration files 
**.env**
| Variable  | default  | description/Effect | 
|---|---|---|
| COMPOSE_PROJECT_NAME | elk  | Stack name that will run Elastic search cluster. In case that this docker-compose will be executed in different directory as default project name is directory name if not provided.  |
| CERTS_DIR  | /usr/share/elasticsearch/config/certificates  | Path for volume mounting with generated certs. |
| ELASTIC_PASSWORD | PleaseChangeMe  | Default password for `elastic` user  |
| INSTANCES_FILE  | instances-1node.yml  | List of services that need generated SSL certificates. 3 node alternative is provided as one node is rather for local host development.  |
| REGENERATE_CERT | False  | In case you need to re/generate additional certificats after you add /remove services in Instances_File switch it to True and execut again `create.sh` script. |
----
**instances-Xnode.yml**
Yaml file that is used by `bin/elasticsearch-certutil` to generate crt and key files for given list of named services like Elastic and Kibana. 

