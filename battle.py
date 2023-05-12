from character import Character


def battle(attacker: Character, defender: Character):
    # Get attacker's damage roll
    if attacker.weapon is None:
        damage_roll = 1  # Default damage roll if no weapon is equipped
    else:
        damage_roll = attacker.weapon.damage_roll()

    # Get defender's armor class
    if defender.armor is None:
        armor_class = 10  # Default armor class if no armor is equipped
    else:
        armor_class = defender.armor.protection

    # Calculate damage
    damage = max(0, damage_roll + armor_class)

    # Apply damage to defender
    defender.take_damage(damage)

    # Print battle outcome
    print(
        f"{attacker.name} attacks {defender.name} with {attacker.weapon.name} "
        f"for {damage} damage. {defender.name} has {defender.health} health remaining.")
