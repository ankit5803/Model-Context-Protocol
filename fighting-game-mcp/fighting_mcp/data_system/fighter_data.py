class Fighter:
    def __init__(self, name, style, health, attack, defense, speed, move="Punch"):
        self.name = name
        self.style = style
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.move = move  # Used in battle narration

    def to_dict(self):
        return {
            "name": self.name,
            "style": self.style,
            "health": self.health,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "move": self.move
        }

class FighterDataSystem:
    def __init__(self):
        self.fighters = [
            Fighter("Ryu", "Balanced", 100, 20, 12, 14, move="Hadouken"),
            Fighter("Ken", "Rushdown", 95, 22, 10, 16, move="Shoryuken"),
            Fighter("Chun-Li", "Speed", 90, 18, 8, 20, move="Spinning Bird Kick"),
            Fighter("Zangief", "Grappler", 120, 25, 18, 8, move="Pile Driver"),
        ]

    def get_all_fighters(self):
        return self.fighters

    def get_fighter(self, name):
        for fighter in self.fighters:
            if fighter.name.lower() == name.lower():
                return fighter
        return None

    def get_fighters_by_style(self, style):
        return [f for f in self.fighters if f.style.lower() == style.lower()]

    def get_matchup_preview(self, name1, name2):
        fighter1 = self.get_fighter(name1)
        fighter2 = self.get_fighter(name2)

        if not fighter1 or not fighter2:
            return {"error": "One or both fighters not found."}

        matchup = {
            "fighter1": fighter1.to_dict(),
            "fighter2": fighter2.to_dict(),
            "analysis": {
                "speed_advantage": fighter1.name if fighter1.speed > fighter2.speed else fighter2.name,
                "attack_advantage": fighter1.name if fighter1.attack > fighter2.attack else fighter2.name,
                "defense_advantage": fighter1.name if fighter1.defense > fighter2.defense else fighter2.name
            }
        }
        return matchup

    def search_fighters(self, query):
        query = query.lower()
        return [
            f for f in self.fighters
            if query in f.name.lower() or query in f.style.lower()
        ]

fighter_data_system = FighterDataSystem()
