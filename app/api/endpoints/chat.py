import uvicorn
import os
from fastapi import FastAPI, HTTPException,APIRouter
from pydantic import BaseModel
# IMPORTANT: You will need to install langchain-groq for this to work
# pip install langchain-groq
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.core.config import settings
# --- Configuration ---
# It's best practice to load secrets like API keys from environment variables.
# We will get the Groq API key from an environment variable named "GROQ_API_KEY".
router = APIRouter()
try:
    GROQ_API_KEY = settings.GROQ_API_KEY
except KeyError:
    # If the environment variable is not set, raise an error.
    raise EnvironmentError("GROQ_API_KEY environment variable not set. Please set it before running the application.")

# Specify the model you want to use from Groq. Llama3 is a great choice.
LLM_MODEL_NAME = "llama3-8b-8192"


# --- FastAPI Application ---

# Initialize the FastAPI app
app = FastAPI(
    title="Groq LLM Connector",
    description="An API to connect to the Groq API for fast LLM inference."
)

# Define the data model for the request body
class ChatRequest(BaseModel):
    message: str

# Initialize the LangChain ChatGroq instance
try:
    llm = ChatGroq(
        model=LLM_MODEL_NAME,
        api_key=GROQ_API_KEY
    )
    print(f"Successfully configured to connect to Groq with model: {LLM_MODEL_NAME}")
except Exception as e:
    print(f"Failed to configure Groq connection. Error: {e}")
    llm = None

# Define the API endpoint for chatting
@router.post("/chat")
async def chat_with_llm(request: ChatRequest):
    """
    Receives a message and sends it to the configured Groq LLM.
    """
    if not llm:
        raise HTTPException(
            status_code=503, 
            detail="LLM service is not available. Check your Groq configuration."
        )
    
    print(f"Sending message to Groq: '{request.message}'")
    
    try:
        # Create the message payload for LangChain
        messages = [HumanMessage(content=request.message)]
        
        # Send the message to the LLM and get the response
        response = llm.invoke(messages)
        
        print(f"Received response from Groq: '{response.content}'")
        
        return {"response": response.content}

    except Exception as e:
        # Handle potential errors during the request
        print(f"An error occurred while communicating with Groq: {e}")
        raise HTTPException(status_code=500, detail=f"Error communicating with Groq: {e}")