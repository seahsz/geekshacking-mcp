# import libraries
from fastmcp import FastMCP
from typing import Annotated, NamedTuple

from anything.todo_db import TodoDB

# Create the DB (Just for simulation)
todo_db = TodoDB()

# Todo class
class Todo(NamedTuple):
        filename: Annotated[str, "Source file containing the #TODO"]
        text: Annotated[str, "No idea"]
        lineNumber: Annotated[int, "Line number of TODO comment"]

# Create the MCP server
mcp = FastMCP('TODO_MCP') # Note: some clients might not accept mcp in the name

# Tools
@mcp.tool(
        name = "tool_batch_add_todo",
        description="Add all the #TODO texts from a source file"
)
def add_todos(
        todos: list[Todo]
) -> int:
    for todo in todos:
         todo_db.add(todo.filename, todo.text, todo.lineNumber)
    return len(todos)

@mcp.tool(
        name = "tool_add_todo",
        description="Add a single #TODO text from a source file"
)
def add_todo(
        filename: Annotated[str, "Source file containing the #TODO"],
        text: Annotated[str, "No idea"],
        lineNumber: Annotated[int, "Line number of TODO comment"]
) -> bool:
    return todo_db.add(filename, text, lineNumber)

# Resource
@mcp.resource(
        name = "resource_get_todos_for_file",
        description="""Gets a list of TODOs for the file. 
            Returns an empty list if the source file does not exist or if no TODOs exist""",
        uri="whatever://{filename}/todos"
)
def get_todos_for_file(
        filename: Annotated[str, "Source file containing the #TODO"],

) -> list[str]:
    todos = todo_db.get(filename)
    return [text for text in todos.values()]

# Start the MCP
def run():
    mcp.run()

if __name__ == "__main__":
    run()