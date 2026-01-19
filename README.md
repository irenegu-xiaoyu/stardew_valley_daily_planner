# My Junimo Assistent - AI tool to strategize farming in Stardew Valley

An AI assistent (Junimo) who will give you the best advice for what to work on for the day!

Implemented tools:

- Download and parse game data
- Scrape Stardew Valley Wiki knowledge in DB and semantic search

## Using multi-agents

Agent Roles
| Agent | Specialty | Core Goal |
| ------ | ----| ----|
| The Money Maker | Crops & Animals | Maximize profit per tile; ensure crops don't die on season change. |
| The Socialite | NPC Relationships | Tracks birthdays and gift preferences; festival schedules |
| The Scavenger | Tasks / Quests | Tracks Community Center bundles and active quest items |
| The Foreman | Coordination | The "Boss" agent. Receives reports from the others and crafts the final schedule. |

### How to use

Config your Gemini API key in gemini_api_config.json \
In project root, run `python3 -m my_package.multi_agents.the_foreman`

### Example output

```
-- Loading AI model config and game data
 ✈️  Load LLM model config: {'api_key': 'xxx', 'model': 'gemini-3-flash-preview'}
-- Start reasoning
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 500, 'day': '1', 'season': 'spring', 'year': '1', 'dailyLuck': -0.093, 'weather': 'Sunny'}
  📚 Found related Wiki context of length 749 in SV Wiki
  📚 Found related Wiki context of length 783 in SV Wiki
  🚀 Using cached farm data...
  🏡 Current Farm Status: {'farmer': 'Master Yi', 'money': 500, 'day': '1', 'season': 'spring', 'year': '1', 'dailyLuck': -0.093, 'weather': 'Sunny'}
  📚 Found related Wiki context of length 1437 in SV Wiki
  📚 Found related Wiki context of length 1210 in SV Wiki
  📚 Found related Wiki context of length 632 in SV Wiki
  📚 Found related Wiki context of length 621 in SV Wiki
  📚 Found related Wiki context of length 434 in SV Wiki
  📚 Found related Wiki context of length 998 in SV Wiki
  📚 Found related Wiki context of length 587 in SV Wiki
  📚 Found related Wiki context of length 1205 in SV Wiki
  📚 Found related Wiki context of length 587 in SV Wiki
  📚 Found related Wiki context of length 555 in SV Wiki
-- Agent Response
 🌟 JUNIMO STRATEGY FOR TODAY

 👾 Morning, neighbor! It's a beautiful, sunny Spring 1—the perfect start for your new life on the farm. Even with the spirits feeling a bit grumpy today, there's plenty of ground to cover!

 1 Plant and Water: Sow your 15 starting Parsnips and spend your 500g at Pierre's on 10 Potato seeds to maximize early profits.
 2 Forage for Bundles: Keep an eye out for a Wild Horseradish, Daffodil, Leek, and Dandelion; you'll need these for the Spring Foraging Bundle later.
 3 Say Hello: Start the "Introductions" quest by greeting townspeople while you're out foraging to get a head start on your social standing.
```

## Using content generator

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
