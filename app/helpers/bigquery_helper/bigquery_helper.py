from google.cloud import bigquery


client = bigquery.Client()


def get_existing_threshold(query):
    result = client.query(query).result()
    existing_threshold = None
    for row in result:
        existing_threshold = row["threshold"]
    return existing_threshold


def add_to_bigquery(insert_query):
    client.query(insert_query).result()
