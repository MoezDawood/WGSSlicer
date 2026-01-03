# Deployment Guide for WGS Slicer

This guide will help you deploy your Streamlit application to various hosting platforms.

## ⚠️ Important Considerations

Your application requires SSH access to a BCM server (`10.66.4.211`). This means:
- The deployment platform must be able to establish SSH connections to this server
- Users will need to provide their BCM credentials
- The server must be accessible from your hosting platform (may require VPN or firewall configuration)

## Option 1: Streamlit Cloud (Recommended - Easiest)

Streamlit Cloud is the easiest way to deploy Streamlit apps.

### Steps:

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `MoezDawood/WGSSlicer`
   - Set the main file path: `WGS_Slicer_v2.py`
   - Click "Deploy"

3. **Configure Environment Variables** (if needed):
   - In Streamlit Cloud dashboard, go to Settings → Secrets
   - Add any required secrets (though your app uses user-provided credentials)

4. **Access your app**: Your app will be available at `https://your-app-name.streamlit.app`

### Advantages:
- ✅ Free tier available
- ✅ Automatic deployments on git push
- ✅ Easy to set up
- ✅ Built specifically for Streamlit

### Limitations:
- ⚠️ SSH connections may be restricted (test first)
- ⚠️ Free tier has resource limits

---

## Option 2: Heroku

### Prerequisites:
- Heroku account (free tier available)
- Heroku CLI installed

### Steps:

1. **Create a `Procfile`** (already created in this repo):
   ```
   web: streamlit run WGS_Slicer_v2.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`** (already created):
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Login to Heroku**:
   ```bash
   heroku login
   ```

4. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

5. **Set buildpacks**:
   ```bash
   heroku buildpacks:add heroku/python
   ```

6. **Deploy**:
   ```bash
   git push heroku main
   ```

7. **Open your app**:
   ```bash
   heroku open
   ```

---

## Option 3: Docker + Cloud Platform

Deploy using Docker for maximum flexibility.

### Steps:

1. **Build Docker image**:
   ```bash
   docker build -t wgs-slicer .
   ```

2. **Run locally** (test first):
   ```bash
   docker run -p 8501:8501 wgs-slicer
   ```

3. **Deploy to cloud**:
   - **AWS**: Use ECS or EC2
   - **Google Cloud**: Use Cloud Run or GKE
   - **Azure**: Use Container Instances or AKS
   - **DigitalOcean**: Use App Platform or Droplets

### Example: Deploy to Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/wgs-slicer

# Deploy to Cloud Run
gcloud run deploy wgs-slicer \
  --image gcr.io/YOUR_PROJECT_ID/wgs-slicer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 4: Self-Hosted Server

If you have access to a server (e.g., BCM server or your own):

### Steps:

1. **SSH into your server**:
   ```bash
   ssh user@your-server.com
   ```

2. **Clone repository**:
   ```bash
   git clone https://github.com/MoezDawood/WGSSlicer.git
   cd WGSSlicer
   ```

3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run with Streamlit**:
   ```bash
   streamlit run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0
   ```

5. **Or use a process manager** (recommended for production):
   ```bash
   # Install PM2 (Node.js process manager)
   npm install -g pm2
   
   # Create ecosystem file
   # Then run:
   pm2 start ecosystem.config.js
   ```

6. **Set up reverse proxy** (nginx example):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

---

## Option 5: Railway

Railway is a modern platform that makes deployment easy.

### Steps:

1. **Go to [Railway](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your repository**
5. **Railway will auto-detect Streamlit and deploy**

---

## Testing SSH Connectivity

Before deploying, test if your hosting platform can connect to the BCM server:

```python
import paramiko

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("10.66.4.211", username="test", password="test")
    print("✅ SSH connection successful")
    client.close()
except Exception as e:
    print(f"❌ SSH connection failed: {e}")
```

## Security Considerations

1. **Never commit credentials** to git
2. **Use environment variables** for sensitive data
3. **Consider using SSH keys** instead of passwords
4. **Implement rate limiting** to prevent abuse
5. **Add authentication** to your Streamlit app if deploying publicly

## Troubleshooting

### SSH Connection Issues
- Check if the hosting platform allows outbound SSH connections
- Verify firewall rules on the BCM server
- Consider using a VPN or SSH tunnel

### Port Issues
- Ensure the port is correctly configured
- Check firewall rules
- Some platforms require specific ports

### Memory/Resource Issues
- Large file processing may require more resources
- Consider upgrading your hosting plan
- Implement file size limits

## Need Help?

- Streamlit Community: https://discuss.streamlit.io
- Streamlit Docs: https://docs.streamlit.io
- Your repository: https://github.com/MoezDawood/WGSSlicer

