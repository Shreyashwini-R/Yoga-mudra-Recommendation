"""
Flask application for Yoga Asana and Mudra prediction and recommendation system.
Integrates ML model for asana prediction with mudra information and guidance.
"""

from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime

from models.predictor import YogaPredictor
from models.mudra_db import MudraDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'yoga-mudra-dev-key')
app.config['JSON_SORT_KEYS'] = False

# Initialize predictor and mudra database
try:
    predictor = YogaPredictor()
    mudra_db = MudraDatabase()
    logger.info("Model and databases loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    predictor = None
    mudra_db = None


@app.route('/')
def index():
    """Render home page"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict yoga asana based on benefits description
    
    Expected JSON:
    {
        "benefits": "description of desired benefits"
    }
    """
    try:
        data = request.get_json()
        if not data or 'benefits' not in data:
            return jsonify({'error': 'Missing benefits field'}), 400
        
        benefits_text = data['benefits'].strip()
        if not benefits_text:
            return jsonify({'error': 'Benefits field cannot be empty'}), 400
        
        if not predictor:
            return jsonify({'error': 'Model not initialized'}), 500
        
        # Get predictions
        prediction = predictor.predict(benefits_text)
        
        # Get complementary mudra recommendations
        mudra_recommendations = mudra_db.get_mudras_for_asana(
            prediction['asana'],
            prediction['confidence']
        )
        
        result = {
            'asana': prediction['asana'],
            'confidence': float(prediction['confidence']),
            'description': prediction.get('description', ''),
            'benefits': prediction.get('benefits', ''),
            'contraindications': prediction.get('contraindications', ''),
            'mudra_recommendations': mudra_recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Prediction successful for: {benefits_text[:50]}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/mudra/<mudra_name>', methods=['GET'])
def get_mudra(mudra_name):
    """Get detailed information about a specific mudra"""
    try:
        mudra_info = mudra_db.get_mudra_details(mudra_name)
        
        if not mudra_info:
            return jsonify({'error': 'Mudra not found'}), 404
        
        return jsonify(mudra_info), 200
        
    except Exception as e:
        logger.error(f"Error retrieving mudra: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/mudras', methods=['GET'])
def list_mudras():
    """Get list of all available mudras"""
    try:
        mudras = mudra_db.get_all_mudras()
        return jsonify({'mudras': mudras, 'count': len(mudras)}), 200
        
    except Exception as e:
        logger.error(f"Error retrieving mudras: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/asanas', methods=['GET'])
def list_asanas():
    """Get list of all available asanas"""
    try:
        asanas = predictor.get_available_asanas() if predictor else []
        return jsonify({'asanas': asanas, 'count': len(asanas)}), 200
        
    except Exception as e:
        logger.error(f"Error retrieving asanas: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Azure deployment"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model_loaded': predictor is not None,
        'mudra_db_loaded': mudra_db is not None
    }
    return jsonify(status), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask app on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
