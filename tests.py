from data import load_data
from animals_card_generator import get_animal_field_value


def print_divider():
    """ Prints a divider to separate each test. """
    print("-" * 42)


# Tests
print("Testing JSON loader.")
animal_data = load_data("animals_data.json")
assert len(animal_data) > 0
print_divider()

print("Testing animal field value extractor.")
field = "training"
animal1 = animal_data[0] # has training field
animal2 = animal_data[1] # doesn't have training field
val1 = get_animal_field_value(animal1, field)
val2 = get_animal_field_value(animal2, field)
assert len(val1)
assert val2 is None