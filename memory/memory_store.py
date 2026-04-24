from firebase_admin import db
from memory.message_history_schema import build_memory_entry

def save_message(session_id:str,human_message:str,ai_message:str):
    ref = db.reference(f"memory/{session_id}")
    ref.push(build_memory_entry(human_message,ai_message))



def get_context(session_id:str,k:int)->str:
    ref = db.reference(f"memory/{session_id}")
    history = ref.order_by_key().limit_to_last(k).get()

    if not history:
        return ""
    
    context = ""
    for entry in history.values():
        context += f"Human:{entry['human']}\nAI::{entry['ai']}\n\n"

    
    return context.strip()