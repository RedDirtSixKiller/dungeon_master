from character import AbilityScores, Character
from equipment import Armor, Weapon
from game_engine import GameEngine
from narrator import Narrator


ability_scores1 = AbilityScores(strength=18, dexterity=14, wisdom=12, constitution=15, intelligence=13, charisma=16)
ability_scores2 = AbilityScores(strength=11, dexterity=18, wisdom=12, constitution=15, intelligence=13, charisma=16)

weapon1 = Weapon(name="Sword", weight=10, speed=3, min_damage=1, max_damage=8)
weapon2 = Weapon(name="Bow", weight=6, speed=4, min_damage=1, max_damage=6)
armor1 = Armor(name="Chain Shirt", weight=20, speed=0, protection=2)
armor2 = Armor(name="Leather", weight=10, speed=0, protection=1)

char1 = Character(
    name="Sturm",
    race="Human",
    char_class="Warrior",
    level=10,
    health=25,
    ability_scores=ability_scores1,
    weapon=weapon1,
    armor=armor1,
)
char2 = Character(
    name="Daisy",
    race="Drow Elf",
    char_class="Rogue",
    level=10,
    health=25,
    ability_scores=ability_scores2,
    weapon=weapon2,
    armor=armor2,
)

engine = GameEngine([char1, char2])
narrator = Narrator()

scene_actions = [
    ("Sturm", "Daisy", "I charge and slash with my sword"),
    ("Daisy", "Sturm", "I fire a quick arrow while stepping back"),
    ("Sturm", "Daisy", "I recover and catch my breath"),
]

for actor, target, text in scene_actions:
    if engine.is_defeated(actor) or engine.is_defeated(target):
        break
    event = engine.perform_action(actor, target, text)

    print(f"\nAction: {actor} -> {target} | '{text}'")
    for roll in event.rolls:
        print(f"  Roll {roll.formula}: {roll.rolls} + {roll.modifier} = {roll.total}")
    print(f"  Outcome: {event.action}, hit={event.hit}, damage={event.damage}")
    actor_hp = engine.characters[actor.lower()].health
    target_hp = engine.characters[target.lower()].health
    print(f"  HP: {actor}={actor_hp}, {target}={target_hp}")
    print(f"  Narrative: {narrator.narrate(event, text)}")

print("\nFinal state:")
for c in (char1, char2):
    print(f"- {c.name}: {c.health} HP")
