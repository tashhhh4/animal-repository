from datetime import date
import json
import requests
import settings

QUERY_CACHEFILE = "query.txt"
FIELDS_CACHEFILE = "fields.json"
STALE_QUERY_AGE = 30 # days

class MissingApiKeyError(Exception):
    """ Raised if the API Key is missing. """
    def __init__(self):
        super().__init__(("Error: Missing API Key. Please make sure that the `.env` "
                         "file exists and contains an active `API_KEY`."))

class InvalidApiKeyError(Exception):
    """ Raised if the API Key exists but is rejected. """
    def __init__(self):
        super().__init__(("Error: Invalid API Key. Double check your API Key from "
                         "API Ninja, copy and paste the exact value as"
                         " API_KEY=<your_key_value> into your `.env` file."))


def clean_data(data_str):
    """ Replaces some problematic characters with appropriate substitutes. """
    data_str = data_str.replace("â€™", "'")  # apostrophe character
    data_str = data_str.replace("â€“", "–")  # dash character
    return data_str


def get_query_cache():
    """ Returns an animal name query from the query cache file, and the number of days since retrieval.
        If the file is missing or corrupted, returns None, None.
    """
    try:
        with open(QUERY_CACHEFILE, 'r', encoding="utf-8") as file:
            data = file.read().splitlines()

        if len(data) != 2:
            return None, None

        query = data[0]
        saved_date = date.fromisoformat(data[1])
        today = date.today()
        days_since = (today - saved_date).days
        return query, days_since

    except FileNotFoundError:
        return None, None

def set_query_cache(query):
    """ Sets the animal name query in the query cache file, and the date. """
    today = date.today()
    date_str = today.isoformat()

    with open(QUERY_CACHEFILE, 'w', encoding="utf-8") as file:
        file.write(query)
        file.write('\n')
        file.write(date_str)


def load_data(file_path):
    """ Loads a JSON file. """
    with open(file_path, "r", encoding="utf-8") as file:
        data_str = file.read()
        cleaned_str = clean_data(data_str)
        return json.loads(cleaned_str)


def validate_data(data):
    """ Checks for errors in the data and raises an appropriate error. """

    if "error" in data:
        if data["error"] == "Missing API Key.":
            raise MissingApiKeyError

        if data["error"] == "Invalid API Key.":
            raise InvalidApiKeyError

        raise Exception("An error occurred:", data["error"])


def save_data(file_path, data):
    """ Overwrites the local JSON datafile with the latest API call. """
    json_data = json.dumps(data)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json_data)


def fetch_data(animal_query):
    """ Fetches JSON data from the Animals API """
    # Check if the query needs to be repeated
    cached_query, days_since = get_query_cache()

    if cached_query is not None and days_since is not None:
        if cached_query == animal_query and days_since < STALE_QUERY_AGE:
            print(f'loading query about {animal_query} from cache')
            data = load_data(settings.JSON_FILENAME)
            validate_data(data)

            return data

    print(f'fetching fresh data about {animal_query}')
    headers = {"X-Api-Key": settings.API_KEY}
    response = requests.get(
        f'https://api.api-ninjas.com/v1/animals?name={animal_query}',
        headers=headers
    )
    data = response.json()
    validate_data(data)
    save_data(settings.JSON_FILENAME, data)

    # Update fields collection
    fields = get_dataset_fields(data)
    update_fields_cache(fields)

    # Remember making this query
    set_query_cache(animal_query)

    return data


def get_dataset_fields(data):
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


def update_fields_cache(new_fields):
    """ Updates the fields cache with new fields if necessary. """
    with open(FIELDS_CACHEFILE, 'r', encoding="utf-8") as file:
        fields = json.loads(file.read())
    for field in new_fields:
        if field not in fields:
            fields[field] = new_fields[field]
    with open(FIELDS_CACHEFILE, 'w', encoding="utf-8") as file:
        file.write(json.dumps(fields))


def get_all_fields():
    """ Gets all discovered fields from the fields cache file, and returns them as a list."""
    with open(FIELDS_CACHEFILE, 'r', encoding="utf-8") as file:
        data = json.loads(file.read())
    return data


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
