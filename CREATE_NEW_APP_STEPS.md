# Create New App - Exact Steps

## Step 1: Click "Create app" Button
- Look at the top right of your Streamlit Cloud dashboard
- Click the blue **"Create app"** button

## Step 2: Fill in the Form

When the form appears, enter these EXACT values:

### Repository
- Click the dropdown
- Select: **`MoezDawood/WGSSlicer`**

### Branch
- Select: **`main`**

### Main file path
- **IMPORTANT**: Type exactly: `WGS_Slicer_v2.py`
- (NOT `streamlit_app.py` - that's why the old app doesn't work!)

### App URL (optional)
- You can leave the default or customize it
- Example: `wgs-slicer-v2` or `wgsslicer`

## Step 3: Click "Deploy"
- Click the **"Deploy"** button
- Wait 1-2 minutes

## Step 4: Your App Will Be Live!
- You'll see a success message
- Your app URL will be: `https://[your-app-name].streamlit.app`
- Click it to open your website!

---

## ⚠️ Important Differences from Old App

Your old app probably used:
- Main file: `streamlit_app.py` ❌

Your NEW app should use:
- Main file: `WGS_Slicer_v2.py` ✅

This is the key difference!

---

## What You'll See During Deployment

1. **Initializing...** - Setting up the environment
2. **Installing dependencies...** - Installing from requirements.txt
3. **Starting app...** - Launching Streamlit
4. **✅ Deployed!** - Your app is live!

If you see any errors, check the logs that appear during deployment.

