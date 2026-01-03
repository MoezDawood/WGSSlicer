# Quick Start: Deploy to Streamlit Cloud

The fastest way to get your app online!

## Step 1: Push to GitHub

Make sure all your files are committed and pushed:

```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

## Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository**: `MoezDawood/WGSSlicer`
   - **Branch**: `main`
   - **Main file path**: `WGS_Slicer_v2.py`
5. Click **"Deploy"**

## Step 3: Access Your App

Your app will be live at: `https://your-app-name.streamlit.app`

## That's it! 🎉

Your Streamlit app is now a website. Any changes you push to GitHub will automatically update the website.

---

## Troubleshooting

### If SSH connections don't work:
- Streamlit Cloud may block outbound SSH connections
- Consider using a different hosting option (see DEPLOYMENT.md)
- Or set up a VPN/proxy solution

### If the app doesn't load:
- Check the logs in Streamlit Cloud dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify the main file path is correct

## Next Steps

- Read `DEPLOYMENT.md` for other hosting options
- Customize `.streamlit/config.toml` for your theme preferences
- Set up environment variables if needed

