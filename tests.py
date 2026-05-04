from data import load_data, fetch_data, get_dataset_fields, get_all_fields, update_fields_cache
from animals_card_generator import get_animal_field_value
import secrets


def print_divider():
    """ Prints a divider to separate each test. """
    print("-" * 42)


# Tests
print("Testing JSON loader.")
animal_data = load_data("animals_data.json")
assert len(animal_data) > 0
print_divider()

# print("Testing animal field value extractor.")
# field = "training"
# animal1 = animal_data[0] # has training field
# animal2 = animal_data[1] # doesn't have training field
# val1 = get_animal_field_value(animal1, field)
# val2 = get_animal_field_value(animal2, field)
# assert len(val1)
# assert val2 is None
# print_divider()

print("Testing Animals API Call (Query=\"Fox\").")
animals_data = fetch_data(secrets.API_KEY, "Fox")
assert len(animals_data)
print_divider()

# print("Testing Animals API Error.")
# json = fetch_data(secrets.API_KEY, "Not A Real Animal Query")
# try:
#     assert len(json)
# except AssertionError:
#     print("Got", len(json), "results.")
# print_divider()

print("Testing field extraction.")
fields = get_dataset_fields(animals_data)
all_fields_old = get_all_fields()
update_fields_cache(fields)
all_fields = get_all_fields()
num_added = len(all_fields) - len(all_fields_old)
print(f"len(all_fields) data fields have been discovered through the Animals API. ({num_added} new added just now.)")