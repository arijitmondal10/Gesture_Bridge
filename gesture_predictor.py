import pickle
import numpy as np

# Load trained model
model = pickle.load(open("models/gesture_model.pkl", "rb"))

def predict_gesture(landmarks):

    landmarks = np.array(landmarks).reshape(1, -1)

    prediction = model.predict(landmarks)

    return prediction[0]