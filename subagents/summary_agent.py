from LLM.llm import subagent_llm
from memory.memory_store import get_context
from logs.logger import logger
import json
from langchain.messages import HumanMessage,SystemMessage
from prompt.prompt import system_instruction_for_summary_subagent
from helper.helper import extract_text_from_response , extract_json
def get_summary(session_id:str,k:int)->str:
    previous_chats = get_context(session_id=session_id,k=k)
    logger.success(f"Chats with {len(previous_chats)} is received")
    final_prompt = system_instruction_for_summary_subagent.format(
        chats=previous_chats
    )
    try:
        response = subagent_llm.invoke([
            SystemMessage(content=final_prompt),
            HumanMessage(content="Summarize this")
        ])
        raw_response = extract_text_from_response(response=response)
        parse = extract_json(raw_response)
        logger.info(f"Summary -> {parse['summary']}")
        return parse["summary"]
    except Exception as subagent_exception:
        logger.error(f"Error caught in subagent (summary) | ERROR -> {subagent_exception}")
        return ""

