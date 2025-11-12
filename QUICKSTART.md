# Quick Start Guide - Yoga Mudra Flask App

## What Has Been Created ✅

Your complete Flask application with mudra support and Azure deployment is ready!

### Core Application Files
- ✅ **app.py** - Main Flask application with REST API endpoints
- ✅ **models/predictor.py** - ML model for yoga asana prediction
- ✅ **models/mudra_db.py** - Complete mudra database with 10+ mudras
- ✅ **templates/index.html** - Beautiful interactive web interface
- ✅ **requirements.txt** - All Python dependencies

### Deployment Files
- ✅ **Dockerfile** - Docker containerization
- ✅ **docker-compose.yml** - Local Docker development
- ✅ **azure-deploy.json** - Azure Resource Manager template
- ✅ **.deployment** - Azure deployment config
- ✅ **startup.sh** - Azure app service startup script
- ✅ **README.md** - Complete documentation

## Quick Start (Local)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Flask App
```powershell
python app.py
```

The app will be available at: **http://localhost:5000**

### 3. Test the API
```powershell
$body = @{
    benefits = "I want flexibility and stress relief"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/predict" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

## Quick Start (Docker)

### 1. Build and Run with Docker Compose
```powershell
docker-compose up --build
```

Access at: **http://localhost:5000**

### 2. View Logs
```powershell
docker-compose logs -f yoga-mudra-app
```

## Deploy to Azure

### Option A: Quick Deploy (Easiest)

```powershell
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name yoga-mudra-rg --location eastus

# 3. Create App Service Plan
az appservice plan create `
  --name yoga-mudra-plan `
  --resource-group yoga-mudra-rg `
  --sku F1 `
  --is-linux

# 4. Create Web App
az webapp create `
  --resource-group yoga-mudra-rg `
  --plan yoga-mudra-plan `
  --name yoga-mudra-$([System.Guid]::NewGuid().ToString().Substring(0,8)) `
  --runtime "PYTHON:3.10"

# 5. Configure for deployment
# (See README.md for detailed steps)
```

### Option B: Deploy from GitHub

1. Push code to GitHub
2. Go to Azure Portal
3. Create Web App → Select "GitHub" as deployment source
4. Authorize and select repository
5. Azure will automatically deploy on push

### Option C: Deploy Docker to Azure Container Registry

```powershell
# 1. Create container registry
az acr create --resource-group yoga-mudra-rg --name yogamudra --sku Basic

# 2. Build and push image
az acr build --registry yogamudra --image yoga-mudra-app:latest .

# 3. Deploy to App Service
az webapp create `
  --resource-group yoga-mudra-rg `
  --plan yoga-mudra-plan `
  --name yoga-mudra-app `
  --deployment-container-image-name yogamudra.azurecr.io/yoga-mudra-app:latest
```

## API Endpoints

### 1. Web Interface
**GET** `http://localhost:5000/`
- Interactive web interface for predictions

### 2. Predict Asana
**POST** `/predict`
```json
{
    "benefits": "flexibility, balance, stress relief"
}
```

### 3. Get Mudras
**GET** `/mudras` - List all mudras
**GET** `/mudra/<name>` - Get mudra details

### 4. Get Asanas
**GET** `/asanas` - List all available asanas

### 5. Health Check
**GET** `/health` - Check if app is running

## Mudra Features

Your app includes 10 powerful mudras:

1. **Gyan Mudra** - Knowledge & Concentration
2. **Chin Mudra** - Consciousness & Meditation
3. **Prana Mudra** - Life Force & Vitality
4. **Apana Mudra** - Digestion & Elimination
5. **Vyana Mudra** - Circulation & Strength
6. **Vayu Mudra** - Air & Joint Health
7. **Akasha Mudra** - Space & Communication
8. **Shuni Mudra** - Patience & Intuition
9. **Buddhi Mudra** - Intellect & Communication
10. **Ashwini Mudra** - Pelvic Floor & Energy

## File Structure Summary

```
Yoga_Mudra/
├── app.py                      # Main Flask app
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker config
├── docker-compose.yml          # Compose config
├── azure-deploy.json           # ARM template
├── startup.sh                  # Azure startup
├── README.md                   # Full documentation
├── QUICKSTART.md              # This file
├── models/
│   ├── predictor.py           # Asana prediction
│   └── mudra_db.py            # Mudra database
├── templates/
│   └── index.html             # Web UI
└── Machine_Learning/           # Existing ML files
    ├── weight.h5
    ├── map.csv
    ├── cluster.json
    └── final_asan1_1.csv
```

## Next Steps

1. ✅ **Test Locally**
   ```powershell
   python app.py
   # Open http://localhost:5000
   ```

2. ✅ **Test with Docker**
   ```powershell
   docker-compose up
   ```

3. ✅ **Deploy to Azure**
   - Follow one of the deployment options above
   - Configure environment variables
   - Test health endpoint

4. ✅ **Customize**
   - Add more mudras in `models/mudra_db.py`
   - Modify UI in `templates/index.html`
   - Add authentication if needed

## Environment Variables (Azure)

Set these in Azure Portal → Configuration:

```
FLASK_ENV = production
SECRET_KEY = your-secret-key-here
PORT = 5000
```

## Troubleshooting

### Model Not Loading?
- Check if `Machine_Learning/weight.h5` exists
- App will use mock predictions as fallback
- View logs: `az webapp log tail --resource-group yoga-mudra-rg --name <app-name>`

### Port Already in Use?
```powershell
# Windows
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# Or use a different port
$env:FLASK_PORT = 5001
python app.py
```

### Docker Issues?
```powershell
docker-compose down
docker-compose up --build
docker system prune
```

## Performance Tips

1. **Use B1 Plan** or higher for production (F1 is free but limited)
2. **Enable Always On** to prevent cold starts
3. **Set Worker Processes** appropriately (default: 4)
4. **Monitor** with Application Insights (Azure)
5. **Cache** responses for frequently used mudras

## Support & Documentation

- 📚 **Full README**: `README.md`
- 🔍 **API Docs**: See `/predict` endpoint in `app.py`
- 🐳 **Docker Docs**: `Dockerfile`
- ☁️ **Azure Docs**: `azure-deploy.json`

## Example Usage

### Web Interface
1. Go to `http://localhost:5000`
2. Enter health benefits (e.g., "flexibility and balance")
3. Click "Predict Asana"
4. Get recommended asana + mudras

### Using cURL
```powershell
curl -X POST http://localhost:5000/predict `
  -H "Content-Type: application/json" `
  -d '{"benefits":"strengthen my core and improve digestion"}'
```

### Using Python
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    'benefits': 'reduce stress and improve sleep'
})
print(response.json())
```

---

## 🎉 You're All Set!

Your complete Yoga Mudra Flask application with Azure deployment is ready to go!

**Start here:**
```powershell
python app.py
# Then open http://localhost:5000 in your browser
```

Happy practicing! 🧘‍♀️🔮

For detailed deployment instructions, see **README.md**
