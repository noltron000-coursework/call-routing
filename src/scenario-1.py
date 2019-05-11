

# Scenario 1: One-time route cost check
#
# You have a carrier route list with 100,000 (100K) entries (in arbitrary order)
# and a single phone number. How quickly can you find the cost of calling this number?
from pathlib import Path

class CallRouting:

    def __init__(self, phone_number_file, routing_file):
        self.routes_file = routing_file  # string without the extension
        self.phone_numbers_file = phone_number_file  # string without the extension
        self.dict_of_routes = {}  # dictionary of string : double
        self.list_of_numbers = []  # list of strings

    def run(self):
        self._get_phone_numbers()
        print(self.list_of_numbers)

    def _get_phone_numbers(self):
        # Subtitute this with your path
        file_path = '/Users/jackson_ho/dev/CS_Course_work/CS1.3/call-routing/data/'
        with open(file_path + self.phone_numbers_file) as f:
            file = f.readline()
            for number in file:
                self.list_of_numbers.append(number)


route = CallRouting('phone-numbers-3.txt', 'route-costs-10.txt')

route.run()

# Just use Command / Control + F to find the phone number in the route file
