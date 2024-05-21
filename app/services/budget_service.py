import datetime

from google.cloud import bigquery
from services import templates
from services.queries import budget_table

import config
from app.helpers import bigquery_helper, notification_helper

client = bigquery.Client()


class BudgetService:
    """Handles budget-related operations."""

    def __init__(self):
        self.dataset_id = config.DATASET_ID
        self.table_id = config.ALERT_THRESHOLD_TABLE_ID

    def handle(self, alert_attrs, alert_data):
        """Handles budget alerts."""
        threshold = self._get_threshold(alert_data)
        if not self._is_new_threshold_greater(threshold):
            return

        interval_str = self._parse_interval(alert_data)

        if not self._is_current_month(interval_str):
            return

        billing_id = alert_attrs.get("billingAccountId")
        budget_name = alert_data.get("budgetDisplayName")
        cost = float(alert_data.get("costAmount"))
        budget = float(alert_data.get("budgetAmount"))

        slack_block = templates.get_slack_block(
            billing_id, threshold, budget, budget_name, interval_str
        )

        if notification_helper.notify(slack_block):
            self._insert_new_threshold(cost, budget, budget_name, threshold)

    def _get_threshold(self, alert_data):
        """Extracts and converts threshold from alert data."""
        return float(alert_data.get("alertThresholdExceeded")) * 100

    def _parse_interval(self, alert_data):
        """Parses interval from alert data."""
        interval = datetime.datetime.strptime(
            alert_data.get("costIntervalStart"), "%Y-%m-%dT%H:%M:%S%z"
        )
        return interval.strftime("%Y-%m-%d %H:%M")

    def _is_current_month(self, interval_str):
        """Checks if the interval falls within the current month."""
        current_year_month = datetime.datetime.utcnow().strftime("%Y-%m")
        year_month_of_budget_interval = interval_str[:7]  # Extract year-month
        return year_month_of_budget_interval == current_year_month

    def _is_new_threshold_greater(self, threshold):
        """Checks if the new threshold is greater."""
        query_to_get_existing_threshold = budget_table.get_existing_threshold_query(
            client, self.dataset_id, self.table_id
        )
        last_existing_threshold = bigquery_helper.get_existing_threshold(
            query_to_get_existing_threshold
        )
        return last_existing_threshold is None or threshold > last_existing_threshold

    def _insert_new_threshold(self, cost, budget, budget_name, threshold):
        """Inserts a new threshold into the database."""
        query_to_insert_threshold = budget_table.get_insert_threshold_query(
            client, self.dataset_id, self.table_id, cost, budget, budget_name, threshold
        )
        bigquery_helper.add_to_bigquery(query_to_insert_threshold)
