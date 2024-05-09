import streamlit as st
from data.data_utils import read_txt_file
from main import main, build_vectorstore
import argparse

STYLE_PATH = "app_utils/style.txt"
STYLE = read_txt_file(STYLE_PATH)

parser = argparse.ArgumentParser(description="Streamlit App")

parser.add_argument(
    "--build_chroma",
    action="store_true",
    help="Whether to build chroma vectors using your resources or not.",
)
args = parser.parse_args()
BUILD_CHROMA = args.build_chroma


def streamlit_app(build_chroma, style=STYLE):
    st.markdown(style, unsafe_allow_html=True)
    st.image("app_utils/recipe.png", width=150)

    st.markdown(
        "<h1 class='title'>Welcome to the Wacky World of CooKinAgent!</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <p class='agent-description'>
    Hey there, culinary adventurer! 🍳🌍 How about adding some zest to your day with a delightful dish suggested by yours truly, the CooKinAgent? Just type in the name of any city, and I'll whip up some tasty recipe suggestions based on the current weather there! 🌤️☔ Let's turn the forecast into a feast! 😄🍲
    </p>
    """,
        unsafe_allow_html=True,
    )

    with st.spinner(
        "We're in the process of making the recipes database in the adpated format, which will be a one-time endeavor! It will take some time, but your patience will be rewarded with the best recipes! 😄"
    ):
        build_vectorstore(build_chroma=build_chroma)

    city = st.text_input(
        "Enter the name of a city you're interested in!",
        placeholder="City Name",
        key="city_input",
    )
    if st.button("Whip Up Some Recipes!", key="get_info"):
        if city:
            with st.spinner("We're whipping up your recipe now! 🥄🍳"):
                agent_response = main(city)
            st.success(agent_response)
        else:
            st.markdown(
                "<p class='warning-text'>Hey there, sparky! Don't leave me hanging! Enter a city name and let's cook up some fun!</p>",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    streamlit_app(build_chroma=BUILD_CHROMA)
