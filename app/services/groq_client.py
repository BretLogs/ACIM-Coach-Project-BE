from groq import Groq
from app.core.config import settings
from app.models.chat import ChatMessage, ChatRequest, ChatResponse
from typing import List

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        
        self.system_prompt = """You are a helpful gym and dietary coaching assistant. Provide safe, concise, goal-oriented guidance for fitness and nutrition.

Key guidelines:
- Focus on evidence-based recommendations
- Keep responses practical and actionable
- Avoid medical claims or diagnoses
- Suggest consulting healthcare professionals for medical conditions
- Prioritize safety in all exercise recommendations
- Be encouraging and supportive

You help with:
- Workout programming and exercise selection
- Basic nutrition and meal planning
- Form cues and exercise technique
- Recovery and injury prevention
- Goal setting and motivation

Always prioritize safety and proper form over intensity."""

    def send_message(self, request: ChatRequest) -> ChatResponse:
        try:
            # Prepare messages for Groq API
            messages = []
            
            # Add system prompt if not already present
            has_system = any(msg.role == "system" for msg in request.conversation_history)
            if not has_system:
                messages.append({"role": "system", "content": self.system_prompt})
            
            # Add conversation history
            for msg in request.conversation_history:
                messages.append({"role": msg.role, "content": msg.content})
            
            # Add user input
            messages.append({"role": "user", "content": request.user_input})
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            updated_history = request.conversation_history.copy()
            updated_history.append(ChatMessage(role="user", content=request.user_input))
            updated_history.append(ChatMessage(role="assistant", content=assistant_response))
            
            # Prepare usage info
            usage = None
            if hasattr(response, 'usage'):
                usage = {
                    "tokens_in": response.usage.prompt_tokens,
                    "tokens_out": response.usage.completion_tokens
                }
            
            return ChatResponse(
                response=assistant_response,
                conversation_history=updated_history,
                usage=usage
            )
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

# Global instance
groq_service = GroqService()
