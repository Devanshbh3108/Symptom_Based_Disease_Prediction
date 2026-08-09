import pickle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Disease & Health Risk Predictor", page_icon="🩺", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

:root {
  --bg1: #07101f;
  --bg2: #111f39;
  --bg3: #1f1438;
  --text: #eef4ff;
  --muted: #9fb1d4;
  --line: #2d456f;
  --accent: #4fd1ff;
  --accent2: #f7b24f;
}

html, body, [class*="css"] {
  font-family: "Space Grotesk", sans-serif;
  color: var(--text);
}

.stApp {
  background:
    radial-gradient(1100px 600px at 8% -18%, rgba(79,209,255,0.22) 0%, transparent 60%),
    radial-gradient(900px 520px at 97% 0%, rgba(247,178,79,0.16) 0%, transparent 56%),
    radial-gradient(900px 520px at 78% 112%, rgba(167,139,250,0.14) 0%, transparent 60%),
    linear-gradient(145deg, var(--bg1), var(--bg2) 48%, var(--bg3));
}

.hero-wrap {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(116,146,198,0.45);
  border-radius: 22px;
  padding: 30px 30px 22px;
  margin-bottom: 20px;
  background:
    radial-gradient(720px 180px at 16% 0%, rgba(79,209,255,0.24), transparent 70%),
    radial-gradient(620px 180px at 90% 0%, rgba(247,178,79,0.16), transparent 72%),
    linear-gradient(180deg, rgba(11,23,44,0.78), rgba(9,19,37,0.84));
  box-shadow: 0 18px 42px rgba(5,10,22,0.52);
}

.hero-wrap::after {
  content: "";
  position: absolute;
  width: 340px;
  height: 340px;
  right: -90px;
  top: -150px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(79,209,255,0.16), rgba(79,209,255,0));
  pointer-events: none;
}

.hero-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  letter-spacing: 0.2px;
  background: linear-gradient(96deg, #7be7ff, #4fd1ff 38%, #ffc26e 82%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin: 0 0 6px;
}

.hero-sub {
  color: var(--muted);
  font-size: 15.5px;
  margin: 0;
  max-width: 780px;
}

.hero-badge {
  display: inline-block;
  margin-bottom: 12px;
  border: 1px solid rgba(79,209,255,0.34);
  background: rgba(79,209,255,0.11);
  color: #c8f2ff;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .4px;
}

.hero-kpis {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 16px;
}

.kpi-chip {
  border-radius: 12px;
  border: 1px solid rgba(159,176,204,0.24);
  background: rgba(11, 24, 45, 0.66);
  padding: 8px 12px;
  color: var(--muted);
  font-size: 13px;
}

.kpi-chip b {
  color: var(--text);
}

/* Result card */
.result-card {
  border-radius: 20px;
  padding: 24px 26px;
  margin: 18px 0;
  border: 1px solid;
  box-shadow: 0 16px 34px rgba(2,8,20,0.36);
}
.result-high {
  background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(220,38,38,0.08));
  border-color: rgba(239,68,68,0.5);
}
.result-medium {
  background: linear-gradient(135deg, rgba(251,146,60,0.15), rgba(249,115,22,0.08));
  border-color: rgba(249,115,22,0.5);
}
.result-low {
  background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(22,163,74,0.08));
  border-color: rgba(34,197,94,0.5);
}
.result-disease {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
}
.result-conf {
  font-size: 14px;
  color: var(--muted);
}

/* Confidence bar */
.conf-bar-wrap {
  background: rgba(255,255,255,0.07);
  border-radius: 999px;
  height: 10px;
  margin: 6px 0 14px;
  overflow: hidden;
}
.conf-bar-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #38bdf8, #a78bfa);
  transition: width 0.6s ease;
}

/* Alt disease rows */
.alt-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid var(--line);
  font-size: 14px;
  color: var(--muted);
}
.alt-row:last-child { border-bottom: none; }
.alt-name { flex: 1; color: var(--text); }
.alt-pct  { min-width: 44px; text-align: right; }

/* Symptom chips */
.chip-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 8px 0 18px;
}
.chip {
  background: rgba(56,189,248,0.12);
  border: 1px solid rgba(56,189,248,0.35);
  border-radius: 999px;
  padding: 4px 14px;
  font-size: 13px;
  color: var(--accent);
}

/* Symptom info box */
.info-box {
  background: rgba(17,34,59,0.82);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 16px 18px;
  margin: 14px 0;
  font-size: 14px;
  color: var(--muted);
  line-height: 1.6;
}
.info-box b { color: var(--text); }

/* Buttons */
.stButton > button {
  background: linear-gradient(96deg, #00b7ff, #2e6cff 55%, #7f5fff);
  color: white;
  border: none;
  border-radius: 14px;
  padding: 0.65rem 1.4rem;
  font-weight: 700;
  font-size: 15px;
  box-shadow: 0 10px 26px rgba(0,183,255,0.24);
  transition: transform .15s, box-shadow .15s, filter .15s;
  width: 100%;
}
.stButton > button:hover {
  transform: translateY(-1px);
  filter: brightness(1.06);
  box-shadow: 0 14px 30px rgba(124,58,237,0.3);
}

/* Multiselect tags */
span[data-baseweb="tag"] {
  background: rgba(56,189,248,0.18) !important;
  border: 1px solid rgba(56,189,248,0.4) !important;
  border-radius: 999px !important;
}

div[data-baseweb="select"] > div {
  background: rgba(8,20,39,0.92) !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stSlider"] {
  background: rgba(8,20,39,0.72) !important;
  border-radius: 10px !important;
}

label, .stMarkdown p, p, span { color: var(--text) !important; }

section.main > div.block-container {
  background: rgba(8,17,33,0.50);
  border: 1px solid rgba(159,176,204,0.14);
  border-radius: 22px;
  backdrop-filter: blur(6px);
  padding-top: 2rem;
  padding-bottom: 2.5rem;
  max-width: 1200px;
}

div[data-testid="stAlert"] { border-radius: 12px; }

.section-card {
  border-radius: 16px;
  border: 1px solid rgba(79,209,255,0.24);
  background: linear-gradient(180deg, rgba(10,21,40,0.70), rgba(9,18,34,0.70));
  padding: 14px 16px;
  margin-bottom: 14px;
  color: var(--muted);
  font-size: 14px;
}

.section-card b {
  color: var(--text);
}

button[data-baseweb="tab"] {
  border-radius: 12px !important;
  border: 1px solid rgba(124,146,185,0.26) !important;
  background: rgba(8,20,39,0.5) !important;
  color: var(--muted) !important;
  margin-right: 8px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
  background: linear-gradient(95deg, rgba(79,209,255,0.20), rgba(247,178,79,0.16)) !important;
  color: var(--text) !important;
  border-color: rgba(79,209,255,0.48) !important;
}

@media (max-width: 768px) {
  .hero-wrap {
    padding: 22px 18px 16px;
  }
  section.main > div.block-container {
    padding-left: 0.9rem;
    padding-right: 0.9rem;
  }
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_disease_model():
    model = pickle.load(open("symptom_disease_model.pkl", "rb"))
    features = pickle.load(open("symptom_features.pkl", "rb"))
    return model, features


@st.cache_resource
def load_health_model():
    model = pickle.load(open("Health_risk_predictor.pkl", "rb"))
    encoders = pickle.load(open("label_encoders.pkl", "rb"))
    return model, encoders


disease_model, FEATURES = load_disease_model()
health_model, encoders = load_health_model()


DISEASE_INFO = {
    "Asthma": {
        "icon": "🫁",
        "desc": "A condition where airways narrow and swell, causing breathing difficulty.",
        "advice": "Use prescribed inhaler, avoid triggers (dust, smoke, pollen), and see a doctor if symptoms worsen.",
        "urgency": "medium",
    },
    "COVID-19": {
        "icon": "🦠",
        "desc": "A viral respiratory illness caused by SARS-CoV-2.",
        "advice": "Isolate immediately, rest, stay hydrated. Seek emergency care for severe breathing difficulty.",
        "urgency": "high",
    },
    "Common Cold": {
        "icon": "🤧",
        "desc": "A mild viral infection of the upper respiratory tract.",
        "advice": "Rest, drink fluids, and take over-the-counter cold medicine. Usually resolves in 7-10 days.",
        "urgency": "low",
    },
    "Dengue": {
        "icon": "🦟",
        "desc": "A mosquito-borne viral disease with high fever and severe body pain.",
        "advice": "See a doctor immediately. Stay hydrated, avoid aspirin/ibuprofen, and rest.",
        "urgency": "high",
    },
    "Flu": {
        "icon": "🌡️",
        "desc": "Influenza, a contagious respiratory illness caused by influenza viruses.",
        "advice": "Rest, stay hydrated, antiviral medications within 48h can help. Avoid contact with others.",
        "urgency": "medium",
    },
    "Food Poisoning": {
        "icon": "🤢",
        "desc": "Illness caused by consuming contaminated food or water.",
        "advice": "Stay hydrated with ORS/fluids. Seek medical attention if symptoms last more than 2 days.",
        "urgency": "medium",
    },
    "Gastritis": {
        "icon": "🫃",
        "desc": "Inflammation of the stomach lining causing abdominal pain and nausea.",
        "advice": "Avoid spicy/acidic foods, eat smaller meals. See a doctor for prescribed antacids.",
        "urgency": "low",
    },
    "Migraine": {
        "icon": "🧠",
        "desc": "Intense recurrent headaches, often with nausea and light sensitivity.",
        "advice": "Rest in a dark, quiet room. Pain relievers may help. See a neurologist for recurring attacks.",
        "urgency": "low",
    },
    "Typhoid": {
        "icon": "🧫",
        "desc": "A bacterial infection caused by Salmonella typhi, spread through contaminated food/water.",
        "advice": "See a doctor immediately, antibiotics are required. Stay hydrated and rest.",
        "urgency": "high",
    },
    "UTI": {
        "icon": "🚿",
        "desc": "Urinary Tract Infection, bacterial infection of the urinary system.",
        "advice": "Drink plenty of water, see a doctor for antibiotics. Avoid holding urine.",
        "urgency": "medium",
    },
}

URGENCY_COLORS = {"low": "result-low", "medium": "result-medium", "high": "result-high"}
URGENCY_LABELS = {"low": "🟢 Non-Urgent", "medium": "🟡 Seek Care Soon", "high": "🔴 See a Doctor Now"}


st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">AI HEALTH ASSISTANT</div>
  <div class="hero-title">🩺 Health Intelligence Suite</div>
  <p class="hero-sub">Use disease prediction from symptoms and lifestyle-based health risk prediction in one place.</p>
  <div class="hero-kpis">
    <div class="kpi-chip"><b>2-in-1</b> Disease + Risk Analysis</div>
    <div class="kpi-chip"><b>Real-Time</b> Confidence Scores</div>
    <div class="kpi-chip"><b>Guided</b> Next-Step Suggestions</div>
  </div>
</div>
""", unsafe_allow_html=True)


tab1, tab2 = st.tabs(["Disease Predictor", "Health Risk Predictor"])


with tab1:
    st.markdown("<div class='section-card'><b>Symptom Intelligence:</b> Select your symptoms and get a ranked disease prediction with urgency guidance.</div>", unsafe_allow_html=True)
    st.markdown("### Select Your Symptoms")
    selected = st.multiselect(
        label="Choose all symptoms you currently have:",
        options=FEATURES,
        placeholder="Start typing or scroll to pick symptoms...",
        help="Select as many symptoms as you have for the most accurate result.",
    )

    _, col2 = st.columns([3, 1])
    with col2:
        clear = st.button("Clear", use_container_width=True, key="clear_symptoms")
    if clear:
        st.rerun()

    predict_clicked = st.button("🔍 Predict Disease", use_container_width=True, key="predict_disease")

    if predict_clicked:
        if not selected:
            st.warning("Please select at least one symptom before predicting.")
        else:
            input_vec = {feat: 0 for feat in FEATURES}
            for s in selected:
                input_vec[s] = 1
            input_df = pd.DataFrame([input_vec])

            probabilities = disease_model.predict_proba(input_df)[0]
            classes = disease_model.classes_
            top_idx = probabilities.argmax()
            top_disease = classes[top_idx]
            top_confidence = probabilities[top_idx] * 100

            info = DISEASE_INFO.get(top_disease, {})
            urgency = info.get("urgency", "medium")
            card_cls = URGENCY_COLORS[urgency]

            chips_html = "".join(f'<span class="chip">{s}</span>' for s in selected)
            st.markdown(f'<div class="chip-wrap">{chips_html}</div>', unsafe_allow_html=True)

            bar_width = min(int(top_confidence), 100)
            st.markdown(f"""
            <div class="result-card {card_cls}">
              <div style="font-size:2.4rem; margin-bottom:4px;">{info.get("icon","🩺")}</div>
              <div class="result-disease">{top_disease}</div>
              <div class="result-conf">Confidence: {top_confidence:.1f}%  ·  {URGENCY_LABELS[urgency]}</div>
              <div class="conf-bar-wrap">
                <div class="conf-bar-fill" style="width:{bar_width}%"></div>
              </div>
              <div class="info-box">
                <b>About:</b> {info.get("desc", "")}<br><br>
                <b>What to do:</b> {info.get("advice", "")}
              </div>
            </div>
            """, unsafe_allow_html=True)

            ranked = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)
            others = [(d, p) for d, p in ranked if d != top_disease and p > 0.01]

            if others:
                st.markdown("#### Other Possibilities")
                rows_html = ""
                for disease, prob in others[:4]:
                    pct = prob * 100
                    bar_w = int(pct)
                    d_info = DISEASE_INFO.get(disease, {})
                    icon = d_info.get("icon", "•")
                    rows_html += f"""
                    <div class="alt-row">
                      <span style="font-size:1.2rem">{icon}</span>
                      <span class="alt-name">{disease}</span>
                      <div class="conf-bar-wrap" style="flex:2; margin:0;">
                        <div class="conf-bar-fill" style="width:{bar_w}%; background: linear-gradient(90deg,#64748b,#94a3b8);"></div>
                      </div>
                      <span class="alt-pct">{pct:.1f}%</span>
                    </div>"""
                st.markdown(f'<div class="info-box" style="padding:12px 16px;">{rows_html}</div>', unsafe_allow_html=True)

            st.caption("⚕️ This tool is for educational purposes only and is not a substitute for professional medical diagnosis. Always consult a qualified doctor.")

    else:
        st.markdown("""
        <div class="info-box">
          <b>How it works:</b><br>
          1. Select all symptoms you are currently experiencing from the dropdown above.<br>
          2. Click <b>Predict Disease</b>.<br>
          3. The AI model will identify the most likely disease with confidence and suggested next steps.<br><br>
          <b>Diseases covered:</b> Asthma · COVID-19 · Common Cold · Dengue · Flu · Food Poisoning · Gastritis · Migraine · Typhoid · UTI
        </div>
        """, unsafe_allow_html=True)


with tab2:
    st.markdown("<div class='section-card'><b>Lifestyle Risk Profiler:</b> Enter daily habits and body metrics to estimate your overall health risk band.</div>", unsafe_allow_html=True)
    st.markdown("### Lifestyle-Based Health Risk")

    c1, c2 = st.columns(2)
    with c1:
        age = st.slider("Age", 18, 80, 25)
        diet = st.selectbox("Diet Quality", ["Poor", "Average", "Good"])
        exercise_days = st.slider("Exercise Days / Week", 0, 7, 3)
        sleep_hours = st.slider("Sleep Hours / Day", 3, 12, 7)
        stress = st.selectbox("Stress Level", ["No", "Low", "Medium", "High"])

    with c2:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=250.0, value=65.0, step=0.5)
        height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=170.0, step=0.5)
        smoking = st.selectbox("Smoking", ["No", "Yes"])
        drinks_alcohol = st.selectbox("Do you drink alcohol?", ["No", "Yes"])
        if drinks_alcohol == "Yes":
            alcohol = st.selectbox("Alcohol Consumption", ["Low", "Medium", "High"])
        else:
            alcohol = "Low"

    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    st.markdown(f"<div class='info-box'><b>Calculated BMI:</b> {bmi:.2f}</div>", unsafe_allow_html=True)

    predict_risk = st.button("🧪 Predict Health Risk", use_container_width=True, key="predict_risk")

    if predict_risk:
        stress_for_model = "Low" if stress == "No" else stress
        risk_input = pd.DataFrame([{
            "age": age,
            "diet": encoders["diet"].transform([diet])[0],
            "exercise_days": exercise_days,
            "sleep_hours": sleep_hours,
            "stress": encoders["stress"].transform([stress_for_model])[0],
            "bmi": bmi,
            "smoking": encoders["smoking"].transform([smoking])[0],
            "alcohol": encoders["alcohol"].transform([alcohol])[0],
            "family_history": encoders["family_history"].transform(["No"])[0],
        }])

        pred = health_model.predict(risk_input)[0]
        probs = health_model.predict_proba(risk_input)[0]

        risk_label = encoders["risk_level"].inverse_transform([pred])[0]
        risk_key = str(risk_label).lower()
        risk_card = URGENCY_COLORS.get(risk_key, "result-medium")

        class_labels = [encoders["risk_level"].inverse_transform([c])[0] for c in health_model.classes_]
        class_map = {label: float(prob) for label, prob in zip(class_labels, probs)}

        st.markdown(f"""
        <div class="result-card {risk_card}">
          <div class="result-disease">Overall Risk: {risk_label}</div>
          <div class="result-conf">Predicted from lifestyle and history inputs.</div>
          <div class="info-box">
            <b>Summary:</b> This estimate is based on age, diet, activity, sleep, stress, BMI, smoking, and alcohol use.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Risk Probabilities")
        for label in ["Low", "Medium", "High"]:
            pct = class_map.get(label, 0.0) * 100
            st.markdown(f"<div class='alt-row'><span class='alt-name'>{label}</span><span class='alt-pct'>{pct:.1f}%</span></div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='conf-bar-wrap' style='margin-top:-6px;'><div class='conf-bar-fill' style='width:{int(pct)}%'></div></div>",
                unsafe_allow_html=True,
            )

        st.caption("⚕️ This is an educational estimate and not a medical diagnosis. For medical advice, consult a qualified doctor.")
    else:
        st.markdown(
            """
            <div class="info-box">
              <b>How it works:</b><br>
              Enter your lifestyle and body metrics, then click <b>Predict Health Risk</b> to estimate low/medium/high health risk.
            </div>
            """,
            unsafe_allow_html=True,
        )
