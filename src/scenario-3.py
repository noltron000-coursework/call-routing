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

"""TODO: Might Have to modify this since I don't know if we have to know the carrier name"""


class CallRouting:

    def __init__(self, phone_number_files, carriers):
        self.carriers = self._format_carriers(carriers)  # A dictionary of {'carrier name', file path}

        self.phone_numbers_paths = []

        for file in phone_number_files:
            self.phone_numbers_paths.append(os.path.join(THIS_FOLDER, file + '.txt'))  # A path string of to the phone number file

        self.dict_of_routes = {}  # dictionary of string : double  {carrier : [(route number, price)]}
        self.list_of_numbers = []  # list of strings  [phone numbers]

    def run(self):
        self._get_routes_from_carriers()
        self._get_phone_numbers()

    def _get_phone_numbers(self):
        """Convert the given phone numbers file to a list of phone number [String]"""
        for path in self.phone_numbers_paths:
            with open(path) as f:
                self.list_of_numbers = f.read().splitlines()

        print(len(self.list_of_numbers))

    def _format_carriers(self, carriers):
        """Format the carrier dictionary value into a proper file path."""
        new_dict = {}
        # Create new dictionary with the proper file path
        for pair in carriers:
            new_dict[pair[0]] = os.path.join(THIS_FOLDER, pair[1] + '.txt')

        return new_dict

    def _get_routes_from_carriers(self):
        """Must be call after self._format_carriers is done."""
        for key in self.carriers.keys():
            with open(self.carriers[key]) as f:
                file = f.read().splitlines()
                for line in file:
                    route_number, price = line.split(',')
                    tup = (route_number, float(price))
                    if key in self.dict_of_routes:
                        self.dict_of_routes[key].append(tup)
                    else:
                        self.dict_of_routes[key] = [tup]


    # def _get_routes_dict(self):
    #     """Convert the given routes file to a dictionary {route number : lowest price}"""
    #     for path in self.routes_paths:
    #         with open(path) as f:
    #             file = f.read().splitlines()
    #
    #             for line in file:
    #                 route_number, price = line.split(",")  # Split the route into route_number , price
    #
    #                 if route_number in self.dict_of_routes:  # Check if the route number existed in the dictionary
    #
    #                     current_value = self.dict_of_routes[route_number]  # The existing price for the route
    #                     new_value = float(price)  # The new price for the same route
    #
    #                     if new_value < current_value:  # Check if the new price is less than the existing price
    #                         self.dict_of_routes[route_number] = new_value
    #
    #                 else:
    #                     self.dict_of_routes[route_number] = float(price)  # Set a new key value to the dictionary

    # def _get_prices(self):
    #     """Get the lowest prices for each phone number by matching the most matched prefix route"""
    #     price_for_phone = {}
    #
    #     for number in self.list_of_numbers:  # loop through the list of phone numbers
    #         num_string = ''  # Act as a prefix for the phone number
    #         for character in number:
    #             num_string += character  # Add a character to the prefix
    #
    #             if num_string in self.dict_of_routes:  # if the prefix is in the dictionary of routes
    #                 price_for_phone[number] = self.dict_of_routes[num_string]  # Set the price to the phone number
    #
    #         if number not in price_for_phone:  # The phone number doesn't have any matching prefixes
    #             price_for_phone[number] = 0
    #
    #     for key in price_for_phone.keys():  # Print the expected output for the assignment
    #         price = price_for_phone[key]
    #         print(key + ',' + str(price))


phone_data_files = (
    "phone-numbers-3",
    "phone-numbers-10",
    "phone-numbers-100",
    "phone-numbers-1000",
    "phone-numbers-10000",
)

route_carriers = (('Carrier A', "route-costs-10"),
                  ('Carrier B', "route-costs-100"),
                  ('Carrier C', "route-costs-600"),
                  ('Carrier D', "route-costs-35000"),
                  ('Carrier E', "route-costs-106000"),
                  ('Carrier F', "route-costs-1000000"))

route = CallRouting(phone_data_files, route_carriers)

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
