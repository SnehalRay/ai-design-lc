'''
Create a basic parking lot system
Park a car
remove a car
check if the car is parked right now

New implementation:
different vehicle types => car, motorcycle and truck and they have different spot size


'''
from enum import Enum
import math
import uuid
from datetime import datetime


class CarType(Enum):
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    BIG_VEHICLE = "big_vehicle"


class Ticket:
    def __init__(self, ticket_id: str, entry_time, assigned_spot):
        self.id = ticket_id
        self.entry_time = entry_time
        self.assigned_spot = assigned_spot


class Car:
    def __init__(self, license_plate: str, car_type: CarType):
        self.license_plate = license_plate
        self.car_type = car_type
        self.ticket = None
        self.bill = 0


class Parking:
    def __init__(self, small_spots: int, medium_spots: int, large_spots: int):
        self.available_spots = {
            'small':  {f'S{i}' for i in range(small_spots)},
            'medium': {f'M{i}' for i in range(medium_spots)},
            'large':  {f'L{i}' for i in range(large_spots)},
        }
        self.cars_parked = {}  # license_plate -> (Car, spot_id, size)

    def _find_spot(self, car_type: CarType) -> tuple[str, str] | None:
        # greedy: use smallest viable spot first
        if car_type == CarType.MOTORCYCLE:
            order = ['small', 'medium', 'large']
        elif car_type == CarType.CAR:
            order = ['medium', 'large']
        else:  # BIG_VEHICLE
            order = ['large']

        for size in order:
            if self.available_spots[size]:
                return self.available_spots[size].pop(), size
        return None

    def park(self, license_plate: str, car_type: CarType, entering_time: datetime) -> bool:
        if license_plate in self.cars_parked:
            return False
        result = self._find_spot(car_type)
        if result is None:
            return False
        spot_id, size = result
        car = Car(license_plate, car_type)
        car.ticket = Ticket(str(uuid.uuid4()), entering_time, spot_id)
        self.cars_parked[license_plate] = (car, spot_id, size)
        return True

    def leave(self, license_plate: str, leaving_time: datetime) -> bool:
        if license_plate in self.cars_parked:
            car, spot_id, size = self.cars_parked[license_plate]
            print(f"Pay: ${self.check_bill(license_plate, leaving_time)}")

            car.ticket = None
            self.available_spots[size].add(spot_id)
            del self.cars_parked[license_plate]
            return True
        return False

    def display_parking(self) -> None:
        for size, spots in self.available_spots.items():
            print(f"{size.capitalize()} spots — {len(spots)} available: {sorted(spots)}")

    def is_parked(self, license_plate: str) -> bool:
        return license_plate in self.cars_parked

    def check_bill(self, license_plate: str, current_time: datetime):
        if license_plate not in self.cars_parked:
            return None
        car, _, _ = self.cars_parked[license_plate]
        hours = math.ceil((current_time - car.ticket.entry_time).total_seconds() / 3600)
        car.bill += hours * 5
        return car.bill


CAR_TYPE_MENU = {
    '1': CarType.MOTORCYCLE,
    '2': CarType.CAR,
    '3': CarType.BIG_VEHICLE,
}


def cli():
    print("=== Parking Lot Setup ===")
    small  = int(input("Number of small spots:  "))
    medium = int(input("Number of medium spots: "))
    large  = int(input("Number of large spots:  "))
    parking = Parking(small, medium, large)

    menu = (
        "\n--- Parking Lot ---\n"
        "1. Park a car\n"
        "2. Remove a car\n"
        "3. Display available spots\n"
        "4. Check if car is parked\n"
        "5. Check bill\n"
        "6. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Choice: ").strip()

        if choice == '1':
            plate = input("License plate: ").strip().upper()
            print("1. Motorcycle  2. Car  3. Big Vehicle")
            car_type = CAR_TYPE_MENU.get(input("Car type: ").strip())
            if car_type is None:
                print("Invalid car type.")
                continue
            if parking.park(plate, car_type, datetime.now()):
                car, spot_id, _ = parking.cars_parked[plate]
                print(f"Parked at spot {spot_id}. Ticket ID: {car.ticket.id}")
            else:
                print("Could not park: duplicate plate or lot full.")

        elif choice == '2':
            plate = input("License plate: ").strip().upper()
            if parking.leave(plate, datetime.now()):
                print("Car removed.")
            else:
                print("License plate not found.")

        elif choice == '3':
            parking.display_parking()

        elif choice == '4':
            plate = input("License plate: ").strip().upper()
            print("Parked." if parking.is_parked(plate) else "Not parked.")

        elif choice == '5':
            plate = input("License plate: ").strip().upper()
            bill = parking.check_bill(plate,datetime.now())
            if bill is None:
                print("License plate not found.")
            else:
                print(f"Current bill: ${bill}")

        elif choice == '6':
            print("Goodbye.")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == '__main__':
    cli()
