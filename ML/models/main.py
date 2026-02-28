import requests
import os
import json

# --- CONFIGURATION ---
URL = 'http://localhost:5000/predict'
FILE_NAME = 'sound.wav'  # The file you want to test

def send_single_file(file_path):
    """Sends a specific audio file to the API and prints the result."""
    
    # 1. Check if the file actually exists
    if not os.path.exists(file_path):
        print(f"ERROR: The file '{file_path}' was not found in this folder.")
        print("Please make sure your recorded audio is named 'sound.wav'.")
        return

    print(f"--- Sending '{file_path}' to Server ---")

    try:
        # 2. Open the file in binary mode
        with open(file_path, 'rb') as audio_file:
            files = {'file': audio_file}
            
            # 3. Make the API request
            response = requests.post(URL, files=files)

        # 4. Handle the response
        if response.status_code == 200:
            result = response.json()
            
            # Print a clean, readable summary
            print("\n[ANALYSIS RESULT]")
            print(f"Detected Emotion : {result.get('detected_emotion', 'N/A').upper()}")
            print(f"Emergency Status : {result.get('emergency_category', 'N/A').upper()}")
            print("-" * 30)
            
            # Print the full raw JSON for debugging
            print("Raw Response:", json.dumps(result, indent=4))
            
        else:
            print(f"!!! Server Error (Code {response.status_code}): {response.text}")

    except requests.exceptions.ConnectionError:
        print("!!! Connection Failed: Is the server.py running at http://localhost:5000?")
    except Exception as e:
        print(f"!!! An unexpected error occurred: {e}")

if __name__ == "__main__":
    send_single_file(FILE_NAME)