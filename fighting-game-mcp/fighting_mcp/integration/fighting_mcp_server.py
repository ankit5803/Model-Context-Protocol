# fighting_mcp/integration/fighting_mcp_server.py

#!/usr/bin/env python3

import asyncio
import json
from typing import Any, Dict, List
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource, LoggingLevel
)
import mcp.types as types

from ..data_system.fighter_data import fighter_data_system
from ..battle_system.battle_engine import battle_engine

# Create the server instance
server = Server("fighting-game-mcp")

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    resources = []
    for fighter in fighter_data_system.get_all_fighters():
        resources.append(
            Resource(
                uri=f"fighter://{fighter.name.lower()}",
                name=f"Fighter: {fighter.name}",
                description=f"{fighter.style} style fighter with {fighter.health} HP",
                mimeType="application/json"
            )
        )
    return resources

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    if not uri.startswith("fighter://"):
        raise ValueError(f"Unknown resource URI: {uri}")

    fighter_name = uri.replace("fighter://", "")
    fighter = fighter_data_system.get_fighter(fighter_name)

    if not fighter:
        raise ValueError(f"Fighter not found: {fighter_name}")

    return json.dumps(fighter.to_dict(), indent=2)

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    return [
        Tool(
            name="get_fighter_info",
            description="Get detailed information about a specific fighter including stats and movelist",
            inputSchema={
                "type": "object",
                "properties": {
                    "fighter_name": {"type": "string", "description": "Name of the fighter"}
                },
                "required": ["fighter_name"]
            }
        ),
        Tool(
            name="list_all_fighters",
            description="Get a list of all available fighters",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="simulate_fight",
            description="Simulate a complete battle between two fighters",
            inputSchema={
                "type": "object",
                "properties": {
                    "fighter1": {"type": "string"},
                    "fighter2": {"type": "string"},
                    "max_turns": {
                        "type": "integer", "default": 20, "minimum": 1, "maximum": 50
                    }
                },
                "required": ["fighter1", "fighter2"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    if name == "get_fighter_info":
        fighter_name = arguments.get("fighter_name")
        fighter = fighter_data_system.get_fighter(fighter_name)
        if not fighter:
            return [types.TextContent(type="text", text=f"Fighter '{fighter_name}' not found.")]
        return [types.TextContent(type="text", text=json.dumps(fighter.to_dict(), indent=2))]

    elif name == "list_all_fighters":
        fighters = fighter_data_system.get_all_fighters()
        info = [
            {
                "name": f.name,
                "style": f.style,
                "health": f.health,
                "attack": f.attack,
                "defense": f.defense,
                "speed": f.speed
            } for f in fighters
        ]
        return [types.TextContent(type="text", text=json.dumps({"fighters": info}, indent=2))]

    elif name == "simulate_fight":
        fighter1 = arguments.get("fighter1")
        fighter2 = arguments.get("fighter2")
        max_turns = arguments.get("max_turns", 20)

        result = battle_engine.simulate_battle(fighter1, fighter2, max_turns)

        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]

        log = f"# Battle Simulation: {fighter1} vs. {fighter2}\n\n"
        log += "## Starting Stats\n"
        log += f"- **{fighter1}**: HP {result['starting_stats'][fighter1]}\n"
        log += f"- **{fighter2}**: HP {result['starting_stats'][fighter2]}\n\n"

        for i, turn in enumerate(result['turns'], 1):
            log += f"## Turn {i}\n"
            for action in turn["actions"]:
                log += f"- {action}\n"
            log += "\n"

        if result.get("winner"):
            log += f"## \U0001F3C6 Winner: **{result['winner']}**\n"
        else:
            log += "## 🤝 The battle ended in a **draw**.\n"

        return [types.TextContent(type="text", text=log)]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fighting-game-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
