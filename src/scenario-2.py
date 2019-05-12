# Scenario 2: List of route costs to check
#
# You have a carrier route list with 100,000 (100K) entries (in arbitrary order)
# and a list of 1000 phone numbers. How can you operationalize the route cost lookup problem?

# import python modules
import time
import platform
import resource

# run convert module
import convert
convert.main()

class CallRouting:
    def __init__(self, phone_numbers, route_costs):
        # import data dictionaries
        # from given text file inputs
        phone_dict = __import__(phone_numbers)
        route_dict = __import__(route_costs)

        # dictionary of string:double...
        # {route number : lowest price}
        self.route_dict = route_dict.dictionary

        # dictionary of phone numbers...
        # {phone number : NONE }
        self.phone_dict = phone_dict.dictionary

        # our goal is to take these two dictionaries, &
        # generate a list of numbers with prices.
        self.get_prices()

    def get_prices(self):
        """
        Get the lowest prices for each phone number.
        Do this by matching the most matched prefix route.
        """
        phone_costs = {}

        for phone in self.phone_dict:  # loop through the list of phone numbers
            prefix = ''  # Act as a searchable prefix for the phone number
            for digit in phone:
                prefix += digit  # Add a digit to the prefix
                if prefix in self.route_dict:  # if the prefix is in the dictionary of routes
                    phone_costs[phone] = self.route_dict[prefix]  # Set the price to the phone number

            if phone not in phone_costs:  # The phone number doesn't have any matching prefixes
                phone_costs[phone] = 0

        for key in phone_costs.keys():  # Print the expected output for the assignment
            price = phone_costs[key]
            print(key + ',' + str(price))


def benchmark():
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

if __name__ == "__main__":
    # stopwatch ready, set, go!
    start = time.time()

    # create CallRouter class.
    route = CallRouting('phone-numbers-1000', 'route-costs-106000')

    # stopwatch finish!!
    end = time.time()

    # print benchmarks
    print('\nRuntime: ' + str(end - start))
    benchmark()
