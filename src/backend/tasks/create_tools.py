from config.database import get_db
from repositories.tool_repository import ToolRepository
from schemas.tool_schema import ToolInput


def create_tools() -> None:
    print("Creating tools...")

    db = next(get_db())

    tool_repository = ToolRepository(db)

    tools = [
        {"name": "current_time_tool", "description": "Returns current date time"},
        {"name": "retriever_tool", "description": "RAG"}
    ]

    for tool in tools:
        if not tool_repository.tool_exists_by_name(tool.get("name")):
            created = tool_repository.create_tool(ToolInput(name=tool.get("name"), description=tool.get("description")))
            print(f"Created tool: {created}")

    print("Creating tools done!")
