import os
import pathlib
from dotenv import load_dotenv, find_dotenv
import subprocess
import logging

DATA_DIR_PATH = pathlib.Path(__file__).parent
RECIPES_FILE_PATH = DATA_DIR_PATH / "recipes.csv"
INTERACTIONS_FILE_PATH = DATA_DIR_PATH / "interactions.csv"

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

recipes_data_id = os.getenv("RECIPES_DATA_ID")
interactions_data_id = os.getenv("INTERACTIONS_DATA_ID")

def gdown_data(recipes_data_id, interactions_data_id, recipes_file_path=RECIPES_FILE_PATH, interactions_file_path=INTERACTIONS_FILE_PATH):
    logging.info("Downloading recipes.csv")
    subprocess.run(["gdown", recipes_data_id, "-O", recipes_file_path])
    logging.info("Downloading interactions.csv")
    subprocess.run(["gdown", interactions_data_id, "-O", interactions_file_path])
    
if __name__ == "__main__":
    gdown_data(recipes_data_id=recipes_data_id, interactions_data_id=interactions_data_id)
