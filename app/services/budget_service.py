import datetime

from google.cloud import bigquery

import config
from app.helpers import bigquery_helper, notification_helper
from app.services import templates
from app.services.queries import budget_table

client = bigquery.Client()


class BudgetService:
    """Handles budget-related operations."""

    def __init__(self):
        self.dataset_id = config.DATASET_ID
        self.table_id = config.ALERT_THRESHOLD_TABLE_ID

    def handle(self, alert_attrs, alert_data):
        """Handles budget alerts."""
        threshold = float(alert_data.get("alertThresholdExceeded")) * 100
        if not self.is_new_threshold_greater(threshold):
            return

        interval = datetime.datetime.strptime(
            alert_data.get("costIntervalStart"), "%Y-%m-%dT%H:%M:%S%z"
        )
        interval_str = interval.strftime("%Y-%m-%d %H:%M")

        current_year_month = datetime.datetime.utcnow().strftime("%Y-%m")
        year_month_of_budget_interval = interval.strftime("%Y-%m")

        if year_month_of_budget_interval != current_year_month:
            return

        billing_id = alert_attrs.get("billingAccountId")
        budget_name = alert_data.get("budgetDisplayName")
        cost = float(alert_data.get("costAmount"))
        budget = float(alert_data.get("budgetAmount"))

        slack_block = templates.get_slack_block(
            billing_id, threshold, budget, budget_name, interval_str
        )

        notify = notification_helper.notify(slack_block)

        if notify is True:
            self.insert_new_threshold(cost, budget, budget_name, threshold)

    def is_new_threshold_greater(self, threshold):
        """Checks if the new threshold is greater."""
        query_to_get_existing_threshold = budget_table.get_existing_threshold_query(
            client, self.dataset_id, self.table_id
        )
        last_existing_threshold = bigquery_helper.get_existing_threshold(
            query_to_get_existing_threshold
        )
        return last_existing_threshold is None or threshold > last_existing_threshold

    def insert_new_threshold(self, cost, budget, budget_name, threshold):
        """Inserts a new threshold into the database."""
        query_to_insert_threshold = budget_table.get_insert_threshold_query(
            client, self.dataset_id, self.table_id, cost, budget, budget_name, threshold
        )
        bigquery_helper.add_to_bigquery(query_to_insert_threshold)
