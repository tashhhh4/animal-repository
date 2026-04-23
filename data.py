import json

def load_data(file_path):
    """ Loads a JSON file. """
    with open(file_path, "r") as file:
        return json.load(file)