./airflow.sh airflow connections delete 'source_db'
./airflow.sh airflow connections delete 'target_db'

./airflow.sh airflow connections add 'source_db' \
    --conn-json '{
        "conn_type": "postgres",
        "login": "postgres",
        "password": "postgres",
        "host": "airflow_etl_source_db_1",
        "port": 5432,
        "schema": "public",
        "extra": {
            "table": "persons",
            "database": "postgres"
        }
    }'
    
./airflow.sh airflow connections add 'target_db' \
    --conn-json '{
        "conn_type": "postgres",
        "login": "postgres",
        "password": "postgres",
        "host": "airflow_etl_target_db_1",
        "port": 5432,
        "schema": "public",
        "extra": {
            "table": "persons",
            "database": "postgres"
        }
    }'
