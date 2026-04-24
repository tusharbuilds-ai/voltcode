from datetime import datetime

def build_memory_entry(human_message:str,ai_message:str)->dict:
    now = datetime.now()
    return{
        "human":human_message,
        "ai":ai_message,
        "timestamp":now.isoformat(),
        "date":now.strftime('%Y-%m-%d')
    }

