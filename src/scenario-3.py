# Scenario 3: Multiple long carrier route lists
#
# You have 5 carrier route lists, each with 10,000,000 (10M) entries (in arbitrary order)
# and a list of 10,000 phone numbers. How can you speed up your route cost lookup solution
# to handle this larger dataset?

from decimaltree import DecimalSearchTree
import os
import resource
import platform
import time

THIS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "data"))


class CallRouting:

    def __init__(self, phone_number_files, carriers):
        self.carriers = self._format_carriers(carriers)  # A dictionary of {'carrier name', file path}

        self.phone_numbers_paths = []
        self.decimal_search_tree = DecimalSearchTree()
        for file in phone_number_files:
            self.phone_numbers_paths.append(os.path.join(THIS_FOLDER, file + '.txt'))  # A path string of to the phone number file

        self.dict_of_routes = {}  # dictionary of string : double  {carrier : [(route number, price)]}
        self.list_of_numbers = []  # list of strings  [phone numbers]

    def run(self):
        start_creating_dict = time.time()
        self._get_routes_from_carriers()
        self._get_phone_numbers()
        end = time.time()
        print("Runtime to create dictionary of carriers and routes, and phone number: " + str(end - start_creating_dict))

        start_creating_tree = time.time()
        self.popuplate_tree()
        end_tree = time.time()
        print('Runtime for creating tree: ' + str(end_tree - start_creating_tree))

        start_searching = time.time()
        self.check_prices()
        end_searching = time.time()
        print("Runtime for searching phone number: " + str(end_searching - start_searching))

    def _get_phone_numbers(self):
        """Convert the given phone numbers file to a list of phone number [String]"""
        for path in self.phone_numbers_paths:
            with open(path) as f:
                self.list_of_numbers = f.read().splitlines()

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

    def popuplate_tree(self):
        """Convert the dictionary of routes prices into a tree"""
        for key in self.dict_of_routes.keys():
            list_of_route_prices = self.dict_of_routes[key]
            for item in list_of_route_prices:
                number = item[0][1:]
                data = (key, item[1])
                self.decimal_search_tree.insert(number, data)

    def check_prices(self):
        """Check the price of the phone numbers in the tree"""
        result_prices = []  # [(phone number, (carrier name, price))]
        for number in self.list_of_numbers:
            search_result = self.decimal_search_tree.find_prices(number[1:])
            if search_result is None:  # signalling that there is no matching prefix for the current number
                result_prices.append((number, ('None', 0)))  # Appending this way to keep everything consistent
            else:
                result_prices.append((number, search_result))  # Found the longest matching prefix and got a price

        return result_prices


phone_data_files = [
    "phone-numbers-3",
    "phone-numbers-10",
    "phone-numbers-100",
    "phone-numbers-1000",
    "phone-numbers-10000",
]

route_carriers = [('Carrier A', "route-costs-10"),
                  ('Carrier B', "route-costs-100"),
                  ('Carrier C', "route-costs-600"),
                  ('Carrier D', "route-costs-35000"),
                  ('Carrier E', "route-costs-106000"),
                  ('Carrier F', "route-costs-1000000")]

route = CallRouting(phone_data_files, route_carriers)

start = time.time()
route.run()
end = time.time()
print('\nOver allRuntime: ' + str(end - start))

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
