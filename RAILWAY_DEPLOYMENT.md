# Railway Deployment Guide

This guide will walk you through deploying your AI Coach API to Railway, including setting up PostgreSQL database and deploying the FastAPI application.

## 🚂 What is Railway?

Railway is a modern platform that makes it easy to deploy applications and databases. It provides:
- **PostgreSQL Database**: Managed PostgreSQL with automatic backups
- **Application Deployment**: Simple Git-based deployments
- **Environment Variables**: Secure environment variable management
- **Custom Domains**: Easy domain configuration
- **SSL Certificates**: Automatic HTTPS

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Git Repository**: Your code should be in a Git repository
3. **Railway CLI** (optional): Install for local development

## 🚀 Step-by-Step Deployment

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Python project

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

### Step 3: Configure Environment Variables

In your Railway project dashboard, go to "Variables" and add:

```bash
# Security
SECRET_KEY=your-super-secret-key-here
ADMIN_USERNAME=korky
ADMIN_PASSWORD=korkabayo

# CORS (optional)
CORS_ORIGINS=https://your-frontend-domain.com

# Groq API
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-8b-8192

# Database (automatically set by Railway)
DATABASE_URL=postgresql://...
```

### Step 4: Deploy Your Application

1. Railway will automatically deploy when you push to your main branch
2. Or you can manually trigger a deployment from the dashboard
3. Railway will use the `railway.json` configuration

### Step 5: Access Your Application

1. Go to your project dashboard
2. Click on your deployed service
3. You'll see your application URL (e.g., `https://your-app.railway.app`)
4. Test your API at `https://your-app.railway.app/docs`

## 🔧 Local Development Setup

### Install Railway CLI

```bash
npm install -g @railway/cli
```

### Login to Railway

```bash
railway login
```

### Link Your Project

```bash
railway link
```

### Run Locally with Railway Environment

```bash
railway run python -m uvicorn app.main:app --reload
```

## 📊 Database Management

### View Database

1. Go to your Railway project
2. Click on your PostgreSQL database
3. Use the built-in database viewer or connect with a database client

### Database Migrations

Railway automatically creates tables on startup, but you can also use Alembic for migrations:

```bash
# Install alembic
pip install alembic

# Initialize alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

## 🔒 Security Best Practices

### Environment Variables

- Never commit sensitive data to Git
- Use Railway's environment variable management
- Rotate secrets regularly

### Database Security

- Railway automatically handles database security
- Use connection pooling for production
- Regular backups are automatic

## 📈 Monitoring and Logs

### View Logs

1. Go to your Railway project
2. Click on your service
3. Go to "Logs" tab
4. View real-time application logs

### Health Checks

Your application includes a health check endpoint at `/health` that Railway uses to monitor your service.

## 🔄 Continuous Deployment

Railway automatically deploys when you push to your main branch. You can also:

1. **Manual Deploy**: Trigger deployments from the dashboard
2. **Preview Deployments**: Deploy from pull requests
3. **Rollback**: Easily rollback to previous versions

## 💰 Pricing

Railway offers:
- **Free Tier**: $5 credit monthly
- **Pro Plan**: Pay-as-you-go pricing
- **Team Plan**: Collaborative features

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check `DATABASE_URL` environment variable
   - Ensure PostgreSQL service is running

2. **Build Failures**
   - Check `requirements.txt` for missing dependencies
   - Verify Python version compatibility

3. **Application Crashes**
   - Check application logs
   - Verify environment variables are set correctly

### Getting Help

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Support](https://railway.app/support)

## 🎉 Next Steps

After successful deployment:

1. **Test Your API**: Visit `/docs` to test all endpoints
2. **Set Up Custom Domain**: Configure your own domain
3. **Monitor Performance**: Use Railway's built-in monitoring
4. **Set Up Alerts**: Configure notifications for issues
5. **Scale Up**: Upgrade your plan as needed

## 🔗 Useful Links

- [Railway Dashboard](https://railway.app/dashboard)
- [Railway CLI Documentation](https://docs.railway.app/develop/cli)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

Your AI Coach API is now ready to run on Railway! 🚂✨
