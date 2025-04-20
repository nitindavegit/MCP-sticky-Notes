# main.py
from mcp.server.fastmcp import FastMCP
import os
# Create an MCP server
mcp = FastMCP("AI sticky notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")
        
@mcp.tool()
def add_note(note:str) ->str:
    """
    Append a new note to the sticky note file.
    
    Args:
        note (str): The note content to be add.
        
    Returns:
        str: A confirmation message indicating a note has been saved.
    
    """
    ensure_file()
    with open(NOTES_FILE,"a") as f:
        f.write(note + "\n")
    return f"Note Saved!"


@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky note file.
    
    Returns:
        str: A string containing all notes separated by newlines.
    
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content =  f.read().strip()
    return content or "No notes found."

@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note from the sticky note file.
    
    Returns:
        str: The latest note content.
    
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes found."
    

@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current notes.
    
    Returns:
        str: A prompt string that includes all notes and asks for a summary.
            if no notes are found, return a message indicating that.
    
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return "No notes yet"
    return f"Summarize the current notes: {content}"