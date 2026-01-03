# Deploy to Streamlit Cloud - Step by Step

## ✅ Step 1: Push Code to GitHub

Your code is already committed! Now push it to GitHub:

**Option A: Using Terminal (if you have GitHub CLI or SSH keys set up)**
```bash
git push origin main
```

**Option B: Using GitHub Desktop**
1. Open GitHub Desktop
2. Click "Push origin" button

**Option C: Manual Push**
If authentication fails, you may need to:
1. Set up a Personal Access Token: https://github.com/settings/tokens
2. Or use SSH keys instead of HTTPS

---

## ✅ Step 2: Deploy to Streamlit Cloud

I've opened Streamlit Cloud in your browser. Follow these steps:

### 2.1 Sign In
- Click "Continue to sign-in" button
- Sign in with your **GitHub account** (the same one that owns the WGSSlicer repository)

### 2.2 Create New App
After signing in:
1. Click **"New app"** button (usually in the top right or on the main dashboard)
2. You'll see a form with these fields:
   - **Repository**: Select `MoezDawood/WGSSlicer`
   - **Branch**: Select `main`
   - **Main file path**: Enter `WGS_Slicer_v2.py`
   - **App URL** (optional): Leave default or customize

### 2.3 Deploy
1. Click **"Deploy"** button
2. Wait for the deployment to complete (usually 1-2 minutes)
3. Your app will be live!

---

## ✅ Step 3: Access Your Website

Once deployed, your app will be available at:
```
https://[your-app-name].streamlit.app
```

You can find the exact URL in the Streamlit Cloud dashboard.

---

## 🔧 Configuration

The app is already configured with:
- ✅ `.streamlit/config.toml` - Streamlit settings
- ✅ `requirements.txt` - All dependencies
- ✅ Proper file structure

---

## ⚠️ Important Notes

### SSH Connection Issue
Your app connects to BCM server via SSH. Streamlit Cloud may block outbound SSH connections. If you see connection errors:

1. **Test the connection** - Try logging in through the app
2. **Alternative solutions**:
   - Use Railway.app (often allows SSH)
   - Deploy on a BCM server directly
   - Set up a VPN/proxy solution

### Environment Variables
If you need to set environment variables:
1. Go to your app in Streamlit Cloud dashboard
2. Click **"Settings"** → **"Secrets"**
3. Add secrets in TOML format

---

## 🐛 Troubleshooting

### App won't deploy
- Check that `WGS_Slicer_v2.py` exists in the root directory
- Verify `requirements.txt` has all dependencies
- Check the logs in Streamlit Cloud dashboard

### App deploys but shows errors
- Check the app logs (click "Manage app" → "Logs")
- Verify all files are pushed to GitHub
- Ensure `annotatedcsvheaders.csv` is in the repository

### SSH connection fails
- This is expected if Streamlit Cloud blocks SSH
- Consider alternative hosting (see DEPLOYMENT.md)

---

## 📞 Need Help?

- Streamlit Community: https://discuss.streamlit.io
- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud

