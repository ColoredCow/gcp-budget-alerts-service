def get_slack_block(billing_id, threshold, budget, budget_name, interval_str):
    slack_block_payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"GCP Billing Budget Alert: {threshold}% of budget reached",
                    "emoji": True,
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Budget Amount:*\n ${budget}"},
                    {"type": "mrkdwn", "text": f"*Budget Period by:*\n {interval_str}"},
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Budget Name:*\n {budget_name}"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Billing Account ID:*\n {billing_id}",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Review your cost details in the <https://console.cloud.google.com/billing/{billing_id}/reports;budgetId={budget_name}|Report Page>",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "View Budget details"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Here", "emoji": True},
                    "value": "click_me_123",
                    "url": "https://console.cloud.google.com/billing/01B5DE-D5C831-42715E/budgets/7ebf6261-1e21-4d45-884b-6170efb15bc4/edit?organizationId=7107561744",
                    "action_id": "button-action",
                },
            },
            {"type": "divider"},
        ]
    }
    return slack_block_payload
