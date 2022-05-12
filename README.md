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

## Run the Example
* Now login to Airflow Webserver UI at http://localhost:5884 using user `airflow` and password `airflow` 
  * Find the DAG named `simple_taskflow_api_etl`, then trigger it.
    * Open any SQL editor such as [DBeaver](https://dbeaver.io/), add new PostgreSQL connection with following field:
      * source_db:
        ```bash
        user: postgres
        password: postgres
        database: postgres
        host: localhost
        port: 5432
        ```
      * target_db:
        ```bash
        user: postgres
        password: postgres
        database: postgres
        host: localhost
        port: 5433
        ```
    * Using `psql` — PostgreSQL interactive terminal
      * Install on Ubuntu and Debian
        ```bash
        sudo apt-get update
        sudo apt-get install postgresql-client
        ```
      * Open 2 terminals, one for `source_db` and one for `target_db`
        ```bash
        [Terminal 1]
        $ psql -h localhost -d postgres -U postgres -p 5432
        Password for user postgres: postgres
        psql (12.10 (Ubuntu 12.10-0ubuntu0.20.04.1), server 14.1)
        WARNING: psql major version 12, server major version 14.
                 Some psql features might not work.
        Type "help" for help.
  
        postgres=# select count(*) from public.persons;
         count 
        -------
          5000
        (1 row)
        ```
        ```bash
        [Terminal 2]
        $ psql -h localhost -d postgres -U postgres -p 5433
        Password for user postgres: postgres
        psql (12.10 (Ubuntu 12.10-0ubuntu0.20.04.1), server 14.1)
        WARNING: psql major version 12, server major version 14.
                 Some psql features might not work.
        Type "help" for help.
  
        postgres=# select count(*) from public.persons;
         count 
        -------
          5000
        (1 row)
        ```
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