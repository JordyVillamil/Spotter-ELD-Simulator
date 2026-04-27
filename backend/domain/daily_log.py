from dataclasses import dataclass, field
from datetime import date
from typing import List
from .trip_event import TripEvent

@dataclass
class DailyLog:
    date: date
    events: List[TripEvent] = field(default_factory=list)
    total_driving_hours: float = 0.0
    total_on_duty_hours: float = 0.0
