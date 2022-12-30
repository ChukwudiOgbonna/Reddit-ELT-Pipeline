# Bash script to output terraform variables to env variables to be used by airflow

# change directory
cd ./terraform

# echo variables to .env file iin airflow directory
echo [aws_config] >> ../airflow/extraction/configuration.conf
echo bucket_name = "$(terraform output -raw s3_bucket_name)" >> ../airflow/extraction/configuration.conf
echo redshift_username = "$(terraform output -raw redshift_username)" >> ../airflow/extraction/configuration.conf
echo redshift_password = "$(terraform output -raw redshift_password)" >> ../airflow/extraction/configuration.conf
echo redshift_hostname = "$(terraform output -raw redshift_cluster_hostname)" >> ../airflow/extraction/configuration.conf
echo redshift_role = "$(terraform output -raw redshift_role)" >> ../airflow/extraction/configuration.conf
echo redshift_port = "$(terraform output -raw redshift_port)" >> ../airflow/extraction/configuration.conf
echo redshift_database = "$(terraform output -raw redshift_dbname)" >> ../airflow/extraction/configuration.conf
echo account_id = "$(terraform output -raw account_id)" >> ../airflow/extraction/configuration.conf
echo aws_region = "$(terraform output -raw aws_region)" >> ../airflow/extraction/configuration.conf
echo [reddit_config] >> ../airflow/extraction/configuration.conf
echo secret = "0tdUHSbRC0FhWsG6fodjSQ_Gch0OSw" >> ../airflow/extraction/configuration.conf
echo developer = "chukwudi23" >> ../airflow/extraction/configuration.conf
echo name = "Chuks-API" >> ../airflow/extraction/configuration.conf
echo client_id = "sA7dWbM0WufzuO5F42_Ung" >> ../airflow/extraction/configuration.conf