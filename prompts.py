from character import Character


class BattlePrompt:
    def __init__(self, char1: Character, char2: Character):
        self.char1 = char1
        self.char2 = char2

    def generate_prompt(self):
        """
        Generate a prompt for the OpenAI plugin to narrate a battle between two characters.

        Returns:
        - str: A detailed prompt for the OpenAI plugin.
        """

        prompt = (f"Create a detailed narration for a battle in a Dungeons & Dragons setting. "
                  f"Here are the details:\n\n"
                  f"Character 1:\n"
                  f"Name: {self.char1.name}\n"
                  f"Class: {self.char1.char_class}\n"
                  f"Weapon: {self.char1.weapon}\n"
                  f"Armor: {self.char1.armor}\n"
                  f"Attack Roll: {self.char1.attack_roll}\n\n"
                  f"Character 2:\n"
                  f"Name: {self.char2.name}\n"
                  f"Class: {self.char2.char_class}\n"
                  f"Weapon: {self.char2.weapon}\n"
                  f"Armor: {self.char2.armor}\n"
                  f"Attack Roll: {self.char2.attack_roll}\n\n"
                  f"Narrate the battle, describing the strategies, actions, and outcome based on the attack rolls "
                  f"provided.")

        return prompt
