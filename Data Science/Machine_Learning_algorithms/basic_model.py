import streamlit as st

st.set_page_config(
    page_title="BMI Calculator",
    page_icon="🧁",
    layout="centered"
)

st.title("BMI Calculator")

st.write(st.write("""
**Body Mass Index (BMI)** is a simple measurement that estimates whether a person's weight is appropriate for their height. It is calculated using a person's weight (in kilograms) divided by the square of their height (in meters). BMI is commonly used to classify individuals as underweight, normal weight, overweight, or obese.
"""))
st.subheader("Enter your details")
# using 2 columns
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        value=70.0,
        step=1.5
    )

with col2:
    height = st.number_input(
        "Height (cm)",
        min_value=1.7,
        value=1.7,
        step=0.01,
        max_value=2.5
    )
if st.button("Calculate BMI", type="primary", use_container_width=True):
    if height > 0:
        bmi = weight / (height ** 2)

        # show result
        st.success(f"Your BMI is {bmi:.2f}")

        if bmi < 18.5:
            st.warning("🟡 Under weight 🟡")

        elif bmi < 25:
            st.success("🟢 Normal weight 🟢")

        elif bmi < 30:
            st.warning("🟠 Over Weight 🟠")

        else:
            st.error("🔴 Obese Please Consult a Doctor Contact on this Number 987654312🔴")
            st.info("""
    ***General Score***

    1. Guide Below 18.5:
    2. Underweight 18.5 to 24.9:
    3. Normal weight 25.0 to 29.9:
    4. Overweight 30.0 and above: Obese
""")

else:
    st.error("Height must be greater then 0")


# SideBar
with st.sidebar:
    st.header("About this app")

    st.write(
        "BMI = kg/m². For imperial units, divide your weight in pounds by height in inches squared and multiply by 703."
    )

    st.caption(
        "Body Mass Index is widely used as an indicator of body fat content. Use our BMI calculator for men & women to know your Body Mass Index and determine your "
    )