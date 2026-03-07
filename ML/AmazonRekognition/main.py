from flask import Blueprint, request, jsonify
import os
import boto3
import io
from dotenv import load_dotenv
from PIL import Image

from AmazonRekognition.bedrock.llm_analyzer import analyze_image_with_llm

load_dotenv()

image_bp = Blueprint("image_bp", __name__)

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


@image_bp.route("/predict-image", methods=["POST"])
def predict_image():
    if "file" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["file"]
    print(f"\n[IMAGE RECEIVED] {image_file.filename}")

    try:
        raw_bytes = image_file.read()

        image_bytes = _prepare_image(raw_bytes)

        print("👀  Rekognition → labels…")
        rek_labels_resp = rekognition.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=20,
            MinConfidence=55,
        )
        labels = [
            {
                "name": lbl["Name"],
                "confidence": round(lbl["Confidence"], 2),
                "parents": [p["Name"] for p in lbl.get("Parents", [])],
                "aliases": [a["Name"] for a in lbl.get("Aliases", [])],
            }
            for lbl in rek_labels_resp["Labels"]
        ]
        print(f"   Labels: {[l['name'] for l in labels]}")

        print("👤  Rekognition → faces…")
        faces = _detect_faces(image_bytes)

        print("🔍  Rekognition → moderation…")
        moderation_labels = _detect_moderation(image_bytes)

        print("📝  Rekognition → text…")
        detected_text = _detect_text(image_bytes)

        rekognition_data = {
            "labels":            labels,
            "faces":             faces,
            "moderation_labels": moderation_labels,
            "detected_text":     detected_text,
        }

        print("🧠  Bedrock LLM multimodal triage…")
        triage = analyze_image_with_llm(
            image_bytes=image_bytes,
            rekognition_data=rekognition_data,
        )

        _print_summary(triage)

        response_payload = {
            "emergency_level":    triage.get("emergency_level", "none"),
            "urgency_score":      triage.get("urgency_score", 0),
            "call_ambulance":     triage.get("call_ambulance", False),
            "call_police":        triage.get("call_police", False),
            "call_fire_department": triage.get("call_fire_department", False),
            "time_critical":      triage.get("time_critical", False),
            "scene_type":         triage.get("scene_type", "normal"),
            "scene_description":  triage.get("scene_description", ""),
            "patient_status":     triage.get("patient_status", {}),
            "detected_injuries":  triage.get("detected_injuries", []),
            "medical_flags":      triage.get("medical_flags", {}),
            "environmental_hazards": triage.get("environmental_hazards", {}),
            "immediate_actions":  triage.get("immediate_actions", []),
            "do_not_actions":     triage.get("do_not_actions", []),
            "first_aid_steps":    triage.get("first_aid_steps", []),
            "dispatcher_report":  triage.get("dispatcher_report", ""),
            "hospital_recommendation": triage.get("hospital_recommendation", "none"),
            "eta_urgency":        triage.get("eta_urgency", "non_urgent"),
            "confidence_score":   triage.get("confidence_score", 0.0),
            "reasoning":          triage.get("reasoning", ""),
            "rekognition": {
                "labels":            [l["name"] for l in labels],
                "labels_detail":     labels,
                "faces_count":       len(faces),
                "faces_detail":      faces,
                "moderation_flags":  moderation_labels,
                "detected_text":     detected_text,
            },
        }

        return jsonify(response_payload), 200

    except Exception as exc:
        print(f"!!! SYSTEM ERROR: {exc}")
        import traceback; traceback.print_exc()
        return jsonify({"error": str(exc)}), 500


def _prepare_image(raw_bytes: bytes) -> bytes:
    """Normalize format and compress to <= 4.5 MB for Rekognition."""
    img = Image.open(io.BytesIO(raw_bytes))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    if len(raw_bytes) > 4_500_000:
        print("⚠️  Compressing large image…")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82)
        raw_bytes = buf.getvalue()

    return raw_bytes


def _detect_faces(image_bytes: bytes) -> list[dict]:
    try:
        resp = rekognition.detect_faces(
            Image={"Bytes": image_bytes},
            Attributes=["ALL"],
        )
        faces = []
        for face in resp.get("FaceDetails", []):
            age = face.get("AgeRange", {})
            emotions = [
                {"type": e["Type"], "confidence": round(e["Confidence"], 2)}
                for e in face.get("Emotions", [])
                if e["Confidence"] > 10
            ]
            faces.append({
                "age_range":       {"low": age.get("Low"), "high": age.get("High")},
                "emotions":        sorted(emotions, key=lambda e: -e["confidence"]),
                "smile":           face.get("Smile", {}).get("Value", False),
                "eyes_open":       face.get("EyesOpen", {}).get("Value", None),
                "mouth_open":      face.get("MouthOpen", {}).get("Value", None),
                "face_confidence": round(face.get("Confidence", 0), 2),
                "gender":          face.get("Gender", {}).get("Value"),
            })
        return faces
    except Exception as exc:
        print(f"   ⚠️  Face detection skipped: {exc}")
        return []


def _detect_moderation(image_bytes: bytes) -> list[dict]:
    try:
        resp = rekognition.detect_moderation_labels(
            Image={"Bytes": image_bytes},
            MinConfidence=50,
        )
        return [
            {"name": m["Name"], "confidence": round(m["Confidence"], 2)}
            for m in resp.get("ModerationLabels", [])
        ]
    except Exception as exc:
        print(f"   ⚠️  Moderation check skipped: {exc}")
        return []


def _detect_text(image_bytes: bytes) -> list[str]:
    try:
        resp = rekognition.detect_text(Image={"Bytes": image_bytes})
        return [
            t["DetectedText"]
            for t in resp.get("TextDetections", [])
            if t["Type"] == "LINE" and t["Confidence"] > 70
        ]
    except Exception as exc:
        print(f"   ⚠️  Text detection skipped: {exc}")
        return []


def _print_summary(triage: dict):
    lvl   = triage.get("emergency_level", "none").upper()
    score = triage.get("urgency_score", 0)
    icons = {"CRITICAL": "🔴", "URGENT": "🟠", "MODERATE": "🟡", "LOW": "🟢", "NONE": "✅"}
    icon  = icons.get(lvl, "❓")
    print("\n" + "─" * 50)
    print(f"  {icon}  LEVEL     : {lvl}  (score {score}/100)")
    print(f"  🚑  AMBULANCE : {'YES - CALL NOW' if triage.get('call_ambulance') else 'No'}")
    print(f"  🏥  HOSPITAL  : {triage.get('hospital_recommendation', 'none').upper()}")
    print(f"  ⏱️  URGENCY   : {triage.get('eta_urgency', 'non_urgent')}")
    print(f"  📋  REASON    : {triage.get('reasoning', '')[:120]}")
    injuries = triage.get("detected_injuries", [])
    if injuries:
        print(f"  🩸  INJURIES  : {', '.join(i['type'] for i in injuries)}")
    actions = triage.get("immediate_actions", [])
    if actions:
        print(f"  ‼️  ACTION 1  : {actions[0]}")
    print("─" * 50 + "\n")
