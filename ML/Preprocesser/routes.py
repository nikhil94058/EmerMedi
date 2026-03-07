# Preprocesser/routes.py
from flask import Blueprint, request, jsonify
from LLM_brain.llm import llm

hospital_bp = Blueprint('hospital_bp', __name__)

def preprocess_data(json_input):
    """Scrapes the triage JSON for hospital-specific features."""
    prompt = """
    You are a medical DB scraper. Extract these features from the JSON:
    1. severity_level, 2. required_facility_type, 3. equipment_needed, 4. hospital_priority.
    Return ONLY JSON.
    """
    return llm(prompt, json_input)

def hospital_finder_logic(scraped_data):
    """Finds top 5 hospitals based on scraped features."""
    prompt = "Based on these medical requirements, suggest the top 5 types of hospitals or departments needed. Return a JSON list 'recommendations' with name, priority, and reason."
    return llm(prompt, scraped_data)

@hospital_bp.route('/find-hospitals', methods=['POST'])
def find_hospitals_route():
    try:
        triage_data = request.get_json()
        if not triage_data:
            return jsonify({"error": "No triage data provided"}), 400

        # Step 1: Extract features
        features = preprocess_data(triage_data)
        
        # Step 2: Find hospitals
        recommendations = hospital_finder_logic(features)

        return jsonify({
            "status": "success",
            "extracted_features": features,
            "hospital_list": recommendations
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500