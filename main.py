from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from character import AbilityScores, Character
from equipment import Armor, Weapon
from narrator import Narrator
from session import AdventureSession


def build_default_session() -> Tuple[AdventureSession, str]:
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

    session = AdventureSession(
        [char1, char2],
        narrator=Narrator(),
        scene_overview="A ruined chapel in the underdark, lit by bioluminescent moss and torch smoke.",
    )
    return session, char1.name


def alive_names(session: AdventureSession) -> List[str]:
    return [c.name for c in session.engine.turn_order if c.health > 0]


def resolve_target(session: AdventureSession, token: str, actor_name: str) -> Optional[str]:
    token = token.strip().lower()
    for name in alive_names(session):
        if name.lower() == token and name.lower() != actor_name.lower():
            return name
    for name in alive_names(session):
        lowered = name.lower()
        if lowered.startswith(token) and lowered != actor_name.lower():
            return name
    return None


def print_status(session: AdventureSession) -> None:
    print("\nCurrent status:")
    for actor in session.scene_state()["actors"]:
        state = "DEFEATED" if actor["defeated"] else "ACTIVE"
        print(f"- {actor['name']} ({actor['class']}): {actor['hp']} HP [{state}]")


def print_turn_result(result) -> None:
    print("  Mechanics:")
    for line in result.mechanics_summary.splitlines():
        print(f"    {line}")
    print(f"  State delta: {result.state_delta}")
    print(f"  Narrative: {result.narrative}")
    if result.ai_state_notes:
        print(f"  AI state notes: {result.ai_state_notes}")
    print(f"  Image prompt: {result.image_prompt}")


def choose_default_target(session: AdventureSession, actor_name: str) -> Optional[str]:
    for name in alive_names(session):
        if name.lower() != actor_name.lower():
            return name
    return None


def parse_player_command(
    session: AdventureSession, actor_name: str, command: str
) -> Optional[Tuple[str, str, str]]:
    raw = "".join(ch for ch in command if ch.isprintable()).strip()
    if not raw:
        return None

    parts = raw.split()
    verb = re.sub(r"[^a-zA-Z]", "", parts[0]).lower()

    if verb in {"quit", "exit"}:
        return ("quit", actor_name, "")
    if verb == "help":
        return ("help", actor_name, "")
    if verb == "status":
        return ("status", actor_name, "")

    if verb == "heal":
        intent = raw if len(parts) > 1 else "I recover and catch my breath."
        return (actor_name, actor_name, intent)

    if verb == "observe":
        if len(parts) < 2:
            target = choose_default_target(session, actor_name)
            if not target:
                return None
            return (actor_name, target, "I observe the battlefield carefully.")
        target = resolve_target(session, parts[1], actor_name)
        if not target:
            return None
        intent = " ".join(parts[2:]).strip() or f"I observe {target} for weaknesses."
        return (actor_name, target, intent)

    if verb == "attack":
        if len(parts) < 2:
            return None
        target = resolve_target(session, parts[1], actor_name)
        if not target:
            return None
        intent = " ".join(parts[2:]).strip() or f"I attack {target} with my weapon."
        return (actor_name, target, intent)

    # Fallback: free text treated as attack intent against first available target.
    target = choose_default_target(session, actor_name)
    if not target:
        return None
    return (actor_name, target, raw)


def ai_turn(session: AdventureSession, actor_name: str, player_name: str):
    actor = session.engine.characters[actor_name.lower()]
    player = session.engine.characters[player_name.lower()]

    if actor.health <= 7:
        return session.process_turn(actor.name, actor.name, "I steady myself and recover.")

    if player.health > 0:
        return session.process_turn(actor.name, player.name, "I fire a quick attack at my foe.")

    target = choose_default_target(session, actor_name)
    if target is None:
        return None
    return session.process_turn(actor.name, target, "I strike at the nearest enemy.")


def run_cli() -> None:
    session, player_name = build_default_session()
    turn_index = 0
    turn_order = [c.name for c in session.engine.turn_order]

    print("Dungeon Master CLI")
    print("Commands: attack <target> [intent], heal [intent], observe [target] [intent], status, help, quit")
    print_status(session)

    while True:
        alive = alive_names(session)
        if player_name not in [name for name in alive]:
            print("\nYou were defeated. Game over.")
            break
        if len(alive) <= 1:
            print(f"\nCombat complete. Winner: {alive[0]}")
            break

        actor_name = turn_order[turn_index % len(turn_order)]
        if session.engine.is_defeated(actor_name):
            turn_index += 1
            continue

        print(f"\nTurn {session.turn_number + 1}: {actor_name}")
        if actor_name.lower() == player_name.lower():
            command = input("> ").strip()
            parsed = parse_player_command(session, actor_name, command)
            if parsed is None:
                print("Invalid command. Try: attack <target>, heal, observe, status, help, quit")
                continue

            if parsed[0] == "quit":
                print("Session ended by player.")
                break
            if parsed[0] == "help":
                print("Commands: attack <target> [intent], heal [intent], observe [target] [intent], status, help, quit")
                continue
            if parsed[0] == "status":
                print_status(session)
                continue

            actor, target, intent = parsed
            result = session.process_turn(actor, target, intent)
            print_turn_result(result)
            turn_index += 1
            continue

        result = ai_turn(session, actor_name, player_name)
        if result is not None:
            print_turn_result(result)
        turn_index += 1

    print("\nFinal state:")
    print_status(session)


if __name__ == "__main__":
    run_cli()
