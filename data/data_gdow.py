import subprocess
import os

def is_chroma_exist(chroma_data_path):
    chroma_dir_exist = os.path.isdir(chroma_data_path)
    return chroma_dir_exist

def is_raw_data_exist(recipes_data_path, interactions_data_path):
    recipes_file_exist = os.path.isfile(recipes_data_path)
    interactions_file_exist = os.path.isfile(interactions_data_path)
    raw_data_files_exist = (recipes_file_exist and interactions_file_exist)
    return raw_data_files_exist

def gdown_raw_data(
    recipes_data_id, interactions_data_id, recipes_data_path, interactions_data_path
):
    raw_data_files_exist = is_raw_data_exist(recipes_data_path=recipes_data_path, interactions_data_path=interactions_data_path)
    
    if not raw_data_files_exist:
        subprocess.run(["gdown", recipes_data_id, "-O", recipes_data_path])
        subprocess.run(["gdown", interactions_data_id, "-O", interactions_data_path])
    
def gdow_chroma(chroma_data_path, chroma_data_id):
    chroma_dir_exist = is_chroma_exist(chroma_data_path=chroma_data_path)
    
    if not chroma_dir_exist:
        subprocess.run(["gdown", chroma_data_id, "-O", chroma_data_path, "--folder"])
