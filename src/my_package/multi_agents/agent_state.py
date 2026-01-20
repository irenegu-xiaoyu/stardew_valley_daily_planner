from typing import TypedDict

class AgentState(TypedDict):
    """State that tracks the workflow"""
    messages: list
    farm_status: dict
    specialist_responses: dict
    next_agents: list[str]
    final_response: dict | None
