import os
import csv
import sys


class CarBase:
    """
        Class Base Car
    """

    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type  # 'car', 'truck', 'spec_machine'
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    """
        Class Passenger Car
    """

    def __init__(self, car_type, brand, photo_file_name, carrying, passenger_seats_count):
        super(Car, self).__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    """
        Class Truck
    """

    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl):
        super(Truck, self).__init__(car_type, brand, photo_file_name, carrying)
        self.body_length, self.body_width, self.body_height = \
            list(map(float, body_whl.split('x'))) if body_whl else (0, 0, 0)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    """
        Class Special Machine
    """

    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super(SpecMachine, self).__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # skip headers
        for row in reader:
            print(row)
            if len(row) == 7:   # check rows len
                car_type, brand, passenger_seats_count, \
                 photo_file_name, body_whl, carrying, extra = tuple(row)
                try:    # check car_type from row
                    if car_type == 'car':
                        car_list.append(Car(car_type, brand, photo_file_name,
                                            carrying, passenger_seats_count))
                    elif car_type == 'truck':
                        car_list.append(Truck(car_type, brand, photo_file_name,
                                              carrying, body_whl))
                    elif car_type == 'spec_machine':
                        car_list.append(SpecMachine(car_type, brand, photo_file_name,
                                                    carrying, extra))
                except TypeError as err:
                    print("TypeError", err.args[0])
    return car_list


if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))
