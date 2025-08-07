"""
Chat routes for AI chat functionality
"""
from fastapi import APIRouter, Request
from services.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
async def chat_with_llama(request: Request):
    """Chat endpoint using OpenRouter API with Llama 3.3 70B"""
    import json
    
    try:
        # Get the request body
        body = await request.json()
        user_message = body.get("message", "")
        
        if not user_message:
            return {"error": "Message is required"}, 400
        
        # Use service to handle chat
        response = await ChatService.chat_with_llama(user_message)
        return response
        
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}, 400
    except Exception as e:
        return {"error": f"Internal server error: {str(e)}"}, 500 