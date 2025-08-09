from langchain_groq import ChatGroq
from app.core.config import settings

# Initialize the LLM object ONCE for the entire application.
# Any agent that needs to talk to the LLM will import this 'llm' instance.
llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=settings.GROQ_API_KEY,
    temperature=0.7,  # Set other parameters here
    # You can add more configuration like streaming=True if needed
)

print("LLM Provider initialized.")