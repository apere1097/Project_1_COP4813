import json


def read_from_file(file_name):
    with open (file_name, "r") as read_file:
        data = json.load(read_file)
        print("\nYou successfully opened {}".format(file_name))
    return data


def save_into_file(data, file_name):
    with open (file_name, "w") as write_file:
        json.dump(data, write_file, indent=2)
        print("You successfully wrote into {}".format(file_name))