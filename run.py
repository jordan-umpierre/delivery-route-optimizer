from pathlib import Path
import sys


APP_DIR = Path(__file__).resolve().parent / "delivery-route-optimizer"
sys.path.insert(0, str(APP_DIR))

import main  # noqa: E402


if __name__ == "__main__":
    packages, total_miles = main.build_simulation()
    main.run_interface(packages, total_miles)
