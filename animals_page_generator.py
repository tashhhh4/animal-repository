import sys
import pathlib
import secrets
import settings
from data import load_data, fetch_data
from animals_card_generator import generate_animal_card_list
from config_editor import load_config


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


if __name__ == "__main__":
    try:
        config = load_config()
        animal_data = fetch_data(secrets.API_KEY, config["query"])
        if not len(animal_data):
            raise ValueError("No data found.")
    except ValueError as e:
        print(e)
        sys.exit()
    animals_str = generate_animal_card_list(animal_data, mode="html")
    generate_animals_page(settings.TEMPLATE_FILENAME, settings.OUTPUT_FILENAME, animals_str)
    path = pathlib.Path(settings.OUTPUT_FILENAME).resolve()
    print(f"Saved view to: {path.as_uri()}")