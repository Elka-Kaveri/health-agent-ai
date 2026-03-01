import streamlit as st
from database import *
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Health Assistant", page_icon="💊", layout="wide")

# ------------------- CUSTOM THEME ------------------- #
st.markdown("""
<style>

/* 🌅 Full Page Orange + Yellow Gradient */
.stApp {
    background: linear-gradient(135deg, #fff3b0 0%, #ffb703 50%, #fb8500 100%);
}

/* Center content */
.block-container {
    padding-top: 3rem;
}

/* White Glass Login Card */
.login-card {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 10px 35px rgba(0,0,0,0.2);
    max-width: 500px;
    margin: auto;
}

/* Dashboard Cards */
.section-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff7f11, #fb8500);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
    border: none;
}

/* Input fields */
div[data-baseweb="input"] > div {
    background-color: white !important;
    border-radius: 8px !important;
    border: 1px solid #ffb703 !important;
}

/* Headings */
h1 {
    color: #8d2c00;
    text-align: center;
}

h4 {
    text-align: center;
    color: #5a2d00;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #fb8500;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ------------------- SESSION ------------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------- LOGIN PAGE ------------------- #
if not st.session_state.logged_in:

    st.markdown("<h1>💊 AI Health Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<h4>Your Smart Wellness Companion</h4>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    choice = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Create Account"):
            try:
                create_user(username, password)
                st.success("Account Created! Please Login.")
            except:
                st.error("Username already exists")

    if choice == "Login":
        if st.button("Login"):
            user = check_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid Credentials")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ------------------- MAIN APP ------------------- #

username = st.session_state.username
name_display = username.split("@")[0].capitalize()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "BMI Calculator", "Diet Plan"])

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title(f"👋 Welcome, {name_display}")

# ------------------- DASHBOARD ------------------- #
if page == "Dashboard":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Step Tracker")

    date = st.date_input("Select Date")
    steps = st.number_input("Enter Steps", min_value=0)

    if st.button("Save Steps"):
        add_steps(username, str(date), steps)
        st.success("Steps Saved")

    data = get_steps(username)

    if data:
        df = pd.DataFrame(data, columns=["Date", "Steps"])
        st.dataframe(df)

        plt.figure()
        plt.plot(df["Date"], df["Steps"])
        plt.xticks(rotation=45)
        plt.title("Step Progress")
        plt.xlabel("Date")
        plt.ylabel("Steps")
        st.pyplot(plt)
    else:
        st.info("No step data yet.")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- BMI ------------------- #
if page == "BMI Calculator":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## ⚖ BMI Calculator")

    weight = st.number_input("Weight (kg)")
    height = st.number_input("Height (m)")

    if st.button("Calculate BMI"):
        if height > 0:
            bmi = weight / (height ** 2)
            st.write("Your BMI:", round(bmi, 2))

            if bmi < 18.5:
                st.warning("Underweight")
            elif bmi < 25:
                st.success("Normal weight")
            else:
                st.error("Overweight")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- DIET ------------------- #
if page == "Diet Plan":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 🥗 Diet Recommendation")

    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain", "General Fitness"])

    if st.button("Generate Diet Plan"):

        if diet_type == "Vegetarian":
            if goal == "Weight Loss":
                st.success("Breakfast: Oats + Fruits")
                st.success("Lunch: Brown Rice + Dal + Salad")
                st.success("Dinner: Vegetable Soup + Chapati")
            elif goal == "Muscle Gain":
                st.success("Breakfast: Paneer + Milk")
                st.success("Lunch: Rice + Rajma")
                st.success("Dinner: Tofu + Chapati")
            else:
                st.success("Balanced Veg Diet: Fruits, Dal, Vegetables")

        else:
            if goal == "Weight Loss":
                st.success("Breakfast: Boiled Eggs")
                st.success("Lunch: Grilled Chicken + Salad")
                st.success("Dinner: Fish (Low Oil)")
            elif goal == "Muscle Gain":
                st.success("Breakfast: Eggs + Peanut Butter")
                st.success("Lunch: Chicken + Rice")
                st.success("Dinner: Fish + Chapati")
            else:
                st.success("Balanced Non-Veg Diet: Eggs, Chicken, Vegetables")

    st.markdown('</div>', unsafe_allow_html=True)