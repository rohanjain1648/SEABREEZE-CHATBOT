from langgraph.graph import StateGraph
from typing import TypedDict
from agents.nodes import router, rag_agent, sales_agent, lead_agent, closer_agent

class AgentState(TypedDict):
    user_input: str
    context: str
    response: str
    lead: dict
    intent: str

graph = StateGraph(AgentState)

graph.add_node("router", router)
graph.add_node("rag", rag_agent)
graph.add_node("sales", sales_agent)
graph.add_node("lead", lead_agent)
graph.add_node("closer", closer_agent)

graph.set_entry_point("router")

graph.add_edge("router", "rag")
graph.add_edge("rag", "sales")
graph.add_edge("sales", "lead")

# Conditional edge
def should_close(state):
    return "high" in state.get("intent", "").lower()

graph.add_conditional_edges(
    "lead",
    should_close,
    {
        True: "closer",
        False: "__end__"
    }
)

graph.add_edge("closer", "__end__")

app_graph = graph.compile()
