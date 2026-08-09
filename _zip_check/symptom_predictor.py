import pickle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Disease Predictor", page_icon="🩺", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

:root {
  --bg1: #0a1324;
  --bg2: #13243d;
  --text: #eaf2ff;
  --muted: #9fb2d0;
  --line: #274265;
  --accent: #38bdf8;
}

html, body, [class*="css"] {
  font-family: "Space Grotesk", sans-serif;
  color: var(--text);
}

.stApp {
  background:
    radial-gradient(1000px 500px at 10% -15%, rgba(0,195,255,0.18) 0%, transparent 60%),
    radial-gradient(900px 500px at 95% 0%, rgba(31,122,255,0.18) 0%, transparent 55%),
    linear-gradient(145deg, var(--bg1), var(--bg2));
}

.hero-wrap {
  border: 1px solid rgba(82,126,182,0.45);
  border-radius: 16px;
  padding: 22px 24px 18px;
  margin-bottom: 18px;
  background:
    radial-gradient(600px 160px at 20% 0%, rgba(56,189,248,0.14), transparent 70%),
    linear-gradient(180deg, rgba(11,23,44,0.7), rgba(9,19,37,0.7));
  box-shadow: 0 10px 28px rgba(5,10,22,0.45);
}

.hero-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  background: linear-gradient(90deg, #67e8f9, #38bdf8 40%, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin: 0 0 6px;
}

.hero-sub {
  color: var(--muted);
  font-size: 15px;
  margin: 0;
}

/* Result card */
.result-card {
  border-radius: 16px;
  padding: 22px 24px;
  margin: 18px 0;
  border: 1px solid;
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
  background: rgba(19,36,61,0.8);
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
  background: linear-gradient(90deg, #00b7ff, #1d4ed8);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.65rem 1.4rem;
  font-weight: 700;
  font-size: 15px;
  box-shadow: 0 8px 22px rgba(0,183,255,0.22);
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
  background: rgba(10,23,44,0.92) !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
}

label, .stMarkdown p, p, span { color: var(--text) !important; }

section.main > div.block-container {
  background: rgba(8,17,33,0.45);
  border: 1px solid rgba(159,176,204,0.14);
  border-radius: 18px;
  backdrop-filter: blur(4px);
  padding-top: 2.5rem;
  padding-bottom: 2.5rem;
}

div[data-testid="stAlert"] { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model    = pickle.load(open("symptom_disease_model.pkl", "rb"))
    features = pickle.load(open("symptom_features.pkl", "rb"))
    return model, features

model, FEATURES = load_model()

# Disease info: typical symptoms shown to user + advice
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
        "advice": "Rest, drink fluids, and take over-the-counter cold medicine. Usually resolves in 7–10 days.",
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
        "desc": "Influenza — a contagious respiratory illness caused by influenza viruses.",
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
        "advice": "See a doctor immediately — antibiotics are required. Stay hydrated and rest.",
        "urgency": "high",
    },
    "UTI": {
        "icon": "🚿",
        "desc": "Urinary Tract Infection — bacterial infection of the urinary system.",
        "advice": "Drink plenty of water, see a doctor for antibiotics. Avoid holding urine.",
        "urgency": "medium",
    },
}

URGENCY_COLORS = {"low": "result-low", "medium": "result-medium", "high": "result-high"}
URGENCY_LABELS = {"low": "🟢 Non-Urgent", "medium": "🟡 Seek Care Soon", "high": "🔴 See a Doctor Now"}


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">🩺 Disease Predictor</div>
  <p class="hero-sub">Select your symptoms below and get an instant AI-powered disease prediction.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Select Your Symptoms")
selected = st.multiselect(
    label="Choose all symptoms you currently have:",
    options=FEATURES,
    placeholder="Start typing or scroll to pick symptoms...",
    help="Select as many symptoms as you have for the most accurate result.",
)

col1, col2 = st.columns([3, 1])
with col2:
    clear = st.button("Clear", use_container_width=True)
if clear:
    st.rerun()

predict_clicked = st.button("🔍 Predict Disease", use_container_width=True)

# ── Prediction ─────────────────────────────────────────────────────────────────
if predict_clicked:
    if not selected:
        st.warning("Please select at least one symptom before predicting.")
    else:
        # Build input vector
        input_vec = {feat: 0 for feat in FEATURES}
        for s in selected:
            input_vec[s] = 1
        input_df = pd.DataFrame([input_vec])

        # Predict
        probabilities  = model.predict_proba(input_df)[0]
        classes        = model.classes_
        top_idx        = probabilities.argmax()
        top_disease    = classes[top_idx]
        top_confidence = probabilities[top_idx] * 100

        info    = DISEASE_INFO.get(top_disease, {})
        urgency = info.get("urgency", "medium")
        card_cls = URGENCY_COLORS[urgency]

        # ── Selected symptoms chips
        chips_html = "".join(f'<span class="chip">{s}</span>' for s in selected)
        st.markdown(f'<div class="chip-wrap">{chips_html}</div>', unsafe_allow_html=True)

        # ── Main result card
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

        # ── Other possible diseases
        ranked = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)
        others = [(d, p) for d, p in ranked if d != top_disease and p > 0.01]

        if others:
            st.markdown("#### Other Possibilities")
            rows_html = ""
            for disease, prob in others[:4]:
                pct       = prob * 100
                bar_w     = int(pct)
                d_info    = DISEASE_INFO.get(disease, {})
                icon      = d_info.get("icon", "•")
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

        # ── Disclaimer
        st.caption("⚕️ This tool is for educational purposes only and is **not** a substitute for professional medical diagnosis. Always consult a qualified doctor.")

elif not predict_clicked:
    # Show helper info when nothing has been predicted yet
    st.markdown("""
    <div class="info-box">
      <b>How it works:</b><br>
      1. Select all symptoms you are currently experiencing from the dropdown above.<br>
      2. Click <b>Predict Disease</b>.<br>
      3. The AI model (trained on 10,000 patient records) will instantly identify the most likely disease along with a confidence score and recommended next steps.<br><br>
      <b>Diseases covered:</b> Asthma · COVID-19 · Common Cold · Dengue · Flu · Food Poisoning · Gastritis · Migraine · Typhoid · UTI
    </div>
    """, unsafe_allow_html=True)
