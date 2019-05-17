"""
Scenario 2: List of route costs to check.

You have a carrier route list with 100,000 (100K) entries &
a list of 1000 phone numbers, in an arbitrary order.
How can you operationalize the route cost lookup problem?
"""


# import necessary modules
import time
import platform
import resource
import convert # local module


class CallRouting:
    def __init__(self, phone_numbers, route_costs):
        # run convert to generate files
        convert.main(phone_numbers, route_costs)

        # import data dictionaries
        # from given text file inputs.
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
        String representation of a dictionary.
        Lines up things pretty nicely!
        """
        pretty_dict = ""
        for key in self.price_dict:
            price = self.price_dict[key]
            # prettify entry before adding to output.
            entry = f"{' '*(14-len(key))}{key}: ${price}\n"
            pretty_dict += entry
        return pretty_dict


    def get_prices(self):
        """
        Get the lowest prices for each phone number.
        Do this by matching the most matched prefix route.
        """
        # loop through the list of phone numbers.
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


def benchmark_memory():
    # get memory usage
    usage = resource.getrusage(
        resource.RUSAGE_SELF).ru_maxrss

    # linux returns kilobytes and macOS returns bytes.
    # here we convert both to megabytes.
    if platform.system() == "linux":
        # convert kb to mb and round to 2 digits.
        usage = round(usage / float(1 << 10), 2)
    else:
        # convert bytes to mb and round to 2 digits.
        usage = round(usage / float(1 << 20), 2)

    # return memory usage string.
    return(f"Memory Usage: {usage} mb")


if __name__ == "__main__":
    # stopwatch ready, set, go!
    start = time.time()

    # NOTE change these values if you want different files.
    phone_numbers = "phone-numbers-10000"
    route_costs = "route-costs-10000000"

    # create CallRouter class, and print its dict.
    route = CallRouting(phone_numbers, route_costs)

    # print the pricelist for the route;
    # required as the expected result for the assignment,
    print(route)

    # stopwatch finish!!
    end = time.time()

    # compute runtime.
    runtime = round(end - start, 3)

    # check if the runtime is too long.
    if runtime > 10:
        # print warning about long runtimes.
        print("""
        The first time this file runs, it is slow.
        It will be faster on your next run.
        __pycache__ will store some data; our app will
        also generates some dictionaries for future use.\n
        """)

    # print benchmarks.
    print(f"     Runtime: {str(runtime)} sec")
    print(benchmark_memory())
