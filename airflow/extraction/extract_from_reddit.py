import configparser
import datetime
import pandas as pd
import pathlib
import praw
import sys
import numpy as np
from validation import validate_input



# Read Configuration File
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
config_file = "configuration.conf"
parser.read(f"{script_path}/{config_file}")

# Configuration Variables
SECRET = parser.get("reddit_config", "secret")
CLIENT_ID = parser.get("reddit_config", "client_id")

# Options for extracting data from PRAW
SUBREDDIT = "dataengineering"
TIME_FILTER = "day"
LIMIT = None

# Extract These fields we need from the Subreddit
POST_FIELDS = [
    "id",
    "title",
    "score",
    "num_comments",
    "author",
    "created_utc",
    "url",
    "upvote_ratio",
    "over_18",
    "edited",
    "spoiler",
    "stickied",
]

# Get output name passed as argument from dag
try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Error with file input. Error {e}")
    sys.exit(1)
date_dag_run = datetime.datetime.strptime(output_name, "%Y%m%d")


def main():
    """Extract Reddit data and load to CSV"""
    validate_input(output_name)
    reddit_instance = api_connect()
    subreddit_posts_object = subreddit_posts(reddit_instance)
    extracted_data = extract_data(subreddit_posts_object)
    transformed_data = transform_basic(extracted_data)
    load_to_csv(transformed_data)


def api_connect():
    """Connect to Reddit API"""
    try:
        instance = praw.Reddit(
            client_id=CLIENT_ID, client_secret=SECRET, user_agent="My User Agent"
        )
        return instance
    except Exception as e:
        print(f"Unable to connect to API. Error: {e}")
        sys.exit(1)


def subreddit_posts(reddit_instance):
    """Create posts object for Reddit instance"""
    try:
        subreddit = reddit_instance.subreddit(SUBREDDIT)
        posts = subreddit.top(time_filter=TIME_FILTER, limit=LIMIT)
        return posts
    except Exception as e:
        print(f"There's been an issue. Error: {e}")
        sys.exit(1)


def extract_data(posts):
    # Convert posts JSON object to dataframe, and filter based on columns
    list_of_records = []
    try:
        for submission in posts:
            # convert submission object attritubtes to dictionary
            record = vars(submission)
            # Extract only relevant columns 
            record = {field : record[field] for field in POST_FIELDS}
            # Append to list
            list_of_records.append(record)
        # Create data frame
        df = pd.DataFrame(list_of_records)
        return df
    except Exception as e:
        print(f"There is an error chuks {e}")
        sys.exit(1)

def transform_basic(df):
    df = df.dropna()
    # Convert UTC to date_time
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    # Convert String booleans to Boolean data type
    df["over_18"] = np.where(
        (df["over_18"] == "False") | (df["over_18"] == False), False, True
    ).astype(bool)
    df["edited"] = np.where(
        (df["edited"] == "False") | (df["edited"] == False), False, True
    ).astype(bool)
    df["spoiler"] = np.where(
        (df["spoiler"] == "False") | (df["spoiler"] == False), False, True
    ).astype(bool)
    df["stickied"] = np.where(
        (df["stickied"] == "False") | (df["stickied"] == False), False, True
    ).astype(bool)
    return df


def load_to_csv(extracted_data_df):
    # Save extracted data to CSV file in /tmp folder
    extracted_data_df.to_csv(f"/tmp/{output_name}.csv", index=False)


if __name__ == "__main__":
    main()