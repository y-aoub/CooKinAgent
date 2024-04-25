import pandas as pd
import humanize
from data.data_utils import read_csv_data, get_data_paths, save_txt_file


def merge_data(data_left: pd.DataFrame, data_right: pd.DataFrame) -> pd.DataFrame:
    merged_data = pd.merge(
        data_left, data_right, left_on="id", right_on="recipe_id", how="left"
    )
    merged_data.drop(columns=["recipe_id"], inplace=True)
    merged_data["review"] = "-" + merged_data["review"].astype(str)
    aggregation_functions = {
        col: "first" for col in data_left.columns if col not in ["id"]
    }
    aggregation_functions.update({"rating": "mean", "review": lambda x: "\n".join(x)})
    merged_data = merged_data.groupby("id").agg(aggregation_functions).reset_index()
    return merged_data


def drop_na(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(subset=["name"])
    return data


def filter_cols(data: pd.DataFrame) -> pd.DataFrame:
    selected_cols = [
        "name",
        "minutes",
        "nutrition",
        "steps",
        "description",
        "ingredients",
        "rating",
        "review",
    ]
    data = data[selected_cols]
    return data


def format_nutrition(nutrition_record: str):
    labels = [
        "calories",
        "total fat",
        "sugar",
        "sodium",
        "protein",
        "saturated fat",
        "carbohydrates",
    ]
    nutrition_list = eval(nutrition_record)
    formatted_nutrition_record = "\n".join(
        f"{label}: {value} {'PDV' if label != 'calories' else 'CAL'}"
        for label, value in zip(labels, nutrition_list)
    )
    return formatted_nutrition_record


def format_nutrition_col(data: pd.DataFrame, func=format_nutrition) -> pd.DataFrame:
    data.loc[:, "nutrition"] = data["nutrition"].apply(func)
    return data


def format_steps(steps_record):
    steps_list = eval(steps_record)
    formatted_steps_record = ", ".join(steps_list)
    return formatted_steps_record


def format_steps_col(data: pd.DataFrame, func=format_steps) -> pd.DataFrame:
    data.loc[:, "steps"] = data["steps"].apply(func)
    return data


def format_ingredients(ingredients_record):
    ingredients_list = eval(ingredients_record)
    formatted_ingredients_record = ", ".join(ingredients_list)
    return formatted_ingredients_record


def format_ingredients_col(data: pd.DataFrame, func=format_ingredients) -> pd.DataFrame:
    data.loc[:, "ingredients"] = data["ingredients"].apply(func)
    return data


def format_minutes(minutes_record):
    time_value = int(minutes_record)
    human_time_value = (
        humanize.precisedelta(time_value * 60, minimum_unit="minutes")
        if time_value <= 60 * 24 * 7
        else "time to be estimated"
    )
    return human_time_value


def format_minutes_col(data: pd.DataFrame, func=format_minutes) -> pd.DataFrame:
    data.loc[:, "time"] = data["minutes"].apply(func)
    data.drop(columns=["minutes"], inplace=True)
    return data


def format_into_text(row) -> str:
    text = f"""Recipe Name:\n{row["name"]}\n\nIngredients:\n{row["ingredients"]}\n\nPreparation Steps:\n{row["steps"]}\n\nPreparation Time:\n{row["time"]}\n\nNutrition Values:\n{row["nutrition"]}\n\nDescription of the Recipe:\n{row["description"]}\n\nRecipe Reviews:\n{row["review"]}\n\nRecipe Rating:\n{row["rating"]}/5.0"""
    return text


def format_into_text_data(data: pd.DataFrame, func=format_into_text):
    data["data_text"] = data.apply(func, axis=1)
    return data


def format_data(data):
    formatted_data = (
        data.pipe(format_nutrition_col)
        .pipe(format_steps_col)
        .pipe(format_ingredients_col)
        .pipe(format_minutes_col)
        .pipe(format_into_text_data)
    )
    return formatted_data


def get_processed_data_text(data, data_text_path=None):
    data_text_list = list(data["data_text"])
    processed_data_text = "\n$$$\n".join(data_text_list)
    if data_text_path:
        save_txt_file(data_text=processed_data_text, data_text_path=data_text_path)
    return processed_data_text

    
def process_data(processed_data_path):
    RECIPES_DATA_PATH, INTERACTIONS_DATA_PATH = get_data_paths(sub_dir="raw_data")

    recipes_data = read_csv_data(data_path=RECIPES_DATA_PATH)
    interactions_data = read_csv_data(data_path=INTERACTIONS_DATA_PATH)

    merged_data = merge_data(data_left=recipes_data, data_right=interactions_data)

    merged_data = drop_na(merged_data)

    filtered_data = filter_cols(merged_data)

    formatted_data = format_data(filtered_data)

    processed_data_text = get_processed_data_text(formatted_data, data_text_path=processed_data_path)
    
    return processed_data_text