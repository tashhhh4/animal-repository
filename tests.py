from data import load_data

def print_divider():
    """ Prints a divider to separate each test. """
    print("-" * 42)


# Tests
print("Testing JSON loader.")
animal_data = load_data("animals_data.json")
animal_data = []
assert len(animal_data) > 0