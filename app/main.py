from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.db_railway import db_service
from app.api import clients, plans, chat, sessions

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered Coach Instructional Management API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        db_service.create_tables_if_not_exist()
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    try:
        db_service.close()
        print("Database connection closed")
    except Exception as e:
        print(f"Error closing database: {e}")

@app.get("/")
async def root():
    return {
        "message": "AI Coach API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
