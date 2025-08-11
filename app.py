# app.py
import streamlit as st
from sec.pipeline.predict_pipeline import CustomData, PredictPipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="EduPredict — Math Score Predictor",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stForm {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4a6fa5;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #3a5a8a;
            transform: translateY(-2px);
        }
        .stNumberInput input, .stSelectbox select {
            border-radius: 8px !important;
        }
        .success-prediction {
            font-size: 1.5rem !important;
            text-align: center;
            padding: 1.5rem;
            background-color: #e8f5e9;
            border-radius: 10px;
            border-left: 5px solid #4caf50;
            margin-top: 1rem;
        }
        .header-image {
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .header-image img {
            width: 100px;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
with col2:
    st.title("EduPredict")
    st.markdown("**Math Performance Predictor**")

st.markdown("""
    <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        Enter student details below to predict their math score. The model expects exact category strings 
        as provided in the dropdown menus.
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

# --- Form UI (two-column feel) ---
with st.form("predict_form"):
    st.subheader("📝 Student Information")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Personal Details**")
        gender_label = st.selectbox("Gender", list(gender_map.keys()))
        ethnicity_label = st.selectbox("Ethnicity Group", list(ethnicity_map.keys()))
        parental_label = st.selectbox("Parental Education", list(parental_education_map.keys()))

    with col2:
        st.markdown("**Academic Details**")
        lunch_label = st.selectbox("Lunch Program", list(lunch_map.keys()))
        test_prep_label = st.selectbox("Test Preparation", list(test_prep_map.keys()))
        writing_score = st.number_input("Writing Score (0–100)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
        reading_score = st.number_input("Reading Score (0–100)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)

    submitted = st.form_submit_button("🔮 Predict Math Score")

if submitted:
    # map displayed labels to the exact values expected by the pipeline
    gender = gender_map[gender_label]
    race_ethnicity = ethnicity_map[ethnicity_label]
    parental_level_of_education = parental_education_map[parental_label]
    lunch = lunch_map[lunch_label]
    test_preparation_course = test_prep_map[test_prep_label]

    # Basic sanity check
    if not (0 <= writing_score <= 100 and 0 <= reading_score <= 100):
        st.error("❌ Scores must be between 0 and 100.")
    else:
        try:
            # Build input object exactly as your Flask app did
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
            
            # Add a spinner for better UX
            with st.spinner('🔍 Analyzing student data...'):
                results = predict_pipeline.predict(pred_df)
                
                st.markdown(f"""
                    <div class="success-prediction">
                        🎯 Predicted Math Score: <strong>{results[0]:.1f} / 100</strong>
                    </div>
                """, unsafe_allow_html=True)
                
                # Performance interpretation
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

                # optional: show raw output for debugging
                with st.expander("📊 Show prediction details"):
                    st.write("Model Input Data:", pred_df)
                    st.write("Raw Prediction Output:", results)

        except Exception as e:
            # If something goes wrong, try to surface helpful info
            err_str = str(e)
            st.error("❌ An error occurred during prediction.")
            st.write("**Error message:**", err_str)

            # If it's the common unknown-category message, show guidance
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
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        EduPredict Math Score Predictor • Powered by Streamlit • 
        <a href="https://github.com/yourusername/edupredict" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)