import unittest
from datetime import datetime

# Importaciones absolutas desde la raíz del proyecto
from backend.domain.hos_calculator import HOSCalculator
from backend.domain.models import DutyStatus


class TestHOSCalculator(unittest.TestCase):

    def test_pickup_and_dropoff_events(self):
        start_time = datetime(2026, 4, 27, 8, 0)
        hos = HOSCalculator(start_time, 10, 10, 0)
        events = hos.generate_trip_events()
        # Ahora usamos 'remarks' en lugar de 'description'
        self.assertIn("Pickup", events[0].remarks)
        self.assertIn("Drop-off", events[-1].remarks)

    def test_fueling_stop_inserted(self):
        start_time = datetime(2026, 4, 27, 8, 0)
        hos = HOSCalculator(start_time, 2000, 50, 0)
        events = hos.generate_trip_events()
        fueling_events = [e for e in events if "fueling" in e.remarks.lower()]

        self.assertGreaterEqual(len(fueling_events), 1)
        for fuel in fueling_events:
            self.assertEqual((fuel.end_time - fuel.start_time).total_seconds(), 1800)

    def test_rest_breaks_and_cumulative_driving(self):
        start_time = datetime(2026, 4, 27, 8, 0)
        hos = HOSCalculator(start_time, 1000, 62.5, 0)  # 16 hours driving
        events = hos.generate_trip_events()
        rest_breaks = [e for e in events if "break" in e.remarks.lower()]

        self.assertGreaterEqual(len(rest_breaks), 1)
        for rest in rest_breaks:
            self.assertEqual((rest.end_time - rest.start_time).total_seconds(), 1800)

    def test_70_hour_limit_and_restart(self):
        start_time = datetime(2026, 4, 27, 8, 0)
        hos = HOSCalculator(start_time, 4000, 50, 0)
        events = hos.generate_trip_events()
        restart_events = [e for e in events if "restart" in e.remarks.lower()]

        self.assertGreaterEqual(len(restart_events), 1)
        for restart in restart_events:
            self.assertEqual(
                (restart.end_time - restart.start_time).total_seconds(), 34 * 3600
            )

    def test_multi_day_trip_and_sleep(self):
        start_time = datetime(2026, 4, 27, 8, 0)
        hos = HOSCalculator(start_time, 2000, 50, 0)
        events = hos.generate_trip_events()
        # Ahora comparamos contra el Enum DutyStatus
        sleep_events = [e for e in events if e.status == DutyStatus.SLEEPER_BERTH]

        self.assertGreaterEqual(len(sleep_events), 1)
        for sleep in sleep_events:
            self.assertEqual(
                (sleep.end_time - sleep.start_time).total_seconds(), 10 * 3600
            )


if __name__ == "__main__":
    unittest.main()
