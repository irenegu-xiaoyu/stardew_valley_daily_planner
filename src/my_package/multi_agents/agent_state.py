from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # This 'reducer' (operator.add) lets messages pile up instead of overwriting
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str  # Tracks which agent should speak next