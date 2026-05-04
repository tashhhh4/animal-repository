import json
import requests


def clean_data(data_str):
    """ Replaces some problematic characters with appropriate substitutes. """
    data_str = data_str.replace("â€™", "'")  # apostrophe character
    data_str = data_str.replace("â€“", "–")  # dash character
    return data_str


def load_data(file_path):
    """ Loads a JSON file. """
    with open(file_path, "r") as file:
        data_str = file.read()
        cleaned_str = clean_data(data_str)
        return json.loads(cleaned_str)


def fetch_data(api_key, animal_query):
    """ Fetches JSON data from the Animals API """
    headers = {"X-Api-Key": api_key}
    response = requests.get(f'https://api.api-ninjas.com/v1/animals?name={animal_query}', headers=headers)
    json = response.json()
    return json


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


def get_values_sample(data, field, subfield, num=3):
    """ Returns a list of `num` length containing a selection of values
        from the same field across different items in the data set.
    """
    i = 0
    values = set() # Use a set to try and capture more unique values
    while num > 0 and i < len(data):
        animal = data[i]
        if field in animal:
            if subfield:
                if subfield in animal[field]:
                    len_before = len(values)
                    values.add(animal[field][subfield])
                    if len_before < len(values):
                        num -= 1
            else:
                len_before = len(values)
                values.add(animal[field])
                if len_before < len(values):
                    num -= 1
        i += 1

    return list(values)
