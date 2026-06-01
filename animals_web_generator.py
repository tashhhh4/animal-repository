import sys
import pathlib
from requests.exceptions import ConnectionError
import settings
from data_fetcher import (
    load_data, fetch_data, MissingApiKeyError, InvalidApiKeyError
)
from animals_card_generator import generate_animal_card_list
from config_editor import load_config


def get_animal_query():
    """ Prompts the user for the name of an animal. """
    while True:
        user_input = input("Please enter the name of an animal: ")
        if not user_input:
            print("Empty input. Please try again: ")
            continue
        return user_input


def generate_animals_page(template_file, output_file, animals_str):
    """ Replaces the placeholder string in `template_file` with `animals_str`,
        and saves the result to a new `output_file`.
    """
    PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"

    if template_file == output_file:
        raise FileError("Danger! Template and output filename are the same! Aborting.")

    with open(template_file, "r") as file:
        template_str = file.read()

    output_str = template_str.replace(PLACEHOLDER, animals_str)

    with open(output_file, "w") as file:
        file.write(output_str)


def main():
    """ Prompts user for animal name input,
    runs a fetch for the animal data,
    and generates a browser-viewable webpage at `animals.html`.
    """
    animal_name = get_animal_query()
    config = load_config()

    try:
        animal_data = fetch_data(animal_name)
    
    except MissingApiKeyError as e:
        print(e)
        return

    except InvalidApiKeyError as e:
        print(e)
        return

    except ConnectionError as e:
        print("Failed to connect to the API service. Please check your internet connection.")
        return

    except Exception as e:
        print(e)
        return

    animals_str = generate_animal_card_list(animal_data, animal_name, mode="html")
    generate_animals_page(settings.TEMPLATE_FILENAME, settings.OUTPUT_FILENAME, animals_str)
    path = pathlib.Path(settings.OUTPUT_FILENAME).resolve()
    print(f"Saved view to: {path.as_uri()}")


if __name__ == "__main__":
    main()