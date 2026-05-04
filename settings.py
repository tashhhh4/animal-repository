import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
JSON_FILENAME = "animals_data.json"
OUTPUT_FILENAME = "animals.html"
TEMPLATE_FILENAME = "animals_template.html"