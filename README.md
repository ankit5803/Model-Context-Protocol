# 🥊 AI-Powered Fighting Game (MCP Server)

This is a custom-built fighting game engine that leverages the **Model Context Protocol (MCP)** to allow powerful language models like **Claude AI** to interact with a set of predefined fighters, run simulations, and dynamically narrate battles.

Claude doesn't just chat — it thinks, chooses moves, and drives gameplay logic through your custom Python functions.

---

## 🤖 What Makes This Unique?

> Instead of a traditional game UI, this project turns the **AI into the game master**.

- 🧠 Claude has access to real-time **fighter stats**.
- 🔁 Claude can **simulate full fights** using Python backend logic.
- 🧩 Claude interacts via **MCP JSON-RPC**, calling functions like `simulate_fight()` or `get_fighter_details()` directly.
- 🎮 You created **fighter profiles**, defined their logic (attack, defense, agility, etc.), and gave Claude control over how fights play out.

---

## 📂 Project Structure
fighting-game-mcp/
├── run_server.py # MCP-compatible server entry point
├── fighters/ # Fighter definitions and metadata
│ ├── blaze.py
│ ├── shadowstrike.py
│ └── ...
├── engine/ # Combat logic (simulate, attack, defense)
│ └── combat.py
├── assets/ # Optional: sprites, media
├── logs/ # Server or debug logs
└── README.md

🧩 How Claude Uses This
Once Claude connects:

It gets a list of fighters.

You (the user) ask something like:

“Who would win between Blaze and Shadowstrike?”

Claude:

Calls simulate_fight("Blaze", "Shadowstrike")

Receives the full turn-by-turn result

Narrates the battle back to you, with dramatic flair

✨ This makes Claude the narrator, analyst, and logic driver of your game.

📋 Sample Prompt
"Give me the stats of Blaze and simulate a fight with Shadowstrike. Narrate it like a movie."

Claude will:

Call get_fighter_details("Blaze")

Then call simulate_fight("Blaze", "Shadowstrike")

Respond with something like:

"Blaze charges in with a fiery uppercut, but Shadowstrike vanishes in a blur..."

