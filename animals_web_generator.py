from data import load_data
from animal_info import generate_animal_card_list

JSON_FILENAME = "animals_data.json"


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
    animal_data = load_data(JSON_FILENAME)
    animals_str = generate_animal_card_list(animal_data, mode="html")
    generate_animals_page("animals_template.html", "animals.html", animals_str)