## Overview
CooKinAgent is a project that retrieves recipes adapted to the current weather in a specified city.

## Data
The raw data used here comes from the following links:

- Recipes data is available in CSV format and can be found [here](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data?select=RAW_recipes.csv).
- Interactions data is also available in CSV format and can be found [here](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data?select=RAW_interactions.csv).

## Setup

### Creating a Virtual Environment
Create a virtual environment to isolate package dependencies. Use one of the following methods:

- Using Python's built-in venv module:
  ```
  python -m venv [environment_path]
  ```
  
- Using the virtualenv package:
  ```
  virtualenv [environment_path]
  ```

### Activating the Environment
Activate the virtual environment by running:
```
source [environment_path]/bin/activate
```

### Installing Dependencies
Install the required Python packages using:
```
pip install -r requirements.txt
```

### Specifying OpenAI API Key
Ensure that a valid OpenAI API Key is specified in your existing .env file located at the root of your project directory. The key should be stored in this format:
```
OPENAI_API_KEY=your-openai-api-key-here
```
Replace your-openai-api-key-here with your actual API key from OpenAI.

If you do not have an OpenAI API key, you can obtain one by registering at https://platform.openai.com/signup.

## Project Structure
CooKinAgent consists of two main scripts located within the CooKinAgent folder:
- `main.py` 
- `app.py` – This is the Streamlit application.

To run the Streamlit app:
```
streamlit run app.py [--build_chroma]
```
By default, `--build_chroma` is set to `False`, meaning that the vectorstore data will not be built from scratch. Instead, it will be downloaded if necessary.

## How It Works
1. Retrieves current weather data for the specified city using the wttr.in API.
2. Generates a response based on `suggestion_system_prompt.txt` and `suggestion_user_prompt.txt`, focusing on common recipes and ingredients specific to the chosen city.
3. Computes the similarity between the suggested response and the data stored in chroma, returning the recipe with the highest similarity score.
4. Formats the response using `formatting_data_system.txt` and `formatting_data_user.txt`, then outputs it to the user.

## Retrieval Strategy
The project uses the Retrieval-Augmented Generation (RAG) approach to select the recipe with the highest similarity score, ensuring that the recipe suggestions are relevant.
