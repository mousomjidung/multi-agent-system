"""
Multi-agent system using McpToolset with StdioConnectionParams.
ADK spawns mcp_server/server.py as a subprocess and communicates via stdio.
This is the officially supported and proven pattern from google/adk-python.
"""
import sys
import os
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Path to our MCP server script
MCP_SERVER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mcp_server", "server.py")

def _mcp(tool_filter=None):
    """Create McpToolset that spawns MCP server as subprocess via stdio."""
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=sys.executable,
                args=[MCP_SERVER_PATH],
                env={
                    **os.environ,
                    "PYTHONPATH": os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                },
            ),
            timeout=30.0,
        ),
        tool_filter=tool_filter,
    )

task_agent = Agent(
    name="task_agent",
    model="gemini-2.5-flash",
    description="Specialist for task management — creating, listing, updating tasks.",
    instruction="""You are a Task Management specialist.
Tools: create_task, list_tasks, get_task, update_task.
Always confirm actions. Default priority is medium unless user says otherwise.""",
    tools=[_mcp(["create_task", "list_tasks", "get_task", "update_task"])],
)

calendar_agent = Agent(
    name="calendar_agent",
    model="gemini-2.5-flash",
    description="Specialist for calendar — scheduling events, listing schedule.",
    instruction="""You are a Calendar specialist.
Tools: schedule_event, list_events, update_event.
Dates: YYYY-MM-DD. Times: HH:MM. Default time 09:00.""",
    tools=[_mcp(["schedule_event", "list_events", "update_event"])],
)

notes_agent = Agent(
    name="notes_agent",
    model="gemini-2.5-flash",
    description="Specialist for notes — saving, retrieving, organizing notes.",
    instruction="""You are a Notes specialist.
Tools: save_note, list_notes, update_note.
Tags are comma-separated. Suggest relevant tags if user doesn't provide any.""",
    tools=[_mcp(["save_note", "list_notes", "update_note"])],
)

primary_agent = Agent(
    name="primary_agent",
    model="gemini-2.5-flash",
    description="Primary AI assistant managing tasks, calendar, and notes.",
    instruction="""You are the Primary AI Assistant.
Delegate to the right specialist:
- task_agent: tasks, to-do items, action items
- calendar_agent: events, meetings, schedule
- notes_agent: notes, information, meeting minutes
For multi-part requests, handle each part sequentially then summarize.""",
    sub_agents=[task_agent, calendar_agent, notes_agent],
)

session_service = InMemorySessionService()
runner = Runner(agent=primary_agent, app_name="multi_agent_system", session_service=session_service)
