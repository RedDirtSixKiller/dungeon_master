from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from character import Character
from game_engine import CombatEvent, GameEngine
from narrator import Narrator


@dataclass
class TurnResult:
    event: CombatEvent
    mechanics_summary: str
    state_delta: Dict[str, object]
    scene_state: Dict[str, object]
    narrative: str
    image_prompt: str


class AdventureSession:
    """High-level gameplay loop: intent -> mechanics -> narrative -> updated scene."""

    def __init__(
        self,
        characters: List[Character],
        narrator: Optional[Narrator] = None,
        scene_overview: str = "A tense dungeon skirmish lit by torches.",
        rng: Optional[random.Random] = None,
    ):
        self.engine = GameEngine(characters, rng=rng)
        self.narrator = narrator or Narrator()
        self.scene_overview = scene_overview
        self.turn_number = 0
        self.history: List[TurnResult] = []
        self._max_hp: Dict[str, int] = {c.name.lower(): c.health for c in characters}

    def process_turn(self, actor_name: str, target_name: str, intent: str) -> TurnResult:
        actor = self.engine.characters[actor_name.lower()]
        target = self.engine.characters[target_name.lower()]
        actor_hp_before = actor.health
        target_hp_before = target.health

        event = self.engine.perform_action(actor_name, target_name, intent)
        self._cap_healing(actor.name, actor_hp_before, event)

        self.turn_number += 1
        mechanics = self._mechanics_summary(event)
        state_delta = self._state_delta(event, actor_hp_before, target_hp_before)
        scene_state = self.scene_state()
        narrative = self.narrator.narrate(event, intent)
        image_prompt = self._image_prompt(event, intent, narrative)

        result = TurnResult(
            event=event,
            mechanics_summary=mechanics,
            state_delta=state_delta,
            scene_state=scene_state,
            narrative=narrative,
            image_prompt=image_prompt,
        )
        self.history.append(result)
        return result

    def scene_state(self) -> Dict[str, object]:
        actors = []
        for character in self.engine.turn_order:
            actors.append(
                {
                    "name": character.name,
                    "class": character.char_class,
                    "race": character.race,
                    "hp": character.health,
                    "defeated": character.health <= 0,
                    "weapon": character.weapon.name if character.weapon else None,
                    "armor": character.armor.name if character.armor else None,
                }
            )
        return {"turn": self.turn_number, "scene_overview": self.scene_overview, "actors": actors}

    def _cap_healing(self, actor_name: str, actor_hp_before: int, event: CombatEvent) -> None:
        if event.action != "heal":
            return
        actor = self.engine.characters[actor_name.lower()]
        max_hp = self._max_hp[actor_name.lower()]
        if actor.health <= max_hp:
            return
        actor.health = max_hp
        healed = max(0, actor.health - actor_hp_before)
        event.damage = -healed
        event.actor_hp = actor.health
        event.target_hp = actor.health

    def _state_delta(self, event: CombatEvent, actor_hp_before: int, target_hp_before: int) -> Dict[str, object]:
        actor_hp_after = self.engine.characters[event.actor.lower()].health
        target_hp_after = self.engine.characters[event.target.lower()].health
        if event.action == "heal":
            target_hp_before = actor_hp_before
            target_hp_after = actor_hp_after

        return {
            "actor": event.actor,
            "target": event.target,
            "action": event.action,
            "actor_hp_before": actor_hp_before,
            "actor_hp_after": actor_hp_after,
            "target_hp_before": target_hp_before,
            "target_hp_after": target_hp_after,
            "damage": event.damage if event.damage > 0 else 0,
            "healing": abs(event.damage) if event.damage < 0 else 0,
            "target_defeated": target_hp_after <= 0,
        }

    @staticmethod
    def _mechanics_summary(event: CombatEvent) -> str:
        lines = [f"action={event.action} | actor={event.actor} | target={event.target}"]
        if event.rolls:
            for index, roll in enumerate(event.rolls, start=1):
                lines.append(
                    f"roll_{index}: {roll.formula} -> {roll.rolls} + {roll.modifier} = {roll.total}"
                )
        else:
            lines.append("rolls: none")
        lines.append(f"hit={event.hit} | damage={event.damage} | actor_hp={event.actor_hp} | target_hp={event.target_hp}")
        return "\n".join(lines)

    def _image_prompt(self, event: CombatEvent, intent: str, narrative: str) -> str:
        return (
            "Illustration prompt for a fantasy RPG scene. "
            f"Scene: {self.scene_overview} "
            f"Turn {self.turn_number}: {event.actor} attempts '{intent}' against {event.target}. "
            f"Outcome: action={event.action}, hit={event.hit}, damage={event.damage}, "
            f"{event.actor} hp={event.actor_hp}, {event.target} hp={event.target_hp}. "
            f"Narrative tone: {narrative}"
        )
