import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge


# Data + rensa nullvärden
df = pd.read_csv("car_price_dataset.csv", sep=(";"))
df.dropna(how="any", inplace=True)

# Data uppdelning
X = df.drop(columns=["Price"])
y = df["Price"]

# Get dummies
X = pd.get_dummies(X, drop_first=True)

# Splitta datan
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.15, random_state=42
)

# Streamlit navigation
nav = st.sidebar.radio("Navigation Menu", ["Purpose", "Data & Modelling"])

if nav == "Purpose":
    st.title("Streamlit Overview")
    st.header("Purpose")
    st.write("""The purpose of this example demonstration is to give you a fast 
             overview of Streamlit where details are omitted. After watching the video
             read the section "Get Started" from the excellent documentation
             available at: [https://docs.streamlit.io/library/get-started](https://docs.streamlit.io/library/get-started)
             and you will know everything you need to create your first 
             Streamlit app. """)
    st.write("Happy Coding!")
    st.write("Antonio Prgomet")
    st.write("[https://www.linkedin.com/in/antonioprgomet/](https://www.linkedin.com/in/antonioprgomet/)")



if nav == "Data & Modelling":
    st.title("Bil pris estimerare")
    st.write("Fyll i information om bilen för att estimera priset.")             
    st.header("Uppgifter")

    # Printa ut input-fält
    user_input = {}
    for col in df.drop(columns=["Price"]).columns:
        if df[col].dtype in [np.int64, np.float64]:
            user_input[col] = st.number_input(f"{col}", value=float(df[col].mean()))
        else:
            user_input[col] = st.selectbox(f"{col}", df[col].unique())

    # Gör om userinput till DataFrame
    input_df = pd.DataFrame([user_input])

    # Samma dummyhantering som träningsdata
    input_df = pd.get_dummies(input_df, drop_first=True)
    input_df = input_df.reindex(columns=X.columns, fill_value=0)

    # Ridge-modell
    ridge = Ridge(alpha=10)
    ridge.fit(X_train, y_train)

    if st.button("Beräkna pris"):
        prediction = ridge.predict(input_df)[0]
        st.success(f"Det estimerade priset för bilen är: {prediction:.2f} dollar")
