# Package record used throughout the delivery simulation.

from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class Package:
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

    delivery_status: str = "At Hub"

    load_time: Optional[time] = None

    delivery_time: Optional[time] = None

    truck_number: Optional[int] = None

    def __str__(self) -> str:
        return (
            f"Package({self.package_id}) | {self.address}, {self.city} {self.state} {self.zip_code} | "
            f"Deadline: {self.deadline} | Weight: {self.weight_kilo} | "
            f"Status: {self.delivery_status} | "
            f"Load: {self.load_time} | Delivered: {self.delivery_time} | Truck: {self.truck_number}"
        )
