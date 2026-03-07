from flask import Flask, jsonify
from flask_cors import CORS
from models.server import audio_bp
from AmazonRekognition.main import image_bp
from Preprocesser.routes import hospital_bp 
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "Healthy",
        "message": "EmerMedi AI Engine is operational.",
        "endpoints": {
            "audio_analysis": "/predict",
            "visual_analysis": "/predict-image"
        }
    }), 200


app.register_blueprint(audio_bp)
app.register_blueprint(image_bp)
app.register_blueprint(hospital_bp) 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)