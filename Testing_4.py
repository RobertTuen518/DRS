import joblib
import pandas as pd
import streamlit as st
import PIL
from sklearn.preprocessing import StandardScaler

# Load the dataset
data = pd.read_csv("USDA_KM.csv")

# Load the model and scaler
kmeans = joblib.load('kmeans.joblib')
# scaler = joblib.load('C:/Users/User/PycharmProjects/Python_Tutorial/scaler.joblib')

# Create a feature matrix
scaled_data = data[['Calories', 'TotalFat', 'Carbohydrate', 'Sugar', 'Protein']]

# Scale the data to improve model performance
scaler = StandardScaler()

# Scale the data to improve model performance
scaler.fit_transform(scaled_data)


def diet_recommendation(calories):
    # Calculate the recommended intake of macronutrients
    Protein = calories * 0.15 / 4
    TotalFat = calories * 0.3 / 9
    Carbohydrate = calories * 0.4 / 4
    Sugar = calories * 0.1 / 4

    # Select foods from the same cluster as the target calorie intake
    filtered_data = data[
        data['cluster'] == kmeans.predict(scaler.transform([[calories, Protein, TotalFat, Carbohydrate, Sugar]]))[0]]

    # Sort the foods by energy density
    sorted_data = filtered_data.sort_values('Calories')

    # Display the top 10 recommendations
    return sorted_data.head(10)

tab1, tab2, tab3, tab4 = st.tabs(["Page 1", "Page 2", "BMI Calculator", "Diet Recommendation"])


def page1():
    with tab1:
        # Page 1
        image = PIL.Image.open('OIP.jpg')
        st.image(image, width=640)

        st.title("Diet Recommendation System")
        st.subheader("Please enter your personal information below:")

        # Create text input for name
        tab1.name = st.text_input("Name")

        # Create numeric input for age
        # age = st.number_input("Age", min_value=0, max_value=120)
        tab1.age = st.slider("Age", 0, 120, 0)

        # Create a select widget for gender
        tab1.gender = st.selectbox("Gender", options=["     ", "Male", "Female"])

        # Create numeric input for height
        tab1.height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, step=0.1)

        # Create numeric input for weight
        tab1.weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1)

        # Create a select widget for physical activity level
        tab1.activity_level = st.selectbox("Physical activity level", options=["Sedentary (little or no exercise)",
                                                                          "Lightly Active (light exercise/sports      1-3 "
                                                                          "days/week)",
                                                                          "Moderately Active (moderate exercise/sports  "
                                                                          " 3-5 days/week)",
                                                                          "Very Active (hard exercise/sports     6-7 days a "
                                                                          "week)",
                                                                          "Extra Active (very hard exercise/sports & a "
                                                                          "physical job)"])

        # Create button to navigate to Page 2
        if st.button("Submit"):
            # Set the active tab to Page 2
            st.session_state = tab2


def page2():
    with tab2:
        # Page 2
        page1()
        st.title("Results")
        st.subheader("Based on the information you provided, your results are as follows:")

        # Calculate BMI
        if tab1.height != 0:
            bmi = tab1.weight / ((tab1.height / 100) ** 2)
            bmi_status = ""
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_status = "Normal weight"
            elif 25 <= bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"
        else:
            bmi = 0

            bmi_status = "Invalid input: height cannot be zero"

        age = float(tab1.age)
        weight = float(tab1.weight)
        height = float(tab1.height)

        # Create a dictionary for each physical activity level
        activity_level_dict = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extra Active": 1.9
        }

        # Calculate total daily energy expenditure based on Harris-Benedict Equation
        activity_level_value = activity_level_dict.get(tab1.activity_level, 1.2)

        if tab1.gender == "Male":
            bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
        else:
            bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

        # Total Daily Energy Expenditure (tdee) in calories multiply Basal Metabolic Rate (bmr) by the
        # appropriate activity factor

        tdee = bmr * activity_level_value

        # Display results
        st.write("Name:     ", tab1.name)
        st.write("Age:      ", tab1.age)
        st.write("Gender:   ", tab1.gender)
        st.write("BMI:  ", round(bmi, 2))
        st.write("BMI Status:       ", bmi_status)

        st.session_state.tdee = round(tdee, 2)

        st.write("Total Daily Energy Expenditure in calories:   ", st.session_state.tdee)

        # Create button to navigate back to Page 1
        if st.button("Back"):
            st.session_state.tab = 1


with tab3:
    # Page 3
    # Create a title for the app
    st.title('Welcome to BMI Calculator 🧮')

    # TAKE WEIGHT INPUT in kg
    weight = st.number_input("Enter your weight     (kg)")

    # radio button to choose height format
    status = st.radio('Select your height format: ',
                      ('cm', 'meter', 'feet'))

    # compare status value
    if status == 'cm':
        # take height input in centimeters
        height = st.number_input('Centimeters')

        try:
            bmi = weight / ((height / 100) ** 2)
        except:
            st.caption(":red[Please enter valid input values.]")

    elif status == 'meter':
        # take height input in meters
        height = st.number_input('Meters')

        try:
            bmi = weight / (height ** 2)
        except:
            st.caption(":red[Please enter valid input values.]")

    else:
        # take height input in feet
        height = st.number_input('Feet')

        # 1 meter = 3.28
        try:
            bmi = weight / ((height / 3.28) ** 2)
        except:
            st.caption(":red[Please enter valid input values.]")

    if not st.button('Calculate BMI'):
        pass
    # check if the button is pressed or not
    else:
        # print the BMI INDEX
        st.text("Your BMI Index is {}.".format(bmi))

        # give the interpretation of BMI index
        if bmi < 18.5:
            st.warning("Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Healthy")
        elif 25 <= bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")

with tab4:
    page2()
    # Page 4
    # Retrieve the value of tdee from st.session_state
    tdee = st.session_state.tdee

    # Create recommend diet button on Page 2
    # Create a button that triggers the diet_recommendation function based on user input
    if st.button("Recommend Diet"):

        # Display the recommendations in a table
        st.info("Top 10 recommended foods:")

        # Call the diet_recommendation function
        recommendations = diet_recommendation(tdee)

        st.write(recommendations)

        recommendations_text = ''

        for i in range(len(recommendations)):
            recommendations_text += str(i + 1) + '. ' + recommendations.iloc[i]['Description'] + '\n'

        st.write(recommendations_text)
