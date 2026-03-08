


from LLM_brain.llm import llm

def hospital_finder(triage_json_data: dict):
    """
    Takes the raw Triage JSON, simplifies it using the preprocessor,
    and asks the LLM to recommend the top 5 most suitable hospital types/names.
    """
    print("data receiver in hf")
    
    # 2. Define the prompt for hospital selection
    # IMPORTANT: We pass a candidate list from Google Places (or a static stub).
    # The model MUST select only from that list so we return real place_id + lat/lng.
    prompt = """
    You are a Strategic Medical Dispatcher.

    You are given:
    - extracted_features: a structured clinical + logistics summary
    - candidate_hospitals: a list of real nearby hospitals with place_id, address, and lat/lng
    - origin: the incident coordinates (may be null)

    TASK:
    1) Choose the top up to 5 best hospitals from candidate_hospitals for this patient.
    2) You MUST ONLY pick hospitals that appear in candidate_hospitals.
       - Do NOT invent hospital names.
       - facility_name MUST exactly match the candidate's name.
       - place_id, address, and location MUST be copied from the candidate.

    Return ONLY a JSON object with a 'recommended_hospitals' array (0 to 5 items).
    Each item must follow this schema:
    {
      "facility_name": "string (exact match from candidate)",
      "place_id": "string (from candidate)",
      "address": "string (from candidate)",
      "location": { "lat": number, "lng": number },
      "category": "Standardized Category (e.g., TRAUMA_CENTER | CARDIAC_CENTER | GENERAL_HOSPITAL)",
      "suitability_score": 0-100,
      "priority_level": "CRITICAL | HIGH | MEDIUM",
      "required_capabilities": ["ICU", "Blood Bank"],
      "justification": "Clinical reasoning for this selection",
      "dispatch_notes": "Logistical notes (keep short)",
      "handover_dept": "Which specific hospital department should be alerted"
    }

    CRITICAL:
    - If candidate_hospitals is empty, return {"recommended_hospitals": []}.
    """
    
    # 3. Call your modular LLM function
    # It sends the task (prompt) and the context (simplified_data)
    result = llm(prompt, triage_json_data)
    
    return result

