import pickle
import numpy as np
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load the trained model
try:
    with open('best_model.pkl', 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: best_model.pkl not found. Please ensure the model file is in the project directory.")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def predict_with_model(features):
    """
    Use the loaded pickle model to make predictions
    """
    if model is None:
        # Fallback to rule-based prediction if model is not available
        return predict_blood_pressure_stage_fallback(features)
    
    try:
        # Convert features to numpy array and reshape for single prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction using the loaded model
        prediction = model.predict(features_array)
        
        # Return the first (and only) prediction
        return int(prediction[0])
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        # Fallback to rule-based prediction
        return predict_blood_pressure_stage_fallback(features)

def predict_blood_pressure_stage_fallback(features):
    """
    Fallback rule-based prediction function
    """
    # Extract systolic and diastolic from features (assuming they are at indices 10 and 11)
    systolic = features[10] if len(features) > 10 else 120
    diastolic = features[11] if len(features) > 11 else 80
    
    # Primary classification based on blood pressure readings
    if systolic < 120 and diastolic < 80:
        return 0  # Normal
    elif systolic < 130 and diastolic < 80:
        return 1  # Elevated
    elif (systolic >= 130 and systolic <= 139) or (diastolic >= 80 and diastolic <= 89):
        return 2  # Stage 1 Hypertension
    elif systolic >= 140 or diastolic >= 90:
        return 3  # Stage 2 Hypertension
    elif systolic > 180 or diastolic > 120:
        return 4  # Hypertensive Crisis
    else:
        return 2  # Default to Stage 1 if unclear

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/predict', methods=['GET'])
def predict_get():
    """Handle GET requests to /predict by redirecting to home"""
    return redirect('/')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle POST requests to /predict"""
    try:
        # Get form data and convert to the format expected by the model
        features = [
            int(request.form['age']),
            int(request.form['gender']),
            int(request.form['history']),
            int(request.form['patient']),
            int(request.form['medication']),
            int(request.form['severity']),
            int(request.form['breath_shortness']),
            int(request.form['visual_changes']),
            int(request.form['nose_bleeding']),
            int(request.form['diagnosis_time']),
            int(request.form['systolic']),
            int(request.form['diastolic']),
            int(request.form['diet_control'])
        ]

        # Get prediction using the loaded model
        prediction_num = predict_with_model(features)

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
        print(f"Prediction error: {e}")
        return render_template('index.html', error="An error occurred while processing your request. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)