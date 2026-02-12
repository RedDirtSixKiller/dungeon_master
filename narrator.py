from __future__ import annotations

import json
from typing import Optional

from game_engine import CombatEvent
from settings import get_openai_api_key, load_dotenv

import importlib.util

OpenAI = None
if importlib.util.find_spec("openai") is not None:
    from openai import OpenAI


class Narrator:
    """Narrates combat outcomes with optional OpenAI enhancement."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None
        load_dotenv()
        api_key = get_openai_api_key()
        if OpenAI and api_key:
            self._client = OpenAI(api_key=api_key)

    def narrate(self, event: CombatEvent, action_text: str) -> str:
        return self.narrate_structured(
            event=event,
            action_text=action_text,
            mechanics_summary="",
            scene_state=None,
        )["narrative"]

    def narrate_structured(
        self,
        event: CombatEvent,
        action_text: str,
        mechanics_summary: str,
        scene_state: Optional[dict],
    ) -> dict:
        fallback = self._fallback_structured(event, action_text)
        if self._client is None:
            return fallback

        prompt = (
            "You are a Dungeon Master assistant for a deterministic rules engine.\n"
            "Return a JSON object only with keys: narrative, scene_overview_update, state_notes, image_prompt_addendum.\n"
            "Rules:\n"
            "- narrative: 2-3 sentences, grounded in mechanics.\n"
            "- scene_overview_update: short string, empty if unchanged.\n"
            "- state_notes: array of short notes about non-mechanical world state changes.\n"
            "- image_prompt_addendum: visual details to append to an image prompt.\n"
            f"Player intent: {action_text}\n"
            f"Resolved event: action={event.action}, actor={event.actor}, target={event.target}, "
            f"hit={event.hit}, damage={event.damage}, actor_hp={event.actor_hp}, target_hp={event.target_hp}.\n"
            f"Roll details: {[(r.formula, r.rolls, r.modifier, r.total) for r in event.rolls]}\n"
            f"Mechanics summary: {mechanics_summary}\n"
            f"Scene state: {scene_state}"
        )
        try:
            response = self._client.responses.create(
                model=self.model,
                input=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            parsed = json.loads(response.output_text.strip())
            return self._validate_structured(parsed, fallback)
        except Exception:
            return fallback

    @staticmethod
    def _fallback(event: CombatEvent, action_text: str) -> str:
        return Narrator._fallback_structured(event, action_text)["narrative"]

    @staticmethod
    def _fallback_structured(event: CombatEvent, action_text: str) -> dict:
        if event.action == "observe":
            return {
                "narrative": (
                    f"{event.actor} pauses to assess the battlefield after trying to '{action_text}'. "
                    f"{event.target} stands at {event.target_hp} HP."
                ),
                "scene_overview_update": "",
                "state_notes": [f"{event.actor} studies {event.target}'s movement."],
                "image_prompt_addendum": "Tense eye contact and cautious footwork.",
            }
        if event.action == "heal":
            healed = abs(event.damage)
            return {
                "narrative": f"{event.actor} steadies their breath and recovers {healed} HP, rising to {event.actor_hp} HP.",
                "scene_overview_update": "",
                "state_notes": [f"{event.actor} regains composure."],
                "image_prompt_addendum": "A brief defensive stance and controlled breathing.",
            }

        if event.hit:
            return {
                "narrative": (
                    f"{event.actor} follows through on '{action_text}' and lands a hit on {event.target}, "
                    f"dealing {event.damage} damage. {event.target} is now at {event.target_hp} HP."
                ),
                "scene_overview_update": "",
                "state_notes": [f"{event.target} is pressured by {event.actor}'s attack."],
                "image_prompt_addendum": "Motion blur from a decisive strike.",
            }
        return {
            "narrative": (
                f"{event.actor} attempts '{action_text}', but {event.target} avoids the blow. "
                f"{event.target} remains at {event.target_hp} HP."
            ),
            "scene_overview_update": "",
            "state_notes": [f"{event.target} evades and keeps distance."],
            "image_prompt_addendum": "A near miss with defensive movement.",
        }

    @staticmethod
    def _validate_structured(payload: dict, fallback: dict) -> dict:
        if not isinstance(payload, dict):
            return fallback

        narrative = payload.get("narrative")
        scene_overview_update = payload.get("scene_overview_update", "")
        state_notes = payload.get("state_notes", [])
        image_prompt_addendum = payload.get("image_prompt_addendum", "")

        if not isinstance(narrative, str) or not narrative.strip():
            return fallback
        if not isinstance(scene_overview_update, str):
            scene_overview_update = ""
        if not isinstance(state_notes, list):
            state_notes = []
        else:
            state_notes = [str(note) for note in state_notes if isinstance(note, (str, int, float))]
        if not isinstance(image_prompt_addendum, str):
            image_prompt_addendum = ""

        return {
            "narrative": narrative.strip(),
            "scene_overview_update": scene_overview_update.strip(),
            "state_notes": state_notes,
            "image_prompt_addendum": image_prompt_addendum.strip(),
        }
