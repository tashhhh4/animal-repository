from requests.exceptions import ConnectionError as RequestsConnectionError
from data_fetcher import (
    fetch_data, get_all_fields, MissingApiKeyError, InvalidApiKeyError
)
from config_editor import load_config


def passes_filter(animal, filter_):
    """ Determines if one animal object matches the rules of the filter. """
    match_case = filter_["match_case"]
    query = filter_["query"]
    actual_value = get_animal_field_value(animal, filter_["field"])
    if not match_case:
        query = query.lower()
        if actual_value is not None:
            actual_value = actual_value.lower()

    if filter_["type"] == "EQUALS":
        if filter_["query"] != actual_value:
            return False

    elif filter_["type"] == "CONTAINS":
        if actual_value is None:
            return False
        if filter_["query"] not in actual_value:
            return False

    else:
        raise ValueError(("Invalid filter type! (You can run config_editor.py "
                          "to remove filters or reset all settings to default.)"
        ))

    return True


def filter_animals(animals, filters):
    """ Removes items from animals which do not match the list of filters. """
    for filter_ in filters:
        animals = [a for a in animals if passes_filter(a, filter_)]
    return animals


def get_animal_field_value(animal, field):
    """ Returns the value from "field" which may be nested in
        either the "characteristics" or "taxonomy" dicts.
        Returns None if the animal does not have this field.
    """
    fields = get_all_fields()
    parent_field = fields[field]
    if field in animal[parent_field]:
        return animal[parent_field][field]

    return None


def serialize_animal(animal, fields=None, mode="txt"):
    """ Given an animal data object, generates an output string with the
        name, diet, first location, and type fields.
    """
    if fields is None:
        fields = ["diet", "type"]
    name = animal["name"]
    location = animal["locations"][0] if animal["locations"] else "Unknown"
    other_traits = [(field, get_animal_field_value(animal, field)) for field in fields]

    output = ''

    if mode == "txt":
        output += f"Name: {name}\n"
        output += f"Location: {location}\n"
        for field_name, value in other_traits:
            if value is not None:
                output += f"{field_name.capitalize()}: {value}\n"
        output += "\n"

    elif mode == "html":
        output += '<li class="cards__item">'
        output += f'<div class="card__title">{name}</div>'
        output += '<ul class="card__text">'
        output += f'<li><strong>Location:</strong> {location}</li>'
        for field_name, value in other_traits:
            if value is not None:
                output += f'<li><strong>{field_name.capitalize()}:</strong> {value}</li>'
        output += '</ul>'
        output += '</li>\n'

    else:
        raise TypeError(f"Invalid argument \"{mode}\" for output mode (txt | html).")

    return output


def generate_animal_card_list(animals, animal_query, mode="txt"):
    """ Generates a list of animal cards.
        `mode`
            "txt": Returns a string that can be printed to the console.
            "html": Returns a string of <li> elements for an HTML template.
    """
    print("Generating card list.")
    config = load_config()

    # Handle empty query result
    if len(animals) == 0:
        output = ''
        if mode == "html":
            output += '<p class="feedback">'
        output += f"There are no animals called \"{animal_query}\"."
        if mode == "html":
            output += '</p>'
        return output

    # Handle empty filter result
    animals = filter_animals(animals, config["filters"])
    if len(animals) == 0:
        output = ''
        if mode == "html":
            output += '<p class="feedback">'
        output += 'There are animals matching the current set of filters.'
        if mode == "html":
            output += '</p>'
        return output

    # Handle successful animal data output
    output = ''
    for animal in animals:
        output += serialize_animal(animal, fields=config["fields"], mode=mode)

    return output


def main():
    """ Runs animal card generator in console output mode based on settings in config.json. """
    config = load_config()

    try:
        animal_data = fetch_data(config["query"])
        print(generate_animal_card_list(animal_data, config["query"]))

    except MissingApiKeyError as e:
        print(e)

    except InvalidApiKeyError as e:
        print(e)

    except RequestsConnectionError as e:
        print("Failed to connect to the API service. Please check your internet connection.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
