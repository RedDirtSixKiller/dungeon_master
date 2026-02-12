import random

from character import AbilityScores, Character
from equipment import Weapon
from game_engine import GameEngine


def _characters():
    c1 = Character(
        name="A",
        race="Human",
        char_class="Fighter",
        level=1,
        health=12,
        ability_scores=AbilityScores(16, 12, 12, 10, 10, 10),
        weapon=Weapon("Longsword", 3, 0, 1, 8),
    )
    c2 = Character(
        name="B",
        race="Elf",
        char_class="Rogue",
        level=1,
        health=10,
        ability_scores=AbilityScores(10, 14, 10, 10, 10, 10),
        weapon=Weapon("Dagger", 1, 0, 1, 4),
    )
    return c1, c2


def test_attack_event_logs_rolls_and_damage():
    c1, c2 = _characters()
    engine = GameEngine([c1, c2], rng=random.Random(1))

    event = engine.perform_action("A", "B", "I attack with my sword")

    assert event.action == "attack"
    assert len(event.rolls) in (1, 2)
    assert event.target == "B"
    assert event.target_hp == c2.health


def test_heal_action_increases_actor_health():
    c1, c2 = _characters()
    c1.health = 3
    engine = GameEngine([c1, c2], rng=random.Random(2))

    event = engine.perform_action("A", "B", "I heal and recover")

    assert event.action == "heal"
    assert c1.health > 3
    assert event.damage < 0
