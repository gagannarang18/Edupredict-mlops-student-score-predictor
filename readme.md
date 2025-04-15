# 🚀 Deployment
API Endpoint: http://127.0.0.1:5000/predictdata
Run: python application.py

# 🏆 Model Performance (R² Scores)
Ridge Regression:       0.8806
Linear Regression:      0.8803  
CatBoost Regressor:     0.8516
Random Forest:          0.8484
AdaBoost:               0.8410
XGBoost:                0.8278
Lasso:                  0.8253
K-Neighbors:            0.7838
Decision Tree:          0.7545

# ⚙️ Installation
1. git clone https://github.com/gagannarang18/mlops-student-score-predictor.git
2. cd student-score-predictor
3. pip install -r requirements.txt
4. python application.py

# 📡 API Example
curl -X POST http://127.0.0.1:5000/predictdata \
-H "Content-Type: application/json" \
-d '{
    "gender": "female",
    "ethnicity": "group C",
    "parental_level_of_education": "bachelor's degree",
    "lunch": "standard",
    "test_preparation_course": "none",
    "writing_score": 74,
    "reading_score": 79
}'

# 🛠️ Tech Stack
- Python 3.8+
- Pandas/Numpy (Data)
- Scikit-learn/CatBoost/XGBoost (ML)
- Flask (API)
-HTML,CSS(UI)