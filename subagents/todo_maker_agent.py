from LLM.llm import subagent_llm
from prompt.prompt import system_instruction_for_todo_subagent
from langchain.messages import HumanMessage,SystemMessage
from helper.helper import extract_text_from_response , extract_json
import json
from logs.logger import logger

def create_todo(user_query:str,agent_planning:str)->str:
    final_todo_prompt = system_instruction_for_todo_subagent.format(
        user_request=user_query,
        agent_plan=agent_planning
    )

    response = subagent_llm.invoke([
        SystemMessage(content=final_todo_prompt),
        HumanMessage(content="Return the todos.")
    ])

    raw_response = extract_text_from_response(response=response)
    parsed = extract_json(raw_response)

    print(parsed)

    logger.info(f"Todo generated -> {parsed}")
    return parsed
    