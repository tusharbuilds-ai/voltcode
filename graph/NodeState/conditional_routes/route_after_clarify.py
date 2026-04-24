from graph.NodeState.state import AgentState

def route_after_clarity(state:AgentState):

    if state['action_taken'] == "general":
        return "general"
    elif state['action_taken'] == "create":
        return "write"
    elif state['action_taken'] == "need_todo":
        return "need_todo"

route_after_clarity(AgentState)