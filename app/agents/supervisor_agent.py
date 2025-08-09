from pathlib import Path
from app.core.config import settings
from app.services.graph_state import AgentState
from app.llm_provider import llm  # Import the central LLM instance
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

# --- Configuration & Setup ---

# Define the structured output for reliable routing.
# This ensures the LLM's response is always machine-readable.
class RouteChoice(BaseModel):
    """The routing choice for the next action."""
    # This should list the names of your specialized agent nodes
    next_agent: str = Field(description="Must be one of ['DiagnosisAgent', 'ResponseAgent', 'end'].")

# Create the parser instance from the Pydantic model.
parser = PydanticOutputParser(pydantic_object=RouteChoice)

# --- Load Prompt Template ---

# Load the supervisor's specific prompt from its file.
# This makes your agent logic cleaner and prompts easier to manage.
try:
    PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "supervisor.txt"
    SUPERVISOR_PROMPT_TEMPLATE = PROMPT_PATH.read_text()
except FileNotFoundError:
    # A fallback to prevent crashes if the file is missing.
    print("Warning: 'supervisor.txt' not found. Using a default inline prompt.")
    SUPERVISOR_PROMPT_TEMPLATE = """
    You are a supervisor routing work to a team of agents. Based on the user's last message, choose the next agent to act.
    {format_instructions}
    The user's last message was: "{last_message}"
    """

# --- Agent Function ---

async def supervisor_agent(state: AgentState):
    """
    Decides which agent should act next using a focused prompt and a structured output parser.
    This function is asynchronous to avoid blocking the server.
    """
    print("---SUPERVISOR AGENT---")
    
    # Get the last message from the state.
    last_message = state.messages[-1].content     
    # Format the prompt template with the dynamic data from the parser and state.
    prompt = SUPERVISOR_PROMPT_TEMPLATE.format(
        last_message=last_message,
        format_instructions=parser.get_format_instructions()
    )
    
    # Asynchronously call the LLM.
    response = await llm.ainvoke(prompt)
    
    # Parse the LLM's response into our structured RouteChoice object.
    route = parser.parse(response.content)
    
    print(f"Supervisor decided: {route.next_agent}")
    
    # Return the next agent's name to the graph state.
    return {"next_agent": route.next_agent}