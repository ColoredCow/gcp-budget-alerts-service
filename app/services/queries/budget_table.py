def get_existing_threshold_query(bigquery_client, dataset_id, table_id):
    return f"""
        SELECT threshold
        FROM `{bigquery_client.project}.{dataset_id}.{table_id}`
        WHERE EXTRACT(YEAR FROM createdAt) = EXTRACT(YEAR FROM CURRENT_TIMESTAMP())
        AND EXTRACT(MONTH FROM createdAt) = EXTRACT(MONTH FROM CURRENT_TIMESTAMP())
        ORDER BY createdAt DESC
        LIMIT 1
    """


def get_insert_threshold_query(
    bigquery_client, dataset_id, table_id, cost, budget, budget_name, threshold
):
    return f"""
        INSERT INTO `{bigquery_client.project}.{dataset_id}.{table_id}` (createdAt, costAmount, budgetAmount, budgetName, threshold)
        VALUES (CURRENT_TIMESTAMP(), {cost}, {budget}, '{budget_name}', {threshold})
    """
