from langchain_core.tools import tool
from pathlib import Path
from logs.logger import logger

@tool
def make_file(file_path:str,content:str):
    """This tool can be used to create and write in file in the system on specified path"""
    logger.info(f"Starting the write the file at user specified path -> {file_path}")
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding="utf-8")
        logger.success(f"File created succesfully at path {path}")
        return f"File created succesfully at path {path}"
    except Exception as file_operation_error:
        logger.error(f"File can not be created. Error captured -> {file_operation_error}")
        return f"Error creating file at path -> {path}"
