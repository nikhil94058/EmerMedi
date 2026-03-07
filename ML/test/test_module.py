import requests
import json
import os
import sys

# --- CONFIGURATION ---
# Ensure your main.py is running on this port
URL = "http://127.0.0.1:5000/find-hospitals"

# This looks for the JSON file in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, "test.json")

def test_hospital_finder():
    print("\n" + "="*50)
    print("🏥 EMERMEDI: HOSPITAL FINDER API TEST")
    print("="*50)

    # 1. Check if the JSON file exists, if not, create a sample one
    if not os.path.exists(JSON_FILE):
        print(f"⚠️  File not found: {JSON_FILE}")
        print("📝 Creating a sample emergency JSON for testing...")
        sample_data = {
            "emergency_level": "critical",
            "urgency_score": 95,
            "scene_type": "traffic_accident",
            "hospital_recommendation": "trauma_center",
            "patient_status": {
                "injury_severity": "life_threatening",
                "consciousness_level": "unconscious"
            },
            "immediate_actions": ["Stop bleeding", "Call 108"]
        }
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=4)
        print(f"✅ Created: {JSON_FILE}")

    # 2. Load the JSON data (Fixing the Unicode/Encoding Error)
    try:
        print(f"📖 Reading input: {os.path.basename(JSON_FILE)}")
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except UnicodeDecodeError:
        print("❌ ERROR: Encoding mismatch. Ensure the file is saved as UTF-8.")
        return
    except json.JSONDecodeError:
        print("❌ ERROR: The file is not a valid JSON. Check for missing commas or brackets.")
        return
    except Exception as e:
        print(f"❌ ERROR: Could not read file: {e}")
        return

    # 3. Send the POST request to the Flask Server
    print(f"📡 Sending request to: {URL}...")
    try:
        response = requests.post(URL, json=payload, timeout=30)
        
        # 4. Process the Response
        if response.status_code == 200:
            result = response.json()
            print("\n" + "✅" + " SUCCESS: Recommendations Received " + "✅")
            print("-" * 50)
            
            # Navigate the JSON structure based on your Blueprint output
            # We check both possible keys 'hospital_list' or 'recommendations'
            hospitals = result.get('hospital_list', {}).get('recommendations', [])
            
            if not hospitals:
                # Fallback in case your LLM returned a different structure
                hospitals = result.get('recommendations', [])

            if hospitals:
                for idx, h in enumerate(hospitals, 1):
                    name = h.get('name', 'N/A')
                    priority = h.get('priority', 'N/A')
                    reason = h.get('reason', 'No reason provided')
                    score = h.get('estimated_suitability_score', '??')
                    
                    print(f"{idx}. [{priority.upper()}] {name}")
                    print(f"   Suitability: {score}/100")
                    print(f"   Reason: {reason}\n")
            else:
                print("⚠️  The API returned success, but the hospital list was empty.")
                print("Full Response:", json.dumps(result, indent=2))

        else:
            print(f"❌ API ERROR: Server returned Status Code {response.status_code}")
            print(f"Response Body: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR: Could not reach the Flask server.")
        print("👉 Make sure 'main.py' is running at http://127.0.0.1:5000")
    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT ERROR: The LLM took too long to respond.")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

    print("="*50)
    print("🏁 TEST ENDED")
    print("="*50 + "\n")

if __name__ == "__main__":
    test_hospital_finder()