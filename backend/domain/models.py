# backend/domain/models.py
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional
from enum import Enum


class DutyStatus(Enum):
    OFF_DUTY = "OFF_DUTY"
    SLEEPER_BERTH = "SLEEPER_BERTH"
    DRIVING = "DRIVING"
    ON_DUTY_NOT_DRIVING = "ON_DUTY_NOT_DRIVING"


@dataclass
class TripEvent:
    start_time: datetime
    end_time: datetime
    status: DutyStatus
    location: Optional[str] = None
    remarks: Optional[str] = None


@dataclass
class DailyLog:
    date: date
    events: List[TripEvent] = field(default_factory=list)
    total_driving_hours: float = 0.0
    total_on_duty_hours: float = 0.0
