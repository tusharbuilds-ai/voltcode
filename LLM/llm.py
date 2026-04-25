from dotenv import load_dotenv
from config.config import GEMINI_MODEL , TEMPERATURE , SUBAGENT_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=TEMPERATURE,
)

subagent_llm = ChatGoogleGenerativeAI(
    model= SUBAGENT_MODEL,
    temperature=TEMPERATURE
)

llm_with_tools = ChatGoogleGenerativeAI(
    model= GEMINI_MODEL,
    temperature=TEMPERATURE
)


