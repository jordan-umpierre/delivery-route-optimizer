# Student ID: 011797435

# WHAT: Import built-in libraries only (allowed).
# WHY: The rubric forbids external libraries; csv/time are built-in.
import csv
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

# WHAT: Import your custom data structures.
# WHY: Task 2 requires a custom hash table and a Package object holding all fields.
from hashtable import HashTable
from package import Package


def load_packages(csv_path: str) -> HashTable:
    # WHAT: Load all package rows from WGUPS_Package_File.csv into a custom HashTable.
    # WHY: Packages must be stored/retrieved by package_id efficiently for routing and status checks.

    # WHAT: Create the custom hash table that will store all package records.
    # WHY: Package ID lookups must be fast during delivery simulation and user status checks.
    package_table = HashTable()

    # WHAT: Open the CSV using csv.reader.
    # WHY: csv.reader correctly handles commas and quoted text in CSV files.
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            # WHAT: Skip non-data header rows and blank lines.
            # WHY: The provided CSV export includes title/column rows before the package rows.
            if not row or not row[0].strip().isdigit():
                continue

            # WHAT: Parse the required package columns from the CSV row.
            # WHY: Task requirements depend on these exact delivery fields being stored with the package.
            # Expected columns: ID, Address, City, State, Zip, Deadline, Weight, (Special Notes...)
            package_id = int(row[0].strip())
            address = row[1].strip()
            city = row[2].strip()
            state = row[3].strip()
            zip_code = row[4].strip()
            deadline = row[5].strip()
            weight_kilo = row[6].strip()

            # WHAT: Build a Package object holding all required delivery fields for this package ID.
            # HOW: Map CSV columns into the Package constructor.
            package = Package(
                package_id=package_id,
                address=address,
                deadline=deadline,
                city=city,
                state=state,
                zip_code=zip_code,
                weight_kilo=weight_kilo,
            )
            # Package 9: wrong address until 10:20, then corrected.
            if package_id == 9:
                package.original_address = address
                package.original_zip_code = zip_code
                package.corrected_address = "410 S State St"
                package.corrected_zip_code = "84111"

            # WHAT: Insert the package into the hash table.
            # WHY: The hash table key is package_id so we can retrieve/update packages efficiently.
            package_table.insert(package_id, package)

    return package_table


def load_distances(csv_path: str) -> Tuple[List[List[float]], Dict[str, int]]:
    """
    WHAT: Load WGUPS_Distance_Table.csv and build:
         - distance_matrix: list-of-lists of floats (often lower-triangular / ragged)
         - address_index_map: location label/address -> row index
    WHY: The delivery algorithm needs O(1) index-based access to distances between locations.

    NOTE: This loader is intentionally robust:
          - It skips the title/header/address-list section automatically
          - It begins when it detects the HUB row containing "HUB" and "0.0"
    """
    distance_matrix: List[List[float]] = []
    address_index_map: Dict[str, int] = {}

    # WHAT: Open the CSV using csv.reader.
    # WHY: csv.reader correctly handles commas and quoted text in CSV files.
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        in_distance_section = False
        row_index = 0

        for row in reader:
            if not row:
                continue

            # WHAT: Detect the start of the numeric distance section.
            # WHY: Your CSV includes many non-distance rows before the actual distance grid.
            joined = " ".join(cell.strip() for cell in row if cell.strip())
            if not in_distance_section:
                # We start when we find a line that includes HUB and also includes a "0.0" value.
                if ("HUB" in joined.upper()) and any(cell.strip().strip('"') == "0.0" for cell in row):
                    in_distance_section = True
                else:
                    continue

            # WHAT: Extract a label for the row (location/address-ish text).
            # WHY: We need a stable mapping from a location string to a matrix index.
            label = None
            for cell in row:
                c = cell.strip().strip('"')
                if not c:
                    continue
                # If it parses as float, it's not a label; keep searching.
                try:
                    float(c)
                    continue
                except ValueError:
                    label = c
                    break

            if label is None:
                continue

            # WHAT: Extract all numeric distances from the row.
            # WHY: The distance grid contains floats; blank cells represent the unused half of the matrix.
            distances: List[float] = []
            for cell in row:
                c = cell.strip().strip('"')
                if not c:
                    continue
                try:
                    distances.append(float(c))
                except ValueError:
                    # Ignore non-numeric cells like labels.
                    pass

            address_index_map[label] = row_index
            distance_matrix.append(distances)
            row_index += 1

    return distance_matrix, address_index_map


def get_distance(distance_matrix: List[List[float]], i: int, j: int) -> float:
    # WHAT: Return the distance between location i and j.
    # WHY: The WGUPS distance table is typically lower-triangular (only one half filled), so we must safely try (i,j) then (j,i).
    if i == j:
        return 0.0

    # Try direct (may fail if the row is shorter / ragged)
    if i < len(distance_matrix) and j < len(distance_matrix[i]):
        return distance_matrix[i][j]

    # Try swapped
    if j < len(distance_matrix) and i < len(distance_matrix[j]):
        return distance_matrix[j][i]

    raise IndexError(f"Distance not found for indices ({i}, {j})")


def get_location_index(package_address: str, address_index_map: Dict[str, int]) -> int:
    # WHAT: Convert a package street address into a distance-table index.
    # WHY: Distance table keys and package addresses don't always match character-for-character.
    # HOW: Normalize both strings (lowercase, remove punctuation, collapse spaces) and match.

    def norm(s: str) -> str:
        s = s.lower().strip()
        # remove punctuation that commonly breaks substring matching
        for ch in [",", ".", "#", '"', "'"]:
            s = s.replace(ch, "")
        # collapse repeated whitespace
        s = " ".join(s.split())
        return s

    target = norm(package_address)

    # 1) Try direct normalized substring match
    for key, idx in address_index_map.items():
        if target in norm(key):
            return idx

    # 2) Fallback: try matching by the first 2-3 tokens (helps with "Station bus Loop" variations)
    tokens = target.split()
    if len(tokens) >= 3:
        short_target = " ".join(tokens[:3])
        for key, idx in address_index_map.items():
            if short_target in norm(key):
                return idx

    raise KeyError(f"Address not found in distance table keys: {package_address}")


def deliver_truck(
        truck_ids: List[int],
        start_time: datetime,
        truck_number: int,
        packages: HashTable,
        distance_matrix: List[List[float]],
        address_index_map: Dict[str, int],
        hub_key: str,
        earliest_departure: datetime | None = None
) -> Tuple[float, datetime, int]:

    # WHAT: Deliver all packages on one truck using Nearest Neighbor.
    # WHY: Required core algorithm for the WGUPS delivery simulation.
    # RETURNS: (total_miles, end_time, end_location_index)

    miles = 0.0
    current_time = start_time
    current_loc = address_index_map[hub_key]

    # If this truck must wait (driver availability / address correction), push departure forward.
    if earliest_departure is not None and current_time < earliest_departure:
        current_time = earliest_departure

    # Package 9 address correction: At 10:20 a.m. WGUPS receives the corrected address for package 9.
    # Update the package record before routing so the distance lookup uses the correct stop.
    if 9 in truck_ids and current_time >= ADDRESS_FIX_TIME:
        p9 = packages.lookup(9)
        p9.address = "410 S State St"
        p9.zip_code = "84111"

    # Mark packages as loaded/en route at departure time
    for pid in truck_ids:
        p = packages.lookup(pid)
        p.truck_number = truck_number
        p.load_time = current_time.time()
        p.delivery_status = "En Route"

    remaining = truck_ids.copy()

    while remaining:
        closest_pid = None
        closest_idx = None
        min_dist = float("inf")

        for pid in remaining:
            p = packages.lookup(pid)
            dest_idx = get_location_index(p.address, address_index_map)
            d = get_distance(distance_matrix, current_loc, dest_idx)
            if d < min_dist:
                min_dist = d
                closest_pid = pid
                closest_idx = dest_idx

        # Travel to closest stop
        miles += min_dist
        minutes = (min_dist / 18.0) * 60.0
        current_time = current_time + timedelta(minutes=minutes)
        current_loc = closest_idx

        # Deliver it
        delivered_pkg = packages.lookup(closest_pid)
        delivered_pkg.delivery_time = current_time.time()
        delivered_pkg.delivery_status = "Delivered"

        remaining.remove(closest_pid)

    return miles, current_time, current_loc


# Truck Package Assignments
# WHAT: Define which packages are loaded onto each truck.
# WHY: Keep behavior deterministic and match WGUPS constraints (truck-only, group deliveries, delays).

# Package 9 address is corrected at 10:20 AM (cannot be delivered before this time).
ADDRESS_FIX_TIME = datetime(2025, 1, 1, 10, 20)

# Packages delayed on flight do not arrive at the hub until 09:05 AM.
DELAYED_FLIGHT_TIME = datetime(2025, 1, 1, 9, 5)
DELAYED_FLIGHT_PACKAGES = {6, 25, 28, 32}

# Truck 1: includes the "must be delivered with" group and early-deadline packages.
TRUCK_1_IDS = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

# Truck 2: includes all "truck 2 only" packages and the delayed-on-flight set.
TRUCK_2_IDS = [3, 6, 18, 25, 28, 32, 36, 38, 4, 5, 7, 8, 10, 11]

# Truck 3: remaining packages (includes package 9 which has a corrected address at 10:20 a.m.)
TRUCK_3_IDS = [2, 9, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39]


'''
# Quick Verification (DISABLED)
# WHAT: Quick proof that deliveries run and package 9 is not delivered before 10:20.
# WHY: This was used for testing; the interface below is the deliverable for D1–D3.
if __name__ == "__main__":
    packages = load_packages("data/WGUPS_Package_File.csv")
    dist_matrix, addr_map = load_distances("data/WGUPS_Distance_Table.csv")
    hub_key = "Western Governors University\n4001 South 700 East, \nSalt Lake City, UT 84107"

    miles1, t1_end_time, _ = deliver_truck(TRUCK_1_IDS, datetime(2025, 1, 1, 8, 0), 1, packages, dist_matrix, addr_map, hub_key)
    miles2, t2_end_time, _ = deliver_truck(TRUCK_2_IDS, datetime(2025, 1, 1, 9, 5), 2, packages, dist_matrix, addr_map, hub_key)

    driver_available = min(t1_end_time, t2_end_time)
    earliest_t3 = max(driver_available, ADDRESS_FIX_TIME)

    miles3, t3_end_time, _ = deliver_truck(TRUCK_3_IDS, driver_available, 3, packages, dist_matrix, addr_map, hub_key, earliest_departure=earliest_t3)

    print("TOTAL miles:", miles1 + miles2 + miles3)
    print("Package 9:", packages.lookup(9))
'''


def print_package_statuses_at_time(packages: HashTable, query_time: datetime):
    # WHAT: Display the status of every package at a user-specified time.
    # WHY: Required interface feature for Task 2 status checks (D1–D3).

    for package_id in range(1, 41):
        p = packages.lookup(package_id)
        # Display-only fix for Package 9: Before 10:20, show the original (incorrect) address even though the simulation later corrects it.
        display_address = p.address
        display_zip = p.zip_code

        if p.package_id == 9 and query_time < ADDRESS_FIX_TIME:
            display_address = getattr(p, "original_address", p.address)
            display_zip = getattr(p, "original_zip_code", p.zip_code)


        # Delayed-on-flight packages are not at the hub until 9:05.
        if package_id in DELAYED_FLIGHT_PACKAGES and query_time < DELAYED_FLIGHT_TIME:
            status = "Delayed"
        elif query_time.time() < p.load_time:
            status = "At Hub"
        elif p.delivery_time is None or query_time.time() < p.delivery_time:
            status = "En Route"
        else:
            status = "Delivered"

        delivered_time_text = ""
        if status == "Delivered" and p.delivery_time is not None:
            delivered_time_text = f" | Delivered Time: {p.delivery_time}"

        print(
            f"Package ID: {p.package_id} | "
            f"Delivery Address: {display_address} | "
            f"Delivery Deadline: {p.deadline} | "
            f"Truck: {p.truck_number} | "
            f"Delivery Status: {status} | "
            f"{delivered_time_text}"
        )

def run_interface(packages: HashTable, total_miles: float):
    # WHAT: Simple command-line menu for checking package statuses.
    # WHY: This is the required interface for Task 2 section D & E

    while True:
        print("\nWGUPS Package Status Interface")
        print("1) View all package statuses at a specific time")
        print("2) View total mileage")
        print("3) Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            time_input = input("Enter time (HH:MM): ").strip()
            hours, minutes = map(int, time_input.split(":"))
            query_time = datetime(2025, 1, 1, hours, minutes)

            print(f"\nPackage statuses at {time_input}:")
            print_package_statuses_at_time(packages, query_time)

        elif choice == "2":
            print(f"\nTotal mileage traveled by all trucks: {total_miles}")

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    # WHAT: Load data, run deliveries to populate times/statuses, then start the interface.
    # WHY: Status checks only make sense after packages have load/delivery times.

    packages = load_packages("data/WGUPS_Package_File.csv")
    dist_matrix, addr_map = load_distances("data/WGUPS_Distance_Table.csv")
    hub_key = "Western Governors University\n4001 South 700 East, \nSalt Lake City, UT 84107"

    # Truck 1 and Truck 2 have fixed start times based on the scenario.
    miles1, t1_end_time, _ = deliver_truck(TRUCK_1_IDS, datetime(2025, 1, 1, 8, 0), 1, packages, dist_matrix, addr_map, hub_key)
    miles2, t2_end_time, _ = deliver_truck(TRUCK_2_IDS, datetime(2025, 1, 1, 9, 5), 2, packages, dist_matrix, addr_map, hub_key)

    # Two-driver rule: Truck 3 can leave when the first driver returns.
    driver_available = min(t1_end_time, t2_end_time)

    # Package 9 rule: address correction at 10:20; Truck 3 cannot depart before that.
    earliest_t3 = max(driver_available, ADDRESS_FIX_TIME)

    miles3, _, _ = deliver_truck(TRUCK_3_IDS, driver_available, 3, packages, dist_matrix, addr_map, hub_key, earliest_departure=earliest_t3)

    # WHAT: Total mileage across all trucks.
    # WHY: Used by the interface menu option to display total mileage.
    total_miles = miles1 + miles2 + miles3

    # Start the user interface for D1–D3 screenshots.
    run_interface(packages, total_miles)
