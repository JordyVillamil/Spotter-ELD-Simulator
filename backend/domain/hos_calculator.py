from datetime import datetime, timedelta
from typing import List
from .trip_event import TripEvent

class HOSCalculator:
    """
    Applies FMCSA HOS rules to generate a list of TripEvent objects for a given trip.
    """
    DRIVING_LIMIT = 11  # hours
    DUTY_WINDOW = 14    # hours
    REST_BREAK = 0.5    # 30 minutes in hours
    CYCLE_LIMIT = 70    # hours in 8 days
    RESTART_HOURS = 34  # hours
    SLEEPER_BERTH = 10  # hours
    FUELING_INTERVAL = 1000  # miles
    FUELING_DURATION = 0.5   # 30 minutes
    PICKUP_ON_DUTY = 1       # hour
    DROPOFF_ON_DUTY = 1      # hour

    def __init__(self, start_time: datetime, total_distance: float, average_speed: float, current_cycle_used: float):
        self.start_time = start_time
        self.total_distance = total_distance
        self.average_speed = average_speed
        self.current_cycle_used = current_cycle_used

    def generate_trip_events(self) -> List[TripEvent]:
        events = []
        current_time = self.start_time
        remaining_distance = self.total_distance
        cycle_used = self.current_cycle_used
        DAILY_DRIVING_LIMIT = self.DRIVING_LIMIT
        DAILY_DUTY_WINDOW = self.DUTY_WINDOW
        REST_BREAK = self.REST_BREAK
        SLEEPER_BERTH = self.SLEEPER_BERTH
        PICKUP_ON_DUTY = self.PICKUP_ON_DUTY
        DROPOFF_ON_DUTY = self.DROPOFF_ON_DUTY
        FUELING_INTERVAL = self.FUELING_INTERVAL
        FUELING_DURATION = self.FUELING_DURATION
        CYCLE_LIMIT = self.CYCLE_LIMIT
        RESTART_HOURS = self.RESTART_HOURS

        # Track daily on-duty hours for 8-day window
        daily_on_duty = []  # List of floats, one per day
        day_start_time = current_time

        # 1 hour On Duty (Not Driving) at Pickup
        pickup_end = current_time + timedelta(hours=PICKUP_ON_DUTY)
        events.append(TripEvent(
            start_time=current_time,
            end_time=pickup_end,
            status="On Duty (Not Driving)",
            description="Pickup: loading and paperwork",
            location="Pickup Location (placeholder)"
        ))
        current_time = pickup_end
        duty_window = PICKUP_ON_DUTY
        driving_hours_today = 0.0
        miles_since_fuel = 0.0
        cycle_used += PICKUP_ON_DUTY

        # Track cumulative driving since last break
        cumulative_driving_since_break = 0.0
        while remaining_distance > 0:
            # If new day, reset daily counters and update 8-day window
            if duty_window == 0.0 and driving_hours_today == 0.0 and len(daily_on_duty) > 0:
                # Advance to next day
                day_start_time = current_time
            # Remove days older than 8 days
            while len(daily_on_duty) > 7:
                cycle_used -= daily_on_duty.pop(0)
            # Enforce 70-hour/8-day limit
            if cycle_used >= CYCLE_LIMIT:
                # Insert 34-hour Off Duty (restart)
                restart_end = current_time + timedelta(hours=RESTART_HOURS)
                events.append(TripEvent(
                    start_time=current_time,
                    end_time=restart_end,
                    status="Off Duty",
                    description="34-hour restart (cycle reset)",
                    location="Rest Area (placeholder)"
                ))
                current_time = restart_end
                # Reset cycle and daily window
                daily_on_duty = []
                cycle_used = 0.0
                duty_window = 0.0
                driving_hours_today = 0.0
                miles_since_fuel = 0.0
                cumulative_driving_since_break = 0.0
                day_start_time = current_time
                continue
            # Calculate max possible driving for this segment
            max_drive = min(
                DAILY_DRIVING_LIMIT - driving_hours_today,
                8 - cumulative_driving_since_break,
                remaining_distance / self.average_speed
            )
            if max_drive <= 0:
                # Need a break or end of day
                if cumulative_driving_since_break >= 8:
                    # Insert 30-min rest break
                    rest_end = current_time + timedelta(hours=REST_BREAK)
                    events.append(TripEvent(
                        start_time=current_time,
                        end_time=rest_end,
                        status="On Duty (Not Driving)",
                        description="30-min rest break",
                        location="Rest Area (placeholder)"
                    ))
                    current_time = rest_end
                    duty_window += REST_BREAK
                    cycle_used += REST_BREAK
                    cumulative_driving_since_break = 0.0
                    continue
                # End of day, record on-duty hours
                if duty_window > 0.0:
                    if len(daily_on_duty) == 7:
                        cycle_used -= daily_on_duty.pop(0)
                    daily_on_duty.append(duty_window)
                # Sleep for 10 hours
                sleep_end = current_time + timedelta(hours=SLEEPER_BERTH)
                events.append(TripEvent(
                    start_time=current_time,
                    end_time=sleep_end,
                    status="Sleeper Berth",
                    description="10-hour sleep",
                    location="Sleeper Berth (placeholder)"
                ))
                current_time = sleep_end
                duty_window = 0.0
                driving_hours_today = 0.0
                miles_since_fuel = 0.0
                cumulative_driving_since_break = 0.0
                day_start_time = current_time
                continue
            # Check if fueling is needed during this segment
            segment_distance = max_drive * self.average_speed
            fueling_distance = FUELING_INTERVAL - miles_since_fuel
            if segment_distance >= fueling_distance:
                # Split the driving segment at the fueling point
                drive_before_fuel = fueling_distance / self.average_speed
                drive_end = current_time + timedelta(hours=drive_before_fuel)
                events.append(TripEvent(
                    start_time=current_time,
                    end_time=drive_end,
                    status="Driving",
                    description="Driving segment",
                    location="En Route (placeholder)"
                ))
                current_time = drive_end
                remaining_distance -= fueling_distance
                driving_hours_today += drive_before_fuel
                duty_window += drive_before_fuel
                cycle_used += drive_before_fuel
                cumulative_driving_since_break += drive_before_fuel
                # Add fueling stop
                fuel_end = current_time + timedelta(hours=FUELING_DURATION)
                events.append(TripEvent(
                    start_time=current_time,
                    end_time=fuel_end,
                    status="On Duty (Not Driving)",
                    description="30-min fueling stop",
                    location="Fuel Station (placeholder)"
                ))
                current_time = fuel_end
                duty_window += FUELING_DURATION
                cycle_used += FUELING_DURATION
                miles_since_fuel = 0.0
                # Continue with the rest of the segment
                max_drive -= drive_before_fuel
                if max_drive <= 0:
                    continue
                segment_distance = max_drive * self.average_speed
            # Driving event (after fueling or if no fueling needed)
            drive_end = current_time + timedelta(hours=max_drive)
            events.append(TripEvent(
                start_time=current_time,
                end_time=drive_end,
                status="Driving",
                description="Driving segment",
                location="En Route (placeholder)"
            ))
            current_time = drive_end
            remaining_distance -= segment_distance
            miles_since_fuel += segment_distance
            driving_hours_today += max_drive
            duty_window += max_drive
            cycle_used += max_drive
            cumulative_driving_since_break += max_drive
            # End of duty window or driving limit
            if driving_hours_today >= DAILY_DRIVING_LIMIT or duty_window >= DAILY_DUTY_WINDOW:
                # End of day, record on-duty hours
                if duty_window > 0.0:
                    if len(daily_on_duty) == 7:
                        cycle_used -= daily_on_duty.pop(0)
                    daily_on_duty.append(duty_window)
                sleep_end = current_time + timedelta(hours=SLEEPER_BERTH)
                events.append(TripEvent(
                    start_time=current_time,
                    end_time=sleep_end,
                    status="Sleeper Berth",
                    description="10-hour sleep"
                ))
                current_time = sleep_end
                duty_window = 0.0
                driving_hours_today = 0.0
                miles_since_fuel = 0.0
                cumulative_driving_since_break = 0.0
                day_start_time = current_time

        # 1 hour On Duty (Not Driving) at Drop-off
        dropoff_end = current_time + timedelta(hours=DROPOFF_ON_DUTY)
        events.append(TripEvent(
            start_time=current_time,
            end_time=dropoff_end,
            status="On Duty (Not Driving)",
            description="Drop-off: unloading and paperwork",
            location="Drop-off Location (placeholder)"
        ))
        current_time = dropoff_end
        if duty_window > 0.0:
            if len(daily_on_duty) == 7:
                cycle_used -= daily_on_duty.pop(0)
            daily_on_duty.append(duty_window)
        cycle_used += DROPOFF_ON_DUTY

        return events
