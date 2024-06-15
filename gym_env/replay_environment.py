from typing import Dict, List, SupportsFloat, Any

import numpy as np
from gymnasium import Env
from gymnasium.core import ActType, ObsType
from gymnasium.vector.utils import spaces
from poke_env.environment import Battle

from gym_env import helpers
from gym_env.reward import RewardValues
from replays.replay import Replay


class ReplayEnv(Env):
    def __init__(self, replays: List[Replay], reward_values: RewardValues = RewardValues()):
        super(ReplayEnv, self).__init__()
        self.observation_space = helpers.build_observation_space()
        self.action_space = spaces.Discrete(14)
        self.turn = 0
        self.replays = replays
        self.current_battle: [Battle, None] = None
        self.current_replay: [Replay, None] = None
        self.reward_values: RewardValues = reward_values
        self._reward_buffer: Dict[Battle, float] = {}

    def step(
            self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        if self.current_battle is None or self.current_battle.finished:
            self.current_battle, self.current_replay = helpers.build_replay_battle(self.replays)
            helpers.execute_replay_turn(self.current_battle, self.current_replay)
        force_switch, done, won = helpers.execute_replay_turn(self.current_battle, self.current_replay)
        if self._reward_buffer.get(self.current_battle, None) is None:
            self._reward_buffer[self.current_battle] = 0
        reward = helpers.calculate_reward(
            won=won,
            battle=self.current_battle,
            previous_value=self._reward_buffer[self.current_battle],
            reward_values=self.reward_values)
        total_reward = reward - self._reward_buffer[self.current_battle]
        self._reward_buffer[self.current_battle] = reward
        if not force_switch:
            self.turn += 1
        return helpers.build_battle_observation(battle=self.current_battle), total_reward, done, False, {}

    def reset(
            self,
            *,
            seed: int | None = None,
            options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        super().reset(seed=seed)
        self.current_battle = None
        self.current_replay = None
        self.turn = 0
        return np.array([-1, -1, -1, -1, 0, 0, 0, 0, 0, 0], dtype=np.float32), {}

    def render(self) -> None:
        if self.current_battle:
            helpers.print_battle(self.current_battle)
        else:
            print('no active battle yet')
        return
