import json

# Note: this character seems to be problematic: ’
# It is not the same as this character: '
# TODO: clean this character


def load_data(file_path):
    """ Loads a JSON file. """
    with open(file_path, "r") as file:
        return json.load(file)


def get_all_fields(data):
    """ Returns a list of all optional animal data fields
        underneath "characteristics" and "taxonomy".
        "Locations" and "Name" cannot be removed.
    """
    fields = {} # childkey: parentkey
    for animal in data:
        for key in animal.keys():
            if key == "name":
                pass
            elif key == "locations":
                pass
            else:
                characteristics_or_taxonomy = animal[key]
                for subkey in characteristics_or_taxonomy.keys():
                    if subkey not in fields:
                        fields[subkey] = key
    return fields
