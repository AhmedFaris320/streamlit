import streamlit as st
import pandas as pd

st.title("BMI Calculator")
st.write("Calculate your Body Mass Index (BMI)")

# Input fields for weight and height
weight = st.number_input("Enter your weight (kg)", min_value=0.0, format="%.2f")
height = st.number_input("Enter your height (cm)", min_value=0.0, format="%.2f")

# Calculate BMI
if st.button("Calculate"):
    if height > 0:
        bmi = weight / ((height/100) ** 2)
        
        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
            advice = "You may need to gain weight. Consider consulting a healthcare provider for a healthy weight gain plan."
        elif 18.5 <= bmi < 25:
            category = "Normal Weight"
            color = "green"
            advice = "Great! You're in the healthy weight range. Maintain your current lifestyle."
        elif 25 <= bmi < 30:
            category = "Overweight"
            color = "orange"
            advice = "You may benefit from losing some weight. Consider a balanced diet and regular exercise."
        else:
            category = "Obese"
            color = "red"
            advice = "Consider consulting a healthcare provider for a weight management plan."
        
        # Display results
        st.success(f"Your BMI is: {bmi:.2f}")
        
        # Display category with color coding
        if color == "blue":
            st.info(f"**Category:** {category}")
        elif color == "green":
            st.success(f"**Category:** {category}")
        elif color == "orange":
            st.warning(f"**Category:** {category}")
        else:
            st.error(f"**Category:** {category}")
        
        # Display health advice
        st.write(f"**Health Advice:** {advice}")
        
        # BMI Chart
        st.subheader("BMI Categories Chart")
        bmi_data = {
            "Category": ["Underweight", "Normal Weight", "Overweight", "Obese"],
            "BMI Range": ["< 18.5", "18.5 - 24.9", "25.0 - 29.9", "≥ 30.0"],
            "Your Status": ["✓" if category == "Underweight" else "",
                           "✓" if category == "Normal Weight" else "",
                           "✓" if category == "Overweight" else "",
                           "✓" if category == "Obese" else ""]
        }
        
        df = pd.DataFrame(bmi_data)
        st.table(df)
        
    else:
        st.error("Height must be greater than 0.")