import json
from LLM_brain.llm import llm  # Ensure your llm file is named llm.py
from Preprocesser.preprocess_input_json import EmergencyProcessor # Assuming the class name from previous step

def hospital_finder(triage_json_data: dict):
    """
    Takes the raw Triage JSON, simplifies it using the preprocessor,
    and asks the LLM to recommend the top 5 most suitable hospital types/names.
    """
    
    # 1. Preprocess the complex JSON to get essential emergency details
    # This makes the prompt "cleaner" and cheaper for the LLM
    processor = EmergencyProcessor()
    simplified_data = processor.process_llm_output(triage_json_data)
    
    # 2. Define the prompt for hospital selection
    # Note: Since the LLM doesn't have your GPS, we ask it to find the BEST 
    # types of facilities based on the specific injuries detected.
    prompt = """
    Based on the provided emergency data, identify the 5 best types of medical facilities 
    or specific departments the patient should be taken to. 
    
    If the location was provided, suggest specific hospital names. 
    If not, suggest the 'Type' of facility (e.g., Level 1 Trauma Center, Burn Unit).
    
    Return the response as a JSON list of objects called 'recommended_hospitals'.
    Each object must have:
    - 'name': (Facility name or Type)
    - 'priority': (High/Medium)
    - 'reason': (Why this is suitable for this specific injury)
    - 'estimated_suitability_score': (0-100)
    """
    
    # 3. Call your modular LLM function
    # It sends the task (prompt) and the context (simplified_data)
    result = llm(prompt, simplified_data)
    
    return result

# --- Example of how to call this in your main.py ---
if __name__ == "__main__":
    # This would be the output coming from your Bedrock/Nova model
    sample_input = {
        "emergency_level": "critical",
        "scene_type": "burns",
        "patient_status": {"injury_severity": "life_threatening"},
        "hospital_recommendation": "trauma_center"
    }
    
    final_hospitals = hospital_finder(sample_input)
    print(json.dumps(final_hospitals, indent=2))