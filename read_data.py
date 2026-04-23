from data import load_data

JSON_FILENAME = 'animals_data.json'

animal_data = load_data(JSON_FILENAME)

def basic_animal_info(animals, mode="txt"):
    """ Given a list of animals, generates a string with the
        name, diet, first location, and type fields.
    """
    for animal in animals:
        name = animal["name"]
        location = animal["locations"][0]
        characteristics = animal["characteristics"]
        diet = characteristics["diet"] if "diet" in characteristics else None
        type_ = characteristics["type"] if "type" in characteristics else None

        if mode="txt":
            output = ""
            output += f"Name: {name}\n"
            if diet:
                output += f"Diet: {diet}\n"
            output += f"Location: {location}\n"
            if type_:
                output += f"Type: {characteristics['type']}\n"
            return output

        elif mode="html":
            output = ""
            output += f"Name: {name}\n"
            if diet:
                output += f"Diet: {diet}\n"
            output += f"Location: {location}\n"
            if type_:
                output += f"Type: {characteristics['type']}\n"
            return output
        
        else:
            raise TypeError(f"Invalid argument \"{mode}\" for mode (txt | html).")




if __name__ == "__main__":
    print(basic_animal_info(animal_data))