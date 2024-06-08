import random
from abc import ABC
from typing import Union, Optional, Dict, Tuple, Any

from gymnasium.core import ActType, ObsType
from poke_env import RandomPlayer, SimpleHeuristicsPlayer, Player
from poke_env.environment import AbstractBattle
from poke_env.player import EnvPlayer, BattleOrder, ForfeitBattleOrder

from gym import helpers
from gym.player import MaxDamagePlayer
from gym.reward import RewardValues


class RLSimpleAgentsEnv(EnvPlayer[ObsType, ActType], ABC):
    _ACTION_SPACE = list(range(2 * 4 + 6))
    _DEFAULT_BATTLE_FORMAT = "gen9randombattle"
    invalid_action = False
    reward_values: RewardValues

    def __init__(self, player: Union[Player, str] = None, reward_values: RewardValues = RewardValues()):
        if player:
            self.opponents = [player]
        else:
            self.opponents = [RandomPlayer(), MaxDamagePlayer(), SimpleHeuristicsPlayer()]
        self.reward_values = reward_values
        super().__init__(random.choice(self.opponents))

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[ObsType, Dict[str, Any]]:
        a, b = super().reset(seed=seed, options=options)
        super().set_opponent(opponent=random.choice(self.opponents))
        return a, b

    def embed_battle(self, battle):
        return helpers.build_battle_observation(battle=battle)

    def calc_reward(self, last_state: AbstractBattle, current_state: AbstractBattle) -> float:
        return self.reward_computing_helper(
            current_state,
            fainted_value=self.reward_values.fainted_value,
            hp_value=self.reward_values.hp_value,
            status_value=self.reward_values.status_value,
            invalid_action_value=self.reward_values.invalid_action_value,
            victory_value=self.reward_values.victory_value)

    def reward_computing_helper(
        self,
        battle: AbstractBattle,
        *,
        fainted_value: float = 0.0,
        hp_value: float = 0.0,
        number_of_pokemons: int = 6,
        starting_value: float = 0.0,
        status_value: float = 0.0,
        victory_value: float = 1.0,
        invalid_action_value: float = 0.0,
    ) -> float:
        if battle not in self._reward_buffer:
            self._reward_buffer[battle] = starting_value
        current_value = 0

        for mon in battle.team.values():
            current_value += mon.current_hp_fraction * hp_value
            if mon.fainted:
                current_value -= fainted_value
            elif mon.status is not None:
                current_value -= status_value

        current_value += (number_of_pokemons - len(battle.team)) * hp_value

        for mon in battle.opponent_team.values():
            current_value -= mon.current_hp_fraction * hp_value
            if mon.fainted:
                current_value += fainted_value
            elif mon.status is not None:
                current_value += status_value

        current_value -= (number_of_pokemons - len(battle.opponent_team)) * hp_value

        if battle.won:
            current_value += victory_value
        elif battle.lost:
            current_value -= victory_value

        if self.invalid_action:
            current_value -= invalid_action_value

        to_return = current_value - self._reward_buffer[battle]
        self._reward_buffer[battle] = current_value

        return to_return

    def describe_embedding(self):
        return helpers.build_observation_space()

    def action_to_move(self, action: int, battle: AbstractBattle) -> BattleOrder:
        self.invalid_action = False
        if action == -1:
            return ForfeitBattleOrder()
        elif (
                action < 4
                and action < len(battle.available_moves)
                and not battle.force_switch
        ):
            return self.agent.create_order(battle.available_moves[action])
        elif (
                battle.can_tera
                and 0 <= action - 4 < len(battle.available_moves)
                and not battle.force_switch
        ):
            return self.agent.create_order(
                battle.available_moves[action - 4], terastallize=True
            )
        elif 0 <= action - 8 < len(battle.available_switches):
            return self.agent.create_order(battle.available_switches[action - 8])
        else:
            self.invalid_action = True
            return self.agent.choose_random_move(battle)

    async def close(self, purge: bool = True):
        super().close(purge)
        await self.agent.ps_client.stop_listening()

