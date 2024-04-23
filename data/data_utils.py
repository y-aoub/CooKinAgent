import pandas as pd
import pathlib
import humanize
import spacy

from langchain_community.document_loaders.csv_loader import CSVLoader

DATA_DIR_PATH = pathlib.Path(__file__).parent
RECIPES_FILE_PATH = DATA_DIR_PATH / "recipes.csv"
INTERACTIONS_FILE_PATH = DATA_DIR_PATH / "interactions.csv"
NLP = spacy.load("en_core_web_sm")

def read_data(data_file_path: pathlib.PosixPath) -> pd.DataFrame:
    data = pd.read_csv(data_file_path, sep=",", encoding="utf-8")
    return data

def merge_data(data_left: pd.DataFrame, data_right: pd.DataFrame) -> pd.DataFrame:
    merged_data = pd.merge(data_left, data_right, left_on='id', right_on='recipe_id', how='left')
    merged_data.drop(columns=['recipe_id'], inplace=True)
    merged_data['review'] = merged_data['review'].astype(str)
    aggregation_functions = {col: 'first' for col in data_left.columns if col not in ['id']}
    aggregation_functions.update({
        'rating': 'mean',
        'review': lambda x: '\n\n'.join(x)
    })
    merged_data = merged_data.groupby('id').agg(aggregation_functions).reset_index()
    return merged_data

def drop_na(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(subset=['name'])
    return data

def filter_cols(data: pd.DataFrame) -> pd.DataFrame:
    selected_cols = ['name', 'minutes', 'nutrition', 'steps', 'description', 'ingredients', 'rating', 'review', 'tags']
    data = data[selected_cols]
    return data

def format_nutrition(nutrition_record):
    labels = ["calories", "total fat", "sugar", "sodium", "protein", "saturated fat", "carbohydrates"]
    nutrition_list = eval(nutrition_record)
    formatted_nutrition_record = '\n'.join(f"{label}: {value} {'PDV' if label != 'calories' else 'CAL'}" for label, value in zip(labels, nutrition_list))
    return formatted_nutrition_record

def format_nutrition_col(data: pd.DataFrame, func=format_nutrition) -> pd.DataFrame:
    data.loc[:, 'nutrition'] = data['nutrition'].apply(func)
    return data

def format_steps(steps_record):
    steps_list = eval(steps_record)
    formatted_steps_record = ', '.join(steps_list)
    return formatted_steps_record

def format_steps_col(data: pd.DataFrame, func=format_steps) -> pd.DataFrame:
    data.loc[:, 'steps'] = data['steps'].apply(func)
    return data

def format_ingredients(ingredients_record):
    ingredients_list = eval(ingredients_record)
    formatted_ingredients_record = ', '.join(ingredients_list)
    return formatted_ingredients_record

def format_ingredients_col(data: pd.DataFrame, func=format_ingredients) -> pd.DataFrame:
    data.loc[:, 'ingredients'] = data['ingredients'].apply(func)
    return data

def format_minutes(minutes_record):
    time_value = int(minutes_record)
    human_time_value = humanize.precisedelta(time_value * 60, minimum_unit='minutes') if time_value <= 60 * 24 * 7 else "time to be estimated"
    return human_time_value

def format_minutes_col(data: pd.DataFrame, func=format_minutes) -> pd.DataFrame:
    data.loc[:, 'time'] = data['minutes'].apply(func)
    data.drop(columns=['minutes'], inplace=True)
    return data

def format_tags(tags_record, nlp=NLP):
    tags_list = eval(tags_record)
    filtered_tags_list = [item for item in tags_list if any(token.ent_type_ in ["GPE", "NORP"] for token in nlp(item))]
    formatted_tags = ", ".join(filtered_tags_list) if filtered_tags_list else "not relative to a region"
    print(formatted_tags)
    return formatted_tags

def format_tags_col(data: pd.DataFrame, func=format_tags) -> pd.DataFrame:
    data.loc[:, 'region'] = data['tags'].apply(func)
    data.drop(columns=['tags'], inplace=True)
    return data

    
if __name__ == "__main__":
    recipes_data = read_data(data_file_path=RECIPES_FILE_PATH)
    interactions_data = read_data(data_file_path=INTERACTIONS_FILE_PATH)
    
    merged_data = merge_data(recipes_data, interactions_data)
    
    merged_data = drop_na(merged_data)
    
    filtered_data = filter_cols(merged_data)
    
    formated_data = format_nutrition_col(filtered_data)
    formated_data = format_steps_col(formated_data)
    formated_data = format_ingredients_col(formated_data)
    formated_data = format_minutes_col(formated_data)
    formated_data = format_tags_col(formated_data)
    
    # raw_data = data    
    
    N = 10000
    
    for col in formated_data.columns:
        print(f"\n-------------------------{col.upper()}-------------------------\n")
        print(formated_data[col][N])
        
    
    
    
    