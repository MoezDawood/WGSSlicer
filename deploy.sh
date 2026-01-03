#!/bin/bash

echo "🚀 Preparing to deploy WGS Slicer to Streamlit Cloud..."
echo ""

# Check if changes are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Update deployment files"
fi

echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to https://share.streamlit.io/"
    echo "2. Sign in with your GitHub account"
    echo "3. Click 'New app'"
    echo "4. Select repository: MoezDawood/WGSSlicer"
    echo "5. Set main file path: WGS_Slicer_v2.py"
    echo "6. Click 'Deploy'"
    echo ""
    echo "Your app will be live at: https://your-app-name.streamlit.app"
else
    echo ""
    echo "❌ Push failed. Please push manually:"
    echo "   git push origin main"
fi

