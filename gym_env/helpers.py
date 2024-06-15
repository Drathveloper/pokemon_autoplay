import json
import logging
import random

import numpy as np

from gymnasium.spaces import Box
from typing import List, Optional, Tuple
from poke_env.environment import Battle, AbstractBattle
from poke_env.data import GenData

from gym_env.reward import RewardValues
from replays.replay import Replay


def build_replay_battle(replays: List[Replay]) -> Tuple[Battle, Replay]:
    random.shuffle(replays)
    next_replay = replays.pop(0)
    battle = Battle(
        next_replay.id,
        next_replay.player_name,
        logging.getLogger("BattleLogger"),
        9,
        False)
    return battle, next_replay


def execute_replay_turn(battle: Battle, replay: Replay):
    log = ''
    force_switch = False
    done = False
    won = None
    while not log.startswith('|turn|'):
        log = replay.battle_log.pop(0)
        try:
            if log.startswith('|win|'):
                split_log = log.split('|')
                if replay.player_name == split_log[2]:
                    won = True
                else:
                    won = False
                done = True
                break
            elif log.startswith('|request|'):
                split_log = log.split('|')
                req = json.loads(split_log[2])
                battle.parse_request(req)
                force_switch = True
                break
            elif not log.startswith('|t:|') and not log == '|':
                battle.parse_message(log.split('|'))
        except Exception as ex:
            print('error happened during execution: ', ex)
    return force_switch, done, won


def calculate_reward(
        battle: AbstractBattle,
        won: Optional[bool],
        previous_value: float,
        number_of_pokemons: int = 6,
        reward_values: RewardValues = RewardValues(),
) -> float:
    current_value = 0
    for mon in battle.team.values():
        current_value += mon.current_hp_fraction * reward_values.hp_value
        if mon.fainted:
            current_value -= reward_values.fainted_value
        elif mon.status is not None:
            current_value -= reward_values.status_value
    current_value += (number_of_pokemons - len(battle.team)) * reward_values.hp_value
    for mon in battle.opponent_team.values():
        current_value -= mon.current_hp_fraction * reward_values.hp_value
        if mon.fainted:
            current_value += reward_values.fainted_value
        elif mon.status is not None:
            current_value += reward_values.status_value
    current_value -= (number_of_pokemons - len(battle.opponent_team)) * reward_values.hp_value
    if won is not None:
        if won:
            current_value += reward_values.victory_value
        else:
            current_value -= reward_values.victory_value
    return current_value - previous_value


def build_observation_space():
    low = [-1, -1, -1, -1, 0, 0, 0, 0, 0, 0]
    high = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1]
    return Box(
        np.array(low, dtype=np.float32),
        np.array(high, dtype=np.float32),
        dtype=np.float32,
    )


def build_battle_observation(battle: AbstractBattle):
    moves_base_power = -np.ones(4)
    moves_dmg_multiplier = np.ones(4)
    for i, move in enumerate(battle.active_pokemon.moves.values()):
        if battle.active_pokemon.fainted:
            break
        # scaling moves base power to improve the learning
        moves_base_power[i] = (move.base_power / 100)
        if move.type:
            moves_dmg_multiplier[i] = move.type.damage_multiplier(
                battle.opponent_active_pokemon.type_1,
                battle.opponent_active_pokemon.type_2,
                type_chart=GenData.from_gen(9).type_chart)
    remaining_mon_team = 6
    for mon in battle.team.values():
        if mon.fainted:
            remaining_mon_team -= 1
    remaining_mon_team /= 6
    remaining_mon_opponent = 6
    for mon in battle.opponent_team.values():
        if mon.fainted:
            remaining_mon_team -= 1
    remaining_mon_opponent /= 6
    return np.concatenate(
        [
            moves_base_power,
            moves_dmg_multiplier,
            [remaining_mon_team, remaining_mon_opponent],
        ],
        dtype=np.float32)


def pick_replay_action(battle: Battle, replay: Replay) -> int:
    action_log = replay.raw_input_log.pop(0)
    action = -1
    action_parts = action_log.split(' ')
    if action_parts[1] == 'move':
        move = action_parts[2]
        if not replay.poke_moves.get(battle.active_pokemon.species, None):
            replay.poke_moves[battle.active_pokemon.species] = []
        if move not in replay.poke_moves.get(battle.active_pokemon.species):
            replay.poke_moves.get(battle.active_pokemon.species).append(move)
        action = replay.poke_moves.get(battle.active_pokemon.species).index(move)
        if "terastallize" in action_parts:
            action += 4
    elif action_parts[1] == 'switch':
        switch_id = int(action_parts[2])
        action = switch_id + 7
    return action


def print_battle(battle: Battle):
    if battle is not None:
        print(
            "  Turn %4d. | [%s][%3d/%3dhp] %10.10s - %10.10s [%3d%%hp][%s]"
            % (
                battle.turn,
                "".join(
                    [
                        "⦻" if mon.fainted else "●"
                        for mon in battle.team.values()
                    ]
                ),
                battle.active_pokemon.current_hp or 0,
                battle.active_pokemon.max_hp or 0,
                battle.active_pokemon.species,
                battle.opponent_active_pokemon.species,
                battle.opponent_active_pokemon.current_hp or 0,
                "".join(
                    [
                        "⦻" if mon.fainted else "●"
                        for mon in battle.opponent_team.values()
                    ]
                ),
            ),
            end="\n" if battle.finished else "\r")
