# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from battle import battle
from character import AbilityScores, Character
from equipment import Weapon, Armor

# Create an AbilityScores object
ability_scores1 = AbilityScores(strength=18, dexterity=14, wisdom=12, constitution=15, intelligence=13, charisma=16)
ability_scores2 = AbilityScores(strength=11, dexterity=18, wisdom=12, constitution=15, intelligence=13, charisma=16)


#Make some weapons
#define fist/unarmed as default
weapon1 = Weapon(name='Sword', weight=10, speed=3, min_damage=1, max_damage=6)
weapon2 = Weapon(name='Bow', weight=6, speed=4, min_damage=1, max_damage=6)

# Create a DnDCharacter object with the above AbilityScores
character1 = Character(name='Sturm', race='Human', class_type='Warrior', level=10, health=25,
                          ability_scores=ability_scores1)
character2 = Character(name='Daisy', race='Elf', class_type='Rogue', level=10, health=25,
                          ability_scores=ability_scores2)



character1.equip_weapon(weapon1)
character2.equip_weapon(weapon2)
# Call the attack() method of the character
battle(character1, character2)



