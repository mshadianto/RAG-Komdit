"""
Multi-Agent System for RAG Komite Audit
Implements specialized expert agents for different audit committee topics
"""
import time
from typing import List, Dict, Optional, Tuple
import logging
from backend.llm_client import llm_client, glm_client
from backend.embeddings import embedding_manager
from backend.database import db
from config.config import settings, AGENT_ROLES, SYSTEM_PROMPTS

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

class ExpertAgent:
    """Base class for expert agents"""
    
    def __init__(self, agent_key: str):
        self.agent_key = agent_key
        self.config = AGENT_ROLES.get(agent_key, {})
        self.name = self.config.get("name", "Unknown Agent")
        self.description = self.config.get("description", "")
        self.expertise = self.config.get("expertise", [])
        logger.info(f"Expert Agent initialized: {self.name}")
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for this expert agent"""
        expertise_list = "\n".join([f"- {exp}" for exp in self.expertise])
        
        return f"""Anda adalah {self.name}, seorang expert dalam bidang Komite Audit.

Deskripsi: {self.description}

Area Expertise Anda:
{expertise_list}

Tugas Anda:
1. Jawab pertanyaan dengan akurat berdasarkan konteks yang diberikan
2. Gunakan pengetahuan expertise Anda untuk memberikan insights mendalam
3. Jika informasi tidak tersedia dalam konteks, gunakan pengetahuan umum Anda dengan jelas menyebutkannya
4. Berikan contoh praktis dan best practices jika relevan
5. Gunakan bahasa Indonesia yang profesional dan mudah dipahami

Format Jawaban:
- Jawab langsung pertanyaan dengan jelas
- Gunakan paragraf untuk penjelasan, bukan bullet points kecuali diminta
- Sertakan referensi ke konteks jika tersedia
- Tambahkan insights tambahan yang relevan dengan expertise Anda"""
    
    async def process_query(
        self,
        query: str,
        context: List[str] = None,
        conversation_history: List[Dict] = None
    ) -> Tuple[str, int, int]:
        """
        Process query and return response
        Returns: (response, execution_time_ms, tokens_used)
        """
        start_time = time.time()
        
        try:
            system_prompt = self._build_system_prompt()
            
            response = await llm_client.generate_with_context(
                system_prompt=system_prompt,
                user_query=query,
                context=context,
                conversation_history=conversation_history
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            tokens_used = llm_client.count_tokens(response)
            
            logger.info(f"{self.name} processed query in {execution_time}ms")
            return response, execution_time, tokens_used
            
        except Exception as e:
            logger.error(f"Error in {self.name} processing: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            return f"Error processing query: {str(e)}", execution_time, 0

class QueryRouter:
    """Routes queries to appropriate expert agents using GLM (with Groq fallback)"""

    def __init__(self):
        self.system_prompt = SYSTEM_PROMPTS["query_router"]
        self.use_glm = glm_client.client is not None
        logger.info(f"Query Router initialized (using {'GLM' if self.use_glm else 'Groq'} for routing)")

    async def route(self, query: str) -> Dict:
        """Route query to appropriate agent(s) - uses GLM if available, falls back to Groq"""
        try:
            if self.use_glm:
                # Use GLM for routing (faster and cheaper)
                routing_decision = await glm_client.route_query(
                    query=query,
                    system_prompt=self.system_prompt
                )
            else:
                # Fallback to Groq if GLM not configured
                routing_decision = await llm_client.route_query(
                    query=query,
                    system_prompt=self.system_prompt
                )
            return routing_decision
        except Exception as e:
            logger.error(f"Error routing query: {str(e)}")
            return {
                "primary_agent": "charter_expert",
                "secondary_agents": [],
                "reasoning": "Default routing due to error"
            }

class ResponseSynthesizer:
    """Synthesizes responses from multiple agents"""
    
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPTS["synthesizer"]
        logger.info("Response Synthesizer initialized")
    
    async def synthesize(
        self,
        query: str,
        agent_responses: Dict[str, str]
    ) -> str:
        """Synthesize multiple agent responses"""
        try:
            if len(agent_responses) == 1:
                # If only one agent, return its response directly
                return list(agent_responses.values())[0]
            
            synthesized = await llm_client.synthesize_responses(
                query=query,
                agent_responses=agent_responses,
                system_prompt=self.system_prompt
            )
            return synthesized
            
        except Exception as e:
            logger.error(f"Error synthesizing responses: {str(e)}")
            # Fallback: concatenate responses
            return "\n\n---\n\n".join([
                f"**{agent}:**\n{response}"
                for agent, response in agent_responses.items()
            ])

class AgentOrchestrator:
    """Orchestrates the multi-agent system"""
    
    def __init__(self):
        self.router = QueryRouter()
        self.synthesizer = ResponseSynthesizer()
        self.agents = {
            key: ExpertAgent(key) 
            for key in AGENT_ROLES.keys()
        }
        logger.info("Agent Orchestrator initialized with all expert agents")
    
    async def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> Tuple[List[str], List[str], List[float]]:
        """
        Retrieve relevant context from vector store
        Returns: (contexts, document_ids, similarity_scores)
        """
        try:
            # Generate query embedding
            query_embedding = embedding_manager.generate_embedding(query)
            
            # Search similar chunks
            results = await db.similarity_search(
                query_embedding=query_embedding,
                match_threshold=similarity_threshold,
                match_count=top_k
            )
            
            if not results:
                logger.warning("No context found for query")
                return [], [], []
            
            contexts = []
            document_ids = []
            similarity_scores = []
            
            for result in results:
                contexts.append(result["content"])
                document_ids.append(result["document_id"])
                similarity_scores.append(result["similarity"])
            
            logger.info(f"Retrieved {len(contexts)} context chunks")
            return contexts, document_ids, similarity_scores
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return [], [], []
    
    async def process_query(
        self,
        query: str,
        session_id: str,
        use_context: bool = True,
        max_agents: int = 2
    ) -> Dict:
        """
        Process query through the multi-agent system
        Returns complete response with metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Route query
            logger.info(f"Processing query: {query[:100]}...")
            routing = await self.router.route(query)
            
            # Step 2: Retrieve context if enabled
            contexts = []
            document_ids = []
            similarity_scores = []
            
            if use_context:
                contexts, document_ids, similarity_scores = await self.retrieve_context(query)
            
            # Step 3: Get conversation history
            conversation_history = await db.get_conversation_history(session_id, limit=5)
            
            # Step 4: Query relevant agents
            agents_to_query = [routing["primary_agent"]]
            if routing.get("secondary_agents"):
                agents_to_query.extend(routing["secondary_agents"][:max_agents-1])
            
            agent_responses = {}
            agent_logs = []
            
            for agent_key in agents_to_query:
                if agent_key in self.agents:
                    agent = self.agents[agent_key]
                    response, exec_time, tokens = await agent.process_query(
                        query=query,
                        context=contexts,
                        conversation_history=conversation_history
                    )
                    agent_responses[agent.name] = response
                    agent_logs.append({
                        "agent_name": agent.name,
                        "agent_key": agent_key,
                        "execution_time_ms": exec_time,
                        "tokens_used": tokens,
                        "status": "success"
                    })
            
            # Step 5: Synthesize responses if multiple agents
            if len(agent_responses) > 1:
                final_response = await self.synthesizer.synthesize(query, agent_responses)
            else:
                final_response = list(agent_responses.values())[0] if agent_responses else "Maaf, tidak dapat memproses pertanyaan."
            
            # Step 6: Calculate total processing time
            total_time = int((time.time() - start_time) * 1000)
            
            # Step 7: Save to database
            conversation = await db.create_conversation(
                session_id=session_id,
                user_query=query,
                agent_response=final_response,
                agents_used=list(agent_responses.keys()),
                context_documents=document_ids,
                similarity_scores=similarity_scores,
                processing_time_ms=total_time
            )
            
            # Step 8: Log agent executions
            if conversation:
                for log in agent_logs:
                    await db.log_agent_execution(
                        conversation_id=conversation["id"],
                        agent_name=log["agent_name"],
                        agent_role=log["agent_key"],
                        input_text=query,
                        output_text=agent_responses.get(log["agent_name"], ""),
                        execution_time_ms=log["execution_time_ms"],
                        tokens_used=log["tokens_used"],
                        status=log["status"]
                    )
            
            logger.info(f"Query processed successfully in {total_time}ms")
            
            return {
                "success": True,
                "response": final_response,
                "agents_used": list(agent_responses.keys()),
                "routing_reasoning": routing.get("reasoning", ""),
                "context_count": len(contexts),
                "processing_time_ms": total_time,
                "conversation_id": conversation["id"] if conversation else None,
                "metadata": {
                    "document_ids": document_ids,
                    "similarity_scores": similarity_scores,
                    "agent_responses": agent_responses if len(agent_responses) > 1 else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "success": False,
                "response": f"Terjadi kesalahan dalam memproses pertanyaan: {str(e)}",
                "agents_used": [],
                "error": str(e)
            }

# Global orchestrator instance
orchestrator = AgentOrchestrator()
