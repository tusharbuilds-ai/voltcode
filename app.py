import typer
from figlet_text.figlet_text import starup_logo
from figlet_text.figlet_text import what_you_want_to_build_today_text
from logs.logger import logger
from langchain.messages import HumanMessage
from graph.graph import build_graph
from rich.console import Console
from rich.text import Text
from config.config import WORKING_DIRECTORY


console = Console()
text = Text(">  What will you build today ?")
text.stylize("bold red",0,53)



filepath_text = Text(">  Volt Code need a working directory path to code. Give the path")
filepath_text.stylize("bold yellow",0,120)


starup_logo()
console.print(filepath_text)

file_path = input("Enter the path to working directory:")

logger.success(f"Added file path to config WORKING_DIRECTORY - > {WORKING_DIRECTORY}")
def main():
    deep_agent = build_graph()
    logger.info("Service started")
    console.print(text)
    


    while True:
        query = input()
        deep_agent.invoke({
            "messages":[HumanMessage(content=query)],
            "goal":query,
            "plan":None,
            "need_clarification":None,
            "clarification_answer":None,
            "question":None,
            "working_dir":None,
            "code":None,
            "file_path":file_path,
            "status":"Thinking",
            "action_taken":[]
        })
        

if __name__ == "__main__":
    typer.run(main)