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
    elif state["action_taken"] == "need_todo":
        return "need_todo"

route_after_thinking(AgentState)