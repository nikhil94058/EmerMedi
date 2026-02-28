import sounddevice as sd
import numpy as np
import wave
import requests
import time
import os

# --- SETTINGS ---
URL = 'http://localhost:5000/predict'
DURATION = 5  # Seconds to record
SAMPLE_RATE = 16000 # Matches server expectation
FILENAME = 'temp_audio.wav'

def record_audio(duration=5, filename=FILENAME):
    """Records audio from the microphone and saves to a WAV file."""
    print(f"\n[LISTENING] Recording for {duration} seconds...")
    
    # Record audio
    recorded_audio = sd.rec(int(duration * SAMPLE_RATE), 
                            samplerate=SAMPLE_RATE, 
                            channels=1, 
                            dtype='float32')
    sd.wait()  # Wait until recording is finished
    
    # Save as 16-bit PCM WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        # Convert float32 to int16
        wf.writeframes((recorded_audio * 32767).astype(np.int16))
    
    return filename

def analyze_audio(filename):
    """Sends the audio file to the Flask server and returns the analysis."""
    try:
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(URL, files=files)
            
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Server returned error {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to server. Is it running?"}

def display_result(data):
    """Prints the categorization results in a clear format."""
    if "error" in data:
        print(f"!!! {data['error']}")
        return

    emotion = data.get('detected_emotion', 'Unknown').upper()
    category = data.get('emergency_category', 'Neutral').upper()

    # Visual formatting for the terminal
    print("-" * 40)
    print(f"SOUND DETECTED : {emotion}")
    print(f"STATUS         : {category}")
    
    if category == "EMERGENCY":
        print("ALERT: High-risk situation detected!")
    elif category == "NON-EMERGENCY":
        print("INFO: Normal activity detected.")
    else:
        print("INFO: Environment is quiet/neutral.")
    print("-" * 40)

if __name__ == '__main__':
    print("--- Emergency Sound Detection System Started ---")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            # 1. Record
            audio_path = record_audio(duration=DURATION)
            
            # 2. Analyze
            result = analyze_audio(audio_path)
            
            # 3. Print Results
            display_result(result)

            # 4. Brief pause before next loop
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n[STOPPED] Monitoring finished.")
        # Cleanup temporary file
        if os.path.exists(FILENAME):
            os.remove(FILENAME)