# backend/domain/hos_calculator.py
from datetime import datetime, timedelta
from typing import List
from .models import TripEvent, DutyStatus


class HOSCalculator:
    """
    Applies FMCSA HOS rules to generate a list of TripEvent objects for a given trip.
    """

    DRIVING_LIMIT = 11.0  # hours
    DUTY_WINDOW = 14.0  # hours
    REST_BREAK = 0.5  # 30 minutes in hours
    CYCLE_LIMIT = 70.0  # hours in 8 days
    RESTART_HOURS = 34.0  # hours
    SLEEPER_BERTH = 10.0  # hours
    FUELING_INTERVAL = 1000.0  # miles
    FUELING_DURATION = 0.5  # 30 minutes
    PICKUP_ON_DUTY = 1.0  # hour
    DROPOFF_ON_DUTY = 1.0  # hour

    def __init__(
        self,
        start_time: datetime,
        total_distance: float,
        average_speed: float,
        current_cycle_used: float,
    ):
        self.start_time = start_time
        self.total_distance = total_distance
        self.average_speed = average_speed
        self.current_cycle_used = current_cycle_used

    def generate_trip_events(self) -> List[TripEvent]:
        events = []
        current_time = self.start_time
        remaining_distance = self.total_distance
        cycle_used = self.current_cycle_used

        duty_window = (
            self.PICKUP_ON_DUTY
        )  # Reloj continuo de 14h (no se detiene en descansos)
        on_duty_today = (
            self.PICKUP_ON_DUTY
        )  # Horas reales trabajadas hoy (para el ciclo de 70h)
        driving_hours_today = 0.0
        miles_since_fuel = 0.0
        cumulative_driving_since_break = 0.0
        daily_on_duty = []

        # 1. EVENTO INICIAL: Pickup
        pickup_end = current_time + timedelta(hours=self.PICKUP_ON_DUTY)
        events.append(
            TripEvent(
                status=DutyStatus.ON_DUTY_NOT_DRIVING,
                start_time=current_time,
                end_time=pickup_end,
                remarks="Pickup location (1 hr)",
            )
        )
        current_time = pickup_end

        # 2. BUCLE PRINCIPAL DE RUTA
        while remaining_distance > 0:

            # A. ¿Necesita reinicio de 34 horas (70-hour rule)?
            if cycle_used >= self.CYCLE_LIMIT:
                restart_end = current_time + timedelta(hours=self.RESTART_HOURS)
                events.append(
                    TripEvent(
                        status=DutyStatus.OFF_DUTY,
                        start_time=current_time,
                        end_time=restart_end,
                        remarks="34-hour restart (cycle reset)",
                    )
                )
                current_time = restart_end
                cycle_used = 0.0
                duty_window = 0.0
                on_duty_today = 0.0
                driving_hours_today = 0.0
                cumulative_driving_since_break = 0.0
                continue

            # B. ¿Terminó su turno o su límite de manejo?
            if (
                driving_hours_today >= self.DRIVING_LIMIT
                or duty_window >= self.DUTY_WINDOW
            ):
                sleep_end = current_time + timedelta(hours=self.SLEEPER_BERTH)
                events.append(
                    TripEvent(
                        status=DutyStatus.SLEEPER_BERTH,
                        start_time=current_time,
                        end_time=sleep_end,
                        remarks="10-hour mandatory sleep",
                    )
                )
                current_time = sleep_end

                # Guardamos las horas reales trabajadas para el cálculo de 8 días
                if len(daily_on_duty) == 8:
                    cycle_used -= daily_on_duty.pop(0)
                daily_on_duty.append(on_duty_today)

                duty_window = 0.0
                on_duty_today = 0.0
                driving_hours_today = 0.0
                cumulative_driving_since_break = 0.0
                continue

            # C. ¿Necesita descanso de 30 min?
            if cumulative_driving_since_break >= 8.0:
                rest_end = current_time + timedelta(hours=self.REST_BREAK)
                events.append(
                    TripEvent(
                        status=DutyStatus.OFF_DUTY,
                        start_time=current_time,
                        end_time=rest_end,
                        remarks="30-min mandatory break",
                    )
                )
                current_time = rest_end
                duty_window += self.REST_BREAK
                # NOTA: Off-Duty no suma a 'cycle_used' ni a 'on_duty_today'
                cumulative_driving_since_break = 0.0
                continue

            # --- CALCULAR AVANCE ---
            time_to_limit = self.DRIVING_LIMIT - driving_hours_today
            time_to_window = self.DUTY_WINDOW - duty_window
            time_to_break = 8.0 - cumulative_driving_since_break
            time_to_fuel = (
                self.FUELING_INTERVAL - miles_since_fuel
            ) / self.average_speed
            time_to_destination = remaining_distance / self.average_speed

            drive_time = min(
                time_to_limit,
                time_to_window,
                time_to_break,
                time_to_fuel,
                time_to_destination,
            )
            if drive_time <= 0.01:
                drive_time = 0.01

            # --- EJECUTAR AVANCE DE MANEJO ---
            drive_end = current_time + timedelta(hours=drive_time)
            events.append(
                TripEvent(
                    status=DutyStatus.DRIVING,
                    start_time=current_time,
                    end_time=drive_end,
                    remarks="Driving segment",
                )
            )

            current_time = drive_end
            distance_driven = drive_time * self.average_speed
            remaining_distance -= distance_driven
            miles_since_fuel += distance_driven

            driving_hours_today += drive_time
            duty_window += drive_time
            on_duty_today += drive_time
            cycle_used += drive_time
            cumulative_driving_since_break += drive_time

            # --- CHEQUEO DE GASOLINA ---
            if miles_since_fuel >= self.FUELING_INTERVAL and remaining_distance > 0:
                fuel_end = current_time + timedelta(hours=self.FUELING_DURATION)
                events.append(
                    TripEvent(
                        status=DutyStatus.ON_DUTY_NOT_DRIVING,
                        start_time=current_time,
                        end_time=fuel_end,
                        remarks="30-min fueling stop",
                    )
                )
                current_time = fuel_end
                duty_window += self.FUELING_DURATION
                on_duty_today += self.FUELING_DURATION
                cycle_used += self.FUELING_DURATION
                miles_since_fuel = 0.0
                cumulative_driving_since_break = 0.0

        # 3. EVENTO FINAL: Drop-off
        dropoff_end = current_time + timedelta(hours=self.DROPOFF_ON_DUTY)
        events.append(
            TripEvent(
                status=DutyStatus.ON_DUTY_NOT_DRIVING,
                start_time=current_time,
                end_time=dropoff_end,
                remarks="Drop-off location (1 hr)",
            )
        )

        return events
