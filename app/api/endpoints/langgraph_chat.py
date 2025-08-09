from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.graph_builder import build_graph
from langchain_core.messages import SystemMessage, HumanMessage
from pathlib import Path
import datetime
import json
from app.services.graph_builder import GraphNodes
# --- Pydantic Model for the Request Body ---
class GraphRequest(BaseModel):
    message: str

# --- Router Setup ---
router = APIRouter()
graph = build_graph()

# --- Load the CORRECT Prompt Template ---
# Load the main system prompt, not the supervisor's.
PROMPT_TEMPLATE_PATH = Path(__file__).parent.parent.parent / "prompts" / "stellar_ai_system.txt"
try:
    STELLAR_AI_PROMPT_TEMPLATE = PROMPT_TEMPLATE_PATH.read_text()
except FileNotFoundError:
    print("CRITICAL ERROR: 'stellar_ai_system.txt' not found.")
    STELLAR_AI_PROMPT_TEMPLATE = "Error: System prompt file not found."

# --- API Endpoint ---
@router.post("/invoke")
async def invoke_graph(request: GraphRequest):
    """
    Invokes the LangGraph agent with a user message and streams the response.
    """
    if "Error" in STELLAR_AI_PROMPT_TEMPLATE:
        return Response(content="Server configuration error: System prompt not found.", status_code=500)

    # --- 1. Format the main system prompt with dynamic data ---
    system_prompt_text = STELLAR_AI_PROMPT_TEMPLATE.format(
        # Make sure your stellar_ai_system.txt has these placeholders
        user_message=request.message,
        current_time=datetime.datetime.now().isoformat(),
        current_location="Cheruthuruthi, Kerala, India" # This can be made dynamic later
    )
    
    # --- 2. Create the initial messages for the graph ---
    initial_messages = [
        SystemMessage(content=system_prompt_text),
        HumanMessage(content=request.message)
    ]
    
    # THE FIX IS HERE:
    # You must provide all required fields for the initial state.
    inputs = {
        "messages": initial_messages,
        "next_agent": GraphNodes.SUPERVISOR # Set the starting agent
    }
    
    # --- 3. Add the missing streaming logic ---
    async def event_stream():
        """
        Runs the graph and yields the final response content as Server-Sent Events.
        """
        try:
            # astream_events is the best way to get detailed events from the graph
            async for event in graph.astream_events(inputs, version="v1"):
                kind = event["event"]
                # We listen for the end of the 'ResponseAgent' node's execution
                if kind == "on_chain_end" and event["name"] == "ResponseAgent":
                    # The final AI message is in the output of this node
                    response_content = event["data"]["output"]["messages"][-1].content
                    
                    # Stream the content as a JSON object
                    yield f"data: {json.dumps({'response': response_content})}\n\n"
            
            # Signal that the stream is complete
            yield "data: [DONE]\n\n"
        except Exception as e:
            print(f"Error during graph execution: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")