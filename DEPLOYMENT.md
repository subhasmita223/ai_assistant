# Therapist Companion - Deployment Guide

## 🚀 Deployment Options

### 1. Standalone Executable (Desktop Distribution) - RECOMMENDED

#### Building the Executable
```bash
# Run the build script
python build_executable.py
```

This creates a single `.exe` file that can be distributed to end users without requiring Python installation.

**Advantages:**
- ✅ No Python installation required on target machines
- ✅ Easy distribution via USB, email, or download
- ✅ Works on Windows machines out of the box
- ✅ Includes all dependencies

**Use Cases:**
- Personal use on different computers
- Distribution to friends/family
- Offline deployment scenarios

---

### 2. Docker Deployment (Cross-Platform)

#### Prerequisites
- Docker installed
- Docker Compose installed

#### Quick Start
```bash
# Build and run with Docker Compose
docker-compose up --build

# For headless/web version (future)
docker-compose --profile web up --build
```

#### Manual Docker Commands
```bash
# Build the image
docker build -t therapist-companion .

# Run the container (Linux with X11)
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/.env:/app/.env:ro \
  therapist-companion

# Run on Windows with X-Server (requires VcXsrv or similar)
docker run -it --rm \
  -e DISPLAY=host.docker.internal:0.0 \
  -v ${PWD}/.env:/app/.env:ro \
  therapist-companion
```

**Advantages:**
- ✅ Consistent environment across different systems
- ✅ Easy scaling and deployment
- ✅ Isolation from host system
- ✅ Version control for deployments

---

### 3. Cloud Deployment

#### AWS EC2 Deployment

1. **Launch EC2 Instance**
   ```bash
   # Ubuntu 22.04 LTS recommended
   # Instance type: t3.medium or larger
   # Security group: Allow SSH (22) and custom ports
   ```

2. **Setup on EC2**
   ```bash
   # Connect via SSH
   ssh -i your-key.pem ubuntu@your-ec2-ip

   # Install Docker
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker ubuntu

   # Clone your repository
   git clone your-repo-url
   cd therapist-companion

   # Setup environment
   echo "API=your-google-api-key" > .env

   # Deploy
   docker-compose up -d
   ```

#### Google Cloud Platform (GCP)

1. **Cloud Run Deployment** (Serverless)
   ```bash
   # Build and push to Google Container Registry
   gcloud builds submit --tag gcr.io/PROJECT-ID/therapist-companion

   # Deploy to Cloud Run
   gcloud run deploy therapist-companion \
     --image gcr.io/PROJECT-ID/therapist-companion \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

2. **Compute Engine Deployment**
   ```bash
   # Create VM instance
   gcloud compute instances create therapist-companion-vm \
     --image-family ubuntu-2204-lts \
     --image-project ubuntu-os-cloud \
     --machine-type e2-medium \
     --zone us-central1-a

   # SSH and setup (similar to EC2)
   ```

#### Azure Deployment

1. **Container Instances**
   ```bash
   # Create resource group
   az group create --name therapist-companion-rg --location eastus

   # Create container instance
   az container create \
     --resource-group therapist-companion-rg \
     --name therapist-companion \
     --image your-registry/therapist-companion \
     --cpu 2 --memory 4 \
     --restart-policy Always
   ```

#### Heroku Deployment (Alternative)
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python main.py" > Procfile

# Deploy
heroku create therapist-companion
heroku config:set API=your-google-api-key
git push heroku main
```

---

### 4. Virtual Private Server (VPS) Deployment

#### DigitalOcean Droplet
```bash
# Create Ubuntu 22.04 droplet
# SSH into droplet
ssh root@your-droplet-ip

# Install dependencies
apt update
apt install python3 python3-pip git docker.io docker-compose -y

# Clone and deploy
git clone your-repo-url
cd therapist-companion
echo "API=your-api-key" > .env
docker-compose up -d
```

#### Linode/Vultr (Similar process)
Same steps as DigitalOcean

---

## 🔧 Environment Setup

### Required Environment Variables
```env
API=your-google-gemini-api-key
```

### Optional Configuration
```env
DEBUG=true
SPEECH_ENABLED=true
DEFAULT_EXPRESSION=neutral
```

---

## 📦 Distribution Methods

### For End Users (Executable)
1. Build using `build_executable.py`
2. Distribute the `dist` folder
3. Include `install.bat` for easy installation
4. Provide user manual

### For Developers (Source Code)
1. Share repository with requirements.txt
2. Include setup instructions
3. Document API key setup
4. Provide development environment setup

### For Enterprise (Docker)
1. Push to private registry
2. Use Docker Compose for orchestration
3. Implement proper secrets management
4. Set up monitoring and logging

---

## 🛡️ Security Considerations

1. **API Key Management**
   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **Network Security**
   - Use HTTPS for all communications
   - Implement proper firewall rules
   - Use VPN for sensitive deployments

3. **Container Security**
   - Use non-root user in containers
   - Scan images for vulnerabilities
   - Keep base images updated

---

## 🔍 Monitoring and Maintenance

### Health Checks
```bash
# Check if application is running
docker ps
curl http://localhost:8080/health  # If web interface exists

# Check logs
docker logs therapist-companion
```

### Updates
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Backup
- Backup conversation histories
- Backup configuration files
- Document deployment procedures

---

## 🎯 Recommended Deployment Strategy

1. **Development**: Local Python environment
2. **Testing**: Docker containers locally
3. **Staging**: Cloud VM with Docker
4. **Production**: Managed cloud service or enterprise VPS
5. **Distribution**: Standalone executables for end users