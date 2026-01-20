# My Junimo Assistant - AI tool to strategize farming in Stardew Valley

An AI assistent (Junimo) who will give you the best advice for what to work on for the day!

## Using multi-agents

Agent Roles
| Agent | Specialty | Core Goal |
| ------ | ----| ----|
| The Money Maker | Crops & Animals & Fishing | Maximize profit |
| The Socialite | NPC Relationships | Tracks birthdays and gift preferences; festival schedules |
| The Scavenger | Tasks / Quests | Tracks Community Center bundles and active quests |
| The Foreman | Coordination | The "Boss" agent. Receives reports from the others and crafts the final schedule using a priority system. |

### How to use

1. Recommend run in a virtual environment
2. In your venv, run `pip install -e .`
3. Config your Gemini API key, LangSmith key in a new `.env` file, see `.env.example`
4. In project root, run `python3 -m my_package.multi_agents.the_foreman`

### Example output

```
-- Loading AI model config and game data
-- Building workflow graph
-- Junimo Assistant Ready! 🌟

============================================================
🌱 What would you like to know? (type 'quit' or 'exit' to stop): what to do  today?

-- Start reasoning
🧠 Classifier: Analyzing request and routing...
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 0, 'day': '2', 'season': 'spring', 'year': '1', 'dailyLuck': -0.07, 'weather': 'Sunny'}
🏡 Farm Status: 0g, spring 2
📋 Routing to: ['money_maker', 'socialite', 'scavenger']
💭 Reasoning: The user's query 'what to do today?' is a general request for daily planning, which requires input from all three specialists to cover farming, social interactions, and collection goals.
💰 Money Maker: Analyzing farm economics...
👥 Socialite: Checking relationships and events...
🔍 Scavenger: Searching for quests and bundles...
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 0, 'day': '2', 'season': 'spring', 'year': '1', 'dailyLuck': -0.07, 'weather': 'Sunny'}
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 0, 'day': '2', 'season': 'spring', 'year': '1', 'dailyLuck': -0.07, 'weather': 'Sunny'}
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 0, 'day': '2', 'season': 'spring', 'year': '1', 'dailyLuck': -0.07, 'weather': 'Sunny'}
  📚 Found related Wiki context of length 1437 in SV Wiki
  📚 Found related Wiki context of length 632 in SV Wiki
  📚 Found related Wiki context of length 906 in SV Wiki
  📚 Found related Wiki context of length 731 in SV Wiki
  📚 Found related Wiki context of length 1726 in SV Wiki
  📚 Found related Wiki context of length 833 in SV Wiki
  📚 Found related Wiki context of length 561 in SV Wiki
  📚 Found related Wiki context of length 1077 in SV Wiki
📊 Aggregating responses from specialists...
✨ Synthesizing final strategy...
🎯 Priority Context: low_money
📊 Agent Priority Order: ['money_maker', 'scavenger', 'socialite']
⚖️  Agent Weights: {'money_maker': 0.6, 'scavenger': 0.3, 'socialite': 0.1}
-- Agent Response

🌟 JUNIMO STRATEGY

👾 *Squeak!* 🍃 Good morning, precious farmer! The forest spirits are dancing because the sun is shining on our valley today! ✨🌟


 1 🌾 Scurry to your fields and plant those Parsnip seeds - they need 4 days of love to grow!                                                                                                  
 2 🔍 Dash through the bushes to find wild Horseradishes and Leeks - they are hidden forest treasures!                                                                                         
 3 🐟 Scuttle down to the docks to visit Willy and receive your magical bamboo pole for catching fishies!                                                                                      

============================================================
🌱 What would you like to know? (type 'quit' or 'exit' to stop): I want to give a gift to Marnie today, what should I get her?

-- Start reasoning
🧠 Classifier: Analyzing request and routing...
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 0, 'day': '2', 'season': 'spring', 'year': '1', 'dailyLuck': -0.07, 'weather': 'Sunny'}
🏡 Farm Status: 0g, spring 2
📋 Routing to: ['socialite']
💭 Reasoning: The user is asking for gift recommendations for an NPC (Marnie), which falls under the socialite's expertise in NPC relationships and gifts.
👥 Socialite: Checking relationships and events...
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 0, 'day': '2', 'season': 'spring', 'year': '1', 'dailyLuck': -0.07, 'weather': 'Sunny'}
  📚 Found related Wiki context of length 772 in SV Wiki
  📚 Found related Wiki context of length 1095 in SV Wiki
📊 Aggregating responses from specialists...
✨ Synthesizing final strategy...
🎯 Priority Context: low_money
📊 Agent Priority Order: ['money_maker', 'scavenger', 'socialite']
⚖️  Agent Weights: {'money_maker': 0.6, 'scavenger': 0.3, 'socialite': 0.1}
-- Agent Response

🌟 JUNIMO STRATEGY

👾 *Squeak!* 🌟 Helping Marnie is a magical idea! ✨ She loves her fluffy friends almost as much as we love the forest spirits! 🍃


 1 🌼 Scurry and gather a yellow Daffodil from the ground; it is a lovely gift she really likes!                                                                                               
 2 🎁 Dash over to her ranch in the forest before the sun gets low to hand her your gift!                                                                                                      
 3 💖 Squeak! Your kindness will make the forest spirits happy and grow your bond with Marnie!                                                                                                 

============================================================
🌱 What would you like to know? (type 'quit' or 'exit' to stop): quit

👋 *Squeak!* Goodbye, farmer! May the valley bring you joy! 🌟
```

### Additional tools

- Run `python3 -m game_data_parser` to parse your local game data
- Run `python3 -m SV_wiki_downloader` to scrape the latest Stardew Valley Wiki knowledge and store in local DB

## [Deprecated] Using content generator

### How to use

Config your Gemini API key in gemini_api_config.json \
In project root, run `python3 -m my_package.model_generate_content.main`

### Example output

```
 ✈️  Load LLM model config: {'api_key': 'xxx', 'model': 'gemini-3-flash-preview'}
 🚀 Using cached farm data...
 🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 500, 'day': '1', 'season': 'spring', 'year': '1', 'dailyLuck': -0.093, 'weather': 'Sunny'}
 🌟 JUNIMO STRATEGY FOR TODAY

*Chirp chirp!* Welcome to your first day in Pelican Town, Master Yi! The sun is shining, the air is fresh, and your new life is just beginning. Even though the spirits are feeling a bit displeased today, there is plenty of work to do on the surface!

**Daily Tasks:**

1.  **Plant Your Gift:** Open the package in your house to find 15 **Parsnip Seeds**. Use your hoe to till 15 spots near your house, plant them, and water them immediately so they can start growing!
2.  **Seed Shopping at Pierre's:** Head to the General Store in town with your 500g. I recommend buying **Potatoes**, as they have a chance to provide multiple crops per harvest, which is great for early profit and farming experience!
3.  **Scavenge for Snacks:** Since your energy is low starting out, head south to the forest below your farm. Look for **Spring Onions** growing in the dirt near the sewer pipe—they are a free way to restore your energy so you can clear more land today!
```
