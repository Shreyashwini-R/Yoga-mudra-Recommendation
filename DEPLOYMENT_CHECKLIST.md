# 🚀 Deployment Checklist - Yoga Mudra Flask App

## Pre-Deployment Verification ✅

### 1. Project Structure
- [x] `app.py` - Main Flask application
- [x] `models/predictor.py` - ML prediction module
- [x] `models/mudra_db.py` - Mudra database
- [x] `models/__init__.py` - Package init
- [x] `templates/index.html` - Web interface
- [x] `Machine_Learning/weight.h5` - Pre-trained model
- [x] `Machine_Learning/map.csv` - Word mappings
- [x] `Machine_Learning/cluster.json` - Asana clusters
- [x] `Machine_Learning/final_asan1_1.csv` - Asana database

### 2. Configuration Files
- [x] `requirements.txt` - Dependencies
- [x] `Dockerfile` - Docker image
- [x] `docker-compose.yml` - Docker compose
- [x] `azure-deploy.json` - ARM template
- [x] `azure-pipelines.yml` - CI/CD pipeline
- [x] `.deployment` - Azure deployment
- [x] `.gitignore` - Git ignore rules
- [x] `startup.sh` - Startup script

### 3. Documentation
- [x] `README.md` - Full documentation
- [x] `QUICKSTART.md` - Quick start guide
- [x] `PROJECT_SUMMARY.md` - Project overview
- [x] `DEPLOYMENT_CHECKLIST.md` - This file

---

## Local Testing ✅

### Step 1: Verify Python Environment
```powershell
# Check Python version (should be 3.10+)
python --version

# Check pip
pip --version

# List installed packages (after requirements install)
pip list
```

### Step 2: Install Dependencies
```powershell
cd c:\Desktop\Yoga_Mudra
pip install -r requirements.txt
```

Expected packages:
- Flask==2.3.3
- tensorflow==2.13.0
- keras==2.13.1
- numpy==1.24.3
- scikit-learn==1.3.0
- gensim==4.3.1
- textblob==0.17.1
- nltk==3.8.1
- gunicorn==21.2.0

### Step 3: Run Locally
```powershell
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Test Web Interface
```powershell
# Open in browser
Start-Process "http://localhost:5000"
```

### Step 5: Test API Endpoint
```powershell
$body = @{ benefits = "flexibility and balance" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/predict" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

Expected response:
```json
{
    "asana": "Yoga Asana Name",
    "confidence": 0.85,
    "mudra_recommendations": [...]
}
```

### Step 6: Test Health Endpoint
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

Expected response:
```json
{
    "status": "healthy",
    "model_loaded": true,
    "mudra_db_loaded": true
}
```

---

## Docker Testing ✅

### Step 1: Build Docker Image
```powershell
cd c:\Desktop\Yoga_Mudra
docker build -t yoga-mudra-app:latest .
```

### Step 2: Run with Docker Compose
```powershell
docker-compose up --build
```

### Step 3: Test Docker Container
```powershell
# Health check
curl http://localhost:5000/health

# Prediction
$body = @{ benefits = "strength" } | ConvertTo-Json
curl -X POST http://localhost:5000/predict `
    -H "Content-Type: application/json" `
    -d $body
```

### Step 4: Verify Container
```powershell
# View running containers
docker ps

# View logs
docker-compose logs -f yoga-mudra-app

# Stop container
docker-compose down
```

---

## Azure Deployment ✅

### Option A: Using Azure CLI

#### Prerequisites
```powershell
# Install Azure CLI
# Download from: https://aka.ms/installazurecliwindows

# Verify installation
az --version

# Login to Azure
az login
```

#### Step 1: Create Resource Group
```powershell
az group create `
    --name yoga-mudra-rg `
    --location eastus
```

#### Step 2: Create App Service Plan
```powershell
az appservice plan create `
    --name yoga-mudra-plan `
    --resource-group yoga-mudra-rg `
    --sku F1 `
    --is-linux
```

#### Step 3: Create Web App
```powershell
$uniqueId = -join ((65..90) + (97..122) | Get-Random -Count 8 | ForEach-Object {[char]$_})
$webAppName = "yoga-mudra-$uniqueId"

az webapp create `
    --resource-group yoga-mudra-rg `
    --plan yoga-mudra-plan `
    --name $webAppName `
    --runtime "PYTHON:3.10"

# Save the web app name for later
Write-Host "Web App Name: $webAppName"
```

#### Step 4: Configure Application Settings
```powershell
az webapp config appsettings set `
    --resource-group yoga-mudra-rg `
    --name $webAppName `
    --settings FLASK_ENV=production SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

#### Step 5: Deploy Code (ZIP Method)
```powershell
# Create ZIP file
Compress-Archive -Path c:\Desktop\Yoga_Mudra -DestinationPath yoga-mudra.zip

# Deploy
az webapp deployment source config-zip `
    --resource-group yoga-mudra-rg `
    --name $webAppName `
    --src yoga-mudra.zip
```

#### Step 6: Verify Deployment
```powershell
# Get the URL
$siteUrl = az webapp show `
    --resource-group yoga-mudra-rg `
    --name $webAppName `
    --query defaultHostName -o tsv

Write-Host "Access your app at: https://$siteUrl"

# Test health endpoint
Invoke-RestMethod -Uri "https://$siteUrl/health"
```

### Option B: Docker Container Deployment

#### Step 1: Create Container Registry
```powershell
az acr create `
    --resource-group yoga-mudra-rg `
    --name yogamudra `
    --sku Basic
```

#### Step 2: Build and Push Docker Image
```powershell
az acr build `
    --registry yogamudra `
    --image yoga-mudra-app:latest `
    .
```

#### Step 3: Create Web App for Container
```powershell
az webapp create `
    --resource-group yoga-mudra-rg `
    --plan yoga-mudra-plan `
    --name yoga-mudra-docker `
    --deployment-container-image-name yogamudra.azurecr.io/yoga-mudra-app:latest
```

#### Step 4: Configure Container
```powershell
$registryUrl = az acr show `
    --resource-group yoga-mudra-rg `
    --name yogamudra `
    --query loginServer -o tsv

az webapp config container set `
    --resource-group yoga-mudra-rg `
    --name yoga-mudra-docker `
    --docker-custom-image-name "yogamudra.azurecr.io/yoga-mudra-app:latest" `
    --docker-registry-server-url "https://$registryUrl"
```

### Option C: Using Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a Web App:
   - Publish: Docker Container or Code
   - Runtime: Python 3.10
   - OS: Linux
   - Plan: Free (F1) or paid
3. Configure deployment source (GitHub/ZIP)
4. Deploy and test

---

## Post-Deployment Verification ✅

### Step 1: Test Web Interface
```powershell
# Open app in browser
Start-Process "https://yoga-mudra-<app-name>.azurewebsites.net"
```

### Step 2: Test Health Endpoint
```powershell
$healthUrl = "https://yoga-mudra-<app-name>.azurewebsites.net/health"
Invoke-RestMethod -Uri $healthUrl
```

### Step 3: Test API
```powershell
$apiUrl = "https://yoga-mudra-<app-name>.azurewebsites.net/predict"
$body = @{ benefits = "flexibility" } | ConvertTo-Json

$response = Invoke-RestMethod -Uri $apiUrl `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response | ConvertTo-Json
```

### Step 4: Configure Monitoring
```powershell
# Enable Application Insights (optional)
az monitor app-insights component create `
    --app yoga-mudra-insights `
    --location eastus `
    --resource-group yoga-mudra-rg

# View logs
az webapp log tail `
    --resource-group yoga-mudra-rg `
    --name yoga-mudra-<app-name>
```

### Step 5: Set Custom Domain (Optional)
```powershell
# Add custom domain
az webapp config hostname add `
    --resource-group yoga-mudra-rg `
    --webapp-name yoga-mudra-<app-name> `
    --hostname yourdomain.com
```

---

## Performance Optimization ✅

### For Production (Azure App Service)

#### 1. Scale Up Plan
```powershell
# Change from F1 (Free) to B1 (Basic)
az appservice plan update `
    --name yoga-mudra-plan `
    --resource-group yoga-mudra-rg `
    --sku B1
```

#### 2. Enable Always On
```powershell
# Prevents cold starts
az webapp config set `
    --resource-group yoga-mudra-rg `
    --name yoga-mudra-<app-name> `
    --always-on true
```

#### 3. Configure Auto-Scaling
```powershell
# Add auto-scale rule
az monitor metrics alert create `
    --name yoga-mudra-scale-up `
    --resource-group yoga-mudra-rg `
    --scopes /subscriptions/<subscription-id>/resourceGroups/yoga-mudra-rg/providers/Microsoft.Web/serverfarms/yoga-mudra-plan `
    --condition "avg Percentage CPU > 80"
```

#### 4. Configure Logging
```powershell
# Enable application logging
az webapp log config `
    --name yoga-mudra-<app-name> `
    --resource-group yoga-mudra-rg `
    --application-logging true `
    --level information
```

---

## Troubleshooting ✅

### Issue: Port Already in Use (Local)
```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000

# Kill the process
Stop-Process -Id <ProcessId>

# Or use different port
$env:FLASK_PORT = 5001
python app.py
```

### Issue: Model Not Loading
```powershell
# Check if files exist
Test-Path c:\Desktop\Yoga_Mudra\Machine_Learning\weight.h5
Test-Path c:\Desktop\Yoga_Mudra\Machine_Learning\map.csv

# App will use mock predictions if model unavailable
# This is expected behavior for graceful degradation
```

### Issue: Dependencies Installation Fails
```powershell
# Upgrade pip
pip install --upgrade pip

# Clear cache
pip cache purge

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

### Issue: Docker Build Fails
```powershell
# Clean up
docker system prune -a

# Rebuild with verbose output
docker build -t yoga-mudra-app:latest . --verbose

# Check Docker daemon
docker info
```

### Issue: Azure Deployment Fails
```powershell
# Check deployment logs
az webapp deployment slot list `
    --resource-group yoga-mudra-rg `
    --name yoga-mudra-<app-name>

# View real-time logs
az webapp log tail `
    --resource-group yoga-mudra-rg `
    --name yoga-mudra-<app-name> `
    --provider "Microsoft.Web/sites"
```

---

## Monitoring & Maintenance ✅

### Daily Checks
- [ ] Health endpoint returns 200 status
- [ ] API responds to predict requests
- [ ] Web interface loads properly
- [ ] No error logs in Azure

### Weekly Checks
- [ ] Review performance metrics
- [ ] Check error rates
- [ ] Monitor response times
- [ ] Verify disk usage

### Monthly Checks
- [ ] Update dependencies
- [ ] Review security logs
- [ ] Optimize database queries
- [ ] Plan scaling adjustments

---

## Cleanup (When Done) 🧹

### Remove Azure Resources
```powershell
# Delete resource group (removes all resources)
az group delete --name yoga-mudra-rg

# Verify deletion
az group show --name yoga-mudra-rg
```

### Clean Docker
```powershell
# Remove image
docker rmi yoga-mudra-app:latest

# Remove containers
docker container prune

# Deep clean
docker system prune -a --volumes
```

### Clean Local
```powershell
# Remove virtual environment
Remove-Item -Recurse venv/

# Remove cache
Remove-Item -Recurse __pycache__/

# Remove ZIP file
Remove-Item yoga-mudra.zip
```

---

## Success Criteria ✅

Your deployment is successful when:

- ✅ Web app loads at URL
- ✅ Health endpoint returns 200
- ✅ Prediction API works correctly
- ✅ Mudra recommendations appear
- ✅ No errors in logs
- ✅ Response time < 2 seconds
- ✅ Can handle multiple requests
- ✅ Database connections stable

---

## Final Verification Checklist

- [ ] All files present in workspace
- [ ] Python environment configured
- [ ] Dependencies installed
- [ ] Local testing successful
- [ ] Docker build successful
- [ ] Docker compose runs without errors
- [ ] Azure resources created
- [ ] Deployment completed
- [ ] Health endpoint responds
- [ ] Web interface loads
- [ ] API predictions work
- [ ] Mudra recommendations display
- [ ] No critical errors in logs
- [ ] Performance acceptable

---

## Support Resources

- 📚 [README.md](./README.md) - Full documentation
- ⚡ [QUICKSTART.md](./QUICKSTART.md) - Quick reference
- 📋 [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - Project overview
- 🔗 [Flask Documentation](https://flask.palletsprojects.com/)
- ☁️ [Azure Documentation](https://docs.microsoft.com/azure/)
- 🐳 [Docker Documentation](https://docs.docker.com/)

---

**Status**: ✅ READY FOR DEPLOYMENT

**Last Updated**: November 11, 2025

**Deployment Checklist Version**: 1.0

---

🎉 **Congratulations!** Your Yoga Mudra Flask App is ready for production deployment!
