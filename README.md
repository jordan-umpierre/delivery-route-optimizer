# Delivery Route Optimizer

Python delivery route optimizer that simulates multi-truck package distribution using a custom hash table, nearest-neighbor routing, and time-based package status tracking.

## What It Demonstrates

- Custom hash table implementation using separate chaining
- CSV parsing with only Python standard-library modules
- Distance matrix loading and lookup for route calculations
- Greedy nearest-neighbor route selection
- Multi-truck delivery simulation with fixed scenario constraints
- Time-based package status reporting from a command-line interface
- Special-case business rules for delayed packages and corrected package addresses

## Features

- Load package and distance data from CSV files
- Store packages in a custom hash table keyed by package ID
- Simulate deliveries across three trucks
- Track whether each package is delayed, at the hub, en route, or delivered at a user-entered time
- Report total mileage across all trucks
- Handle delayed-flight packages that arrive at 9:05 AM
- Correct package 9's address after 10:20 AM before it is routed

## Tech Stack

- Python 3.10+
- Python standard library only
- CSV file processing
- Custom data structures
- Greedy routing heuristic

## Project Structure

```text
.
|-- README.md
`-- delivery-route-optimizer/
    |-- main.py
    |-- hashtable.py
    |-- package.py
    `-- data/
        |-- WGUPS_Package_File.csv
        `-- WGUPS_Distance_Table.csv
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/jordan-umpierre/delivery-route-optimizer.git
cd delivery-route-optimizer
python run.py
```

You can also run it from inside the app folder:

```bash
cd delivery-route-optimizer
python main.py
```

If your system uses `python3` instead of `python`, substitute `python3` in either command.

The `data/` folder should contain:

- `WGUPS_Package_File.csv`
- `WGUPS_Distance_Table.csv`

## Test And Verify

Run the smoke tests from the repository root:

```bash
python -m unittest discover -s tests
```

Manual checks to try:

- Choose option `1` and enter `08:35` to inspect early delivery status.
- Choose option `1` and enter `10:20` to confirm package 9 uses its corrected address after the correction time.
- Choose option `2` to print total mileage across the simulated routes.

## Example Menu

```text
WGUPS Package Status Interface
1) View all package statuses at a specific time
2) View total mileage
3) Exit
```

## How It Works

- Packages are loaded from `data/WGUPS_Package_File.csv` into a custom hash table.
- Distances are loaded from `data/WGUPS_Distance_Table.csv` into a matrix for route calculations.
- Each truck is assigned a deterministic package list based on the scenario constraints.
- The route planner repeatedly chooses the nearest remaining delivery stop.
- Package load and delivery times are recorded during the simulation.
- The CLI compares the user-entered time against each package's load and delivery time to show the correct status.

## Limitations

- Truck assignments are deterministic and scenario-specific.
- The nearest-neighbor heuristic is fast and explainable, but it is not guaranteed to find a globally optimal route.
- The program expects the provided WGUPS CSV file format.

