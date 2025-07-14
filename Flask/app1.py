# app1.py
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the saved model
model = joblib.load('best_model.pkl')

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

            # Reshape input for prediction
            input_data = np.array([[age, gender, history, patient, medication, severity,
                                    breath_shortness, visual_changes, nose_bleeding,
                                    diagnosis_time, systolic, diastolic, diet_control]])

            prediction = model.predict(input_data)[0]

            # Map numeric prediction to readable label
            stage_map = {
                0: "Normal",
                1: "Elevated",
                2: "Hypertension Stage 1",
                3: "Hypertension Stage 2",
                4: "Hypertensive Crisis"
            }

            result = stage_map.get(int(prediction), "Unknown")

            return render_template('result.html', prediction=result)
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)