import json


# Note: this character seems to be problematic: ’
# It is not the same as this character: '
# TODO: clean this character


def load_data(file_path):
    """ Loads a JSON file. """
    with open(file_path, "r") as file:
        return json.load(file)