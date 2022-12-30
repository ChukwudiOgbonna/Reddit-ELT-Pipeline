# Reddit-ELT-Pipeline
This project creates a data pipeline to extract data from reddit sub [r/dataengineering](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiV5qu41aH8AhV2VaQEHa2NASAQFnoECBoQAQ&url=https%3A%2F%2Fwww.reddit.com%2Fr%2Fdataengineering%2F&usg=AOvVaw2VxlQ4Vi0wLbFf5nK0Nnw8)

Output is a Amazon QuickSight Dashboard report, providing some insights into the Data Engineering official subreddit.

## Motivation
Most People like to do fancy things with data, create ML models, create cool dashboards, but nobody ever asks, where did this data come from?
A model is only as good as the data it is trained on. Insights can only be accurately drawn on clean data.

My motivation for making this project is to provide Data scientists, data analysts, and Business analysts access to clean and structured data
This project provided me with a good opporttunity to learn DevOps and IaaC tools. 

## Architecture

![My Image](architecture.jpg)

1. Extract Data using Reddit API
2. Load Data into S3 Bucket - Our Data Lake
3. The Staging Area acts as an intermediary between the S3 Bucket and Redshift Cluster
4. The Redshift is a Data Warehouse - OLAP
5. Amazon QuickSight is used to create dashboards
6. Airflow is used as our workflow orchestrator
7. Docker is package airflow in a container
8. Terraform is an IaC tool used to provision our resources like S3 Bucket and Redshift Cluster
9. dbt is the T in ELT, used to provide tranformation logic to tables in our warehouse

## Output

![My Image1](dashboard.jpg)

Output from Amazon QuickSight dashboard link can be found here [link](https://us-east-1.quicksight.aws.amazon.com/sn/accounts/004743222442/dashboards/d08552d0-7cdb-4e90-9f3c-6b6623b9a82f?directory_alias=chukwudi)






