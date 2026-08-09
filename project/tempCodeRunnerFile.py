import streamlit as st
import pickle
import numpy as np
import plotly.express as px
import pyttsx3

st.set_page_config(page_title="Health Risk Predictor", page_icon="💙", layout="wide")

PRIMARY = "#4C6FFF"
# Background gradient
BG_GRADIENT = "linear-gradient(135deg, #0b132b 0%, #112040 45%, #1f3a93 100%)"

st.markdown(
    f"""
    <style>
    .main {{
        background: {BG_GRADIENT};
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }}
    .block-container {{
        padding: 2rem 3rem;
    }}
    h1 {{
        background: linear-gradient(120deg, #8ab4ff 0%, #4c6fff 50%, #9b8bff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.3px;
    }}
    h2, h3, h4 {{
        color: #e2e8f0;
        letter-spacing: 0.2px;
    }}
    .stSelectbox, .stNumberInput, .stSlider {{
        background: #0e1a33;
        padding: 0.5rem 0.8rem;
        border-radius: 12px;
        border: 1px solid rgba(155,139,255,0.35);
    }}
    .stButton>button {{
        background: {PRIMARY};
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(76,111,255,0.25);
    }}
    .stAlert {{
        border-radius: 12px;
        background: #0e1a33;
        border: 1px solid rgba(155,139,255,0.35);
        color: #e2e8f0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


model=pickle.load(open("Health_risk_predictor.pkl","rb"))

encoders=pickle.load(open("label_encoders.pkl","rb"))
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


st.title("Health Risk Predictor")

col1, col2 = st.columns(2)
with col1:
    age=st.slider("Age",18,80,22)
    diet=st.selectbox("Diet Quality",["Poor","Average","Good"])
    exercise=st.slider("Exercise Day Per Week",0,7,3)
    sleep=st.slider("Sleep Hours",3,12,6)
    stress=st.selectbox("Stress Level",['Low','Medium','High'])
with col2:
    weight = st.number_input("Weight (kg)",20.0,200.0)
    height_cm = st.number_input("Height (cm)",100.0,220.0)
    smoking=st.selectbox("Smoking",["Yes","No"])
    drink = st.selectbox("Do you drink alcohol?", ["No", "Yes"])

if drink == "Yes":
    alcohol = st.selectbox("Alcohol Consumption Level", ["Low", "Medium", "High"])
else:
    # Encoder has classes ['High', 'Low', 'Medium']; map non-drinkers to 'Low' to avoid unseen label errors
    alcohol = "Low"

height_m = height_cm / 100
bmi = weight / (height_m ** 2)

st.write("Calculated BMI:", round(bmi,2))
family_history=st.selectbox("Family History of Disease",["Yes","No"])

if st.button("Predict Risk"):

    input_data=[age,
                encoders["diet"].transform([diet])[0],
                exercise,
                sleep,
                encoders["stress"].transform([stress])[0],
                bmi,
                encoders["smoking"].transform([smoking])[0],
                encoders["alcohol"].transform([alcohol])[0],
                encoders["family_history"].transform([family_history])[0],
                ]

    prediction=model.predict([input_data])
    probs=model.predict_proba([input_data])

    risk_label=encoders['risk_level'].inverse_transform([prediction[0]])[0]
    st.success(risk_label)

    # Play a brief audio cue that matches the predicted risk level
    def speak_risk(level: str):
        msgs = {
            "Low": "Your predicted health risk is low.",
            "Medium": "Your predicted health risk is moderate. Consider improving your lifestyle habits.",
            "High": "Your predicted health risk is high. Please consult a healthcare professional.",
        }
        speak(msgs.get(level, f"Your predicted health risk is {level}."))

    speak_risk(risk_label)

   # Bar Chart for lifestyle factors

    factors ={
       "Diet":encoders['diet'].transform([diet])[0],
        "Exercise":exercise,
        "Sleep":sleep,
        "Stress":encoders['stress'].transform([stress])[0],
        "BMI":bmi,
   }
    bar_fig=px.bar(
        x=list(factors.keys()),
        y=list(factors.values()),
        # The `labels={"x":"Factors","y":"value"}` parameter in the `px.bar()` function is used to
        # specify the labels for the x-axis and y-axis of the bar chart. In this case, it sets the
        # label for the x-axis to "Factors" and the label for the y-axis to "value". This helps
        # provide context and clarity to the data being visualized in the bar chart by indicating what
        # each axis represents.
        # The `labels={"x":"Factors","y":"value"}` parameter in the `px.bar()` function is used to
        # specify the labels for the x-axis and y-axis of the bar chart created using Plotly Express.
        labels={"x":"Factors","y":"value"},
        title="Your Lifestyle Factors"
    )
    bar_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        margin=dict(t=50, b=10, l=10, r=10),
        colorway=[PRIMARY]
    )
    st.plotly_chart(bar_fig)
    # ================== AI HEALTH REPORT ==================

# ---------- Disease Risk Section ----------
st.subheader("Possible Lifestyle Disease Risks")

diseases = []

if bmi > 25:
    diseases.append("Type 2 Diabetes")
    diseases.append("Heart Disease")

if smoking == "Yes":
    diseases.append("Lung Disease")
    diseases.append("Cancer Risk")

if alcohol == "High":
    diseases.append("Liver Disease")

if exercise < 2:
    diseases.append("Obesity")

if sleep < 6:
    diseases.append("Depression")
    diseases.append("Hypertension")

if stress == "High":
    diseases.append("Anxiety Disorders")

if family_history == "Yes":
    diseases.append("Genetic Health Risks")

if len(diseases) > 0:
    st.error("You may be at risk of:")
    for d in set(diseases):
        st.write("•", d)
else:
    st.success("No major lifestyle disease risks detected.")


# ---------- Final Health Summary ----------
st.subheader("Overall Health Summary")

disease_scores = {
    "Heart Disease": 0,
    "Type 2 Diabetes": 0,
    "Lung Disease": 0,
    "Liver Disease": 0,
    "Hypertension": 0,
    "Depression/Anxiety": 0,
}

if bmi > 25:
    disease_scores["Heart Disease"] += 25
    disease_scores["Type 2 Diabetes"] += 30

if exercise < 2:
    disease_scores["Heart Disease"] += 20

if sleep < 6:
    disease_scores["Hypertension"] += 20
    disease_scores["Depression/Anxiety"] += 25

if stress == "High":
    disease_scores["Depression/Anxiety"] += 30
    disease_scores["Hypertension"] += 15

if smoking == "Yes":
    disease_scores["Lung Disease"] += 40
    disease_scores["Heart Disease"] += 20

if alcohol == "High":
    disease_scores["Liver Disease"] += 40

if family_history == "Yes":
    for d in disease_scores:
        disease_scores[d] += 10

top_disease = max(disease_scores, key=disease_scores.get)
top_score = disease_scores[top_disease]

st.success(f"Highest Risk Disease: {top_disease}")
st.info(f"Estimated likelihood: {top_score}%")


# ---------- Personalized Recommendations ----------
st.subheader("Personalized Health Recommendations")

if bmi > 25:
    st.warning("Maintain BMI between 18.5 – 24.9")

if exercise < 3:
    st.warning("Do at least 30 minutes of exercise daily")

if sleep < 7:
    st.warning("Aim for 7–8 hours of sleep")

if stress == "High":
    st.warning("Try meditation or yoga")

if smoking == "Yes":
    st.warning("Consider quitting smoking")

if alcohol == "High":
    st.warning("Reduce alcohol consumption")


# ---------- Medical Disclaimer ----------
st.caption("This AI tool is for educational purposes only and not a medical diagnosis.")
