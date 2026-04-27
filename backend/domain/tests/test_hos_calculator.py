import unittest
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from domain.hos_calculator import HOSCalculator

class TestHOSCalculator(unittest.TestCase):
    def test_simple_trip(self):
        # Arrange: 500 miles, 50 mph, 0 cycle used, start at 2026-04-27 08:00
        start_time = datetime(2026, 4, 27, 8, 0)
        total_distance = 500
        average_speed = 50
        current_cycle_used = 0
        hos = HOSCalculator(start_time, total_distance, average_speed, current_cycle_used)
        # Act
        events = hos.generate_trip_events()
        # Assert
        # Should be only driving, no rest or sleep needed
        total_driving = sum((e.end_time - e.start_time).total_seconds() / 3600 for e in events if e.status == "Driving")
        self.assertAlmostEqual(total_driving, total_distance / average_speed, places=2)
        self.assertTrue(all(e.status in ["Driving", "On Duty (Not Driving)", "Sleeper Berth"] for e in events))

    def test_rest_break_inserted(self):
        # Arrange: 500 miles, 62.5 mph, 0 cycle used, start at 2026-04-27 08:00
        # 8 hours driving = 500 miles
        start_time = datetime(2026, 4, 27, 8, 0)
        total_distance = 500
        average_speed = 62.5
        current_cycle_used = 0
        hos = HOSCalculator(start_time, total_distance, average_speed, current_cycle_used)
        # Act
        events = hos.generate_trip_events()
        # Assert
        rest_breaks = [e for e in events if e.status == "On Duty (Not Driving)" and "rest" in (e.description or "")]
        self.assertTrue(len(rest_breaks) >= 1)
        # Rest break should be 30 minutes
        for rest in rest_breaks:
            self.assertEqual((rest.end_time - rest.start_time).total_seconds(), 1800)

if __name__ == "__main__":
    unittest.main()
