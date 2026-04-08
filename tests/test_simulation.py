from pathlib import Path
import sys
import unittest


APP_DIR = Path(__file__).resolve().parents[1] / "delivery-route-optimizer"
sys.path.insert(0, str(APP_DIR))

import main  # noqa: E402


class SimulationTests(unittest.TestCase):
    def test_hub_address_resolves_from_street_address(self) -> None:
        _, address_index_map = main.load_distances(str(main.DISTANCE_CSV))

        self.assertEqual(main.get_location_index(main.HUB_ADDRESS, address_index_map), 0)

    def test_build_simulation_runs_end_to_end(self) -> None:
        packages, total_miles = main.build_simulation()

        self.assertGreater(total_miles, 0)
        self.assertIsNotNone(packages.lookup(1).delivery_time)
        self.assertEqual(packages.lookup(9).address, "410 S State St")


if __name__ == "__main__":
    unittest.main()
