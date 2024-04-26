import os
from dotenv import find_dotenv, load_dotenv
from src.api_calls import (
    set_api_url,
    set_openai_embeddings,
    set_openai_llm,
    set_chain,
    weather_api_call,
    openai_api_call,
    filter_response,
    set_user_prompt,
)
from src.embeddings import split_text, build_chroma_data, similarity_search
from data.data_utils import get_data_paths, read_txt_file, get_api_key, get_data_ids
from data.data_gdow import gdown_raw_data, gdow_chroma
from data.data_processing import process_data

DOTENV_PATH = find_dotenv()
load_dotenv(DOTENV_PATH)

def build_vectorsctore(build_chroma):
    embeddings = set_openai_embeddings(retry_max_seconds=40)
    RECIPES_DATA_ID, INTERACTIONS_DATA_ID, CHROMA_DATA_ID = get_data_ids(recipes_data_id_key="RECIPES_DATA_ID",
                                                         intercations_data_id_key="INTERACTIONS_DATA_ID" ,
                                                         chroma_data_id_key="CHROMA_DATA_ID")
    RECIPES_DATA_ID, INTERACTIONS_DATA_ID, CHROMA_DATA_ID = get_data_ids(recipes_data_id_key="RECIPES_DATA_ID",
                                                         intercations_data_id_key="INTERACTIONS_DATA_ID" ,
                                                         chroma_data_id_key="CHROMA_DATA_ID")
     
    RECIPES_DATA_PATH, INTERACTIONS_DATA_PATH = get_data_paths(sub_dir="raw_data")
    PROCESSED_DATA_PATH, CHROMA_DATA_PATH = get_data_paths(sub_dir="processed_data")
    
    if build_chroma:
        gdown_raw_data(recipes_data_id=RECIPES_DATA_ID,
                        interactions_data_id=INTERACTIONS_DATA_ID,
                        recipes_data_path=RECIPES_DATA_PATH,
                        interactions_data_path=INTERACTIONS_DATA_PATH)
        processed_data = process_data(processed_data_path=PROCESSED_DATA_PATH)
        splitted_text = split_text(text=processed_data)
        build_chroma_data(
            splitted_text, chroma_data_path=CHROMA_DATA_PATH, embeddings=embeddings
            )
    else:
        gdow_chroma(chroma_data_id=CHROMA_DATA_ID, chroma_data_path=CHROMA_DATA_PATH)

def main(city):

    OPENAI_API_KEY = get_api_key(openai_api_key="OPENAI_API_KEY")
    (
        SUGGESTING_SYSTEM_PROMPT_PATH,
        SUGGESTING_USER_PROMPT_PATH,
        FORMATTING_SYSTEM_PROMPT_PATH,
        FORMATTING_USER_PROMPT_PATH,
    ) = get_data_paths(sub_dir="input_data")
   
    _, CHROMA_DATA_PATH = get_data_paths(sub_dir="processed_data") 
    
    url = set_api_url(city)

    weather_response = weather_api_call(url=url)
    filtered_weather_response = filter_response(response_dict=weather_response)

    suggesting_user_prompt = read_txt_file(data_text_path=SUGGESTING_USER_PROMPT_PATH)
    suggesting_system_prompt = read_txt_file(data_text_path=SUGGESTING_SYSTEM_PROMPT_PATH)
    formatting_user_prompt = read_txt_file(data_text_path=FORMATTING_USER_PROMPT_PATH)
    formatting_system_prompt = read_txt_file(data_text_path=FORMATTING_SYSTEM_PROMPT_PATH)

    suggesting_user_prompt = set_user_prompt(*(suggesting_user_prompt, *filtered_weather_response))
    
    llm = set_openai_llm(openai_api_key=OPENAI_API_KEY, temperature=0.3)
    chain = set_chain(llm=llm)
    embeddings = set_openai_embeddings(retry_max_seconds=40)
    
    openai_response = openai_api_call(
        chain=chain,
        system_prompt=suggesting_system_prompt,
        user_prompt=suggesting_user_prompt,
    )

    unformatted_agent_response = similarity_search(
        chroma_data_path=CHROMA_DATA_PATH,
        openai_response=openai_response,
        embeddings=embeddings,
    )
    formatting_user_prompt = set_user_prompt(
        *(formatting_user_prompt, *filtered_weather_response, unformatted_agent_response)
    )
    formatted_agent_response = openai_api_call(
        chain=chain,
        system_prompt=formatting_system_prompt,
        user_prompt=formatting_user_prompt,
    )

    return formatted_agent_response
