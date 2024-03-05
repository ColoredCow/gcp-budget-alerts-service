"""
Module: main
Description: Contains the main function for handling billing alerts.
"""

import base64
import json

from app import services
from utils import logger


def handle(payload, context):
    """
    Function to handle billing alerts.

    Args:
        payload (dict): Payload containing alert attributes and data.
        context (dict): Context information.

    Returns:
        dict: Response message and status code.
    """
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
        logger.error("Error while handling the payload for billing alert: %s", e)
        return {"message": "Something went wrong!"}, 400
    return {"message": "Success"}, 200
