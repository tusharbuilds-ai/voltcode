from graph.NodeState.state import AgentState

def route_after_clarity(state:AgentState):

    if state['action_taken'] == "general":
        return "general"
    elif state['action_taken'] == "create":
        return "write"

route_after_clarity(AgentState)