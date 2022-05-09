# Airflow ETL
ETL practice with Airflow, Docker Compose

## Architecture
For more details, please take a look at [architecture](docs/architecture.md)

## Information
* Install [Docker](https://www.docker.com/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

## Deployment
* Initialize environment
```bash
mkdir -p ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
* Initialize database
```bash
docker-compose -f airflow.yaml up airflow-init
```
* Running Airflow
```bash
docker-compose -f airflow.yaml up -d
docker-compose -f postgres.yaml up -d
```
* Initialize environment
```bash
./init/env.sh
```
* Now find the DAG named `simple_taskflow_api_etl` and trigger it. 
## DAGs
All the DAGs are in the folder `dags`, and the configuration files are store in folder `entries`. Each configuration 
file is corresponding to a DAG.

Config entries followed by this [entries_guide](entries/entries_guide.md)

## Configuring connections
Add the following line to `./init/env.sh` 
```bash
./airflow.sh airflow connections add <source-name> \
    --conn-json '{
        "conn_type": "<conn-type>",
        "login": "<username>",
        "password": "<password>",
        "host": "<host>",
        "port": <port>,
        "schema": "<schema>",
        "extra": {
            "table": "<table-name>",
            "database": "<db-name>"
        }
    }'
```

## Additional info
* Running CLI commands
```bash
./airflow.sh python
```
* Clean environment
```bash
docker-compose down --volumes --rmi all
```
* Update modules code
  * Re-build whl file 
    ```bash
     python setup.py bdist_wheel
    ```
  * Re-build docker images
    ```bash
    docker-compose -f airflow.yaml build --no-cache
    ```
* Scale worker to 3
```bash
docker-compose -f airflow.yaml --scale airflow-worker=3 up -d
```

## Contact me
:mailbox: Mail: [trantathuy.hust@gmail.com](mailto:trantathuy.hust@gmail.com)  
:technologist: Linkedin: [Huy Tran](https://www.linkedin.com/in/trantathuy/)