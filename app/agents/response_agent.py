from pathlib import Path
from app.services.graph_state import AgentState
from app.llm_provider import llm
from langchain_core.messages import AIMessage

# Load the main system prompt template once
PROMPT_TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "stellar_ai_system.txt"
STELLAR_AI_PROMPT_TEMPLATE = PROMPT_TEMPLATE_PATH.read_text()

async def response_agent(state: AgentState):
    """
    Synthesizes all collected information into a final, structured response for the user.
    """
    print("---AGENT: RESPONSE---")

    # --- THE FIX IS HERE ---
    # Access attributes directly using dot notation.
    # Use 'or' to provide a default value if the attribute is None.
    user_message = state.messages[-1].content
    diagnosis = state.diagnosis or "Not determined."
    context = state.context or "No specific local context available."

    # This prompt synthesizes the collected data for the final LLM call.
    synthesis_prompt = f"""
You are Stellar AI. You have performed an internal analysis. Now, generate the final user-facing response based on this data.
Follow the XML schema and persona rules from your main system prompt.

INTERNAL ANALYSIS:
- User's Query: "{user_message}"
- Initial Diagnosis possibilities: "{diagnosis}"
- Public Health Context: "{context}"

Now, generate the complete and final <consultation> response.
"""

    final_response = await llm.ainvoke(synthesis_prompt)

    print(f"Final Response Generated:\n{final_response.content}")

    # Append the new AI message to the existing list of messages
    new_messages = state.messages + [AIMessage(content=final_response.content)]
    
    # Return the updated messages list
    return {"messages": new_messages}