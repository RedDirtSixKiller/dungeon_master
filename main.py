
from battle import Battle
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
char1 = Character(name='Sturm', race='Human', char_class='Warrior', level=10, health=25,
                  ability_scores=ability_scores1)
char2 = Character(name='Daisy', race='Drow Elf', char_class='Rogue', level=10, health=25,
                  ability_scores=ability_scores2)



# Call the attack() method of the character
battle = Battle(char1, char2)
battle.start()

