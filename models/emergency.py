"""
models/emergency.py
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Emergency:

    event_id: str

    event_type: str          # Flood, Landslide, Fire...

    area_id: str

    area_name: str

    severity: str            # Low / Medium / High / Critical / Extreme

    description: str

    timestamp: datetime

    status: str = "ACTIVE"