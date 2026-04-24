import json
from data import load_data, get_all_fields, get_values_sample

DATA_FILENAME = "animals_data.json"
CONFIG_FILENAME = "config.json"
ANIMAL_DATA = load_data(DATA_FILENAME)
FIELDS = get_all_fields(ANIMAL_DATA)
FILTER_TYPES = {
    "EQUALS": "Matches only if the field value is EXACTLY the same as the filter.",
    "CONTAINS": "Matches if the filter text is found anywhere in the field.",
}


# IO

def load_config():
    """ Loads the config. """
    with open(CONFIG_FILENAME, "r") as file:
        config = json.load(file)
    return config


def save_config(config):
    """ Saves the config. """
    with open(CONFIG_FILENAME, "w") as file:
        new_config = json.dumps(config)
        file.write(new_config)


# Print Helpers

def show_title():
    """ Prints a title for the script """
    print("Config Editor for Animal Repository HTML Generator")
    print("--------------------------------------------------")


def print_comma_list(list_):
    """ Prints a list inline, comma separated. """
    items = ", ".join(list_)
    print(items)


def print_vertical_list(list_, tab=4):
    """ Prints a list vertically, one item on each line. """
    for item in list_:
        print(f"{' ' * tab}{item}")


def print_filter_list(flist):
    """ Prints a list of filters showing all current settings. """
    for i, filter in enumerate(flist):
        print(f"{i + 1}: {filter['field']} {filter['type']} {filter['query']}")


# Misc Helper

def split_user_args(user_args, onlyin):
    """ Splits a user space-separated string into a list,
        removing empty strings and items not present in the
        `onlyin` reference list.
    """
    return [a for a in user_args.split(" ") if a in onlyin]


# Commands

def add_fields():
    """ Allows user to choose any number of fields available in the dataset. """
    print("Available fields:")
    print_comma_list(list(FIELDS))
    user_input = input("Input desired fields, separated by spaces: ")
    user_args_cleaned = split_user_args(user_input, onlyin=FIELDS)
    config = load_config()
    for field in user_args_cleaned:
        if field not in config["fields"]:                
            config["fields"].append(field)
    save_config(config)
    print("Saved config.")


def remove_fields():
    """ Allows user to remove any number of fields from display. """
    config = load_config()
    print("Active fields:")
    print_comma_list(config["fields"])
    user_input = input("Remove desired fields, separated by spaces: ")
    user_args_cleaned = split_user_args(user_input, onlyin=config["fields"])
    for field in user_args_cleaned:
        if field in config["fields"]:
            config["fields"].remove(field)
    save_config(config)
    print("Saved config.")


def add_filter():
    """ Allows user to add a filter on the dataset. """
    print()
    print("Fields available for filtering:")
    print_comma_list(list(FIELDS))
    print()
    user_input = input("Enter field to filter by: ")
    print()
    user_args_cleaned = split_user_args(user_input, onlyin=FIELDS)
    if len(user_args_cleaned) == 0:
        print("Field not found.")
        return
    if len(user_args_cleaned) > 1:
        print("Only one field can be filtered at a time.")
        return
    filter_field = user_args_cleaned[0]
    print(f"Composing filter on {filter_field}. Some examples of values found here are:")
    sample_values = get_values_sample(ANIMAL_DATA, FIELDS[filter_field], filter_field, num=6)
    print_vertical_list(sample_values, tab=8)
    print()
    print("Available filters are:")
    filter_type_descriptions = (
        [f"{filter}: {description}" for filter, description in FILTER_TYPES.items()])
    print_vertical_list(filter_type_descriptions, tab=8)
    print()
    user_input = input("Choose filter type: ")
    user_input_cleaned = split_user_args(user_input, onlyin=FILTER_TYPES)
    if len(user_input_cleaned) != 1:
        print("Invalid filter type.")
        return
    filter_type = user_input_cleaned[0]
    filter_text = input("Enter filter text: ")

    config = load_config()
    config["filters"].append({
        "field": filter_field,
        "type": filter_type,
        "query": filter_text
    })
    save_config(config)
    print("Filter added.")


def remove_filter():
    """ Allows the user to remove a filter by list index. """
    config = load_config()
    filters = config["filters"]
    if len(filters) == 0:
        print("There are no active filters.")
        return
    print("Current filters:")
    print_filter_list(filters)
    try:
        user_number = int(input("Filter to remove (number): "))
        target_index = user_number - 1
        if target_index < 0:
            raise ValueError
        filters.pop(target_index)
    except (ValueError, IndexError):
        print("Number input failed.")
        return
    config["filters"] = filters
    save_config(config)
    print("Filter removed.")


def show_config():
    """ Prints out all of the current settings. """
    config = load_config()
    print("Field Selection:")
    print_comma_list(config["fields"])
    print()
    print("Active Filters:")
    print_filter_list(config["filters"])


available_commands = {
    "add_fields": add_fields,
    "remove_fields": remove_fields,
    "add_filter": add_filter,
    "remove_filter": remove_filter,
    "show_config": show_config,
}


def run_user_command(command):
    """ Runs a command from available commands. """
    if command not in available_commands:
        print("Unknown command", command)
    else:
        func = available_commands[command]
        if not func:
            print(command, "is not yet implemented.")
        else:
            func()


# Console Interaction

def get_user_command(prompt):
    """ Gets a user command, skipping blank line Enters. """
    while True:
        user_command = input(prompt)
        if not user_command:
            continue
        return user_command


def show_menu():
    """ Prints executable commands from `available_commands`. """
    print("Available commands (Ctrl+C to exit):")
    for command in available_commands:
        print(command)


def run_set_config():
    """ Repeatedly gets and executes user commands. """
    while True:
        show_title()
        show_menu()
        while True:
            command = get_user_command("Run: ")
            run_user_command(command)
            print()
            show_menu()


if __name__ == "__main__":
    try:
        run_set_config()
    except KeyboardInterrupt:
        pass
