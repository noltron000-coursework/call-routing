# Scenario 2: List of route costs to check
#
# You have a carrier route list with 100,000 (100K) entries (in arbitrary order)
# and a list of 1000 phone numbers. How can you operationalize the route cost lookup problem?
import time
import os

THIS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))


class CallRouting:

        def __init__(self, phone_number_file, routing_file):
            self.routes_file = os.path.join(THIS_FOLDER, routing_file)  # string without the extension
            self.phone_numbers_file = os.path.join(THIS_FOLDER, phone_number_file)  # string without the extension
            self.dict_of_routes = {}  # dictionary of string : double
            self.list_of_numbers = []  # list of strings

        def run(self):
            start = time.time()
            self._get_routes_dict()
            print(self.dict_of_routes)
            end = time.time()
            print(end - start)


        def _get_phone_numbers(self):
            # Subtitute this with your path
            with open(self.phone_numbers_file) as f:
                file = f.readlines()
                for number in file:
                    self.list_of_numbers.append(number[:-2])

        def _get_routes_dict(self):
            file_path = '/Users/jackson_ho/dev/CS_Course_work/CS1.3/call-routing/data/'
            with open(self.routes_file) as f:
                file = f.readlines()
                for route in file:
                    route_number, price = route.split(",")
                    if route_number in self.dict_of_routes:
                        list_of_prices = self.dict_of_routes[route_number]
                        list_of_prices.append(float(price[:-1]))
                    else:
                        self.dict_of_routes[route_number] = [float(price[:-1])]


route = CallRouting('phone-numbers-3.txt', 'route-costs-1000000.txt')

route.run()
