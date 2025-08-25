#!/bin/bash

# Railway Deployment Script
# This script helps you deploy your AI Coach API to Railway

echo "🚂 Railway Deployment Script"
echo "============================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed."
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please log in to Railway..."
    railway login
fi

# Check if project is linked
if [ ! -f ".railway" ]; then
    echo "🔗 Linking project to Railway..."
    railway link
fi

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment completed!"
echo "📝 Next steps:"
echo "   1. Go to your Railway dashboard"
echo "   2. Add a PostgreSQL database"
echo "   3. Configure environment variables"
echo "   4. Test your API at the provided URL"
