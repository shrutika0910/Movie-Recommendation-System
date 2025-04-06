from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    return "Model is live!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run()
