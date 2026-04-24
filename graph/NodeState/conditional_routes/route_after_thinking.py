from graph.NodeState.state import AgentState

def route_after_thinking(state:AgentState):
    print(state["action_taken"])
    print(state["need_clarification"])

    if state['need_clarification'] ==True:
        return "clarify"
    elif state['action_taken'] == "general":
        return "general"
    elif state['action_taken'] == "create":
        return "write"

route_after_thinking(AgentState)