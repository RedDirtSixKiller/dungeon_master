import random

from character import AbilityScores, Character
from equipment import Weapon
from session import AdventureSession


class DummyNarrator:
    def narrate(self, event, action_text):
        return f"{event.actor}::{event.action}::{action_text}"


class StructuredDummyNarrator:
    def narrate(self, event, action_text):
        return "fallback"

    def narrate_structured(self, event, action_text, mechanics_summary, scene_state):
        return {
            "narrative": f"Structured:{event.actor}:{event.action}",
            "scene_overview_update": "The chapel fills with drifting ash.",
            "state_notes": ["A pillar collapses near the altar."],
            "image_prompt_addendum": "Ash clouds and cracked stone floor.",
        }


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


def test_process_turn_emits_mechanics_state_and_prompt():
    c1, c2 = _characters()
    session = AdventureSession([c1, c2], narrator=DummyNarrator(), rng=random.Random(1))

    result = session.process_turn("A", "B", "I attack with my sword")

    assert "action=attack" in result.mechanics_summary
    assert "roll_1" in result.mechanics_summary
    assert result.state_delta["actor"] == "A"
    assert result.state_delta["target"] == "B"
    assert "Illustration prompt for a fantasy RPG scene" in result.image_prompt
    assert result.scene_state["turn"] == 1


def test_healing_is_capped_at_starting_max_hp():
    c1, c2 = _characters()
    c1.health = 11
    session = AdventureSession([c1, c2], narrator=DummyNarrator(), rng=random.Random(2))

    result = session.process_turn("A", "B", "I recover and heal")

    assert c1.health == 11
    assert result.event.action == "heal"
    assert result.event.damage == 0
    assert result.state_delta["healing"] == 0


def test_structured_narrator_updates_scene_and_state_notes():
    c1, c2 = _characters()
    session = AdventureSession([c1, c2], narrator=StructuredDummyNarrator(), rng=random.Random(1))

    result = session.process_turn("A", "B", "I attack with my sword")

    assert result.narrative == "Structured:A:attack"
    assert result.scene_state["scene_overview"] == "The chapel fills with drifting ash."
    assert result.ai_state_notes == ["A pillar collapses near the altar."]
    assert "Ash clouds and cracked stone floor." in result.image_prompt
