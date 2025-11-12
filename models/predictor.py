"""
Model predictor module for yoga asana prediction based on benefits.
Loads the trained Keras model and handles predictions.
"""

import numpy as np
import json
import os
import logging
import re
from pathlib import Path
import csv

try:
    import tensorflow as tf
    from tensorflow import keras
    from keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Configuration
ML_DIR = Path(__file__).parent.parent / 'Machine_Learning'
MODEL_WEIGHTS = ML_DIR / 'weight.h5'
MAP_FILE = ML_DIR / 'map.csv'
CLUSTER_FILE = ML_DIR / 'cluster.json'
CSV_DATA_FILE = ML_DIR / 'final_asan1_1.csv'


class YogaPredictor:
    """Handles prediction of yoga asanas based on benefits description"""
    
    def __init__(self):
        """Initialize the predictor with model and tokenizers"""
        self.model = None
        self.tokenizer = None
        self.word_index_map = {}
        self.index_to_word_map = {}
        self.asana_data = {}
        self.clusters = {}
        self.vocab_size = 365
        self.vocab_size2 = 237
        self.embed_size = 20
        self.sequence_length = 50
        
        self._load_components()
    
    def _load_components(self):
        """Load all necessary components"""
        try:
            if not KERAS_AVAILABLE:
                logger.warning("TensorFlow/Keras not available. Using mock predictions.")
                return
            
            # Load asana data from CSV
            self._load_asana_data()
            
            # Load word mappings
            self._load_word_mappings()
            
            # Load clusters
            self._load_clusters()
            
            # Build tokenizer
            self._build_tokenizer()
            
            # Load model
            self._load_model()
            
            logger.info("All components loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading components: {str(e)}")
            # Don't raise - allow graceful degradation
    
    def _load_asana_data(self):
        """Load asana information from CSV file"""
        try:
            if not CSV_DATA_FILE.exists():
                logger.warning(f"CSV file not found: {CSV_DATA_FILE}")
                return
            
            with open(CSV_DATA_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    asana_id = i + 1  # Starting from 1
                    self.asana_data[asana_id] = {
                        'name': row.get('AName', ''),
                        'description': row.get('Description', ''),
                        'benefits': row.get('Benefits', ''),
                        'contraindications': row.get('Contraindications', ''),
                        'breathing': row.get('Breathing', ''),
                        'level': row.get('Level', ''),
                        'variations': row.get('Variations', '')
                    }
            
            logger.info(f"Loaded {len(self.asana_data)} asanas from CSV")
        except Exception as e:
            logger.error(f"Error loading asana data: {str(e)}")
    
    def _load_word_mappings(self):
        """Load word to index and index to word mappings"""
        try:
            if not MAP_FILE.exists():
                logger.warning(f"Map file not found: {MAP_FILE}")
                return
            
            with open(MAP_FILE, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        idx = int(row[0])
                        word = row[1]
                        self.index_to_word_map[idx] = word
                        self.word_index_map[word] = idx
            
            logger.info(f"Loaded {len(self.word_index_map)} word mappings")
        except Exception as e:
            logger.error(f"Error loading word mappings: {str(e)}")
    
    def _load_clusters(self):
        """Load asana clusters"""
        try:
            if not CLUSTER_FILE.exists():
                logger.warning(f"Cluster file not found: {CLUSTER_FILE}")
                return
            
            with open(CLUSTER_FILE, 'r') as f:
                self.clusters = json.load(f)
            
            logger.info(f"Loaded {len(self.clusters)} clusters")
        except Exception as e:
            logger.error(f"Error loading clusters: {str(e)}")
    
    def _build_tokenizer(self):
        """Build tokenizer from word mappings"""
        try:
            # Create tokenizer
            self.tokenizer = Tokenizer()
            self.tokenizer.word_index = self.word_index_map
            logger.info("Tokenizer built successfully")
        except Exception as e:
            logger.error(f"Error building tokenizer: {str(e)}")
    
    def _load_model(self):
        """Load pre-trained Keras model"""
        try:
            if not MODEL_WEIGHTS.exists():
                logger.warning(f"Model weights not found: {MODEL_WEIGHTS}")
                return
            
            # Build model architecture
            from keras.models import Sequential
            from keras.layers import Dense, Embedding, Lambda, Flatten
            import keras.backend as K
            
            self.model = Sequential()
            self.model.add(Embedding(self.vocab_size + 1, self.embed_size, 
                                    input_length=self.sequence_length))
            self.model.add(Lambda(lambda x: K.mean(x, axis=1), 
                                 output_shape=(self.embed_size,)))
            self.model.add(Dense(self.vocab_size2 - 2, activation='softmax'))
            self.model.compile(loss=tf.keras.losses.CategoricalCrossentropy(), 
                             optimizer='adam', metrics=['accuracy'])
            
            # Load weights
            self.model.load_weights(str(MODEL_WEIGHTS))
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
    
    def _preprocess_text(self, text):
        """Preprocess input text"""
        text = text.lower()
        text = re.sub(r'[^A-Za-z\n]+', ' ', text)
        # Simple stopword removal
        stopwords = {'a', 'an', 'the', 'and', 'or', 'in', 'is', 'it', 'to', 'of', 'for'}
        words = [w for w in text.split() if w not in stopwords]
        return ' '.join(words)
    
    def predict(self, benefits_text):
        """
        Predict the best yoga asana for given benefits.
        
        Args:
            benefits_text: String description of desired benefits
            
        Returns:
            dict with predicted asana and confidence
        """
        try:
            # Preprocess input
            processed_text = self._preprocess_text(benefits_text)
            
            if not processed_text:
                return {
                    'asana': 'Unknown',
                    'confidence': 0.0,
                    'error': 'Invalid input'
                }
            
            # If model not available, return mock prediction
            if self.model is None:
                return self._mock_prediction(benefits_text)
            
            # Tokenize
            sequences = self.tokenizer.texts_to_sequences([processed_text])
            
            # Pad sequences
            padded = pad_sequences(sequences, self.sequence_length, 
                                 padding='post', truncating='pre')
            
            # Predict
            prediction = self.model.predict(padded, verbose=0)
            
            # Get top prediction
            predicted_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_idx])
            
            # Convert index to asana ID (add 3 offset as in original training)
            asana_id = predicted_idx + 3
            
            # Get asana details
            asana_info = self.asana_data.get(asana_id, {})
            asana_name = asana_info.get('name', f'Asana {asana_id}')
            
            return {
                'asana': asana_name,
                'asana_id': asana_id,
                'confidence': confidence,
                'description': asana_info.get('description', ''),
                'benefits': asana_info.get('benefits', ''),
                'contraindications': asana_info.get('contraindications', ''),
                'level': asana_info.get('level', ''),
                'breathing': asana_info.get('breathing', '')
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'asana': 'Unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _mock_prediction(self, benefits_text):
        """Return mock prediction when model not available"""
        # Simple keyword matching for demonstration
        benefits_lower = benefits_text.lower()
        
        keyword_asanas = {
            'flexibility': ('Uttanasana', 2),
            'strength': ('Adho Mukha Svanasana', 5),
            'balance': ('Vrksasana', 8),
            'calm': ('Lotus Pose', 1),
            'energy': ('Surya Namaskar', 3),
            'digestion': ('Trikonasana', 4),
            'back': ('Bhujangasana', 6),
            'hip': ('Pigeon Pose', 9),
        }
        
        for keyword, (asana, asana_id) in keyword_asanas.items():
            if keyword in benefits_lower:
                asana_info = self.asana_data.get(asana_id, {})
                return {
                    'asana': asana,
                    'asana_id': asana_id,
                    'confidence': 0.75,
                    'description': asana_info.get('description', ''),
                    'benefits': asana_info.get('benefits', ''),
                    'contraindications': asana_info.get('contraindications', ''),
                    'is_mock': True
                }
        
        # Default prediction
        return {
            'asana': 'Child Pose',
            'asana_id': 1,
            'confidence': 0.5,
            'is_mock': True
        }
    
    def get_available_asanas(self):
        """Get list of all available asanas"""
        return [
            {
                'id': asana_id,
                'name': info['name'],
                'level': info.get('level', '')
            }
            for asana_id, info in sorted(self.asana_data.items())
        ]
