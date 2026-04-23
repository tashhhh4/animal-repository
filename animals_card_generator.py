from data import load_data

JSON_FILENAME = "animals_data.json"


def serialize_animal(animal, mode):
    """ Given an animal data object, generates an output string with the
        name, diet, first location, and type fields.
    """
    name = animal["name"]
    location = animal["locations"][0]
    characteristics = animal["characteristics"]
    diet = characteristics["diet"] if "diet" in characteristics else None
    type_ = characteristics["type"] if "type" in characteristics else None

    output = ''

    if mode == "txt":
        output += f"Name: {name}\n"
        if diet:
            output += f"Diet: {diet}\n"
        output += f"Location: {location}\n"
        if type_:
            output += f"Type: {characteristics['type']}\n"
        output += "\n"

    elif mode == "html":
        output += '<li class="cards__item">'
        output += f'<div class="card__title">{name}</div>'
        output += '<ul class="card__text">'
        if diet:
            output += f'<li><strong>Diet:</strong> {diet}</li>'
        output += f'<li><strong>Location:</strong> {location}</li>'
        if type_:
            output += f'<li><strong>Type:</strong> {type_}</li>'
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
    output = ''
    for animal in animals:
        output += serialize_animal(animal, mode)
    return output


if __name__ == "__main__":
    animal_data = load_data(JSON_FILENAME)
    print(generate_animal_card_list(animal_data))