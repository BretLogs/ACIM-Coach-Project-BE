# AI Coach - Backend (FastAPI)

A high-performance REST API for the AI-powered Coach Instructional Management system, built with FastAPI and AWS DynamoDB.

## Features

- **Authentication**: JWT-based authentication with secure token management
- **Client Management**: Full CRUD operations for client profiles
- **Workout Plans**: Weekly workout plan management with flexible scheduling
- **AI Integration**: Groq AI-powered coaching chatbot
- **Cloud Storage**: AWS DynamoDB for scalable data persistence
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: AWS DynamoDB
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **AI Integration**: Groq API client
- **Cloud**: AWS (DynamoDB, potential Lambda deployment)
- **Documentation**: Automatic OpenAPI generation

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration and settings
│   │   └── security.py        # JWT and password utilities
│   ├── models/                # Pydantic models
│   │   ├── auth.py            # Authentication models
│   │   ├── client.py          # Client data models
│   │   ├── plan.py            # Workout plan models
│   │   └── chat.py            # Chat/AI models
│   ├── api/                   # API endpoints
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── clients.py         # Client management endpoints
│   │   ├── plans.py           # Workout plan endpoints
│   │   └── chat.py            # AI chat endpoints
│   └── services/              # Business logic and external integrations
│       ├── db.py              # DynamoDB service
│       ├── groq_client.py     # Groq AI integration
│       └── repositories/      # Data access layer
│           ├── users_repo.py  # User data operations
│           ├── clients_repo.py # Client data operations
│           └── plans_repo.py   # Plan data operations
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.9+
- AWS Account (for DynamoDB)
- Groq API Key
- pip or poetry for dependency management

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory:
   ```env
   # Security
   SECRET_KEY=your-super-secret-key-change-in-production
   ADMIN_USERNAME=korky
   ADMIN_PASSWORD=korkabayo
   
   # AWS Configuration
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   
   # DynamoDB Tables
   DDB_TABLE_USERS=users
   DDB_TABLE_CLIENTS=clients
   DDB_TABLE_PLANS=plans
   
   # Groq AI
   GROQ_API_KEY=your-groq-api-key
   GROQ_MODEL=llama-3.1-70b-versatile
   
   # CORS (for development)
   CORS_ORIGINS=http://localhost:8081,http://localhost:19006,exp://localhost:8081
   ```

5. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Client Management

- `POST /clients` - Create new client
- `GET /clients` - List all clients
- `GET /clients/{client_id}` - Get specific client
- `PUT /clients/{client_id}` - Update client
- `DELETE /clients/{client_id}` - Delete client

### Workout Plans

- `GET /plans/weeks/{client_id}?weekOffset=0|1` - Get week plan
- `PUT /plans/weeks/{client_id}` - Save week plan

### AI Chat

- `POST /chat` - Send message to AI assistant

## Data Models

### Client Model

```json
{
  "client_id": "uuid",
  "name": "John Doe",
  "age": 30,
  "sex": "male",
  "height_cm": 180.0,
  "weight_kg": 80.0,
  "activity_level": "moderate",
  "goals": "Build muscle and lose fat",
  "bmr": 1800,
  "tdee": 2400,
  "calorie_maintenance": 2400,
  "notes": "Previous knee injury",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Week Plan Model

```json
{
  "client_id": "uuid",
  "week_start_iso": "2024-01-01",
  "days": [
    {
      "day": "Mon",
      "workouts": [
        {
          "exercise": "Bench Press",
          "sets": 3,
          "reps": 10,
          "rest_sec": 120,
          "notes": "Focus on form"
        }
      ]
    }
  ]
}
```

## Database Schema

### DynamoDB Tables

#### Users Table
- **Primary Key**: `username` (String)
- **Attributes**: `hashed_password`

#### Clients Table
- **Primary Key**: `client_id` (String)
- **Sort Key**: `username` (String)
- **Attributes**: All client fields plus timestamps

#### Plans Table
- **Primary Key**: `client_id` (String)
- **Sort Key**: `week_start_iso` (String)
- **Attributes**: `days` (List), `updated_at`

## Authentication

**Note**: Authentication has been removed for single-user deployment. All endpoints are now publicly accessible without authentication requirements.

## AI Integration

The chatbot uses Groq AI with a specialized system prompt for fitness coaching:

- **Model**: Llama 3.1 70B (configurable)
- **Context**: Fitness and nutrition coaching assistant
- **Safety**: Emphasizes safety and recommends professional consultation
- **Features**: Conversation history, usage tracking

## Deployment

### Local Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

#### Option 1: AWS Lambda (Serverless)

1. Install AWS SAM CLI
2. Configure `template.yaml` for Lambda deployment
3. Deploy with `sam deploy`

#### Option 2: Docker Container

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 3: Traditional Server

Deploy to EC2, DigitalOcean, or similar with:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AWS_REGION` | AWS region for DynamoDB | Yes | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes | - |
| `GROQ_API_KEY` | Groq AI API key | Yes | - |
| `GROQ_MODEL` | Groq model name | No | `llama-3.1-70b-versatile` |
| `DDB_TABLE_*` | DynamoDB table names | No | `clients`, `plans` |

## Development

### Code Style

- Follow PEP 8 style guidelines
- Use type hints throughout
- Document all functions and classes
- Use Pydantic models for data validation

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Setup

The application automatically creates DynamoDB tables on startup if they don't exist. For production, create tables manually with appropriate provisioning.

## Error Handling

The API includes comprehensive error handling:

- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **404**: Not Found (resource doesn't exist)
- **500**: Internal Server Error (unexpected errors)

All errors return consistent JSON format:
```json
{
  "detail": "Error description"
}
```

## Performance

- **Async/Await**: Full async support for concurrent requests
- **Connection Pooling**: Efficient database connections
- **Caching**: Consider Redis for session/token caching in production
- **Rate Limiting**: Implement rate limiting for production use

## Security

- **JWT Tokens**: Secure authentication with expiration
- **Password Hashing**: bcrypt for password security
- **CORS**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic model validation
- **SQL Injection**: Not applicable (NoSQL DynamoDB)

## Monitoring

Consider implementing:

- **Logging**: Structured logging with Python logging
- **Metrics**: CloudWatch or Prometheus metrics
- **Health Checks**: `/health` endpoint for monitoring
- **Error Tracking**: Sentry or similar error tracking

## Contributing

1. Follow the established code architecture
2. Add proper type hints and documentation
3. Include tests for new endpoints
4. Update API documentation
5. Ensure security best practices

## License

This project is part of the AI-powered Coach Instructional Management system.
