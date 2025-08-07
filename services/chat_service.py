"""
Chat service for handling AI chat functionality using OpenRouter API
"""
import os
import json
import aiohttp
from typing import Dict, Any
from fastapi import HTTPException


class ChatService:
    """Service for AI chat operations using OpenRouter API"""
    
    @staticmethod
    async def chat_with_llama(user_message: str) -> Dict[str, Any]:
        """
        Send a message to Llama 3.3 70B via OpenRouter API
        
        Args:
            user_message: The user's message to send to the AI
            
        Returns:
            dict: Response containing the AI's reply and model info
            
        Raises:
            HTTPException: If there's an error with the API call
        """
        try:
            if not user_message:
                raise HTTPException(status_code=400, detail="Message is required")
            
            # Get API key from environment
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
            
            # Prepare the request to OpenRouter
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://fastopp.local",  # Replace with your domain
                "X-Title": "FastOpp AI Demo"
            }
            
            payload = {
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant. Provide clear, concise, "
                            "and accurate responses. Be friendly and engaging in your "
                            "communication style."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # Make request to OpenRouter
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise HTTPException(status_code=500, detail=f"OpenRouter API error: {error_text}")
                    
                    result = await response.json()
                    
                    # Extract the assistant's response
                    assistant_message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    return {
                        "response": assistant_message,
                        "model": "meta-llama/llama-3.3-70b-instruct:free"
                    }
                    
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 