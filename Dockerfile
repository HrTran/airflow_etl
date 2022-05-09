FROM apache/airflow:2.3.0
COPY requirements.txt .
COPY ./dist/common_utils-0.0.0-py3-none-any.whl .
RUN pip install -r requirements.txt
RUN pip install common_utils-0.0.0-py3-none-any.whl