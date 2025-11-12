# Yoga Asana & Mudra Predictor

A Flask-based web application that predicts suitable yoga asanas based on desired health benefits and recommends complementary mudras for a holistic practice.

## Features

✨ **Intelligent Asana Prediction**: ML-powered prediction of suitable yoga asanas based on health benefits

🔮 **Mudra Recommendations**: Automatically suggests complementary hand gestures (mudras) for each asana

📚 **Comprehensive Database**: 10+ mudras with detailed information on benefits, techniques, and chakra alignments

🎯 **REST API**: Full-featured API for integration with other applications

🌐 **Interactive Web UI**: Beautiful, responsive interface for easy interaction

📊 **Health Check Endpoint**: Built-in monitoring for Azure deployment

## Project Structure

```
Yoga_Mudra/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose for local development
├── azure-deploy.json           # Azure Resource Manager template
├── .deployment                 # Azure deployment configuration
├── .gitignore                  # Git ignore rules
├── models/
│   ├── __init__.py            # Package initialization
│   ├── predictor.py           # Yoga asana prediction model
│   └── mudra_db.py            # Mudra database and recommendations
├── templates/
│   └── index.html             # Web UI
└── Machine_Learning/           # Pre-trained models and data
    ├── weight.h5              # Trained Keras model weights
    ├── map.csv                # Word index mappings
    ├── cluster.json           # Asana clusters
    └── final_asan1_1.csv      # Asana database
```

## Prerequisites

- Python 3.10+
- pip package manager
- Docker (for containerized deployment)
- Azure CLI (for Azure deployment)
- Git

## Local Development

### 1. Clone and Setup

```bash
cd Yoga_Mudra
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

Access the app at `http://localhost:5000`

## API Endpoints

### 1. Predict Asana
**POST** `/predict`

Request body:
```json
{
    "benefits": "I want to improve flexibility and reduce back pain"
}
```

Response:
```json
{
    "asana": "Uttanasana",
    "asana_id": 2,
    "confidence": 0.85,
    "description": "Standing forward bend...",
    "benefits": "Stretches hamstrings, calves, and hips...",
    "level": "Intermediate",
    "mudra_recommendations": [
        {
            "name": "Gyan Mudra",
            "english_name": "Gesture of Knowledge",
            "benefits": ["Enhances concentration", "Improves mental clarity"],
            "how_to": "Touch the tip of index finger to thumb...",
            "duration": "15-20 minutes daily",
            "chakras": ["Root Chakra", "Crown Chakra"]
        }
    ]
}
```

### 2. Get All Mudras
**GET** `/mudras`

Response:
```json
{
    "mudras": [
        {
            "name": "Gyan Mudra",
            "english_name": "Gesture of Knowledge",
            "chakras": ["Root Chakra", "Crown Chakra"],
            "elements": ["Air", "Space"],
            "level": "Beginner"
        }
    ],
    "count": 10
}
```

### 3. Get Mudra Details
**GET** `/mudra/<mudra_name>`

Response:
```json
{
    "name": "Gyan Mudra",
    "english_name": "Gesture of Knowledge",
    "elements": ["Air", "Space"],
    "chakras": ["Root Chakra", "Crown Chakra"],
    "benefits": [
        "Enhances concentration and memory",
        "Improves focus and mental clarity",
        "Reduces anxiety and stress"
    ],
    "how_to": "Touch the tip of the index finger to the tip of the thumb...",
    "duration": "15-20 minutes daily",
    "related_asanas": ["Padmasana", "Sukhasana"],
    "level": "Beginner"
}
```

### 4. List All Asanas
**GET** `/asanas`

Response:
```json
{
    "asanas": [
        {
            "id": 1,
            "name": "Padmasana",
            "level": "Beginner"
        }
    ],
    "count": 224
}
```

### 5. Health Check
**GET** `/health`

Response:
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00",
    "model_loaded": true,
    "mudra_db_loaded": true
}
```

## Deployment to Azure

### Option 1: Using Azure CLI (Recommended)

#### 1. Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name yoga-mudra-rg --location eastus

# Create App Service Plan
az appservice plan create \
  --name yoga-mudra-plan \
  --resource-group yoga-mudra-rg \
  --sku F1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group yoga-mudra-rg \
  --plan yoga-mudra-plan \
  --name yoga-mudra-app-<unique-id> \
  --runtime "PYTHON:3.10"
```

#### 2. Deploy from Git (Recommended for Simple Deployment)

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Setup deployment
az webapp deployment source config-zip \
  --resource-group yoga-mudra-rg \
  --name yoga-mudra-app-<unique-id> \
  --src <path-to-app-folder>
```

#### 3. Deploy with Docker (Recommended for Production)

```bash
# Create Container Registry
az acr create \
  --resource-group yoga-mudra-rg \
  --name yogamudra \
  --sku Basic

# Build and push Docker image
az acr build \
  --registry yogamudra \
  --image yoga-mudra-app:latest \
  .

# Configure Web App for Docker
az webapp config container set \
  --resource-group yoga-mudra-rg \
  --name yoga-mudra-app-<unique-id> \
  --docker-custom-image-name yogamudra.azurecr.io/yoga-mudra-app:latest \
  --docker-registry-server-url https://yogamudra.azurecr.io \
  --docker-registry-server-user <username> \
  --docker-registry-server-password <password>
```

### Option 2: Using Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Web App"
4. Fill in the details:
   - **Resource Group**: Create new (yoga-mudra-rg)
   - **Name**: yoga-mudra-app-<unique-name>
   - **Publish**: Docker Container
   - **Operating System**: Linux
   - **App Service Plan**: Create new (yoga-mudra-plan)
5. Go to "Docker" tab and configure:
   - **Image Source**: Docker Hub or Azure Container Registry
   - **Image and tag**: yoga-mudra-app:latest
6. Click "Review + Create"
7. Deploy the code using Git or FTP

### Option 3: Using Azure Resource Manager Template

```bash
az deployment group create \
  --resource-group yoga-mudra-rg \
  --template-file azure-deploy.json \
  --parameters \
    webAppName=yoga-mudra-app-<unique-id> \
    location=eastus \
    sku=B1
```

### Configuration After Deployment

1. Set environment variables in Azure Portal:
   - Go to Configuration → Application Settings
   - Add `FLASK_ENV`: `production`
   - Add `SECRET_KEY`: Your secure key

2. Enable logging:
   - App Service logs → Enable Application Logging
   - Enable Web server logging

3. Test the health endpoint:
   ```bash
   curl https://yoga-mudra-app-<unique-id>.azurewebsites.net/health
   ```

## Troubleshooting

### Model Loading Issues

If the pre-trained model fails to load:

1. Check if `Machine_Learning/weight.h5` exists
2. Verify the model file path is correct
3. The app will use mock predictions if the model is unavailable
4. Check logs: `az webapp log tail --resource-group yoga-mudra-rg --name yoga-mudra-app-<unique-id>`

### Performance Optimization

For production deployments:

1. **Scale Up**: Use B1 or S1 plan for better performance
2. **Always On**: Enable "Always On" to prevent cold starts
3. **Multiple Instances**: Enable auto-scaling in production
4. **Caching**: Implement Redis caching for frequently accessed data
5. **CDN**: Use Azure CDN for static assets

## Available Mudras

1. **Gyan Mudra** - Gesture of Knowledge
2. **Chin Mudra** - Consciousness Gesture
3. **Prana Mudra** - Gesture of Life Force
4. **Apana Mudra** - Gesture of Digestion
5. **Vyana Mudra** - Gesture of Circulation
6. **Vayu Mudra** - Gesture of Air
7. **Akasha Mudra** - Gesture of Space/Ether
8. **Shuni Mudra** - Gesture of Patience
9. **Buddhi Mudra** - Gesture of Intellect
10. **Ashwini Mudra** - Horse Gesture

## Chakras Covered

- Root Chakra (Muladhara)
- Sacral Chakra (Svadhisthana)
- Solar Plexus Chakra (Manipura)
- Heart Chakra (Anahata)
- Throat Chakra (Vishuddha)
- Third Eye Chakra (Ajna)
- Crown Chakra (Sahasrara)

## Elements Balanced

- **Air** - Movement, flexibility, mental activity
- **Fire** - Transformation, digestion, energy
- **Water** - Emotion, fluidity, intuition
- **Earth** - Stability, grounding, strength
- **Space/Ether** - Connection, expansion, awareness

## Development

### Adding New Mudras

Edit `models/mudra_db.py` and add to the `MUDRAS` dictionary:

```python
'Your Mudra': {
    'name': 'Your Mudra',
    'english_name': 'English Translation',
    'elements': ['Element1', 'Element2'],
    'chakras': ['Chakra1', 'Chakra2'],
    'benefits': ['Benefit1', 'Benefit2', ...],
    'how_to': 'Instructions...',
    'duration': '15 minutes daily',
    'related_asanas': ['Asana1', 'Asana2'],
    'contraindications': ['Condition1', 'Condition2'],
    'level': 'Beginner|Intermediate|Advanced'
}
```

### Adding New Asana-Mudra Associations

Edit `ASANA_MUDRA_MAP` in `models/mudra_db.py`:

```python
'Your Asana': ['Mudra1', 'Mudra2']
```

## Testing

Run the health check:

```bash
curl http://localhost:5000/health
```

Test the prediction endpoint:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"benefits": "flexibility and strength"}'
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the API documentation
3. Check Azure documentation
4. Contact the development team

## Acknowledgments

- Based on Keras/TensorFlow machine learning models
- Yoga and mudra information from traditional Sanskrit sources
- Built with Flask and modern web technologies

## Future Enhancements

- [ ] User accounts and personalized recommendations
- [ ] Integration with fitness trackers
- [ ] Video tutorials for each asana and mudra
- [ ] Multi-language support
- [ ] Mobile app (iOS/Android)
- [ ] Advanced analytics and progress tracking
- [ ] Integration with calendar for scheduling
- [ ] Community features and user reviews

---

Happy practicing! 🧘‍♀️🔮
