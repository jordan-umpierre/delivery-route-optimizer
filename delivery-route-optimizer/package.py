# WHAT: Define a Package data model that stores all WGUPS package fields.
# WHY: The program must store/retrieve package information (address, deadline, city, zip, weight, status/time) and update status throughout the delivery simulation.

from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class Package:
    # WHAT: Represents one package and all required delivery information.
    # WHY: Package records must be stored in the custom hash table and updated as trucks deliver them.

    package_id: int
    address: str
    deadline: str
    city: str
    state: str
    zip_code: str
    weight_kilo: str
    # Package 9 special-case support (wrong address until 10:20)
    original_address: str | None = None
    original_zip_code: str | None = None
    corrected_address: str | None = None
    corrected_zip_code: str | None = None


    # Tracking / simulation fields

    # WHAT: Current status of the package ("At Hub", "En Route", "Delivered").
    # WHY: The UI must show the correct package status at any user-entered time.
    delivery_status: str = "At Hub"

    # WHAT: Time the package was loaded onto a truck.
    # WHY: Helps determine when a package transitions from "At Hub" to "En Route".
    load_time: Optional[time] = None

    # WHAT: Time the package was delivered.
    # WHY: Required to show delivery status with time and determine "Delivered" at user-entered times.
    delivery_time: Optional[time] = None

    # WHAT: Which truck delivered the package.
    # WHY: Helpful for debugging, reporting, and showing assignments.
    truck_number: Optional[int] = None

    def __str__(self) -> str:
        #WHAT: Provide a readable string representation of the package.
        #WHY: Makes it easy to print package records during lookup and debugging verification.
        return (
            f"Package({self.package_id}) | {self.address}, {self.city} {self.state} {self.zip_code} | "
            f"Deadline: {self.deadline} | Weight: {self.weight_kilo} | "
            f"Status: {self.delivery_status} | "
            f"Load: {self.load_time} | Delivered: {self.delivery_time} | Truck: {self.truck_number}"
        )
