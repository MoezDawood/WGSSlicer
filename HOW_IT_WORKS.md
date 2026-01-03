# How the App Works - Architecture Explained

## The Flow

1. **You deploy the Streamlit app** on the BCM server (10.66.4.211:8501)
2. **Users access the website** at `http://10.66.4.211:8501` from their browser
3. **Users see a login page** in the web browser (no SSH needed!)
4. **Users enter their BCM username/password** in the web form
5. **The app uses those credentials** to SSH into the BCM data server and fetch files
6. **Users interact with the app** through the web browser

## Important Points

- ✅ Users do NOT need to SSH to the server
- ✅ Users just open the website in their browser
- ✅ The login happens in the web browser
- ✅ The app handles all the SSH connections server-side

## Current Issue

If you can't access `http://10.66.4.211:8501`, it's likely:
1. **Firewall blocking port 8501** (even though it's not in use)
2. **App not actually running** on 8501
3. **Network routing issue**

Let's verify what's happening.

