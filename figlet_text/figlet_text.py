from pyfiglet import Figlet
from rich import _console



def starup_logo():
    startup_logo = Figlet(font="slant")
    print(startup_logo.renderText("Volt Code"))


def what_you_want_to_build_today_text():
    what_you_want_to_build_today_text = Figlet(font="pepper")
    print(what_you_want_to_build_today_text.renderText("What do you want to build today ?"))


def ask_question_from_the_user(question:str):
    ask_question_from_the_user = question
    print(f"[bold_yellow]{ask_question_from_the_user}[/bold_yellow]")


