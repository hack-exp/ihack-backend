from app.services.graph_state import AgentState
from app.llm_provider import llm # Assuming you have a central llm object

async def diagnosis_agent(state: AgentState):
    """
    Analyzes the user's message to identify potential medical conditions.
    """
    print("---AGENT: DIAGNOSIS---")
    
    # THE FIX: Use dot notation to access the messages list
    user_message = state.messages[-1].content

    # Create a focused prompt for this specific task
    prompt = f"""
You are a medical diagnosis expert. Analyze the following user message to identify key symptoms and list potential medical conditions.
Do not generate a full response. Simply list the possible conditions.

User message: "{user_message}"

Potential Conditions:
"""

    response = await llm.ainvoke(prompt)
    
    print(f"Diagnosis Found: {response.content}")

    # Update the state with the findings from this agent
    return {"diagnosis": response.content}