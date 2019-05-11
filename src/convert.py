import os


def parse_data(data_files):
    """
    read_data() will check if the python data file exists.
    if it doesn"t exist, it will open the text data file,
    & it will then create the respective python data file.
    """
    # get data folder from using os
    DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "data"))

    # loop through each data file here.
    for file_name in data_files:
        # record the path of the data files.
        file_path_txt = os.path.join(DATA_FOLDER, file_name + ".txt")
        file_path_py = os.path.join(DATA_FOLDER, "dict-" + file_name + ".py")

        #  do nothing if the python data file exists.
        try:
            file = open(file_path_py, "r")
            print(file_name + ".py exists!")

        # otherwise, take the text data file and process it.
        # here we will create the python data file.
        except:
            print(os.getcwd())
            # open text file for reading
            txt_file = open(file_path_txt,"r")
            # create new python file for writing
            py_file = open(file_path_py,"w+")

            for line in txt_file.readlines():
                # we need to parse each line into data
                # check if there are any commas
                pass

            # close files for good practice
            txt_file.close()
            py_file.close()

if __name__ == "__main__":
    # all the names of the data files.
    main_data_files = (
        "phone-numbers-3",
        "phone-numbers-10",
        "phone-numbers-100",
        "phone-numbers-1000",
        "phone-numbers-10000",
        "route-costs-10",
        "route-costs-100",
        "route-costs-600",
        "route-costs-35000",
        "route-costs-106000",
        "route-costs-1000000"
    )
    # run the function process here.
    parse_data(main_data_files)
