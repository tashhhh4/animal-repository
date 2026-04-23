from data import load_data

JSON_FILENAME = "animals_data.json"


def basic_animal_info(animals, mode="txt"):
    """ Given a list of animals, generates a string with the
        name, diet, first location, and type fields.
    """
    output = ""

    for animal in animals:
        name = animal["name"]
        location = animal["locations"][0]
        characteristics = animal["characteristics"]
        diet = characteristics["diet"] if "diet" in characteristics else None
        type_ = characteristics["type"] if "type" in characteristics else None

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
            output += f"Name: {name}<br/>"
            if diet:
                output += f"Diet: {diet}<br/>"
            output += f"Location: {location}<br/>"
            if type_:
                output += f"Type: {characteristics['type']}<br/>"
            output += '</li>\n'
        
        else:
            raise TypeError(f"Invalid argument \"{mode}\" for mode (txt | html).")

    return output


if __name__ == "__main__":
    animal_data = load_data(JSON_FILENAME)
    print(basic_animal_info(animal_data))