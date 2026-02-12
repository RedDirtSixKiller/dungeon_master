from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Dict, List, Optional

from character import Character


@dataclass
class DiceRoll:
    formula: str
    rolls: List[int]
    modifier: int = 0

    @property
    def total(self) -> int:
        return sum(self.rolls) + self.modifier


@dataclass
class CombatEvent:
    actor: str
    target: str
    action: str
    hit: Optional[bool]
    damage: int
    actor_hp: int
    target_hp: int
    rolls: List[DiceRoll] = field(default_factory=list)


class GameEngine:
    """Lightweight rules engine for text-driven combat actions."""

    def __init__(self, characters: List[Character], rng: Optional[random.Random] = None):
        if len(characters) < 2:
            raise ValueError("GameEngine requires at least two characters")
        self.characters: Dict[str, Character] = {c.name.lower(): c for c in characters}
        self.turn_order: List[Character] = characters[:]
        self.log: List[CombatEvent] = []
        self._rng = rng or random.Random()

    def roll(self, num: int, sides: int, modifier: int = 0) -> DiceRoll:
        rolls = [self._rng.randint(1, sides) for _ in range(num)]
        return DiceRoll(formula=f"{num}d{sides}", rolls=rolls, modifier=modifier)

    @staticmethod
    def ability_modifier(score: int) -> int:
        return (score - 10) // 2

    def armor_class(self, character: Character) -> int:
        dex_mod = self.ability_modifier(character.ability_scores.dexterity)
        armor_bonus = character.armor.protection if character.armor else 0
        return 10 + dex_mod + armor_bonus

    def parse_action(self, text: str) -> str:
        lowered = text.lower()
        if any(token in lowered for token in ("heal", "potion", "recover")):
            return "heal"
        if any(token in lowered for token in ("inspect", "look", "observe")):
            return "observe"
        return "attack"

    def perform_action(self, actor_name: str, target_name: str, description: str) -> CombatEvent:
        actor = self.characters[actor_name.lower()]
        target = self.characters[target_name.lower()]
        action = self.parse_action(description)

        if action == "heal":
            roll = self.roll(1, 8, self.ability_modifier(actor.ability_scores.constitution))
            healed = max(1, roll.total)
            actor.health += healed
            event = CombatEvent(
                actor=actor.name,
                target=actor.name,
                action=action,
                hit=None,
                damage=-healed,
                actor_hp=actor.health,
                target_hp=actor.health,
                rolls=[roll],
            )
            self.log.append(event)
            return event

        if action == "observe":
            event = CombatEvent(
                actor=actor.name,
                target=target.name,
                action=action,
                hit=None,
                damage=0,
                actor_hp=actor.health,
                target_hp=target.health,
                rolls=[],
            )
            self.log.append(event)
            return event

        attack_roll = self.roll(1, 20, self.ability_modifier(actor.ability_scores.strength) + 2)
        hit = attack_roll.total >= self.armor_class(target)
        damage = 0
        rolls = [attack_roll]
        if hit:
            weapon_roll = self.roll(
                1,
                actor.weapon.max_damage,
                self.ability_modifier(actor.ability_scores.strength),
            )
            # honor weapon minimum damage as a floor
            damage = max(actor.weapon.min_damage, weapon_roll.total)
            target.health -= damage
            rolls.append(weapon_roll)

        event = CombatEvent(
            actor=actor.name,
            target=target.name,
            action=action,
            hit=hit,
            damage=damage,
            actor_hp=actor.health,
            target_hp=target.health,
            rolls=rolls,
        )
        self.log.append(event)
        return event

    def is_defeated(self, name: str) -> bool:
        return self.characters[name.lower()].health <= 0
