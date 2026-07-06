"""
mcp/notification_server.py

Handles notification delivery.

Current Version:
    Console output

Future Integrations:
    - Email
    - SMS
    - WhatsApp
    - Firebase Push
    - Twilio
"""

from datetime import datetime


class NotificationServer:

    def __init__(self):

        self.history = []

    # ---------------------------------------------------------

    def send_alert(self, alert):

        self.history.append(alert)

        print("\n" + "=" * 70)
        print("PUBLIC ALERT")
        print("=" * 70)
        print(f"Area      : {alert.area_name}")
        print(f"Priority  : {alert.priority_level}")
        print(f"Title     : {alert.title}")
        print(f"Message   : {alert.message}")
        print(f"Time      : {alert.issued_at}")
        print("=" * 70 + "\n")

        return True

    # ---------------------------------------------------------

    def send_sms(
        self,
        phone_number,
        message
    ):

        print(
            f"[SMS] {phone_number} : {message}"
        )

        return True

    # ---------------------------------------------------------

    def send_email(
        self,
        email,
        subject,
        body
    ):

        print(
            f"[EMAIL] {email} : {subject}"
        )

        return True

    # ---------------------------------------------------------

    def send_whatsapp(
        self,
        phone_number,
        message
    ):

        print(
            f"[WHATSAPP] {phone_number} : {message}"
        )

        return True

    # ---------------------------------------------------------

    def get_history(self):

        return self.history

    # ---------------------------------------------------------

    def clear_history(self):

        self.history.clear()