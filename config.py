import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

if ENVIRONMENT == "development":
    from os import path
    from dotenv import load_dotenv

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, ".env"))

TESTING = os.environ.get("TESTING")
DEBUG = os.environ.get("DEBUG")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
DATASET_ID = os.environ.get("DATASET_ID")
ALERT_THRESHOLD_TABLE_ID = os.environ.get("ALERT_THRESHOLD_TABLE_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
DATASET_LOCATION = os.environ.get("DATASET_LOCATION")
