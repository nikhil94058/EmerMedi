import boto3
import json
import os
import re
from botocore.config import Config

def llm(input_task: str, data: any, model_id: str = "us.amazon.nova-2-lite-v1:0") -> dict:
    """
    Modular text-to-text function that strictly returns a JSON object.
    
    Args:
        input_task: The logic/instruction (e.g. "Assess emergency level")
        data: The raw data to process (e.g. emotion list, sensor data)
    """
    
    # 1. Setup AWS Client
    config = Config(read_timeout=120, connect_timeout=60, retries={'max_attempts': 2})
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"), config=config)

    # 2. Strict Prompting (Forcing JSON)
    # We embed the instruction to ensure the model doesn't talk back with "Sure, here is your JSON:"
    formatted_data = json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)
    
    prompt = f"""
    You are a data processing engine. 
    DATA TO ANALYZE:
    {formatted_data}

    INSTRUCTION:
    {input_task}

    CRITICAL: Your response must be ONLY a valid JSON object. 
    Do not include any introductory text, explanations, or markdown formatting.
    """

    try:
        # 3. Call Bedrock
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.1} # Low temperature = high consistency
        )

        # 4. Extract Text
        res_text = response["output"]["message"]["content"][0]["text"].strip()

        # 5. Robust JSON Extraction
        # This handles cases where the model ignores instructions and adds ```json ... ```
        json_match = re.search(r'\{.*\}', res_text, re.DOTALL)
        if json_match:
            clean_json = json_match.group(0)
            return json.loads(clean_json)
        else:
            # If no curly braces found, try to parse the whole thing
            return json.loads(res_text)

    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Model returned invalid JSON formatting",
            "raw_output": res_text[:200]
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e)
        }

# --- EXAMPLE USAGE ---

# 1. Defining the data (e.g. from your emotion detector)
emotion_data = {
    "detected_emotions": ["Extreme Fear", "Panic"],
    "intensity_score": 0.95,
    "duration_seconds": 10
}

# 2. Defining the task
task = """
Determine if this is an emergency. 
Return JSON with:
- "is_emergency": boolean
- "severity": "low/medium/high"
- "action_required": "string"
"""

# 3. Running the function
result = llm(task, emotion_data)



if __name__ == "__main__":
    # Move all your example/test code inside here
    test_data = {"emotion": "panic"}
    test_task = "Is this an emergency?"
    result = llm(test_task, test_data)
    
    # Safely check for the key
    if "is_emergency" in result:
        print(result["is_emergency"])
    else:
        print("Test Result:", result)