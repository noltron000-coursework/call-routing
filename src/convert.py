import os

def parse_data(data_files, make_dict_helper):
    """
    read_data() will check if the python data file exists.
    if it doesn"t exist, it will open the text data file,
    & it will then create the respective python data file.
    """

    try: # create the dict folder if it doesn't exist
        os.mkdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "dict")))
    except: # otherwise, don't let python freak out haha!
        pass 

    # get folders from using os
    DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "data"))
    DICT_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "dict"))

    # loop through each data file here.
    for file_name in data_files:
        # record the path of the data files.
        file_path_txt = os.path.join(DATA_FOLDER, file_name + ".txt")
        file_path_py = os.path.join(DICT_FOLDER, file_name + ".py")

        try: # do nothing if the python data file exists.
            # open the python file if it exists...
            file = open(file_path_py, "r")
            # if there was no error, it exists!

        except: # otherwise, process the text data file.
            # open text file for reading
            txt_file = open(file_path_txt,"r")
            # create new python file for writing
            py_file = open(file_path_py,"w+")

            # generate dictionary using the helper function.
            dictionary = make_dict_helper(txt_file)
            # print data into file to be imported later.
            print('dictionary = ' + str(dictionary), file=py_file)

            # close files for good practice
            txt_file.close()
            py_file.close()

def _make_phone_dict(file):
    # start with an empty dictionary of phone numbers.
    phone_dict = {}
    for line in file.readlines():
        # get the phone number from this line.
        # remove the \n newline char, its not needed.
        phone = line[:-2]
        # add the phone number to the dictionary.
        # notice how there is no value associated with it.
        phone_dict[phone] = None
    # return the comprehensive phone_dict we just created.
    return phone_dict

def _make_route_dict(file):
    # start with an empty dictionary of route costs.
    route_dict = {}
    for line in file.readlines():
        # get the route and price from this line.
        route, price = line.split(",")
        price = float(price)

        # check if route exists.
        # if it does, add the price to its price list.
        if route in route_dict:
            # TODO just check if its greater or lesser
            route_dict[route].append(price)
        # otherwise, create a new price list with one value.
        else:
            route_dict[route] = [price]
    # return the comprehensive route_dict we just created.
    return route_dict

def main():
    # all the names of the data files.
    phone_data_files = (
        "phone-numbers-3",
        "phone-numbers-10",
        "phone-numbers-100",
        "phone-numbers-1000",
        "phone-numbers-10000",
    )
    route_data_files = (
        "route-costs-10",
        "route-costs-100",
        "route-costs-600",
        "route-costs-35000",
        "route-costs-106000",
        "route-costs-1000000"
    )
    # run the function process here.
    print('generating data files...')
    parse_data(phone_data_files, _make_phone_dict)
    parse_data(route_data_files, _make_route_dict)
    print('...process completed!')

if __name__ == "__main__":
    main()
