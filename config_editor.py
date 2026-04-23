import json
from data import load_data, get_all_fields

DATA_FILENAME = "animals_data.json"
CONFIG_FILENAME = "config.json"
ANIMAL_DATA = load_data(DATA_FILENAME)
FIELDS = get_all_fields(ANIMAL_DATA)

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

    user_args = user_input.split(" ")
    user_args_cleaned = split_user_args(user_args, onlyin=FIELDS)
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


def show_config():
    """ Prints out all of the current settings. """
    config = load_config()
    print("Field Selection:")
    print_comma_list(config["fields"])
    print()
    print("Active Filters:")
    print(config["filters"])


available_commands = {
    "add_fields": add_fields,
    "remove_fields": remove_fields,
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
