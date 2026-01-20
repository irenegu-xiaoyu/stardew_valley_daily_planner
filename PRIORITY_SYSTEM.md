# Agent Priority System

## Overview

The synthesis step now includes a dynamic priority system that adjusts agent influence based on farm context.

## Priority Contexts

### 1. **Low Money** (< 1000g)

- **Priority Order**: Money Maker → Scavenger → Socialite
- **Weights**: 60% / 30% / 10%
- **Rationale**: Focus on earning money and collecting valuable items

### 2. **Early Season** (Days 1-7)

- **Priority Order**: Money Maker → Scavenger → Socialite
- **Weights**: 50% / 30% / 20%
- **Rationale**: Plant crops early and prepare for the season

### 3. **Late Season** (Days 22-28)

- **Priority Order**: Scavenger → Money Maker → Socialite
- **Weights**: 50% / 30% / 20%
- **Rationale**: Complete bundles and quests before season ends

### 4. **Festival Day**

- **Priority Order**: Socialite → Money Maker → Scavenger
- **Weights**: 60% / 20% / 20%
- **Rationale**: Focus on social interactions during festivals

### 5. **Default**

- **Priority Order**: Money Maker → Socialite → Scavenger
- **Weights**: 40% / 30% / 30%
- **Rationale**: Balanced approach for normal gameplay

## How It Works

### 1. Context Detection

The `determine_priority_context()` function checks:

- Current money (from farm_status)
- Day of season (1-28)
- Season name
- Festival dates (TODO)

### 2. Priority Assignment

The `get_prioritized_responses()` function:

- Determines active context(s)
- Applies appropriate priority order
- Assigns weights to each agent
- Sorts responses by priority

### 3. Synthesis

The `synthesize_final_response()` function:

- Labels responses with priority levels
- Includes weights in the prompt
- Instructs the LLM to emphasize higher-priority advice
- Stores priority metadata in final response

## Customization

### Adding New Contexts

Edit `PRIORITY_RULES` in `the_foreman.py`:

```python
PRIORITY_RULES = {
    "your_context": {
        "priority_order": ["agent1", "agent2", "agent3"],
        "weights": {"agent1": 0.5, "agent2": 0.3, "agent3": 0.2}
    }
}
```

### Modifying Detection Logic

Update `determine_priority_context()` to add new conditions:

```python
def determine_priority_context(state: AgentState) -> dict:
    # Add your logic here
    if your_condition:
        contexts.append("your_context")
```

## Output

The final response now includes:

- `greetings`: Cheerful Junimo greeting
- `todos`: 3 prioritized tasks
- `priority_context`: Active context names
- `agent_weights`: Dictionary of agent weights used

## Example Flow

```
Farm Status: 500g, Spring Day 3
↓
Context Detection: ["low_money", "early_season"]
↓
Active Context: "low_money" (first match)
↓
Priority Order: Money Maker (60%) → Scavenger (30%) → Socialite (10%)
↓
Synthesis: Emphasizes money-making tasks
```
