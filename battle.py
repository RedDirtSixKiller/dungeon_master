from character import Character


from character import Character
from get_story import get_completion

def battle(attacker: Character, defender: Character, narrate: bool = False):
    while attacker.health > 0 and defender.health > 0:
        # Get attacker's damage roll
        if attacker.weapon is None:
            damage_roll = 1  # Default damage roll if no weapon is equipped
        else:
            damage_roll = attacker.weapon.damage_roll()

        # Get defender's armor class
        if defender.armor is None:
            armor_class = -10  # Default armor class if no armor is equipped
        else:
            armor_class = defender.armor.protection

        # Calculate damage
        damage = max(0, damage_roll - armor_class)

        # Apply damage to defender
        defender.take_damage(damage)

        # Generate battle narrative
        if narrate:
            prompt = f"""
            Your task is to act as a dungeon master describing a combat action in dungeons and dragons.\
            Write a narrative where the characters' information is delimited by <char></char>\
            and the action is delimited by <act></act>

            Action: <char>{attacker.name}</char> <act>attacks with {attacker.weapon.name}</act> <char>{defender.name}</char>
            """
            narrative = get_completion(prompt)
            print(narrative)

        # Print battle outcome
        print(
            f"{attacker.name} attacks {defender.name} with {attacker.weapon.name} "
            f"for {damage} damage. {defender.name} has {defender.health} health remaining.")