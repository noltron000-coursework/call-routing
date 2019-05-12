# Scenario 3: Multiple long carrier route lists
#
# You have 5 carrier route lists, each with 10,000,000 (10M) entries (in arbitrary order)
# and a list of 10,000 phone numbers. How can you speed up your route cost lookup solution
# to handle this larger dataset?

import time
import os
import resource
import platform

THIS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "data"))


class CallRouting:

    def __init__(self, phone_number_files, routing_files):
        self.routes_paths = []
        for file in routing_files:
            self.routes_paths.append(os.path.join(THIS_FOLDER, file))  # A path string of to the route file)

        self.phone_numbers_paths = []

        for file in phone_number_files:
            self.phone_numbers_paths.append(os.path.join(THIS_FOLDER, file)) # A path string of to the phone number file

        self.dict_of_routes = {}  # dictionary of string : double  {route number : lowest price}
        self.list_of_numbers = []  # list of strings  [phone numbers]

    def run(self):
        self._get_routes_dict()
        self._get_phone_numbers()
        self._get_prices()

    def _get_phone_numbers(self):
        """Convert the given phone numbers file to a list of phone number [String]"""
        for path in self.phone_numbers_paths:
            with open(path) as f:
                file = f.readlines()
                for number in file:
                    self.list_of_numbers.append(number[:-2])

    def _get_routes_dict(self):
        """Convert the given routes file to a dictionary {route number : lowest price}"""
        for path in self.routes_paths:
            with open(path) as f:
                file = f.readlines()

                for line in file:
                    route_number, price = line.split(",")  # Split the route into route_number , price

                    if route_number in self.dict_of_routes:  # Check if the route number existed in the dictionary

                        current_value = self.dict_of_routes[route_number]  # The existing price for the route
                        new_value = float(price[:-1])  # The new price for the same route

                        if new_value < current_value:  # Check if the new price is less than the existing price
                            self.dict_of_routes[route_number] = new_value

                    else:
                        self.dict_of_routes[route_number] = float(price[:-1])  # Set a new key value to the dictionary

    def _get_prices(self):
        """Get the lowest prices for each phone number by matching the most matched prefix route"""
        price_for_phone = {}

        for number in self.list_of_numbers:  # loop through the list of phone numbers
            num_string = ''  # Act as a prefix for the phone number
            for character in number:
                num_string += character  # Add a character to the prefix

                if num_string in self.dict_of_routes:  # if the prefix is in the dictionary of routes
                    price_for_phone[number] = self.dict_of_routes[num_string]  # Set the price to the phone number

            if number not in price_for_phone:  # The phone number doesn't have any matching prefixes
                price_for_phone[number] = 0

        for key in price_for_phone.keys():  # Print the expected output for the assignment
            price = price_for_phone[key]
            print(key + ',' + str(price))


route = CallRouting(['phone-numbers-10000.txt'], ['route-costs-10000000.txt'] * 5)

start = time.time()
route.run()
end = time.time()
print('\nRuntime: ' + str(end - start))

# get memory usage
usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

# linux returns kb and macOS returns bytes,
# here we convert both to mb
if platform.system() == 'linux':
    # convert kb to mb and round to 2 digits
    usage = round(usage / float(1 << 10), 2)
else:
    # convert bytes to mb and round to 2 digits
    usage = round(usage / float(1 << 20), 2)

# print memory usage
print("Memory Usage: {} mb.".format(usage))
