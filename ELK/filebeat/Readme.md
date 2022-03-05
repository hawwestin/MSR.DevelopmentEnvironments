# Filebeat docker configuration

Yaml configuration file was extracted from official downloaded zip. Please use yaml file instead of `docker-compose.yml` environemt section to provide variables for filebeat. Provide only values in .env file or envrionemnt section. 

Volume `applicationLogPath` is a stub to be connected from local host developed envrionemnt in other container stack. This can be hard mounted to directory with application logs if needed. You can mount as many as you want. 

Be advice that filebeat inputs yaml section need to be adjusted to  application directory schema as regex glob '\*' is for one level of directory depth.
