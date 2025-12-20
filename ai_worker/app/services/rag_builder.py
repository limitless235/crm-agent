from app.services.vector_store import vector_service

class RAGContextBuilder:
    def build_prompt(self, user_query: str, ticket_context: list = None):
        # 1. Retrieve relevant info
        search_results = vector_service.query(user_query, n_results=3)
        retrieved_docs = search_results.get('documents', [[]])[0]
        
        # 2. Add ticket context (conversation history)
        history_str = ""
        if ticket_context:
            for msg in ticket_context:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_str += f"{role}: {msg.get('content')}\n"

        # 3. Assemble final prompt
        system_prompt = (
            "You are a helpful senior AI support engineer. "
            "Use the provided context to answer the user query. "
            "If the information is not in the context, say you don't know but offer general assistance.\n"
            "CONTEXT:\n" + "\n".join(retrieved_docs) + "\n\n"
            "HISTORY:\n" + history_str + "\n"
        )
        
        user_prompt = f"USER QUERY: {user_query}\n\nASSISTANT:"
        
        return system_prompt + user_prompt

rag_builder = RAGContextBuilder()
