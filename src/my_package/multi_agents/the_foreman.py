from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from my_package.utils.load_env_config import load_env_config
from my_package.utils.tool_functions import get_farm_status, search_wiki, handle_tool_errors
from my_package.multi_agents.agent_state import AgentState
from my_package.multi_agents.priority_system import determine_priority_context, get_prioritized_responses
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

checkpointer = InMemorySaver()


print(f"-- Loading AI model config and game data")
config = load_env_config()

model = ChatGoogleGenerativeAI(
    model=config["model"],
    api_key=config["api_key"],
    temperature=1.0,
    max_tokens = 10000,
    timeout = 120000,
    max_retries=2,
)

tools = [get_farm_status, search_wiki]
middleware = [handle_tool_errors]

# -- Define the Specialists --
money_maker_agent = create_agent(
    model=model, 
    tools=tools,
    middleware=middleware,
    system_prompt="""You are the Money Maker specialist optimizing for money. 
    Ways to earn money:
    - Earn money by growing and selling crops. Ensure crops don't die on season change.
    - Raising and selling animal products. 
    - Fishing.
    - Maximize profit per tile.
    - Give specific advice on which crop seeds to buy and grow, which animals to buy.  
    """,
)

socialite_agent = create_agent(
    model=model, 
    tools=tools,
    middleware=middleware,
    system_prompt="""You are the Socialite specialist. Things to plan are:
    - Increase NPC hearts, 
    - Gift giving on NPC birthdays
    - Attend festivals.
    """,
)

scavenger_agent = create_agent(
    model=model, 
    tools=tools,
    middleware=middleware,
    system_prompt="""You are the Scavenger specialist. Things to plan are:
    - Collecting Community Center Bundles 
    - Finish active quests items.
    """,
)


# -- Define Router Model --
class RouteDecision(BaseModel):
    """Decision on which agents to route to"""
    agents: list[Literal["money_maker", "socialite", "scavenger"]] = Field(
        description="List of specialist agents to consult based on the user query"
    )
    reasoning: str = Field(
        description="Brief explanation of why these agents were chosen"
    )

# -- Build the Supervisor Router --
ROUTER_PROMPT = """You are JunimoMind, a high-level Stardew Valley strategist. 
Your goal is to help the player optimize their farm while maintaining a helpful, Junimo-like tone.

Available specialists:
- money_maker: Handles crops, animals, profit optimization, farming strategies
- socialite: Handles NPC relationships, birthdays, festivals, gifts
- scavenger: Handles Community Center bundles, quests, item collection

For a general "what should I do today" query, route to ALL three agents.
For specific queries, route only to relevant agents.

Examples:
- "what should I do today?" → ["money_maker", "socialite", "scavenger"]
- "what crops should I plant?" → ["money_maker"]
- "whose birthday is today?" → ["socialite"]
- "what do I need for the spring bundle?" → ["scavenger"]
"""

router_model = model.with_structured_output(RouteDecision)

# -- Node Functions --
def classifier(state: AgentState) -> AgentState:
    """Classifier decides which agents to call and captures farm status"""
    print(f"🧠 Classifier: Analyzing request and routing...")
    
    user_message = state["messages"][-1].content
    
    # Try to get farm status early for priority determination
    try:
        farm_status_result = get_farm_status.invoke({})
        if isinstance(farm_status_result, dict):
            state["farm_status"] = farm_status_result
            print(f"🏡 Farm Status: {farm_status_result.get('money', 0)}g, {farm_status_result.get('season', '?')} {farm_status_result.get('day', '?')}")
    except Exception as e:
        print(f"⚠️  Could not fetch farm status: {e}")
        state["farm_status"] = {}
    
    decision = router_model.invoke([
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": user_message}
    ])
    
    print(f"📋 Routing to: {decision.agents}")
    print(f"💭 Reasoning: {decision.reasoning}")
    
    state["next_agents"] = decision.agents
    state["specialist_responses"] = {}
    
    return state

def money_maker_node(state: AgentState) -> dict:
    """Money maker specialist node"""
    print(f"💰 Money Maker: Analyzing farm economics...")
    
    user_message = state["messages"][-1].content
    result = money_maker_agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    
    return {
        "agent": "money_maker",
        "response": result["messages"][-1].content
    }

def socialite_node(state: AgentState) -> dict:
    """Socialite specialist node"""
    print(f"👥 Socialite: Checking relationships and events...")
    
    user_message = state["messages"][-1].content
    result = socialite_agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    
    return {
        "agent": "socialite",
        "response": result["messages"][-1].content
    }

def scavenger_node(state: AgentState) -> dict:
    """Scavenger specialist node"""
    print(f"🔍 Scavenger: Searching for quests and bundles...")
    
    user_message = state["messages"][-1].content
    result = scavenger_agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    
    return {
        "agent": "scavenger",
        "response": result["messages"][-1].content
    }

def aggregate_responses(state: AgentState) -> AgentState:
    """Aggregate all specialist responses"""
    print(f"📊 Aggregating responses from specialists...")
    return state

class FinalResponse(BaseModel):
    """Final structured response"""
    greetings: str = Field(description="A cheerful, whimsical Junimo-style greeting with emojis and personality. Include sounds like *squeak!* or *boop!*")
    todos: str = Field(description="Exactly 3 daily tasks in markdown numbered list format, each starting with a relevant emoji. Make them feel magical and actionable.")

SYNTHESIS_PROMPT = """You are JunimoMind, synthesizing advice from your specialist team.

Create a cohesive daily strategy with a MAGICAL JUNIMO PERSONALITY:

**Greeting Style:**
   - Use playful Junimo sounds like "*squeak!*", "*boop!*", or "*chirp!*"
   - Include nature/farm emojis (🌱🌟✨🍃💚🌈)
   - Be encouraging and whimsical
   - Reference the valley, stars, or forest spirits

If user asks for a general questions "what to do today?", response with Daily Tasks Format.
**Daily Tasks Format (exactly 3 tasks):**
   - Use markdown numbered list with emoji for each task
   - Start each task with a relevant emoji (🌾💰👥🎁🔍📦🐟🌸)
   - Make tasks feel magical but actionable
   - Add personality with words like "dash", "scurry", "magical", "precious"
   - Keep tasks concise but charming
If user asks for a specific game mechanics, response with 2~3 sentences with direct answers.


EXAMPLE STYLE:
Greeting: "*Squeak squeak!* 🌟 Good morning, farmer! The forest spirits whisper of great fortune today! ✨"

Tasks:
1. 🌾 Plant those precious Cauliflower seeds before the moon changes - 12 days to harvest! \n
2. 💝 Dash over to Haley with a Daffodil - it's her birthday and she'll adore you for it! \n
3. 🔍 Scurry to the beach to catch some magical Anchovies for the Ocean Bundle! \n

IMPORTANT: The specialist responses are provided in priority order with weights.
- Higher priority agents should have MORE influence on your final recommendations
- Higher weighted advice should contribute MORE tasks to your final list
- Integrate advice from all agents, but emphasize the higher priority ones

Current Context: {context_description}

"""

def synthesize_final_response(state: AgentState) -> AgentState:
    """Synthesize final response from all specialist inputs with priority weighting"""
    print(f"✨ Synthesizing final strategy...")
    
    # Get prioritized and weighted responses
    prioritized_responses = get_prioritized_responses(state)
    priority_context = determine_priority_context(state)
    
    # Build specialist context with priority markers
    specialist_context_parts = []
    for i, (agent, response, weight) in enumerate(prioritized_responses):
        priority_label = f"[PRIORITY {i+1} - Weight: {weight:.0%}]"
        specialist_context_parts.append(
            f"{priority_label} **{agent.upper()} ADVICE:**\n{response}"
        )
    
    specialist_context = "\n\n".join(specialist_context_parts)
    
    # Build context description
    context_desc = f"Active contexts: {', '.join(priority_context['contexts'])}"
    farm_status = priority_context['farm_status']
    if farm_status:
        context_desc += f" | Money: {farm_status.get('money', 'unknown')}g"
        context_desc += f" | Date: {farm_status.get('season', '?')} {farm_status.get('day', '?')}"
    
    synthesis_model = model.with_structured_output(FinalResponse)
    
    final = synthesis_model.invoke([
        {"role": "system", "content": SYNTHESIS_PROMPT.format(context_description=context_desc)},
        {"role": "user", "content": f"User asked: {state['messages'][-1].content}\n\nSpecialist responses (in priority order):\n{specialist_context}"}
    ])
    
    state["final_response"] = {
        "greetings": final.greetings,
        "todos": final.todos,
        "priority_context": priority_context['contexts'],
        "agent_weights": {agent: weight for agent, _, weight in prioritized_responses}
    }
    
    return state

# -- Routing Logic using Send API --
def route_to_specialists(state: AgentState) -> list[Send]:
    """Use Send API to dynamically route to selected specialists"""
    agents = state["next_agents"]
    
    # Map agent names to node functions
    agent_map = {
        "money_maker": "money_maker",
        "socialite": "socialite",
        "scavenger": "scavenger"
    }
    
    # Create Send objects for each selected agent
    return [Send(agent_map[agent], state) for agent in agents]

def collect_specialist_response(state: AgentState, response: dict) -> AgentState:
    """Collect response from a specialist"""
    state["specialist_responses"][response["agent"]] = response["response"]
    return state

# -- Build the Graph --
print(f"-- Building workflow graph")

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("classifier", classifier)
workflow.add_node("money_maker", money_maker_node)
workflow.add_node("socialite", socialite_node)
workflow.add_node("scavenger", scavenger_node)
workflow.add_node("aggregate", aggregate_responses)
workflow.add_node("synthesize", synthesize_final_response)

# Add edges
workflow.add_edge(START, "classifier")
workflow.add_conditional_edges(
    "classifier",
    route_to_specialists,
    ["money_maker", "socialite", "scavenger"]
)
workflow.add_edge("money_maker", "aggregate")
workflow.add_edge("socialite", "aggregate")
workflow.add_edge("scavenger", "aggregate")
workflow.add_edge("aggregate", "synthesize")
workflow.add_edge("synthesize", END)

# Compile the graph
app = workflow.compile(checkpointer=checkpointer)

print(f"-- Junimo Assistant Ready! 🌟\n")

# Human-in-the-loop interaction
while True:
    print("=" * 60)
    user_input = input("🌱 What would you like to know? (type 'quit' or 'exit' to stop): ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\n👋 *Squeak!* Goodbye, farmer! May the valley bring you joy! 🌟")
        break
    
    if not user_input:
        print("⚠️  Please enter a question or request!\n")
        continue
    
    print(f"\n-- Start reasoning")
    
    # Run the workflow
    result = app.invoke(
        {
            "messages": [HumanMessage(content=user_input)],
            "specialist_responses": {},
            "next_agents": [],
            "final_response": None,
            "farm_status": {}
        },
        config={"configurable": {"thread_id": "junimo_1"}}
    )
    
    print(f"-- Agent Response")
    
    print(f"\n🌟 JUNIMO STRATEGY\n")
    
    if result["final_response"]:
        text = result["final_response"]
        print(f"👾 {text['greetings']}\n")
        console = Console()
        md = Markdown(text['todos'])
        console.print(md)
        print()
    else:
        print("❌ No response generated\n")


