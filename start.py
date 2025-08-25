#!/usr/bin/env python3
"""
Startup script for the AI Coach backend API.
This script initializes the database and starts the FastAPI server.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting AI Coach API...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Alternative docs at: http://localhost:8000/redoc")
    print("💻 Health check at: http://localhost:8000/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
