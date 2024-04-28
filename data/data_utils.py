import os
import pathlib
import pandas as pd

DATA_DIR_PATH = pathlib.Path(__file__).parent


def get_data_paths(sub_dir, data_dir_path=DATA_DIR_PATH):

    sub_dir_path = data_dir_path / sub_dir

    if sub_dir == "raw_data":
        recipes_data_path = sub_dir_path / "recipes.csv"
        interactions_data_path = sub_dir_path / "interactions.csv"
        return str(recipes_data_path), str(interactions_data_path)

    if sub_dir == "input_data":
        suggesting_system_prompt_path = sub_dir_path / "suggesting_system_prompt.txt"
        suggesting_user_prompt_path = sub_dir_path / "suggesting_user_prompt.txt"
        formatting_system_prompt_path = sub_dir_path / "formatting_system_prompt.txt"
        formatting_user_prompt_path = sub_dir_path / "formatting_user_prompt.txt"
        return (
            str(suggesting_system_prompt_path),
            str(suggesting_user_prompt_path),
            str(formatting_system_prompt_path),
            str(formatting_user_prompt_path),
        )

    if sub_dir == "processed_data":
        processed_data_path = sub_dir_path / "processed_data.txt"
        chroma_data_path = sub_dir_path / "chroma_data"
        return str(processed_data_path), str(chroma_data_path)


def read_csv_data(data_path: pathlib.PosixPath) -> pd.DataFrame:
    data = pd.read_csv(data_path, sep=",", encoding="utf-8")
    return data


def save_txt_file(data_text, data_text_path):
    with open(data_text_path, "w") as f:
        f.write(data_text)


def read_txt_file(data_text_path: str):
    f = open(data_text_path, "r")
    content = f.read()
    return content


def get_data_ids(
    recipes_data_id_key, intercations_data_id_key, chroma_data_id_key=None
):
    recipes_data_id = os.getenv(recipes_data_id_key)
    intercations_data_id = os.getenv(intercations_data_id_key)
    chroma_data_id = os.getenv(chroma_data_id_key)
    return recipes_data_id, intercations_data_id, chroma_data_id


def get_api_key(openai_api_key):
    openai_api_key = os.getenv(openai_api_key)
    return openai_api_key
