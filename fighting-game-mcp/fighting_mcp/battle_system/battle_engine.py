import random
from copy import deepcopy
from ..data_system.fighter_data import fighter_data_system

class BattleEngine:
    def simulate_battle(self, name1: str, name2: str, max_turns: int = 20) -> dict:
        fighter1 = deepcopy(fighter_data_system.get_fighter(name1))
        fighter2 = deepcopy(fighter_data_system.get_fighter(name2))

        if not fighter1 or not fighter2:
            return {"error": "One or both fighters not found."}

        result = {
            "starting_stats": {
                fighter1.name: fighter1.health,
                fighter2.name: fighter2.health,
            },
            "turns": [],
            "winner": None,
        }

        for turn in range(1, max_turns + 1):
            if fighter1.health <= 0 or fighter2.health <= 0:
                break

            turn_events = {"turn": turn, "actions": []}

            # Fighter 1 attacks Fighter 2
            damage1 = self.calculate_damage(fighter1, fighter2)
            fighter2.health -= damage1
            fighter2.health = max(fighter2.health, 0)
            turn_events["actions"].append(
                f"{fighter1.name} used {fighter1.move}! It dealt {damage1} damage.\n  • {fighter2.name} HP: {fighter2.health}"
            )

            if fighter2.health <= 0:
                turn_events["actions"].append(f"{fighter2.name} fainted!")
                result["turns"].append(turn_events)
                result["winner"] = fighter1.name
                break

            # Fighter 2 attacks Fighter 1
            damage2 = self.calculate_damage(fighter2, fighter1)
            fighter1.health -= damage2
            fighter1.health = max(fighter1.health, 0)
            turn_events["actions"].append(
                f"{fighter2.name} used {fighter2.move}! It dealt {damage2} damage.\n  • {fighter1.name} HP: {fighter1.health}"
            )

            if fighter1.health <= 0:
                turn_events["actions"].append(f"{fighter1.name} fainted!")
                result["turns"].append(turn_events)
                result["winner"] = fighter2.name
                break

            result["turns"].append(turn_events)

        if not result["winner"]:
            result["winner"] = "Draw"

        return result

    def calculate_damage(self, attacker, defender) -> int:
        base_damage = max(5, attacker.attack - defender.defense // 2)
        return random.randint(base_damage - 3, base_damage + 3)

battle_engine = BattleEngine()
