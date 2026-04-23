from data import load_data

JSON_FILENAME = 'animals_data.json'

animal_data = load_data(JSON_FILENAME)

def print_basic_animal_info(animals):
    """ Given a list of animals, prints the name, diet,
        first location, and type fields.
    """
    for animal in animals:
        characteristics = animal['characteristics']
        locations = animal['locations']

        print(f"Name: {animal['name']}")

        if "diet" in characteristics:
            print(f"Diet: {characteristics['diet']}")

        print(f"Location: {locations[0]}")

        if "type" in characteristics:
            print(f"Type: {characteristics['type']}")
            
        print()


if __name__ == "__main__":
    print_basic_animal_info(animal_data)