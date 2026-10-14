import streamlit as st
import pandas as pd
import numpy as np

# pip install scikit-learn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import pickle

# pip install plotly
import plotly.express as px
import os

# streamlit run Model_example01.py

# page config
st.set_page_config(
    page_title="IRIS ML CLASSIFICATION",
    page_icon="😎",
    layout="centered"
)

st.title("IRIS Flower Species Classifier")
st.write("Train a Machine Learning Model")

# side bar
st.sidebar.header("Model Settings")

# options - train a new model
train_new = st.sidebar.checkbox("Train a new Model",value=True)

@st.cache_resource
@st.cache_resource
def load_and_train_model():
    #load data
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target
    target_names = iris.target_names

    # split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # train random forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, X, y, target_names, accuracy, X_train.columns.tolist()


if train_new or not os.path.exists("iris_model.pkl"):
    model, X, y, target_names, accuracy, feature_names = load_and_train_model()

    # save model
    with open("iris_model.pkl", "wb") as f:
        pickle.dump((model, target_names, feature_names), f)

    st.sidebar.success(f"Model Trained | Accuracy : {accuracy:.2%}")

else:
    with open("iris_model.pkl", "rb") as f:
        model, target_names, feature_names = pickle.load(f)

    st.sidebar.success("Loaded Pre-Trained Model")
#Main input
st.subheader("Enter the flower Measurements")

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.slider("Sepal Length (cm)", 4.0, 8.0, 5.0, 0.1)
    sepal_width = st.slider("Sepal Width (cm)", 2.0, 4.5, 3.0, 0.1)

with col2:
    petal_length = st.slider("Petal Length (cm)", 1.0, 7.0, 4.0, 0.1)
    petal_width = st.slider("Petal Width (cm)", 0.1, 2.5, 1.0, 0.1)

#create a input dataframe for prediction\
input_data = pd.DataFrame({
    "sepal length (cm)": [sepal_length],
    "sepal width (cm)": [sepal_width],
    "petal length (cm)": [petal_length],
    "petal width (cm)": [petal_width]
})

if st.button("Predict Species", type="primary", use_container_width=True):

    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]

    predicted_species = target_names[prediction]

    st.success(f"Predicted species : {predicted_species}")

    # show probabilities
    st.write("Prediction probabilities:")

    prob_df = pd.DataFrame({
        "Species": target_names,
        "Probability": prediction_proba
    })

    st.bar_chart(prob_df.set_index("Species"))

# model performance section
st.subheader("Model Performance")

if 'accuracy' in locals():
    st.metric("Test Accuracy", f"{accuracy:.2%}")

if st.checkbox("Show Dataset"):
    st.write("### IRIS DATASET PREVIEW")

    iris_df = pd.DataFrame(X)
    iris_df["Species"] = pd.Series(y).map({
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    })

    st.dataframe(iris_df.head())

    # scatter
    fig = px.scatter(
        iris_df,
        x="sepal length (cm)",
        y="petal length (cm)",
        color="Species",
        title="Sepal Width vs Petal Length",
        hover_data=["sepal length (cm)", "petal length (cm)"]
    )

    st.plotly_chart(fig, use_container_width=True)