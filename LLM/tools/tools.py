from langchain_core.tools import tool
from pathlib import Path
from logs.logger import logger
import config.config as config

@tool
def make_file(file_path:str,content:str):
    """Create file at exact path with content"""
    logger.info(f"Starting the write the file at user specified path -> {file_path}")
    try:
        full_path = Path(config.WORKING_DIRECTORY)/file_path
        full_path.parent.mkdir(parents=True,exist_ok=True)
        full_path.write_text(content,encoding="utf-8")
        logger.success(f"File created succesfully at path {full_path}")
        return f"File created succesfully at path {full_path}"
    except Exception as file_operation_error:
        logger.error(f"File can not be created. Error captured -> {file_operation_error}")
        return f"Error creating file at path -> {full_path}"
    

@tool 
def create_directory(path:str):
    """Create directory at the given path"""
    try: 
        full_path = Path(config.WORKING_DIRECTORY)/path
        full_path.mkdir(parents=True,exist_ok=True)
        logger.success(f"Direct created succesfully at path {full_path}")
        return f"Created directory {path}"
    except Exception as directory_creation_error:
        logger.error(f"Directory can not be created -> {directory_creation_error}")


@tool
def read_file(path:str) ->str:
    """Read content of exisitng file."""
    full_path = Path(config.WORKING_DIRECTORY)/path
    if not full_path.exists():
        return f"File not found {full_path}"
    return full_path.read_text(encoding="utf-8")
