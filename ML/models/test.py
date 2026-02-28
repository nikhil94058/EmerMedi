import os
import time
import numpy as np
import librosa
import sounddevice as sd
from tensorflow.keras.models import load_model

# Load the pre-trained model from the specified path
model_path = 'C:/Users/Hp/OneDrive/Desktop/sem4/coding/New folder/Nirbhaya/Nirbhaya/models/Emotion_Voice_Detection_Model.h5'  # Update with your model's path
model = load_model(model_path)

# Function to preprocess and predict real-time input
def predict_audio_class(audio_data):
    X, sr = librosa.load(audio_data, sr=16000)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sr, n_mfcc=40).T, axis=0)
    
    # Reshape to match model input shape (1, 40, 1)
    mfccs = np.expand_dims(mfccs, axis=0)  # Shape (1, 40)
    mfccs = np.expand_dims(mfccs, axis=-1)  # Shape (1, 40, 1)

    # Predict class label
    predictions_probabilities = model.predict(mfccs)
    prediction = np.argmax(predictions_probabilities, axis=1)

    return prediction[0]

# Function to record audio for a specified duration
def record_audio(duration=3):
    print(f"Recording for {duration} seconds...")
    recorded_audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
    sd.wait()  # Wait until the recording is finished
    print("Recording complete.")
    return recorded_audio.flatten()  # Flatten to 1D array

# Continuous loop for real-time predictions
try:
    while True:
        # Record audio (5 seconds duration)
        audio_data = record_audio(duration=5)

        # Print the audio data shape for debugging
        print(f"Recorded audio data shape: {audio_data.shape}")

        # Predict the class of the recorded audio
        predicted_class = predict_audio_class(audio_data)

        # Print the predicted class
        print("Predicted class for recorded audio:", predicted_class)

        # Optional: Add a delay before the next recording
        print("Waiting before the next recording...")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping the real-time predictions.")
