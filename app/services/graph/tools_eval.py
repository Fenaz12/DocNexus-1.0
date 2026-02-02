
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from app.services.vector_store import vector_store_service

# Remove 'UserContext' class entirely if not used elsewhere

@tool
def get_retrievel_tool(query: str, config: RunnableConfig) -> str:
    """
    Search and return information about the uploaded documents.
    """
    # Safely get the user_id from the config dictionary
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id")
    
    if not user_id:
        return "Error: User ID not found in configuration."

    print(f"🔍 Tool Execution: Searching docs for User {user_id}...")
    
    retriever = vector_store_service.get_retreiver(user_id)
    docs = retriever.invoke(query)
    
    if not docs:
        return "No relevant documents found."
    
    formatted_docs = "\n\n---\n\n".join([doc.page_content for doc in docs])
    return formatted_docs