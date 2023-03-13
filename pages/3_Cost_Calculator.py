import math
import streamlit as st
import matplotlib.pyplot as plt

# globals
# --- drinks/food
DRINK_FOOD_VEGAS_SCALAR = 1.5
DRINK_SERVER_SPEED_FASTEST = 20  # min
DRINK_SERVER_SPEED_SLOWEST = 60  # min
AVG_SERVERS_PER_DAY = 5

# --- conversions
DAYS_TO_MIN = 1440
HOURS_TO_MIN = 60

# --- taxes
TAX_RATE = 0.0685 + 0.0153

# --- assumptions
HOURS_GAMBLE_PER_DAY = 8
ADDITIONAL_HAPPY_TAX = 0.20

# --- colors
COLOR_OPTIONS = {
    "Pinks": ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff"],
    "Neons": ["#8ecae6", "#219ebc", "#023047", "#ffb703", "#fb8500"],
    "Sun and Sea": ["#ffbe0b", "#fb5607", "#ff006e", "#8338ec", "#3a86ff"],
    "Tommy Hilfiger": ["#e63946", "#f1faee", "#a8dadc", "#457b9d", "#1d3557"],
}


# # global settings
# st.set_page_config(
#    page_title="Vegas Costimator",
#    page_icon="♣",
#    layout="wide",
#    initial_sidebar_state="expanded",
# )


# helper functions
def foodTipRelabel(val):
    return f"{val}%"


# Add User Inputs
# -1- number of days in vegas
numDays = st.sidebar.text_input(
    label=':violet[Number of Days in Vegas]',
    value=5,
    help="PUT MESSAGE HERE TO EXPLAIN",
)
try:
    numDays = int(numDays)
except Exception:
    st.sidebar.error(f"Number of Days you entered ({numDays}) "
                     "is wrong format. It must be a number.")

# -1- number of people going to vegas
numPeople = st.sidebar.text_input(
    label=':violet[Number of People Going to Vegas]',
    value=1,
    help="PUT MESSAGE HERE TO EXPLAIN",
)
try:
    numPeople = int(numPeople)
except Exception:
    st.sidebar.error(f"Number of People you entered ({numPeople}) "
                     "is wrong format. It must be a number.")
st.sidebar.caption(body="---")

# -2- betting style
betStyleDict = {
    "Slow and Steady": 5,
    "Continual Button Hits": 10,
    "Fast as Possible": 20,
}
betStyle = st.sidebar.selectbox(
    label=':green[Preferred Betting Style]',
    options=list(betStyleDict.keys()),
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # hits per min
betSpeed = betStyleDict[betStyle]

# -2- betting slot machine preference
betLevel = st.sidebar.slider(
    label=':green[Prefrerred Betting Range]',
    min_value=0.0,
    max_value=20.0,
    value=(2.0, 18.0),
    format="$%.2f",
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # $ per hit

# -2- machine denomination and return rate
machineDenom = st.sidebar.select_slider(
    label=':green[Preferred Machine Denomination]',
    value="1¢",
    options=["1¢", "5¢", "25¢", "$1", "$5+"],
    help="PUT MESSAGE HERE TO EXPLAIN",
)
returnPer = {
    "1¢": 0.884,
    "5¢": 0.917,
    "25¢": 0.894,
    "$1": 0.925,
    "$5+": 0.873,
}  # avg machine return prob.
st.sidebar.caption(body="---")

# -3- meals per day
numMeals = st.sidebar.selectbox(
    label=':blue[Number of FULL Meals/Day]',
    options=[1, 2, 3],
    index=1,
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # num of meals eaten by one person per day

# -3- snacks per day
numSnacks = st.sidebar.selectbox(
    label=':blue[Number of Snacks/Day]',
    options=[1, 2, 3],
    index=1,
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # percentage of meal

# -3- price of local burger
mealCost = st.sidebar.text_input(
    label=':blue[Cost of Burger in Your City (No Tax)]',
    value="%.2f" % 18.00,
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # percentage of meal
try:
    mealCost = mealCost.replace("$", "")
    mealCost = float(mealCost)
    mealCost *= DRINK_FOOD_VEGAS_SCALAR
    snackCost = mealCost * 0.5
except Exception:
    st.sidebar.error(f"Cost you entered ({mealCost}) is wrong format. "
                     "It must be a number with two decimal places.")

# -3- price of local cocktail
drinkCost = st.sidebar.text_input(
    label=':blue[Cost of a Cocktail in Your City (No Tax)]',
    value="%.2f" % 8.00,
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # percentage of meal
try:
    drinkCost = drinkCost.replace("$", "")
    drinkCost = float(drinkCost)
    drinkCost *= DRINK_FOOD_VEGAS_SCALAR
except Exception:
    st.sidebar.error(f"Cost you entered ({drinkCost}) is wrong format. "
                     "It must be a number with two decimal places.")

# -3- dining tip rate
foodTip = st.sidebar.select_slider(
    label=':blue[Expected Dining Tip Rate]',
    value=10.0,
    options=list(range(0, 26)),
    format_func=foodTipRelabel,
    help="PUT MESSAGE HERE TO EXPLAIN",
)  # percent
st.sidebar.caption(body="---")

# --- caption for author and update
st.sidebar.caption(body="Made by: :red[James Michael Ballow]")
st.sidebar.caption(body="Last Updated: :red[March 2023]")


# Calculations
# --- tips
drinkTip = 2 * int(drinkCost * (foodTip/100))
serverTip = int(drinkTip * 0.75)

# --- gambling
rateOfReturn = returnPer[machineDenom]
minutesGambling = numDays * HOURS_GAMBLE_PER_DAY * HOURS_TO_MIN
totBets = minutesGambling * betSpeed

# --- drinks during gambling
minDrinks = minutesGambling / DRINK_SERVER_SPEED_SLOWEST
maxDrinks = minutesGambling / DRINK_SERVER_SPEED_FASTEST
totServers = numDays * AVG_SERVERS_PER_DAY
totNewServerTip = totServers * serverTip

# --- food
totMeals = numDays * numMeals
totSnacks = numDays * numSnacks
tax = (1 + TAX_RATE)
tip = (1 + foodTip/100)

# --- all costs
cost = {
    "gambling": {
        "loBet": totBets * (1 - rateOfReturn) * betLevel[0] * numPeople,
        "hiBet": totBets * (1 - rateOfReturn) * betLevel[1] * numPeople,
        "minDrinks": minDrinks * drinkTip * numPeople + totNewServerTip,
        "maxDrinks": maxDrinks * drinkTip * numPeople + totNewServerTip,
    },
    "food": {
        "snacks": (totSnacks * snackCost) * tax * tip * numPeople,
        "meals": (totMeals * mealCost) * tax * tip * numPeople,
        "alcohol": (totMeals * drinkCost) * tax * tip * numPeople,
    },
}
cost["gambling"]["lo"] = cost["gambling"]["loBet"] \
                       + cost["gambling"]["minDrinks"]
cost["gambling"]["hi"] = cost["gambling"]["hiBet"] \
                       + cost["gambling"]["maxDrinks"]
cost["food"]["lo"] = cost["food"]["snacks"] \
                    + cost["food"]["meals"] \
                    + cost["food"]["alcohol"]
cost["food"]["hi"] = cost["food"]["snacks"] * ADDITIONAL_HAPPY_TAX \
                    + cost["food"]["meals"] * ADDITIONAL_HAPPY_TAX\
                    + cost["food"]["alcohol"] * ADDITIONAL_HAPPY_TAX
cost["total"] = {
    "loEstimate": cost["gambling"]["lo"] + cost["food"]["lo"],
    "hiEstimate": cost["gambling"]["hi"] + cost["food"]["hi"],
}


# visuals
# --- color palette
pieColors = st.radio(
    label="Pie Chart Color",
    options=list(COLOR_OPTIONS.keys()),
    index=1
)

# --- header
st.header(":red[Approximate Cost to Gamble and Eat (Everyone in Trip)]")

# --- pie chart showing cost breakdown
loTotFactor = 100 / cost["total"]["loEstimate"]
hiTotFactor = 100 / cost["total"]["hiEstimate"]
aht = (1 + ADDITIONAL_HAPPY_TAX)
sizes = {
    "loEstimate": [
        (cost["gambling"]["lo"] * loTotFactor),
        (cost["gambling"]["minDrinks"] * loTotFactor),
        (cost["food"]["snacks"] * loTotFactor),
        (cost["food"]["meals"] * loTotFactor),
        (cost["food"]["alcohol"] * loTotFactor)
    ],
    "hiEstimate": [
        (cost["gambling"]["hi"] * hiTotFactor),
        (cost["gambling"]["maxDrinks"] * hiTotFactor),
        (cost["food"]["snacks"] * hiTotFactor) * aht,
        (cost["food"]["meals"] * hiTotFactor) * aht,
        (cost["food"]["alcohol"] * hiTotFactor) * aht
    ],
}
labels = {
    "loEstimate": [
        f"Gambling (Bets) - ${'%1.2f' % cost['gambling']['loBet']}",
        f"Gambling (Drinks) - ${'%1.2f' % cost['gambling']['minDrinks']}",
        f"Food (Snacks) - ${'%1.2f' % cost['food']['snacks']}",
        f"Food (Meals) - ${'%1.2f' % cost['food']['meals']}",
        f"Food (Drinks) - ${'%1.2f' % cost['food']['alcohol']}"
    ],
    "hiEstimate": [
        f"Gambling (Bets) - ${'%1.2f' % (cost['gambling']['hiBet'])}",
        "Gambling (Drinks) - "
        f"${'%1.2f' % (cost['gambling']['maxDrinks'] * aht)}",
        f"Food (Snacks) - ${'%1.2f' % (cost['food']['snacks'] * aht)}",
        f"Food (Meals) - ${'%1.2f' % (cost['food']['meals'] * aht)}",
        f"Food (Drinks) - ${'%1.2f' % (cost['food']['alcohol'] * aht)}"
    ],
}
explode = (
    0.05,
    0.05,
    0.05,
    0.05,
    0.05
)

# low estimate
fig1, ax = plt.subplots()
fig1.set_facecolor("#2b2d42")
ax.pie(
    sizes["loEstimate"],
    explode=explode,
    labeldistance=1.5,
    colors=COLOR_OPTIONS[pieColors],
    shadow=False,
    startangle=45
)
ax.axis('equal')
ax.legend(labels["loEstimate"], loc="lower left")

# high estimate
fig2, ax = plt.subplots()
fig2.set_facecolor("#2b2d42")
ax.pie(
    sizes["hiEstimate"],
    explode=explode,
    labeldistance=1.5,
    colors=COLOR_OPTIONS[pieColors],
    shadow=False,
    startangle=45
)
ax.axis('equal')
ax.legend(labels["hiEstimate"], loc="lower left")

# place pie into two columns
col1, col2 = st.columns(2)
with col1:
    dollar = '%.2f' % cost['total']['loEstimate']
    st.header(f"Low Estimate (${dollar})")
    st.pyplot(fig1)
    st.markdown(
        body=f"""
            #### Assumptions
            1. Gambling is only at the lowest betting rate of
               :red[${int(betLevel[0])} per bet].
            2. Gambling at a :red[{betStyle}] pace
               (:red[{betSpeed} bets per min]).
            3. You win :red[NO] jackpots, and you average a
               :red[{rateOfReturn*100}% return rate].
            4. You encounter :red[{totServers} drink servers]
               in Vegas.
            5. Give each drink server :red[${math.ceil(serverTip + drinkTip)}]
               for the :red[first drink].
            6. Give each drink server :red[${math.ceil(drinkTip)}] for
               :red[every drink after the first one].
            7. You eat :red[{numMeals} meals per day], each
               costing :red[${'%1.2f' % (mealCost)}].
            8. You eat :red[{numSnacks} snacks per day], each
               costing :red[${'%1.2f' % (snackCost)}].
            9. You have :red[1 alcoholic drink per meal] (not per snack).
        """
    )

with col2:
    dollar = '%.2f' % cost['total']['hiEstimate']
    st.header(f"High Estimate (${dollar})")
    st.pyplot(fig2)
    st.markdown(
        body=f"""
            #### Assumptions
            1. Gambling is only at the highest betting rate of
               :red[${int(betLevel[1])} per bet].
            2. Gambling at a :red[{betStyle}] pace
               (:red[{betSpeed} bets per min]).
            3. You win :red[NO] jackpots, and you average a
               :red[{rateOfReturn*100}% return rate].
            4. You encounter :red[{totServers} drink servers]
               in Vegas.
            5. Give each drink server
               :red[${math.ceil((serverTip + drinkTip) * aht)}]
               for the :red[first drink].
            6. Give each drink server :red[${math.ceil(drinkTip * aht)}] for
               :red[every drink after the first one].
            7. You eat :red[{numMeals} meals per day], each
               costing :red[${'%1.2f' % (mealCost * aht)}].
            8. You eat :red[{numSnacks} snacks per day], each
               costing :red[${'%1.2f' % (snackCost * aht)}].
            9. You have :red[1 alcoholic drink per meal] (not per snack).
        """
    )
