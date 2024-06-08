from typing import Optional, Tuple

import numpy as np
from gymnasium import spaces
from stable_baselines3 import DQN
from stable_baselines3.common.noise import ActionNoise

from gym import helpers


class CustomDQN(DQN):
    def __init__(
            self,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

    def _sample_action(
            self,
            learning_starts: int,
            action_noise: Optional[ActionNoise] = None,
            n_envs: int = 1,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sample an action according to the exploration policy.
        This is either done by sampling the probability distribution of the policy,
        or sampling a random action (from a uniform distribution over the action space)
        or by adding noise to the deterministic output.

        :param action_noise: Action noise that will be used for exploration
            Required for deterministic policy (e.g. TD3). This can also be used
            in addition to the stochastic policy for SAC.
        :param learning_starts: Number of steps before learning for the warm-up phase.
        :param n_envs:
        :return: action to take in the environment
            and scaled action that will be stored in the replay buffer.
            The two differs when the action space is not normalized (bounds are not [-1, 1]).
        """
        unscaled_action = -1
        # ugly hack to sync actions from env we are working on
        env = self.env.envs[0].env
        if env.__class__.__name__ == "ReplayEnv":
            # override all this behavior to return exactly the action we want
            if env.current_battle is None or env.current_battle.finished:
                env.current_battle, env.current_replay = helpers.build_replay_battle(env.replays)
                helpers.execute_replay_turn(env.current_battle, env.current_replay)
            if env.current_replay:
                raw_action = helpers.pick_replay_action(env.current_battle, env.current_replay)
                unscaled_action = np.array([raw_action for _ in range(n_envs)])

            # Rescale the action from [low, high] to [-1, 1]
            if isinstance(self.action_space, spaces.Box):
                scaled_action = self.policy.scale_action(unscaled_action)
                buffer_action = scaled_action
                action = self.policy.unscale_action(scaled_action)
            else:
                buffer_action = unscaled_action
                action = buffer_action
            return action, buffer_action
        return super()._sample_action(learning_starts, action_noise, n_envs)

