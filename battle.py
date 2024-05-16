from actions import Actions
import random

class Battle:
    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2

    def determine_initiative(self):
        roll1 = random.randint(1, 20) + self.char1.ability_scores.dexterity
        roll2 = random.randint(1, 20) + self.char2.ability_scores.dexterity

        if roll1 > roll2:
            return self.char1, self.char2
        elif roll1 < roll2:
            return self.char2, self.char1
        else:  # If both characters have the same roll, choose randomly
            return random.choice([(self.char1, self.char2), (self.char2, self.char1)])

    def start(self):
        while self.char1.health > 0 and self.char2.health > 0:
            attacker, defender = self.determine_initiative()
            Actions.attack(attacker, defender)
            if defender.health > 0:
                Actions.attack(defender, attacker)

        # Declare the winner
        if self.char1.health > 0:
            print(f"{self.char1.name} is the winner!")
        else:
            print(f"{self.char2.name} is the winner!")