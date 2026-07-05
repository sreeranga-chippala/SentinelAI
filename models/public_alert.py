"""
models/public_alert.py
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PublicAlert:

    alert_id: str

    area_id: str

    area_name: str

    priority_level: str

    title: str

    message: str

    issued_at: datetime

    target: str

    status: str