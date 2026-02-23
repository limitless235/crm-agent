from app.ai.embeddings import embeddings_manager
from app.ai.faiss_index import faiss_manager

class RAGContextBuilder:
    def build_prompt(self, user_query: str, ticket_context: list = None):
        # 1. Retrieve relevant info from FAISS (Mandatory for Phase 9.3)
        query_vector = embeddings_manager.get_embedding(user_query)
        search_results = faiss_manager.search(query_vector, k=3)
        
        retrieved_docs = [res['document'][:1000] for res in search_results]  # Truncate long docs
        doc_ids = [res['id'] for res in search_results]
        
        # 2. Add ticket context (last 5 messages only)
        history_str = ""
        if ticket_context:
            for msg in ticket_context[-5:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                content = msg.get('content', '')[:500] # Truncate history content
                history_str += f"{role}: {content}\n"

        # 3. Assemble final prompt with strict delimitation
        context_str = "\n".join([f"--- DOCUMENT {i+1} ---\n{doc}" for i, doc in enumerate(retrieved_docs)])
        
        system_instructions = (
            "You are an expert productivity agent for customer service teams. "
            "Your goal is to perform a DEEP ANALYSIS of the current situation using the provided context.\n\n"
            "=== START OF CONTEXT ===\n"
            f"{context_str if context_str else 'NO RELEVANT CONTEXT FOUND.'}\n"
            "=== END OF CONTEXT ===\n\n"
            "STRICT ANALYTICAL REQUIREMENTS (DO NOT USE PLACEHOLDERS):\n"
            "1. Answer the user's query accurately using ONLY the context.\n"
            "2. Identify the customer's sentiment (e.g. Frustrated, Neutral, Happy).\n"
            "3. Summarize the key issues based on the content of the message.\n"
            "4. Provide a 1-sentence historical summary based on the history log.\n"
            "5. Generate a professional draft response the agent can send to the customer.\n"
            "6. Extract key entities like Product Models, Serial Numbers, or Error Codes into a JSON object.\n"
            "7. Predict a Customer Satisfaction (CSAT) score from 1 (Very Frustrated) to 5 (Delighted).\n"
        )
        
        history_history = f"HISTORY:\n{history_str}\n" if history_str else ""
        user_prompt = f"USER QUERY: {user_query}\n\nASSISTANT:"
        
        prompt = system_instructions + history_history + user_prompt
        
        return prompt, doc_ids

rag_builder = RAGContextBuilder()
