from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]
    goal:str

    #Thinking state
    plan:str
    need_clarification:bool
    question:list[str]
    clarification_answer:dict

    #Action phase
    working_dir:str
    code:str
    file_path:str


    status:str
    action_taken: str
