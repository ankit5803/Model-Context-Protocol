#!/usr/bin/env python3

import os
import sys
import argparse

from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Run Fighting Game MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Get the project root directory
    project_root = Path(__file__).parent

    # Add the project root to Python path
    sys.path.insert(0, str(project_root))

    print(" Fighting Game MCP Server",file=sys.stderr)
    print("=" * 50)

    try:
        import mcp
        print(" MCP library found",file=sys.stderr)
    except ImportError:
        print(" MCP library not found. Please install it with: pip install mcp",file=sys.stderr)
        return 1

    try:
        from fighting_mcp.data_system.fighter_data import fighter_data_system
        from fighting_mcp.battle_system.battle_engine import battle_engine

        print(f"Loaded {len(fighter_data_system.fighters)} fighters",file=sys.stderr)

        print(" Running system test...",file=sys.stderr)
        result = battle_engine.simulate_battle("Ryu", "Ken", max_turns=3)
        if "error" in result:
            print(f" System test failed: {result['error']}",file=sys.stderr)
            return 1
        print("System test passed",file=sys.stderr)

    except Exception as e:
        print(f" Error loading modules: {e}",file=sys.stderr)
        return 1

    print("\n Starting Fighting Game MCP Server...",file=sys.stderr)
    print("=" * 50)

    server_script = project_root / "fighting_mcp" / "integration" / "fighting_mcp_server.py"
    if not server_script.exists():
        print(f" Server script not found: {server_script}",file=sys.stderr)
        return 1

    try:
        if args.debug:
            print(" Debug mode enabled",file=sys.stderr)

        print(" Fighting Game MCP Server is now running!",file=sys.stderr)
        print("\nTo connect Claude to this server:",file=sys.stderr)
        print("1. Open Claude Desktop App",file=sys.stderr)
        print("2. Go to Settings > MCP Servers",file=sys.stderr)
        print("3. Click 'Add Server'",file=sys.stderr)
        print(f"4. Enter the path: {server_script}",file=sys.stderr)
        print("5. Click 'Add' and restart Claude",file=sys.stderr)
        print("\nTry these:",file=sys.stderr)
        print("- Tell me about Ryu",file=sys.stderr)
        print("- Simulate a fight between Chun-Li and Zangief",file=sys.stderr)
        print("=" * 50)

        from fighting_mcp.integration.fighting_mcp_server import main as server_main
        import asyncio
        asyncio.run(server_main())

    except KeyboardInterrupt:
        print("\n Shutting down Fighting Game MCP Server...",file=sys.stderr)
        return 0
    except Exception as e:
        print(f" Error running server: {e}",file=sys.stderr)
        return 1

if __name__ == "__main__":
    exit(main())
