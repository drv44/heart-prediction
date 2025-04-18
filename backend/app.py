from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import os

HERE = os.path.dirname(__file__)
MODEL_PATH = os.path.abspath(os.path.join(HERE, '..', 'models', 'ensemble.pkl'))
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained VotingClassifier (ensemble model)
voting_clf = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return "API running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)

    # Make prediction using the ensemble model
    prediction = voting_clf.predict(features)
    risk = 'High' if prediction[0] == 1 else 'Low'

    return jsonify({'risk': risk})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
