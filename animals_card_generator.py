from data import load_data, get_all_fields
from config_editor import load_config

JSON_FILENAME = "animals_data.json"
CONFIG_FILENAME = "config.json"
ANIMAL_DATA = load_data(JSON_FILENAME)
FIELDS = get_all_fields(ANIMAL_DATA)


def passes_filter(animal, filter):
    """ Determines if one animal object matches the rules of the filter. """
    filter_type = filter["type"]
    query = filter["query"]
    actual_value = get_animal_field_value(animal, filter["subfield"])

    if filter["type"] == "EQUALS":
        if filter["query"] != actual_value:
            return False

    elif filter["type"] == "CONTAINS":
        if filter["query"] not in actual_value:
            return False

    else:
        raise ValueError("Invalid filter type! (You can run config_editor.py to remove filters or reset all settings to default.)")

    return True


def filter_animals(animals, filters):
    """ Removes items from animals which do not match the list of filters. """
    for filter in filters:
        animals = [a for a in animals if passes_filter(a, filter)]
    return animals


def get_animal_field_value(animal, field):
    """ Returns the value from "field" which may be nested in
        either the "characteristics" or "taxonomy" dicts.
        Returns None if the animal does not have this field.
    """
    parent_field = FIELDS[field]
    if field in animal[parent_field]:
        return animal[parent_field][field]
    else:
        return None


def serialize_animal(animal, fields=["diet", "type"], mode="txt"):
    """ Given an animal data object, generates an output string with the
        name, diet, first location, and type fields.
    """
    name = animal["name"]
    location = animal["locations"][0]
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
        # if diet:
        #     output += f'<li><strong>Diet:</strong> {diet}</li>'
        # if type_:
        #     output += f'<li><strong>Type:</strong> {type_}</li>'
        for field_name, value in other_traits:
            if value is not None:
                output += f'<li><strong>{field_name.capitalize()}:</strong> {value}</li>'
        output += '</ul>'
        output += '</li>\n'
    
    else:
        raise TypeError(f"Invalid argument \"{mode}\" for output mode (txt | html).")
    
    return output


def generate_animal_card_list(animals, mode="txt"):
    """ Generates a list of animal cards.
        `mode`
            "txt": Returns a string that can be printed to the console.
            "html": Returns a string of <li> elements for an HTML template.
    """
    config = load_config()
    animals = filter_animals(animals, config["filters"])
    output = ''
    for animal in animals:
        output += serialize_animal(animal, fields=config["fields"], mode=mode)
    return output


if __name__ == "__main__":
    animal_data = load_data(JSON_FILENAME)
    print(generate_animal_card_list(animal_data))