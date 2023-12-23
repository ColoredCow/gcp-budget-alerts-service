import json
import base64

from utils import logger
from app import services


# Endpoint of the cloud function.
def handle(payload, context):
    try:
        alert_attrs = payload.get("attributes")
        alert_data = json.loads(base64.b64decode(payload.get("data")).decode("utf-8"))
        logger.info(
            "new billing alert; context=%s, attributes=%s, data=%s",
            context,
            alert_attrs,
            alert_data,
        )

        budget_service = services.BudgetService()
        budget_service.handle(alert_attrs, alert_data)

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        return {"message": "Something went wrong!"}, 400
    return {"message": "Success"}, 200
