from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TripEvent:
    start_time: datetime
    end_time: datetime
    status: str  # e.g., 'Driving', 'Off Duty', 'Sleeper Berth', 'On Duty (Not Driving)'
    location: Optional[str] = None
    description: Optional[str] = None
