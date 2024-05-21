"""Notification Helper Module.

This module provides functions for sending notifications.
"""

from app import services


def notify(slack_block):
    """Notify on slack."""
    notification_service = services.SlackService()
    send_alert = notification_service.send_alert(slack_block)
    return send_alert
