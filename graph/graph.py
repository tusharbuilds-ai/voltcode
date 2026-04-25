from langgraph.graph import StateGraph,START,END
from graph.NodeState.state import AgentState
from graph.NodeState.conditional_routes.route_after_thinking import route_after_thinking
from graph.NodeState.conditional_routes.route_after_clarify import route_after_clarity
from logs.logger import logger
from LLM.llm import llm, llm_with_tools
import json
from LLM.tools.tools import make_file,create_directory
from helper.helper import extract_text_from_response
from langchain.messages import HumanMessage,SystemMessage
from prompt.prompt import system_instruction_for_thinking_node , system_instruction_for_act_write,system_instruction_for_act_general
from figlet_text.figlet_text import ask_question_from_the_user
from config.config import WORKING_DIRECTORY
from memory.memory_store import save_message,get_context
from subagents.summary_agent import get_summary
from subagents.todo_maker_agent import create_todo
from helper.helper import execute_tool

import memory.firebase_config
# think node is the main working head. It think and plans and decide whether to ask questions to user or act on the ask.
def think_node(state:AgentState):
    logger.info("Agent started thinking...")
    try:
        final_prompt = system_instruction_for_thinking_node.format(
             chat_summary=get_summary("101",6)
        )
        response = llm.invoke([
            SystemMessage(content=final_prompt),
            HumanMessage(content=state["messages"][-1].content)
        ])

        raw = response.content[0]["text"].strip()
        parsed = json.loads(raw)    
    
        logger.info("Agent thinking completed")
        try:
            return{
                "plan":parsed["planed"],
                "need_clarification":parsed["need_clarififaction_bool"],
                "question":parsed["question_asked"],
                "action_taken":parsed["action_taken"]
            }
        except Exception as e:
            logger.error(f"The following error was raised in thinking node -> {e}")

    except Exception as error:
        logger.error(f"Error raised in [def think_node] while invoking LLM -> {error}")


# clarify_node agent used this node to ask questions againt the user request

def clarify_node(state:AgentState):
    logger.info("Agent asking you few questions for it clarification..")
    questions = state["question"]
    answers = {}

    for question in questions:
        ask_question_from_the_user(question)
        answer = input(">")
        answers[question] = answer
    
    return{
        "clarification_answer":answers,
        "need_clarification":False
    }


# act node function to write  file

def act_node_write(state:AgentState):
    logger.info("Agent now prepareing you solution....")
    act_prompt = system_instruction_for_act_write.format(
        user_query=state['goal'],
        agent_planning=state['plan'],
        question_answered=state['clarification_answer'],
    )

    try:
        response = llm.invoke([
            SystemMessage(content=act_prompt),
            HumanMessage(content="These are the insights")
        ])

        logger.info("Final response generated")
        
        

        raw_output = extract_text_from_response(response=response) 
       
        parsed_output = json.loads(raw_output)

        print(parsed_output["problem_solved"])
        print(parsed_output["algorith_used"])
        print(parsed_output["optimization"])
        print(parsed_output["filename"])
        print(parsed_output["code"])
        print(parsed_output["suggestion"])

        filename= str(parsed_output["filename"])

        try:
            save_message(
                session_id="101",
                human_message=state["goal"],
                ai_message=raw_output
            )
            logger.success("message history saved")
        except Exception as write_act_message_history_saved:
            logger.error(f"Can not save the write message history. Error caught -> {write_act_message_history_saved}")
        
        try:
            logger.info(f"Starting to create the file in directory {WORKING_DIRECTORY+filename}")
            make_file.invoke({
                "file_path":state["file_path"]+filename,
                "content":parsed_output["code"]
            })
        except Exception as file_creatiion_exception:
            logger.error(f"Starting to create the file in directory {WORKING_DIRECTORY} | Error - > {file_creatiion_exception}") 
        
    except Exception as error_in_final_generation:
        logger.error(f"Error caught in final generation phase ->{error_in_final_generation}")

# act node function to answer general queries

def act_node_general(state:AgentState):
    logger.info("Agent now prepareing you solution....")
    act_prompt = system_instruction_for_act_general.format(
        user_query=state['goal'],
        agent_planning=state['plan'],
        question_answered=state['clarification_answer'],
    )

    try:
        response = llm.invoke([
            SystemMessage(content=act_prompt),
            HumanMessage(content="These are the insights")
        ])

        logger.info("Final response generated")
        
        

        raw_output = extract_text_from_response(response=response) 
       
        parsed_output = json.loads(raw_output)



        print(parsed_output["problem_solved"])
        print(parsed_output["explanation"])
        print(parsed_output["suggestion"])


        try:
            save_message(
                session_id="101",
                human_message=state["goal"],
                ai_message=raw_output,
            )
            logger.success(f"General message history saved for session")
        except Exception as FirebaseDB:
            logger.critical(f"Message history can not be stored critical error - > {FirebaseDB}")
        
    except Exception as error_in_final_generation:
        logger.error(f"Error caught in final generation phase ->{error_in_final_generation}")


# Node to handle complex project requests

def todo_for_complex_project(state:AgentState):
    logger.info("Agent making the todo list...")
    received_todo = create_todo(state["goal"],state["plan"])

    print(type(received_todo))

    for step,task in received_todo.items():
        print(f"\n[{step}] {task}....")

    return{
        "todos" : received_todo
    }

# Node to handle complex project execution

def execution_node(state:AgentState):
    todos = state["todos"]
    completed = state.get("completed_todos",[])

    for step,task in todos.items():
        if step in completed:
            continue

        print(f"[{step}] : {task}")

        llm_with_tool = llm_with_tools.bind_tools(
            [make_file,
             create_directory]
        )

        response = llm_with_tool.invoke([
            HumanMessage(content=f"""Execute this build step.
            Working directory: {WORKING_DIRECTORY}
            
            Rules:
            - Create directories with create_directory
            - Create files with make_file
            - For dependencies: write package.json
              or requirements.txt (don't install)
            - Always include setup instructions
              in a README.md
            """),
            HumanMessage(content=task)
        ])

        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call)
                logger.info(f"/ {step}: {result}")

            completed.append(step)
    return{
        "completed":completed,
        "reponse":f"Project done"
    }

# function to builf langgraph stated graph

def build_graph():
    try:
        logger.info("Graph build started")
        graph = StateGraph(AgentState)

        graph.add_node("think",think_node)
        graph.add_node("clarify",clarify_node)
        graph.add_node("write",act_node_write)
        graph.add_node("general",act_node_general) 
        graph.add_node("todo_for_complex_project",todo_for_complex_project)
        graph.add_node("execution_node",execution_node)


        graph.add_edge(START,"think")

        graph.add_conditional_edges("think",route_after_thinking,{
            "clarify":"clarify",
            "general":"general",
            "write":"write",
            "need_todo":"todo_for_complex_project"
        })
        
        graph.add_conditional_edges("clarify",route_after_clarity,{
            "general":"general",
            "write":"write",
            "need_todo":"todo_for_complex_project"
        })

        
        graph.add_edge("write",END)
        graph.add_edge("general",END)
        graph.add_edge("todo_for_complex_project","execution_node")
        graph.add_edge("execution_node",END)
        logger.info("Graph build completed")

        app = graph.compile()
        
        return app

    except  Exception as error:
        logger.error(f"Error in build_graph function -> {error}")