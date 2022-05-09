import pandas as pd
import psycopg2
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine


def get_postgres_uri(user, password, host, port, database):
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


class Postgres:
    def __init__(self, connection_name):
        self.name = connection_name
        self.options = self._get_options()
        self.conn = None
        self.cursor = None
        self.connect()

    def _get_options(self):
        connection = BaseHook.get_connection(self.name)
        extra = connection.extra_dejson
        return {
            "schema": connection.schema,
            "host": connection.host,
            "port": connection.port,
            "user": connection.login,
            "password": connection.password,
            "dbname": extra['database'],
            "table": extra['table'],
            "uri": get_postgres_uri(connection.login, connection.password, connection.host, connection.port,
                                    extra['database'])
        }

    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.options['dbname'],
                                         user=self.options['user'],
                                         password=self.options['password'],
                                         host=self.options['host'],
                                         port=self.options['port'])
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"SET SCHEMA '{self.options['schema']}'")
            self.conn.commit()
        except Exception as e:
            raise Exception("Error connecting to the database.")

    def _is_connected(self):
        try:
            return self.conn is not None and self.cursor is not None
        except:
            return False

    def disconnect(self):
        if self._is_connected():
            try:
                self.cursor.close()
                self.conn.close()
            except Exception as e:
                raise Exception("There is a problem disconnecting from the database")
        else:
            print("No connection to close")

    def execute(self, query):
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error execute query {query}. Err={type(e).__name__}: {str(e)} ")
            raise Exception(f"Cannot execute query: {query}")

    def read_dataframe(self, query):
        print(f"Connection uri: {self.options['uri']}\n")
        db = create_engine(self.options['uri'])
        conn = db.connect()
        return pd.read_sql(query, conn)

    def write_dataframe(self, dataframe, mode):
        """
        Write the existing dataframe to Postgres

        :param dataframe: Pandas dataframe
        :param mode: ‘fail’, ‘replace’, ‘append’.
        Follow by: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
        """
        db = create_engine(self.options['uri'])
        conn = db.connect()
        dataframe.to_sql(self.options['table'], con=conn, if_exists=mode, index=False)
