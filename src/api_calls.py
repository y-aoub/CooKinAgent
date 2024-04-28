import requests
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


def set_user_prompt(
    user_prompt,
    city,
    country,
    humidity,
    cloudcover,
    temp_C,
    precipMM,
    weatherDesc,
    windspeedKmph,
    recipe=None,
):
    user_prompt_template = PromptTemplate.from_template(user_prompt)
    if recipe:
        user_prompt = user_prompt_template.format(
            recipe=recipe,
            city=city,
            country=country,
            humidity=humidity,
            cloudcover=cloudcover,
            temp_C=temp_C,
            precipMM=precipMM,
            weatherDesc=weatherDesc,
            windspeedKmph=windspeedKmph,
        )
    else:
        user_prompt = user_prompt_template.format(
            city=city,
            country=country,
            humidity=humidity,
            cloudcover=cloudcover,
            temp_C=temp_C,
            precipMM=precipMM,
            weatherDesc=weatherDesc,
            windspeedKmph=windspeedKmph,
        )
    return user_prompt


def set_openai_llm(openai_api_key, temperature=0.7):
    llm = OpenAI(
        openai_api_key=openai_api_key, temperature=temperature, max_tokens=1024
    )
    return llm


def set_openai_embeddings(retry_max_seconds):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large", retry_max_seconds=retry_max_seconds
    )
    return embeddings


def set_chain(llm):
    prompt = ChatPromptTemplate.from_messages(
        [("system", "{system_prompt}"), ("user", "{user_prompt}")]
    )
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain


def openai_api_call(chain, system_prompt, user_prompt):
    return chain.invoke({"system_prompt": system_prompt, "user_prompt": user_prompt})


def set_api_url(location):
    location = location.lower().replace(" ", "%20")
    url = f"https://wttr.in/{location}?format=j2"
    return url


def weather_api_call(url):
    response_dict = dict(requests.get(url).json())
    return response_dict


def filter_response(response_dict):
    current_condition = response_dict["current_condition"][0]
    nearest_area = response_dict["nearest_area"][0]

    city = nearest_area["areaName"][0]["value"]
    country = nearest_area["country"][0]["value"]

    humidity = current_condition["humidity"]
    cloudcover = current_condition["cloudcover"]
    temp_C = current_condition["temp_C"]
    precipMM = current_condition["precipMM"]
    weatherDesc = current_condition["weatherDesc"][0]["value"]
    windspeedKmph = current_condition["windspeedKmph"]

    return (
        city,
        country,
        humidity,
        cloudcover,
        temp_C,
        precipMM,
        weatherDesc,
        windspeedKmph,
    )
