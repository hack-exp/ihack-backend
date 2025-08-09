from app.services.graph_state import AgentState
from app.llm_provider import llm
from app.api.tools.medical_rag_tool import medical_rag_tool # <-- Import your RAG tool

async def diagnosis_agent(state: AgentState):
    """
    Uses the RAG tool to find relevant medical data and then asks the LLM
    to form a diagnosis based on that data.
    """
    print("---AGENT: DIAGNOSIS---")
    
    user_message = state.messages[-1].content

    # 1. Use the RAG tool to retrieve relevant context from your private data
    retrieved_context = medical_rag_tool.retrieve(query=user_message)

    # 2. Create a new, context-aware prompt for the LLM
    prompt = f"""You are a medical diagnosis expert.
Use ONLY the following retrieved medical records to analyze the user's symptoms and list potential conditions.
Do not use any outside knowledge.

--- RETRIEVED MEDICAL RECORDS ---
{retrieved_context}
---------------------------------

User's Symptoms: "{user_message}"

Based on the records provided, what are the most likely potential conditions?
"""

    # 3. Ask the LLM (LM Studio) to analyze the retrieved context
    response = await llm.ainvoke(prompt)
    
    print(f"Diagnosis Found: {response.content}")

    # 4. Update the state with the findings
    return {"diagnosis": response.content}