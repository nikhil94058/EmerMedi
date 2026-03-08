
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import json
from LLM_brain.llm import llm  
from Preprocesser.preprocess_input_json import preprocess_data # Assuming the class name from previous step

def hospital_finder(triage_json_data: dict):
    """
    Takes the raw Triage JSON, simplifies it using the preprocessor,
    and asks the LLM to recommend the top 5 most suitable hospital types/names.
    """
    print("data receiver in hf")
    
    # 2. Define the prompt for hospital selection
    # Note: Since the LLM doesn't have your GPS, we ask it to find the BEST 
    # types of facilities based on the specific injuries detected.
    prompt = """
    You are a Strategic Medical Dispatcher. Based on the patient's emergency incident data and the provided list of REAL nearby medical facilities, identify the top 5 most suitable hospitals for this specific emergency.

    STRICT RULES:
    1. DO NOT invent or hallucinate hospital names or locations.
    2. You MUST ONLY select hospitals from the list of available facilities provided in the input data context.
    3. Match the patient's critical medical needs (e.g., Cardiac, Trauma, Stroke) with the hospital's capabilities.
    4. Ensure exact GPS coordinates (latitude/longitude) are copied perfectly from the input data so they can be plotted on a map.

    Return ONLY a JSON object with a 'recommended_hospitals' array. 
    Each object must follow this exact backend-friendly schema:
    {
      "facility_name": "Exact Name of the hospital from the provided list",
      "latitude": 0.000000, 
      "longitude": 0.000000,
      "address": "Exact address of the hospital from the provided list",
      "category": "Standardized Category (e.g., TRAUMA_CENTER, CARDIAC_CARE)",
      "suitability_score": 0-100,
      "priority_level": "CRITICAL | HIGH | MEDIUM",
      "required_capabilities":["List", "of", "needed", "services", "e.g.", "ICU", "Cath Lab"],
      "justification": "Clinical reasoning for why this specific hospital is the best fit",
      "dispatch_notes": "Logistical notes (e.g., 'Use sirens, prep for Code Blue')",
      "eta_impact": "How the distance/location affects this choice",
      "handover_dept": "Which specific hospital department should be alerted"
    }
    """
    
    # 3. Call your modular LLM function
    # It sends the task (prompt) and the context (simplified_data)
    result = llm(prompt, triage_json_data)
    
    return result


# =====================================================================
# TEST BLOCK: Demonstrating the API Input & Output for the Backend Team
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🏥 TESTING HOSPITAL FINDER API FOR BACKEND INTEGRATION")
    print("="*50)

    # 1. Mock Input: What the frontend/triage system will send to this function
    mock_incoming_triage_data = {
        "incident_id": "EMERG-9942",
        "emergency_type": "MEDICAL",
        "patient_status": "CRITICAL",
        "detected_symptoms":["Severe chest pain", "Shortness of breath", "Left arm numbness"],
        "vitals_estimated": {"heart_rate": "130 bpm", "condition": "diaphoretic"},
        "location": "Downtown Business District",
        "emotion_detected": "Highly Distressed/Panicked"
    }

    print("\n[INPUT] Data received from Triage/Preprocessor:")
    print(json.dumps(mock_incoming_triage_data, indent=2))
    
    print("\n[PROCESSING] LLM is determining the best facilities (Please wait...)...\n")

    try:
        # 2. Call the API function
        api_response = hospital_finder(mock_incoming_triage_data)
        
        # 3. Display the exact JSON Output for the backend team
        print("\n" + "="*50)
        print("✅ [FINAL API OUTPUT] Backend will receive this exact JSON:")
        print("="*50)
        print(json.dumps(api_response, indent=4))
        
    except Exception as e:
        print(f"\n❌ [ERROR] LLM Call Failed: {e}")
        print("\n[FALLBACK MOCK OUTPUT] If successful, the backend receives this structure:")
        
        # Fallback dummy data just so the backend team can see the schema even if the API key fails during the test
        dummy_backend_response = {
            "recommended_hospitals":[
                {
                    "facility_name": "City General Cardiology Center",
                    "category": "CARDIAC_CENTER",
                    "suitability_score": 98,
                    "priority_level": "CRITICAL",
                    "required_capabilities": ["Cardiac Cath Lab", "Cardiac ICU", "24/7 Cardiologist"],
                    "justification": "Symptoms heavily indicate an acute myocardial infarction (heart attack) requiring immediate catheterization.",
                    "dispatch_notes": "Use sirens, notify hospital for Code STEMI activation prior to arrival.",
                    "eta_impact": "Closest facility with an active Cath Lab. Traffic is heavy; use bus lanes.",
                    "handover_dept": "Emergency Resuscitation Bay / Cardiology Team"
                }
            ]
        }
        print(json.dumps(dummy_backend_response, indent=4))