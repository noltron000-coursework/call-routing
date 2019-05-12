"""
Scenario 2: List of route costs to check.

You have a carrier route list with 100,000 (100K) entries &
a list of 1000 phone numbers, in an arbitrary order.
How can you operationalize the route cost lookup problem?
"""

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
        # {route number:lowest price}
        self.route_dict = route_dict.dictionary

        # dictionary of phone string...
        # {phone number:NONE }
        self.phone_dict = phone_dict.dictionary

        # dictionary of string:double...
        # {phone number:lowest price}
        self.price_dict = {}

        # our goal is to take the first two dictionaries, &
        # generate a list of numbers with prices.
        self.get_prices()

    def __repr__(self):
        """
        """
        pretty_dict = ""
        for key in self.price_dict:
            price = self.price_dict[key]
            # prettify entry before adding to output
            entry = f"{' '*(14-len(key))}{key}: ${price}\n"
            pretty_dict += entry
        return pretty_dict

    def get_prices(self):
        """
        Get the lowest prices for each phone number.
        Do this by matching the most matched prefix route.
        """
        # loop through the list of phone numbers
        for phone in self.phone_dict:
            # slowly expand on the search of our phone num.
            # we start with the broadest possible match.
            # as the loop continues, it gets more specific.
            # ---
            # for example: 3334445678
            # step 1)  3
            # step 2)  33
            # step 3)  333
            # step 4)  3334
            # step 5)  33344
            # step 6)  333444
            # step 7)  3334445
            # step 8)  33344456
            # step 9)  333444567
            # step 10) 3334445678
            # "prefix" represents this gradient of changes.
            prefix = ""

            # loop a number of times equal to phone length.
            for digit in phone:
                # specify an additional digit on prefix.
                prefix += digit
                # check if prefix matches an entry exactly.
                if prefix in self.route_dict:
                    # set the price to the phone number.
                    self.price_dict[phone] = self.route_dict[prefix]
            pass  # end for loop

            # check if phone# has no matching prefixes.
            if phone not in self.price_dict:
                self.price_dict[phone] = 0
        pass  # end for loop

        # print the expected output for the assignment,
def benchmark_memory():
    # get memory usage
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # linux returns kb and macOS returns bytes,
    # here we convert both to mb
    if platform.system() == "linux":
        # convert kb to mb and round to 2 digits
        usage = round(usage / float(1 << 10), 2)
    else:
        # convert bytes to mb and round to 2 digits
        usage = round(usage / float(1 << 20), 2)

    # return memory usage string
    return(f"Memory Usage: {usage} mb")

if __name__ == "__main__":
    # stopwatch ready, set, go!
    start = time.time()

    # create CallRouter class, and print its dict
    route = CallRouting("phone-numbers-1000", "route-costs-106000")
    print(route)

    # stopwatch finish!!
    end = time.time()

    # print benchmarks
    print(f"     Runtime: {str(round(end - start, 3))} sec")
    print(benchmark_memory())
