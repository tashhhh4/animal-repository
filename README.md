# Animal Repository
A webpage which tracks and displays information about various mammalian species.

|               |                                    |
|---------------|------------------------------------|
| Author        | Natasha Libera                     |
| Course        | MSIT Software Entwicklung Jan 2026 |
| Codio Project | Zootopia                           |


## Demo Page
The generated pages follow this design:
![Top of Animal Repository Webpage](screenshot.png)

## Available Scripts
### Animal Facts Generator
Prints out the animal data to the console

    python animals_card_generator.py

### Animal Webpage Generator
Generates an HTML page that can be run in the
browser to see a formatted list of fact cards.

    python animals_page_generator.py

Output: `animals.html`

### Config Editor
A tool which allows the user to choose the fields displayed and set filters for data used in output generation.
Supported settings:
* add or remove data fields
* add or remove query filters
* change the animal search query


    python config_editor.py

Output: `config.json`


## Configuring venv
If you run the scripts on your computer with Python, you will need to activate a virtual environment to run it.

1. Download or git clone the code to a folder on your computer.
2. Open a terminal in the same folder and run `python -m venv .venv` (the command may be slightly different depending on your OS and your python installation)
3. Run `./.venv/Scripts/activate`
4. Run pip install:


    pip install -r requirements.txt

After these steps, you should be able to run the 3 main scripts.