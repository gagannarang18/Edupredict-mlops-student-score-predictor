import pickle
from flask import Flask, request, render_template, flash, redirect, url_for
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sec.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Configure secret key for session management
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Validate form data
            reading_score = float(request.form.get('reading_score'))
            writing_score = float(request.form.get('writing_score'))
            
            if not (0 <= reading_score <= 100) or not (0 <= writing_score <= 100):
                flash('Scores must be between 0 and 100', 'error')
                return redirect(url_for('predict_datapoint'))
            
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=reading_score,
                writing_score=writing_score
            )
            
            pred_df = data.get_data_as_data_frame()
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            
            # Format the result nicely
            result_message = f"Predicted Math Score: {results[0]:.1f}"
            flash('Prediction successful!', 'success')
            return render_template('home.html', results=result_message)
            
        except ValueError:
            flash('Please enter valid scores', 'error')
            return redirect(url_for('predict_datapoint'))
        except Exception as e:
            app.logger.error(f"Error during prediction: {str(e)}")
            flash('An error occurred during prediction. Please try again.', 'error')
            return redirect(url_for('predict_datapoint'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)