"""
LLM Client for RAG Komite Audit System
Handles communication with Groq API
"""
from groq import Groq
from typing import List, Dict, Optional
import json
import logging
from config.config import settings

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with Groq API"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.temperature = settings.AGENT_TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        logger.info(f"LLM Client initialized with model: {self.model}")
    
    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
        json_mode: bool = False
    ) -> str:
        """Generate completion from Groq API"""
        try:
            response_format = {"type": "json_object"} if json_mode else None
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                response_format=response_format
            )
            
            response = chat_completion.choices[0].message.content
            return response
            
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise
    
    async def generate_with_context(
        self,
        system_prompt: str,
        user_query: str,
        context: List[str] = None,
        conversation_history: List[Dict] = None,
        temperature: float = None
    ) -> str:
        """Generate completion with context and conversation history"""
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    messages.append({
                        "role": "user",
                        "content": msg.get("user_query", "")
                    })
                    if msg.get("agent_response"):
                        messages.append({
                            "role": "assistant",
                            "content": msg.get("agent_response", "")
                        })
            
            # Build user message with context
            user_message = user_query
            if context:
                context_text = "\n\n---\n\n".join([
                    f"[Context {i+1}]\n{ctx}" 
                    for i, ctx in enumerate(context)
                ])
                user_message = f"""Konteks Referensi:
{context_text}

---

Pertanyaan: {user_query}

Jawab berdasarkan konteks di atas. Jika informasi tidak tersedia dalam konteks, jelaskan berdasarkan pengetahuan umum tentang Komite Audit dan sebutkan bahwa ini adalah pengetahuan umum."""
            
            messages.append({"role": "user", "content": user_message})
            
            response = await self.generate_completion(
                messages=messages,
                temperature=temperature
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating with context: {str(e)}")
            raise
    
    async def route_query(
        self,
        query: str,
        system_prompt: str
    ) -> Dict:
        """Route query to appropriate agent"""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Pertanyaan: {query}"}
            ]
            
            response = await self.generate_completion(
                messages=messages,
                json_mode=True
            )
            
            routing_decision = json.loads(response)
            logger.info(f"Query routed to: {routing_decision.get('primary_agent')}")
            return routing_decision
            
        except Exception as e:
            logger.error(f"Error routing query: {str(e)}")
            # Return default routing on error
            return {
                "primary_agent": "charter_expert",
                "secondary_agents": [],
                "reasoning": "Error in routing, using default agent"
            }
    
    async def synthesize_responses(
        self,
        query: str,
        agent_responses: Dict[str, str],
        system_prompt: str
    ) -> str:
        """Synthesize multiple agent responses into coherent answer"""
        try:
            # Build synthesis prompt
            responses_text = "\n\n".join([
                f"=== {agent_name} ===\n{response}"
                for agent_name, response in agent_responses.items()
            ])
            
            synthesis_prompt = f"""Berdasarkan insights dari berbagai expert agents berikut:

{responses_text}

Pertanyaan original: {query}

Tugas Anda: Sintesiskan informasi di atas menjadi jawaban yang komprehensif, koheren, dan mudah dipahami."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": synthesis_prompt}
            ]
            
            synthesized_response = await self.generate_completion(messages=messages)
            logger.info("Responses synthesized successfully")
            return synthesized_response
            
        except Exception as e:
            logger.error(f"Error synthesizing responses: {str(e)}")
            # Return concatenated responses on error
            return "\n\n".join(agent_responses.values())
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)"""
        # Rough estimation: 1 token ≈ 4 characters for English/Indonesian mix
        return len(text) // 4

# Global LLM client instance
llm_client = LLMClient()
