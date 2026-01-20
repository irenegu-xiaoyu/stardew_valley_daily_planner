"""
Priority system for agent response synthesis.
Determines which specialist agents should have more influence based on farm context.
"""

from my_package.multi_agents.agent_state import AgentState

# -- Priority Configuration --
PRIORITY_RULES = {
    "low_money": {
        "threshold": 1000,
        "priority_order": ["money_maker", "scavenger", "socialite"],
        "weights": {"money_maker": 0.6, "scavenger": 0.3, "socialite": 0.1}
    },
    "festival_day": {
        "priority_order": ["socialite", "money_maker", "scavenger"],
        "weights": {"socialite": 0.6, "money_maker": 0.2, "scavenger": 0.2}
    },
    "early_season": {  # First 7 days of season
        "priority_order": ["money_maker", "scavenger", "socialite"],
        "weights": {"money_maker": 0.5, "scavenger": 0.3, "socialite": 0.2}
    },
    "late_season": {  # Last 7 days of season
        "priority_order": ["scavenger", "money_maker", "socialite"],
        "weights": {"scavenger": 0.5, "money_maker": 0.3, "socialite": 0.2}
    },
    "default": {
        "priority_order": ["money_maker", "socialite", "scavenger"],
        "weights": {"money_maker": 0.4, "socialite": 0.3, "scavenger": 0.3}
    }
}


def determine_priority_context(state: AgentState) -> dict:
    """Determine which priority context applies based on farm status"""
    farm_status = state.get("farm_status", {})
    
    # Check various conditions
    money = farm_status.get("money", 0)
    day = int(farm_status.get("day", 15))
    season = farm_status.get("season", "spring")
    
    contexts = []
    
    # Check money situation
    if money < PRIORITY_RULES["low_money"]["threshold"]:
        contexts.append("low_money")
    
    # Check season timing
    if day <= 7:
        contexts.append("early_season")
    elif day >= 22:
        contexts.append("late_season")
    
    # TODO: Add festival detection logic here
    # if is_festival_day(day, season):
    #     contexts.append("festival_day")
    
    return {
        "contexts": contexts if contexts else ["default"],
        "farm_status": farm_status
    }


def get_prioritized_responses(state: AgentState) -> list[tuple[str, str, float]]:
    """
    Get specialist responses prioritized and weighted based on context.
    Returns: list of (agent, response, weight) tuples
    """
    priority_context = determine_priority_context(state)
    contexts = priority_context["contexts"]
    
    # Use the first matching context, or default
    active_context = contexts[0] if contexts else "default"
    priority_config = PRIORITY_RULES.get(active_context, PRIORITY_RULES["default"])
    
    priority_order = priority_config["priority_order"]
    weights = priority_config["weights"]
    
    print(f"🎯 Priority Context: {active_context}")
    print(f"📊 Agent Priority Order: {priority_order}")
    print(f"⚖️  Agent Weights: {weights}")
    
    # Sort responses by priority order
    specialist_responses = state["specialist_responses"]
    prioritized = []
    
    for agent in priority_order:
        if agent in specialist_responses:
            weight = weights.get(agent, 0.33)
            prioritized.append((agent, specialist_responses[agent], weight))
    
    # Add any remaining agents not in priority order
    for agent, response in specialist_responses.items():
        if agent not in priority_order:
            prioritized.append((agent, response, 0.1))
    
    return prioritized
