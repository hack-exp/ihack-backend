from langgraph.graph import StateGraph, END
from app.services.graph_state import AgentState

# --- Import your new, specialized agents ---
from app.agents.diagnosis_agent import diagnosis_agent
from app.agents.context_agent import context_agent
from app.agents.response_agent import response_agent
from app.agents.supervisor_agent import supervisor_agent # The supervisor remains

from langgraph.graph import StateGraph, END
from app.services.graph_state import AgentState

# --- Import your agents and node constants ---
from app.agents.supervisor_agent import supervisor_agent
from app.agents.diagnosis_agent import diagnosis_agent
from app.agents.context_agent import context_agent
from app.agents.response_agent import response_agent
# --- Define constants for node names to avoid typos ---
class GraphNodes:
    SUPERVISOR = "Supervisor"
    DIAGNOSIS = "DiagnosisAgent"
    CONTEXT = "ContextAgent"
    RESPONSE = "ResponseAgent"
    END = END # Use the official END constant


def build_graph():
    """
    Builds the multi-agent graph for the Stellar AI medical advisor.
    """
    graph_builder = StateGraph(AgentState)

    # --- Add the nodes for each specialized agent ---
    graph_builder.add_node(GraphNodes.SUPERVISOR, supervisor_agent)
    graph_builder.add_node(GraphNodes.DIAGNOSIS, diagnosis_agent)
    graph_builder.add_node(GraphNodes.CONTEXT, context_agent)
    graph_builder.add_node(GraphNodes.RESPONSE, response_agent)

    # --- Define the graph's control flow ---

    # The graph always starts with the supervisor
    graph_builder.set_entry_point(GraphNodes.SUPERVISOR)

    # Define the conditional routing from the supervisor
    def router(state: AgentState):
        """A router that returns the next agent's name from the state object."""
        # THE FIX: Use dot notation to access the attribute
        print(f"---ROUTING to: {state.next_agent}---")
        return state.next_agent

    # Add the conditional edge from the supervisor
    graph_builder.add_conditional_edges(
        GraphNodes.SUPERVISOR,
        router,
        {
            # The keys here match the possible outputs from the supervisor
            GraphNodes.DIAGNOSIS: GraphNodes.DIAGNOSIS,
            GraphNodes.RESPONSE: GraphNodes.RESPONSE,
            GraphNodes.END: GraphNodes.END
        }
    )

    # --- Define the sequential workflow for a new query ---
    graph_builder.add_edge(GraphNodes.DIAGNOSIS, GraphNodes.CONTEXT)
    graph_builder.add_edge(GraphNodes.CONTEXT, GraphNodes.RESPONSE)
    graph_builder.add_edge(GraphNodes.RESPONSE, GraphNodes.END)


    # Compile the graph
    graph = graph_builder.compile()
    
    print("Graph compiled successfully!")
    return graph