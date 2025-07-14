# app.py
from flask import Flask, render_template, request, redirect
import numpy as np

app = Flask(__name__)

def predict_blood_pressure_stage(age, gender, history, patient, medication, severity,
                                breath_shortness, visual_changes, nose_bleeding,
                                diagnosis_time, systolic, diastolic, diet_control):
    """
    Mock prediction function that uses rule-based logic
    to determine blood pressure stage based on standard medical guidelines
    """
    
    # Primary classification based on blood pressure readings
    if systolic < 120 and diastolic < 80:
        base_stage = 0  # Normal
    elif systolic < 130 and diastolic < 80:
        base_stage = 1  # Elevated
    elif (systolic >= 130 and systolic <= 139) or (diastolic >= 80 and diastolic <= 89):
        base_stage = 2  # Stage 1 Hypertension
    elif systolic >= 140 or diastolic >= 90:
        base_stage = 3  # Stage 2 Hypertension
    elif systolic > 180 or diastolic > 120:
        base_stage = 4  # Hypertensive Crisis
    else:
        base_stage = 2  # Default to Stage 1 if unclear
    
    # Adjust based on risk factors
    risk_score = 0
    
    # Age factor
    if age >= 2:  # 51+ years
        risk_score += 1
    
    # History of hypertension
    if history == 1:
        risk_score += 1
    
    # Severe symptoms
    if severity == 2:
        risk_score += 1
    
    # Concerning symptoms
    if breath_shortness == 1:
        risk_score += 1
    if visual_changes == 1:
        risk_score += 1
    if nose_bleeding >= 1:
        risk_score += 1
    
    # Not on medication but should be
    if base_stage >= 2 and medication == 0:
        risk_score += 1
    
    # Adjust stage based on risk factors
    if risk_score >= 3 and base_stage < 4:
        base_stage = min(base_stage + 1, 4)
    elif risk_score >= 2 and base_stage < 3:
        base_stage = min(base_stage + 1, 3)
    
    return base_stage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            age = int(request.form['age'])
            gender = int(request.form['gender'])
            history = int(request.form['history'])
            patient = int(request.form['patient'])
            medication = int(request.form['medication'])
            severity = int(request.form['severity'])
            breath_shortness = int(request.form['breath_shortness'])
            visual_changes = int(request.form['visual_changes'])
            nose_bleeding = int(request.form['nose_bleeding'])
            diagnosis_time = int(request.form['diagnosis_time'])
            systolic = int(request.form['systolic'])
            diastolic = int(request.form['diastolic'])
            diet_control = int(request.form['diet_control'])

            # Get prediction using rule-based system
            prediction_num = predict_blood_pressure_stage(
                age, gender, history, patient, medication, severity,
                breath_shortness, visual_changes, nose_bleeding,
                diagnosis_time, systolic, diastolic, diet_control
            )

            # Map numeric prediction to readable label
            stage_map = {
                0: "Normal",
                1: "Elevated",
                2: "Hypertension Stage 1",
                3: "Hypertension Stage 2",
                4: "Hypertensive Crisis"
            }

            result = stage_map.get(prediction_num, "Unknown")

            return render_template('result.html', prediction=result)
            
        except ValueError as e:
            return render_template('index.html', error="Please fill in all fields with valid values.")
        except KeyError as e:
            return render_template('index.html', error=f"Missing required field: {e}")
        except Exception as e:
            return render_template('index.html', error="An error occurred while processing your request. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)