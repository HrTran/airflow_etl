import json

import pandas as pd
import pendulum

from airflow.decorators import dag, task

from common.modules.connector.Postgres import Postgres


@dag(
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 5, 8, tz="UTC"),
    catchup=False,
    tags=['example'],
)
def simple_taskflow_api_etl():
    def convert_json_to_sql(fields_json):
        output = ""
        for item in fields_json:
            field_name = item['name']
            if isinstance(field_name, list):
                output += ", ".join(field_name)
        return output

    @task()
    def extract(input_config):
        output = {}
        for item in input_config:
            if item['type'] == 'postgres':
                connection = Postgres(item['db'])
                for table in item['select']:
                    table_name = table['table']
                    fields = convert_json_to_sql(table['fields'])
                    query = f"SELECT {fields} FROM {table_name}"
                    print(f"Execute: {query}\n")
                    data = connection.read_dataframe(query)
                    output[table_name] = data.to_dict()
                connection.disconnect()

        return output

    @task()
    def transform(transform_config, tables):
        for item in transform_config:
            table_name = item['table']
            for ops in item['operations']:
                df = pd.DataFrame.from_dict(tables[table_name])
                df = df.eval(ops)
                tables[table_name] = df.to_dict()
        return tables

    @task()
    def load(output_config, tables):
        for item in output_config:
            if item['type'] == 'postgres':
                df = pd.DataFrame.from_dict(tables[item['table']])
                write_mode = item['write_mode']
                connection = Postgres(item['db'])
                connection.write_dataframe(df, write_mode)
                connection.disconnect()

    with open('./entries/etl.json') as f:
        config = json.load(f)
        if config['isDisable']:
            return
        extract_data = extract(config['input'])
        transform_data = transform(config['transformation'], extract_data)
        load(config['output'], transform_data)


simple_etl_dag = simple_taskflow_api_etl()
