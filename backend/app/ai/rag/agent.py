"""
ForgeAI RAG Agent.

Uses LangChain and Google Gemini to generate answers grounded in retrieved context.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class RagAgent:
    """Agent for generating grounded answers using LLMs."""

    def __init__(self):
        """Initialize the LLM."""
        self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            google_api_key=self.settings.gemini_api_key,
            temperature=0.0, # Low temperature for strict factual answers
        )

    async def generate_answer(self, query: str, context_chunks: list[dict], chat_history: list[dict] = None) -> tuple[str, list[dict]]:
        """Generate an answer based ONLY on the provided context.

        Args:
            query: The user's question.
            context_chunks: List of retrieved chunks.
            chat_history: Previous messages in the conversation.

        Returns:
            Tuple of (Generated Answer, List of Sources).
        """
        if not context_chunks:
            return "I could not find any relevant information in your uploaded documents to answer this question.", []

        # Format context
        context_parts = []
        sources = []
        for i, chunk in enumerate(context_chunks):
            source_id = i + 1
            context_parts.append(f"--- Document [{source_id}]: {chunk['filename']} ---\n{chunk['content']}\n")
            sources.append({
                "id": source_id,
                "filename": chunk["filename"],
                "document_id": chunk["document_id"],
                "similarity": chunk["similarity"]
            })
            
        formatted_context = "\n".join(context_parts)

        # Build prompt
        system_prompt = (
            "You are ForgeAI, an enterprise AI assistant. "
            "Your task is to answer the user's question based ONLY on the provided context documents.\n\n"
            "STRICT RULES:\n"
            "1. You must only use facts from the provided context.\n"
            "2. If the answer cannot be found in the context, say EXACTLY: 'I could not find the answer to this question in the uploaded documents.'\n"
            "3. Do not use outside knowledge or hallucinate information.\n"
            "4. Cite the source document using [Document Name] when stating facts.\n"
            "5. Keep the answer concise and professional.\n\n"
            f"CONTEXT:\n{formatted_context}"
        )

        messages = [SystemMessage(content=system_prompt)]
        
        # Add history
        if chat_history:
            # Add up to last 5 messages for context window management
            for msg in chat_history[-5:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))

        # Add current query
        messages.append(HumanMessage(content=query))

        logger.info("Invoking LLM for generation")
        response = await self.llm.ainvoke(messages)
        
        return response.content, sources
