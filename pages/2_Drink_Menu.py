import streamlit as st
import requests


# globals
DRINK_NAME_SEARCH_API = \
    r"https://www.thecocktaildb.com/api/json/v1/1/search.php?s="

# initialization
session = requests.Session()
drinkList = [
    'Bellini',
    'Bloody Mary',
    'Boulevardier',
    'Daiquiri',
    'Gimlet',
    'Long Island',
    'Mai Tai',
    'Manhattan',
    'Margarita',
    'Martinez',
    'Martini',
    'Mimosa',
    'Mint Julep',
    'Mojito',
    'Moscow Mule',
    'Negroni',
    'Old Fashioned',
    'Penicillin',
    'Pina Colada',
    'Sangria',
    'Screwdriver',
    'Sex on the Beach',
    'Sidecar',
    'Tom Collins',
    'Whiskey Sour',
    'White Russian'
    ]


# functions
@st.cache_data
def fetch(url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


# sidebar
famousDrinkName = st.sidebar.radio(
    label="Popular Drinks",
    options=drinkList,
    index=0
).replace(" ", "+").lower()

# --- caption for author and update
st.sidebar.caption(body="Made by: :red[James Michael Ballow]")
st.sidebar.caption(body="Last Updated: :red[March 2023]")

# grab data
data = fetch(f"{DRINK_NAME_SEARCH_API}{famousDrinkName}")
if not data:
    st.error("Developer Error: API No longer supports "
             f"drink information for {famousDrinkName}")

# grab drink information
# --- simple information
drinkName = data["drinks"][0]["strDrink"]
drinkImgAdress = data["drinks"][0]["strDrinkThumb"]
drinkImgSource = data["drinks"][0]["strImageSource"]
drinkVidAdress = data["drinks"][0]["strVideo"]
drinkAllowImg = data["drinks"][0]["strCreativeCommonsConfirmed"]
drinkGlass = data["drinks"][0]["strGlass"].capitalize()
instructions = data["drinks"][0]["strInstructions"]


# --- get ingredients and quantities
ingredients = []
for idx in range(1, 16):
    ing = data["drinks"][0][f"strIngredient{idx}"]
    if ing:
        quant = data["drinks"][0][f"strMeasure{idx}"]
        if quant and quant[-1] == " ":
            quant = quant[:-1]
        if quant:
            ingredients.append(f"{ing} - (:red[{quant}])")
        else:
            ingredients.append(ing)
    else:
        break

# --- alternatives
data["drinks"].pop(0)
alternatives = []
for a in data["drinks"]:
    alternatives.append(a["strDrink"])


# visuals
col1, col2 = st.columns(2)
with col1:
    st.markdown(body=f"## {drinkName}")
    st.image(
        image=drinkImgAdress,
        caption=f"""
            Sample Image of {drinkName} †.
        """,
        width=None,
    )

with col2:
    st.markdown(body="## Ingredients")
    ingString = ""
    for ingredient in ingredients:
        ingString += f"1. {ingredient}\n"
    st.markdown(ingString)

    st.markdown(body="## Drink Variations")
    altString = ""
    for alt in alternatives:
        altString += f"1. {alt}\n"
    st.markdown(altString or "None Found")


with st.expander("See Assembly Instructions"):
    instructions = instructions.replace("\r", "")
    instructions = instructions.replace("\n", " ")
    steps = instructions.split(".")
    stepString = ""
    for step in steps[:-1]:
        stepString += f"1. {step}.\n"
    st.markdown(stepString)

    if drinkVidAdress is not None:
        st.markdown("  ")
        st.write(
            f'''
                <a target="_blank" href="{drinkVidAdress}">
                    <button style="background-color: #2b2d42; border-radius:
                        5%; border: 2px solid #d62828; color: white; padding:
                        10px 25px">
                        Watch Video Demonstration
                    </button>
                </a>
            ''',
            unsafe_allow_html=True
        )
        st.markdown("  ")

st.caption(body=f"""† Image source: {drinkImgSource or drinkImgAdress}""")
