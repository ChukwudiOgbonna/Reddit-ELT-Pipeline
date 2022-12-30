import boto3
import pathlib
import configparser
import sys



# Load AWS Credentials
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
parser.read(f"{script_path}/configuration.conf")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
AWS_REGION = parser.get("aws_config", "aws_region")

# Parse arguments from Dag
try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Command line argument not passed. Error {e}")
    sys.exit(1)

# Name for our S3 file
FILENAME = f"{output_name}.csv"

def main():
    conn = connect_to_s3()
    upload_file_to_s3(conn)

def connect_to_s3():
    # Get an S3 Client
    try:
        conn = boto3.client("s3")
        return conn
    except Exception as e:
        print(f"Can't connect to S3. Error: {e}")
        sys.exit(1)

def upload_file_to_s3(conn):
    # Upload CSV to S3 bucket
    try:
        conn.upload_file(
        Filename= "/tmp/" + FILENAME, Bucket=BUCKET_NAME, Key=FILENAME
    )
    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    main()











