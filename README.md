# Delivery Route Optimizer

Python delivery route optimizer that simulates multi-truck package distribution using a custom hash table, nearest-neighbor routing, and time-based package status tracking.

## Overview

This project is a logistics delivery simulation built in Python. It loads package and distance data from CSV files, stores package records in a custom hash table, and simulates deliveries across multiple trucks using a nearest-neighbor routing approach.

The program also tracks package status throughout the day so users can check whether a package is at the hub, en route, or delivered at a specific time.

## Features

- Custom hash table implementation for package storage and lookup
- Multi-truck delivery simulation
- Nearest-neighbor route selection
- Time-based package status tracking
- Total mileage reporting
- Command-line interface for package status checks
- Support for delayed packages and package 9 address correction

## Technologies Used

- Python
- CSV file processing
- Custom data structures
- Greedy routing heuristic

## Project Structure

```text
delivery-route-optimizer/
├── main.py
├── hashtable.py
├── package.py
├── data/
│   ├── WGUPS_Package_File.csv
│   └── WGUPS_Distance_Table.csv
└── README.md
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/jordan-umpierre/delivery-route-optimizer.git
   cd delivery-route-optimizer
   ```

2. Make sure the `data` folder contains:
   - `WGUPS_Package_File.csv`
   - `WGUPS_Distance_Table.csv`

3. Run the program:
   ```bash
   python main.py
   ```

## How It Works

- Packages are loaded from a CSV file into a custom hash table
- Distances are loaded into a matrix for route calculations
- Each truck is assigned a set of packages
- The program uses a nearest-neighbor heuristic to choose the next delivery stop
- Package statuses are updated as trucks leave the hub and complete deliveries
- Users can query package statuses at specific times through the CLI

## Example Menu

```text
WGUPS Package Status Interface
1) View all package statuses at a specific time
2) View total mileage
3) Exit
```

## Limitations

- Truck assignments are currently hardcoded
- Routing uses a greedy nearest-neighbor approach and is not guaranteed to be globally optimal
- The program depends on the expected CSV file format

## Author

Jordan Umpierre
