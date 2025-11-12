"""
Mudra database module for storing and retrieving mudra information.
Provides mudra recommendations based on yoga asanas and benefits.
"""

import logging
import json

logger = logging.getLogger(__name__)


class MudraDatabase:
    """Database of mudras and their properties"""
    
    # Complete mudra database with properties
    MUDRAS = {
        'Gyan Mudra': {
            'name': 'Gyan Mudra',
            'english_name': 'Gesture of Knowledge',
            'elements': ['Air', 'Space'],
            'chakras': ['Root Chakra', 'Crown Chakra'],
            'benefits': [
                'Enhances concentration and memory',
                'Improves focus and mental clarity',
                'Reduces anxiety and stress',
                'Increases wisdom and creativity',
                'Improves brain function',
                'Aids in meditation'
            ],
            'how_to': 'Touch the tip of the index finger to the tip of the thumb, with other three fingers extended.',
            'duration': '15-20 minutes daily',
            'best_time': 'Morning during meditation',
            'related_asanas': ['Padmasana', 'Sukhasana', 'Vajrasana'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Chin Mudra': {
            'name': 'Chin Mudra',
            'english_name': 'Consciousness Gesture',
            'elements': ['Air', 'Space'],
            'chakras': ['Crown Chakra'],
            'benefits': [
                'Enhances concentration',
                'Calms the mind',
                'Promotes inner awareness',
                'Aids meditation',
                'Improves mental clarity',
                'Reduces restlessness'
            ],
            'how_to': 'Touch the tip of index finger to thumb, palm facing upward, other fingers extended.',
            'duration': '10-20 minutes',
            'best_time': 'Any time, preferably morning',
            'related_asanas': ['Meditation poses', 'Padmasana', 'Sukhasana'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Prana Mudra': {
            'name': 'Prana Mudra',
            'english_name': 'Gesture of Life Force',
            'elements': ['Fire', 'Water'],
            'chakras': ['Root Chakra', 'Heart Chakra'],
            'benefits': [
                'Activates dormant energy',
                'Improves physical vitality',
                'Enhances vision and eye health',
                'Reduces fatigue',
                'Activates life force energy',
                'Improves immunity'
            ],
            'how_to': 'Touch tips of ring and little finger to thumb, other two extended.',
            'duration': '15 minutes daily',
            'best_time': 'Morning or evening',
            'related_asanas': ['Surya Namaskar', 'Standing poses'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Apana Mudra': {
            'name': 'Apana Mudra',
            'english_name': 'Gesture of Digestion',
            'elements': ['Earth', 'Fire'],
            'chakras': ['Root Chakra', 'Sacral Chakra'],
            'benefits': [
                'Aids digestion',
                'Improves elimination',
                'Reduces constipation',
                'Regulates menstrual cycle',
                'Detoxifies the body',
                'Improves urinary function'
            ],
            'how_to': 'Touch tips of middle, ring, and little fingers to thumb, index extended.',
            'duration': '15-20 minutes',
            'best_time': 'Morning on empty stomach',
            'related_asanas': ['Twists', 'Forward bends', 'Child Pose'],
            'contraindications': ['Pregnancy'],
            'level': 'Beginner'
        },
        'Vyana Mudra': {
            'name': 'Vyana Mudra',
            'english_name': 'Gesture of Circulation',
            'elements': ['Air', 'Fire'],
            'chakras': ['Heart Chakra'],
            'benefits': [
                'Improves circulation',
                'Strengthens heart',
                'Reduces high blood pressure',
                'Enhances respiratory function',
                'Increases energy flow',
                'Improves physical strength'
            ],
            'how_to': 'All fingertips touch thumb tip, hands in prayer position.',
            'duration': '15 minutes',
            'best_time': 'Morning or evening',
            'related_asanas': ['Bhujangasana', 'Chest openers'],
            'contraindications': [],
            'level': 'Intermediate'
        },
        'Vayu Mudra': {
            'name': 'Vayu Mudra',
            'english_name': 'Gesture of Air',
            'elements': ['Air'],
            'chakras': ['Heart Chakra', 'Throat Chakra'],
            'benefits': [
                'Relieves joint pain',
                'Reduces arthritis symptoms',
                'Eases paralysis',
                'Reduces nervousness',
                'Improves circulation',
                'Calms anxiety'
            ],
            'how_to': 'Fold index finger and touch thumb, other three extended.',
            'duration': '15 minutes, 2-3 times daily',
            'best_time': 'Morning and evening',
            'related_asanas': ['Gentle stretches', 'Joint mobilization'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Akasha Mudra': {
            'name': 'Akasha Mudra',
            'english_name': 'Gesture of Space/Ether',
            'elements': ['Space/Ether'],
            'chakras': ['Throat Chakra', 'Crown Chakra'],
            'benefits': [
                'Improves hearing',
                'Reduces ear problems',
                'Enhances communication',
                'Improves dental health',
                'Opens throat chakra',
                'Increases spaciousness in body'
            ],
            'how_to': 'Touch middle finger to thumb, other fingers extended.',
            'duration': '12-15 minutes daily',
            'best_time': 'Morning',
            'related_asanas': ['Neck stretches', 'Throat openers'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Shuni Mudra': {
            'name': 'Shuni Mudra',
            'english_name': 'Gesture of Patience',
            'elements': ['Earth', 'Space'],
            'chakras': ['Root Chakra', 'Third Eye Chakra'],
            'benefits': [
                'Increases patience',
                'Improves focus and discipline',
                'Enhances intuition',
                'Reduces procrastination',
                'Brings stability',
                'Sharpens mind'
            ],
            'how_to': 'Touch middle finger to thumb, other fingers extended.',
            'duration': '15 minutes daily',
            'best_time': 'Morning meditation',
            'related_asanas': ['Meditation poses', 'Sukhasana'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Buddhi Mudra': {
            'name': 'Buddhi Mudra',
            'english_name': 'Gesture of Intellect',
            'elements': ['Water', 'Space'],
            'chakras': ['Throat Chakra', 'Heart Chakra'],
            'benefits': [
                'Enhances intellect and understanding',
                'Improves communication',
                'Increases concentration',
                'Aids meditation',
                'Improves memory',
                'Strengthens intuition'
            ],
            'how_to': 'Touch little finger to thumb, other fingers extended.',
            'duration': '12-15 minutes',
            'best_time': 'During study or work',
            'related_asanas': ['Forward bends', 'Seated poses'],
            'contraindications': [],
            'level': 'Beginner'
        },
        'Ashwini Mudra': {
            'name': 'Ashwini Mudra',
            'english_name': 'Horse Gesture',
            'elements': ['Fire', 'Earth'],
            'chakras': ['Root Chakra', 'Sacral Chakra'],
            'benefits': [
                'Strengthens pelvic floor',
                'Improves sexual function',
                'Regulates menstrual cycle',
                'Prevents hemorrhoids',
                'Awakens kundalini energy',
                'Improves bladder control'
            ],
            'how_to': 'Rhythmic contraction and relaxation of anal sphincter muscles.',
            'duration': '5-10 minutes daily',
            'best_time': 'Morning after toilet',
            'related_asanas': ['Mula Bandha practice', 'Pranayama'],
            'contraindications': ['Pregnancy', 'Hemorrhoids'],
            'level': 'Intermediate'
        }
    }
    
    # Asana-Mudra relationships
    ASANA_MUDRA_MAP = {
        'Padmasana': ['Gyan Mudra', 'Chin Mudra', 'Prana Mudra'],
        'Sukhasana': ['Gyan Mudra', 'Chin Mudra', 'Buddhi Mudra'],
        'Vajrasana': ['Prana Mudra', 'Apana Mudra'],
        'Uttanasana': ['Apana Mudra', 'Vayu Mudra'],
        'Adho Mukha Svanasana': ['Vyana Mudra', 'Prana Mudra'],
        'Bhujangasana': ['Vyana Mudra', 'Akasha Mudra'],
        'Trikonasana': ['Vyana Mudra', 'Prana Mudra'],
        'Vrksasana': ['Vayu Mudra', 'Shuni Mudra'],
        'Surya Namaskar': ['Prana Mudra', 'Vyana Mudra'],
        'Child Pose': ['Apana Mudra', 'Buddhi Mudra']
    }
    
    def __init__(self):
        """Initialize mudra database"""
        logger.info(f"Initialized Mudra Database with {len(self.MUDRAS)} mudras")
    
    def get_mudra_details(self, mudra_name):
        """
        Get detailed information about a specific mudra
        
        Args:
            mudra_name: Name of the mudra
            
        Returns:
            dict with mudra details or None if not found
        """
        # Try exact match first
        if mudra_name in self.MUDRAS:
            return self.MUDRAS[mudra_name]
        
        # Try case-insensitive match
        for name, details in self.MUDRAS.items():
            if name.lower() == mudra_name.lower():
                return details
        
        logger.warning(f"Mudra not found: {mudra_name}")
        return None
    
    def get_all_mudras(self):
        """Get list of all available mudras"""
        return [
            {
                'name': name,
                'english_name': details.get('english_name', ''),
                'chakras': details.get('chakras', []),
                'elements': details.get('elements', []),
                'level': details.get('level', '')
            }
            for name, details in sorted(self.MUDRAS.items())
        ]
    
    def get_mudras_for_asana(self, asana_name, confidence=1.0):
        """
        Get mudra recommendations for a specific asana
        
        Args:
            asana_name: Name of the yoga asana
            confidence: Prediction confidence (0-1)
            
        Returns:
            list of recommended mudras with details
        """
        recommended_mudras = []
        
        # Find exact or close match
        matching_key = None
        for key in self.ASANA_MUDRA_MAP:
            if key.lower() == asana_name.lower():
                matching_key = key
                break
        
        if not matching_key:
            # If not found, recommend general mudras
            mudra_names = ['Gyan Mudra', 'Prana Mudra', 'Vyana Mudra']
        else:
            mudra_names = self.ASANA_MUDRA_MAP[matching_key]
        
        # Build recommendations
        for mudra_name in mudra_names:
            if mudra_name in self.MUDRAS:
                mudra_detail = self.MUDRAS[mudra_name]
                recommended_mudras.append({
                    'name': mudra_name,
                    'english_name': mudra_detail.get('english_name', ''),
                    'benefits': mudra_detail.get('benefits', [])[:3],  # Top 3 benefits
                    'how_to': mudra_detail.get('how_to', ''),
                    'duration': mudra_detail.get('duration', ''),
                    'chakras': mudra_detail.get('chakras', []),
                    'confidence_match': float(confidence),
                    'level': mudra_detail.get('level', '')
                })
        
        return recommended_mudras
    
    def get_mudras_by_benefit(self, benefit_keyword):
        """
        Find mudras that provide a specific benefit
        
        Args:
            benefit_keyword: Keyword to search in benefits
            
        Returns:
            list of mudras with matching benefits
        """
        matching_mudras = []
        keyword_lower = benefit_keyword.lower()
        
        for mudra_name, details in self.MUDRAS.items():
            benefits = details.get('benefits', [])
            if any(keyword_lower in benefit.lower() for benefit in benefits):
                matching_mudras.append({
                    'name': mudra_name,
                    'english_name': details.get('english_name', ''),
                    'matching_benefits': [b for b in benefits if keyword_lower in b.lower()]
                })
        
        return matching_mudras
    
    def get_mudras_by_chakra(self, chakra_name):
        """
        Find mudras that work with a specific chakra
        
        Args:
            chakra_name: Name of the chakra
            
        Returns:
            list of mudras for that chakra
        """
        matching_mudras = []
        
        for mudra_name, details in self.MUDRAS.items():
            chakras = details.get('chakras', [])
            if any(chakra_name.lower() in c.lower() for c in chakras):
                matching_mudras.append({
                    'name': mudra_name,
                    'english_name': details.get('english_name', ''),
                    'level': details.get('level', '')
                })
        
        return matching_mudras
    
    def get_mudras_by_element(self, element_name):
        """
        Find mudras associated with a specific element
        
        Args:
            element_name: Name of the element
            
        Returns:
            list of mudras for that element
        """
        matching_mudras = []
        
        for mudra_name, details in self.MUDRAS.items():
            elements = details.get('elements', [])
            if any(element_name.lower() in e.lower() for e in elements):
                matching_mudras.append({
                    'name': mudra_name,
                    'english_name': details.get('english_name', ''),
                    'level': details.get('level', '')
                })
        
        return matching_mudras
