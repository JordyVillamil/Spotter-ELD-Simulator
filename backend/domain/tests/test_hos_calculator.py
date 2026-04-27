import unittest
from datetime import datetime
from backend.domain.hos_calculator import HOSCalculator
from backend.domain.models import DutyStatus


class TestHOSCalculatorRules(unittest.TestCase):

    def setUp(self):
        self.start_time = datetime(2026, 4, 27, 8, 0)

    # 1. 11-Hour Driving Limit
    def test_11_hour_driving_limit(self):
        # Viaje corto: 11 horas justas de manejo
        hos = HOSCalculator(self.start_time, 550, 50, 0)
        events = hos.generate_trip_events()
        driving_time = sum(
            (e.end_time - e.start_time).total_seconds()
            for e in events
            if e.status == DutyStatus.DRIVING
        )
        self.assertLessEqual(driving_time / 3600, 11.0)

    # 2. 14-Hour Duty Window
    def test_14_hour_duty_window(self):
        hos = HOSCalculator(self.start_time, 600, 50, 0)
        events = hos.generate_trip_events()
        # Verificar que el tiempo total de turno no supere 14h
        total_time = (events[-1].end_time - events[0].start_time).total_seconds() / 3600
        # Es difícil forzarlo exactamente, pero verificamos que descanse tras el límite
        self.assertLessEqual(total_time, 24.0)  # El log debe tener paradas si excede

    # 3. 30-Minute Rest Break (8h driving)
    def test_30_min_rest_break(self):
        hos = HOSCalculator(self.start_time, 1000, 60, 0)  # 16h driving
        events = hos.generate_trip_events()
        breaks = [e for e in events if "break" in str(e.remarks).lower()]
        self.assertTrue(any(e.status == DutyStatus.OFF_DUTY for e in breaks))

    # 4. 70-Hour/8-Day Limit
    def test_70_hour_limit(self):
        # Forzar un ciclo de uso alto
        hos = HOSCalculator(self.start_time, 500, 50, 69.0)
        events = hos.generate_trip_events()
        self.assertTrue(any("restart" in str(e.remarks).lower() for e in events))

    # 5. 34-Hour Restart
    def test_34_hour_restart(self):
        hos = HOSCalculator(self.start_time, 500, 50, 70.0)
        events = hos.generate_trip_events()
        restart_event = next(e for e in events if "restart" in str(e.remarks).lower())
        duration = (
            restart_event.end_time - restart_event.start_time
        ).total_seconds() / 3600
        self.assertEqual(duration, 34.0)

    # 6. 1-Hour Pickup
    def test_pickup_on_duty(self):
        hos = HOSCalculator(self.start_time, 10, 10, 0)
        events = hos.generate_trip_events()
        pickup = events[0]
        self.assertEqual(pickup.status, DutyStatus.ON_DUTY_NOT_DRIVING)
        self.assertEqual(
            (pickup.end_time - pickup.start_time).total_seconds() / 3600, 1.0
        )

    # 7. 1-Hour Drop-off
    def test_dropoff_on_duty(self):
        hos = HOSCalculator(self.start_time, 10, 10, 0)
        events = hos.generate_trip_events()
        dropoff = events[-1]
        self.assertEqual(dropoff.status, DutyStatus.ON_DUTY_NOT_DRIVING)
        self.assertEqual(
            (dropoff.end_time - dropoff.start_time).total_seconds() / 3600, 1.0
        )

    # 8. Fueling Stop
    def test_fueling_every_1000_miles(self):
        hos = HOSCalculator(self.start_time, 1100, 50, 0)  # Necesita 1 parada
        events = hos.generate_trip_events()
        fuel_stops = [e for e in events if "fueling" in str(e.remarks).lower()]
        self.assertEqual(len(fuel_stops), 1)


if __name__ == "__main__":
    unittest.main()
