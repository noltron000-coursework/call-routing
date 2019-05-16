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
import pickle


THIS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "data"))


class CallRouting:

    def __init__(self, phone_number_files, carriers):
        self.carriers = self._format_carriers(carriers)  # A dictionary of {'carrier name', file path}

        self.phone_numbers_paths = []
        self.decimal_search_tree = self.check_pickle()
        for file in phone_number_files:
            self.phone_numbers_paths.append(os.path.join(THIS_FOLDER, file + '.txt'))  # A path string of to the phone number file

        self.dict_of_routes = {}  # dictionary of string : double  {carrier : [(route number, price)]}
        self.list_of_numbers = []  # list of strings  [phone numbers]

    def check_pickle(self):
        """Check if the tree was already made."""
        try:
            tree = pickle.load(open("save.p", "rb"))
            if tree:
                return tree

        except FileNotFoundError:  # Signalling that the tree hadn't been made yet
            return DecimalSearchTree()

    def run(self):
        """This function will run all the functions necessary"""
        start_creating_phone_numbers = time.perf_counter()
        self._get_phone_numbers()
        end = time.perf_counter()
        print("Runtime to create a list of phone number: " + str(end - start_creating_phone_numbers))

        start_creating_tree = time.perf_counter()
        if self.decimal_search_tree.size == 0:
            start_creating_dict = time.perf_counter()
            self._get_routes_from_carriers()
            end_dict = time.perf_counter()
            print("Runtime to create a dictionary of route numbers: " + str(end_dict - start_creating_dict))
            self.popuplate_tree()
        else:
            pass
        end_tree = time.perf_counter()

        print(self.decimal_search_tree.size)
        pickle.dump(self.decimal_search_tree, open("save.p", "wb"))
        print('Runtime for creating tree: ' + str(end_tree - start_creating_tree))

        start_searching = time.perf_counter()
        result = self.check_prices()
        end_searching = time.perf_counter()
        print("Runtime for searching phone number: " + str(end_searching - start_searching))

        start_writing_file = time.perf_counter()
        self.write_result(result)
        end_writing = time.perf_counter()
        print("Runtime of writing result to file:"  + str(end_writing - start_writing_file))

    def _get_phone_numbers(self):
        """Convert the given phone numbers file to a list of phone number [String]"""
        for path in self.phone_numbers_paths:
            with open(path) as f:
                self.list_of_numbers = f.read().splitlines()  # O(n) where n is the number of phone numbers

    def _format_carriers(self, carriers):
        """Format the carrier dictionary value into a proper file path."""
        new_dict = {}
        # Create new dictionary with the proper file path
        for pair in carriers:  # O(n) where n is that number of route files
            new_dict[pair[0]] = os.path.join(THIS_FOLDER, pair[1] + '.txt')

        return new_dict

    def _get_routes_from_carriers(self):
        """Must be call after self._format_carriers is done.
           This function read the route file and dictionary of carrier, route numbers and prices
           Example: {"Carrier name": [(route number, price)]}"""
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
        """Convert the dictionary of routes prices into a tree
           The data in the tree node will be a tuple of ("Carrier name", price)"""
        for key in self.dict_of_routes.keys():
            list_of_route_prices = self.dict_of_routes[key]
            for item in list_of_route_prices:
                number = item[0][1:]
                data = (key, item[1])
                self.decimal_search_tree.insert(number, data)

    def check_prices(self):
        """Check the price of the phone numbers in the tree.
           This function will traverse the tree accordance to the phone number and return the price of the
           longest matching prefix, other wise return 0.
           Example Output: Found ("Carrier name", price)
                           Not Found (None, 0)  """

        result_prices = []  # [(phone number, (carrier name, price))]
        for number in self.list_of_numbers:
            search_result = self.decimal_search_tree.find_prices(number[1:])
            if search_result is None:  # signalling that there is no matching prefix for the current number
                result_prices.append((number, ('None', 0)))  # Appending this way to keep everything consistent
            else:
                result_prices.append((number, search_result))  # Found the longest matching prefix and got a price

        return result_prices

    def write_result(self, result_list):
        """Write the result to a new file"""
        with open("result-cost-3.txt", 'w') as f:
            for result in result_list:
                f.write(str(result[0]) + ',' + str(result[1][1]) + '\n')


phone_data_files = [
        "phone-numbers-3",
        "phone-numbers-10",
        "phone-numbers-100",
        "phone-numbers-1000",
        "phone-numbers-10000",
                    ]

route_carriers = [
        ('Carrier A', "route-costs-10"),
        ('Carrier B', "route-costs-100"),
        ('Carrier C', "route-costs-600"),
        ('Carrier D', "route-costs-35000"),
        ('Carrier E', "route-costs-106000"),
        ('Carrier F', "route-costs-1000000"),
        ('Carrier G', "route-costs-10000000")
                ]

route = CallRouting(phone_data_files, route_carriers)

start = time.perf_counter()
route.run()
end = time.perf_counter()
print('\nOverall Runtime: ' + str(end - start))

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
