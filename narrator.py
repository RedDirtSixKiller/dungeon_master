from __future__ import annotations

import os
from typing import Optional

from game_engine import CombatEvent

import importlib.util

OpenAI = None
if importlib.util.find_spec("openai") is not None:
    from openai import OpenAI


class Narrator:
    """Narrates combat outcomes with optional OpenAI enhancement."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None
        api_key = os.getenv("OPENAI_API_KEY")
        if OpenAI and api_key:
            self._client = OpenAI(api_key=api_key)

    def narrate(self, event: CombatEvent, action_text: str) -> str:
        if self._client is None:
            return self._fallback(event, action_text)

        prompt = (
            "You are a Dungeon Master. Keep the narration to 2-3 sentences and include concrete mechanics.\n"
            f"Player intent: {action_text}\n"
            f"Resolved event: action={event.action}, actor={event.actor}, target={event.target}, "
            f"hit={event.hit}, damage={event.damage}, actor_hp={event.actor_hp}, target_hp={event.target_hp}.\n"
            f"Roll details: {[(r.formula, r.rolls, r.modifier, r.total) for r in event.rolls]}"
        )
        response = self._client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.output_text.strip()

    @staticmethod
    def _fallback(event: CombatEvent, action_text: str) -> str:
        if event.action == "observe":
            return (
                f"{event.actor} pauses to assess the battlefield after trying to '{action_text}'. "
                f"{event.target} stands at {event.target_hp} HP."
            )
        if event.action == "heal":
            healed = abs(event.damage)
            return f"{event.actor} steadies their breath and recovers {healed} HP, rising to {event.actor_hp} HP."

        if event.hit:
            return (
                f"{event.actor} follows through on '{action_text}' and lands a hit on {event.target}, "
                f"dealing {event.damage} damage. {event.target} is now at {event.target_hp} HP."
            )
        return (
            f"{event.actor} attempts '{action_text}', but {event.target} avoids the blow. "
            f"{event.target} remains at {event.target_hp} HP."
        )
