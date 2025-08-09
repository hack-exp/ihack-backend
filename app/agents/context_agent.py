from app.services.graph_state import AgentState
from app.llm_provider import llm
import datetime

async def context_agent(state: AgentState):
    """
    Adds local and temporal context to the diagnosis.
    """
    print("---AGENT: CONTEXT---")

    # THE FIX: Access the attribute directly.
    # Pydantic handles the default value if it's None.
    diagnosis = state.diagnosis or "No diagnosis available."

    current_date = datetime.date.today().strftime("%B %Y")
    location = "Cheruthuruthi, Kerala, India"

    prompt = f"""
You are a public health expert. The initial diagnosis suggests: "{diagnosis}".
How might the current location ({location}) and time ({current_date}, post-monsoon season) influence these conditions?
Provide a brief, one-paragraph analysis.

Contextual Analysis:
"""

    response = await llm.ainvoke(prompt)

    print(f"Context Found: {response.content}")

    return {"context": response.content}
