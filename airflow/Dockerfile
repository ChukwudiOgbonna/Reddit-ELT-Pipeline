FROM apache/airflow:latest
RUN pip3 install boto3 botocore pyarrow
RUN pip install -U poetry
RUN pip3 install 'apache-airflow[amazon]'
