import streamlit as st
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="EduPredict — Math Score Predictor",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for styling and alignment ---
st.markdown("""
    <style>
        /* Base styling and colors adapt to Streamlit themes */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Form container */
        .stForm {
            background-color: var(--secondary-background-color) !important;
            border-radius: 12px;
            padding: 2rem 2.5rem;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            color: var(--text-color) !important;
        }
        /* Input styling */
        .stNumberInput input, .stSelectbox select {
            border-radius: 8px !important;
            color: var(--text-color) !important;
            background-color: var(--secondary-background-color) !important;
            border: 1.5px solid rgba(128,128,128,0.25) !important;
            padding: 0.5rem 0.75rem !important;
            font-size: 1rem !important;
            transition: border-color 0.2s ease;
        }
        .stNumberInput input:focus, .stSelectbox select:focus {
            border-color: var(--primary-color) !important;
            outline: none !important;
            box-shadow: 0 0 8px var(--primary-color);
        }
        /* Button styling */
        .stButton>button {
            background-color: var(--primary-color) !important;
            color: var(--white, #fff) !important;
            border-radius: 10px;
            padding: 0.7rem 1.25rem;
            width: 100%;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        }
        .stButton>button:hover {
            filter: brightness(0.85);
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0,0,0,0.25);
        }
        /* Prediction result card with green highlight for light/dark modes */
        .success-prediction {
            font-size: 1.2rem !important;
            text-align: center;
            padding: 1.5rem 1.8rem;
            background-color: rgba(56, 142, 60, 0.15) !important;  /* subtle green tint */
            border-radius: 14px;
            border-left: 6px solid #388e3c; /* green border */
            margin-top: 1.6rem;
            color: var(--text-color) !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            font-weight: 600;
        }
        .success-prediction strong {
            color: #2e7d32 !important;  /* darker green */
            font-weight: 800;
            font-size: 1.8rem;
        }
        /* Header image and title alignment */
        .header-image {
            text-align: center;
            margin-bottom: 1.8rem;
        }
        .header-image img {
            width: 90px;
            height: auto;
            margin: 0 auto;
            display: block;
        }
        /* Header text */
        .app-title {
            font-weight: 700;
            font-size: 2.4rem;
            margin-bottom: 0.1rem;
            color: var(--primary-color);
        }
        .app-subtitle {
            font-size: 1.15rem;
            color: var(--text-color);
            margin-bottom: 2rem;
            font-weight: 500;
        }
        /* Info box for performance interpretation */
        .stInfo {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            margin-top: 1rem !important;
            border-left: 5px solid var(--primary-color) !important;
            padding-left: 1rem !important;
            color: var(--text-color) !important;
            background-color: var(--secondary-background-color) !important;
            border-radius: 8px;
        }
        /* Form section headers */
        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            color: var(--primary-color);
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 0.25rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
col1, col2 = st.columns([1, 4], gap="small")
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
with col2:
    st.markdown('<div class="app-title">EduPredict</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Math Performance Predictor</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="background-color: var(--secondary-background-color); padding: 1.2rem 1.5rem; border-radius: 12px; margin-bottom: 2.5rem; color: var(--text-color); font-size: 1.05rem;">
        Enter student details below to predict their math score with accuracy and insight.
    </div>
""", unsafe_allow_html=True)

# --- mappings to ensure exact values that match training ---
gender_map = {
    "Male": "male",
    "Female": "female",
    "Other / Prefer not to say": "other"
}

ethnicity_map = {
    "Group A": "group A",
    "Group B": "group B",
    "Group C": "group C",
    "Group D": "group D",
    "Group E": "group E",
}

parental_education_map = {
    "Associate's Degree": "associate's degree",
    "Bachelor's Degree": "bachelor's degree",
    "High School Diploma": "high school",
    "Master's Degree": "master's degree",
    "Some College": "some college",
    "Some High School": "some high school",
}

lunch_map = {
    "Free / Reduced": "free/reduced",
    "Standard": "standard",
}

test_prep_map = {
    "None": "none",
    "Completed": "completed",
}

# --- Form UI (with neat two-column layout) ---
with st.form("predict_form"):
    st.markdown('<div class="section-header">📝 Student Information</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("**Personal Details**")
        gender_label = st.selectbox("Gender", list(gender_map.keys()))
        ethnicity_label = st.selectbox("Ethnicity Group", list(ethnicity_map.keys()))
        parental_label = st.selectbox("Parental Education", list(parental_education_map.keys()))

    with col2:
        st.markdown("**Academic Details**")
        lunch_label = st.selectbox("Lunch Program", list(lunch_map.keys()))
        test_prep_label = st.selectbox("Test Preparation", list(test_prep_map.keys()))
        writing_score = st.number_input("Writing Score (0–100)", min_value=0.0, max_value=100.0, value=70.0, step=1.0, format="%.0f")
        reading_score = st.number_input("Reading Score (0–100)", min_value=0.0, max_value=100.0, value=70.0, step=1.0, format="%.0f")

    submitted = st.form_submit_button("🔮 Predict Math Score")

if submitted:
    gender = gender_map[gender_label]
    race_ethnicity = ethnicity_map[ethnicity_label]
    parental_level_of_education = parental_education_map[parental_label]
    lunch = lunch_map[lunch_label]
    test_preparation_course = test_prep_map[test_prep_label]

    if not (0 <= writing_score <= 100 and 0 <= reading_score <= 100):
        st.error("❌ Scores must be between 0 and 100.")
    else:
        try:
            data = CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score
            )
            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            with st.spinner('🔍 Analyzing student data...'):
                results = predict_pipeline.predict(pred_df)

            st.markdown(f"""
                <div class="success-prediction">
                    🎯 Predicted Math Score: <strong>{results[0]:.1f} / 100</strong>
                </div>
            """, unsafe_allow_html=True)

            performance = ""
            if results[0] >= 85:
                performance = "🌟 Excellent performance!"
            elif results[0] >= 70:
                performance = "👍 Good performance"
            elif results[0] >= 50:
                performance = "📈 Average performance - room for improvement"
            else:
                performance = "⚠️ Below average - consider additional support"

            st.info(f"**Performance Interpretation:** {performance}")

            with st.expander("📊 Show prediction details"):
                st.write("Model Input Data:", pred_df)
                st.write("Raw Prediction Output:", results)

        except Exception as e:
            err_str = str(e)
            st.error("❌ An error occurred during prediction.")
            st.write("**Error message:**", err_str)
            if "Found unknown categories" in err_str or "unknown categories" in err_str:
                st.markdown(
                    """
                    **🔎 Likely cause:** One or more categorical values sent to the trained encoder
                    do not exactly match the categories used during training.
                    
                    **💡 What you can do:**
                    - Use the exact dropdown options in the UI (we map labels to expected values)
                    - Re-train the pipeline with normalized casing/values if you want case-insensitive inputs
                    """
                )

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: var(--text-color); font-size: 0.9rem; margin-top: 1rem;">
        EduPredict Math Score Predictor • Powered by Streamlit • 
        <a href="https://github.com/gagannarang18/mlops-student-score-predictor" target="_blank" style="color: var(--primary-color); text-decoration: none; font-weight: 600;">
            GitHub
        </a>
    </div>
""", unsafe_allow_html=True)
