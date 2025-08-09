from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

# By using `add_messages`, new messages are appended to the list
from langgraph.graph.message import add_messages

class AgentState(BaseModel):
    """
    A robust, structured state for the multi-agent graph.
    """
    # Use Field(default_factory=list) for mutable defaults like lists
    messages: List[BaseMessage] = Field(default_factory=list)
    
    # The name of the agent that should act next
    next_agent: str

    # Add specific fields for each piece of data your agents generate.
    # Use Optional to indicate they might not be present at the start.
    diagnosis: Optional[str] = None
    context: Optional[str] = None

    # This is a special method used by LangGraph to merge new messages
    # into the existing message list. It's important to keep this.
    def __init__(self, **data):
        super().__init__(**data)
        self.messages = data.get('messages', [])

    @classmethod
    def from_dict(cls, data: dict) -> "AgentState":
        return cls(**data)

    def to_dict(self) -> dict:
        return self.model_dump()