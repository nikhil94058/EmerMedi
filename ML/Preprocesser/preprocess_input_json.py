from LLM_brain.llm import llm
import json

def preprocess_data(json_input: dict):
    """
    Acts as a DB sorter to scrape only hospital-relevant features 
    from the raw triage analysis.
    """
    
    # Refined prompt to ensure the LLM behaves like a precise data scraper
    prompt = """
    You are a Medical Database Sorter. Your job is to scrape the provided JSON 
    and extract ONLY the features required for a Hospital Finder service.
    
    Extract and return a JSON object with these specific keys:
    1. 'severity_level': (How critical is the situation?)
    2. 'required_facility_type': (Trauma Center, Burn Unit, Cardiac ER, etc.)
    3. 'patient_condition': (The primary injury/disease like 'Head Trauma' or 'Cardiac Arrest')
    4. 'equipment_needed': (e.g., Ventilator, MRI, Operating Room)
    5. 'location_context': (Any mention of location or scene environment)
    6. 'review_score_priority': (Scale 1-10: How important is hospital rating for this case? 
       Example: 1 for immediate life-saving, 10 for minor surgery)

    CRITICAL: Return ONLY valid JSON. No conversational text.
    """
    
    # Call the LLM to perform the 'scraping' logic
    scraped_features = llm(prompt, json_input)
    
    return scraped_features

# --- Integration Example ---
if __name__ == "__main__":
    # Example raw input from your triage model
    raw_data = {
        "emergency_level": "critical",
        "scene_type": "cardiac_event",
        "patient_status": {"consciousness_level": "unconscious"},
        "detected_injuries": [],
        "medical_flags": {"cardiac_event_suspected": True},
        # ... (rest of the 50+ lines of JSON)
    }

    # Scrape the useful bits
    hospital_search_features = preprocess_data(raw_data)
    
    print("--- SCRAPED FEATURES FOR HOSPITAL FINDER ---")
    print(json.dumps(hospital_search_features, indent=2))