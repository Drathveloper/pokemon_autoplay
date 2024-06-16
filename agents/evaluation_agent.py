import asyncio
import os

import numpy as np
from poke_env import RandomPlayer, SimpleHeuristicsPlayer
from stable_baselines3 import DQN

from gym_env.player import MaxDamagePlayer
from gym_env.reward import RewardValues
from gym_env.simple_agents_environment import RLSimpleAgentsEnv


async def evaluate(name, env_player, model_path):
    logs_path = "../out/logs/"
    gamma = 0.99
    model = DQN.load(model_path)
    total_rewards = []
    discounted_rewards = []
    for i in range(1, 100):
        episode_reward = 0
        discounted_reward = 0
        t = 0
        obs, reward, done, _, info = env_player.step(0)
        while not done:
            action, _ = model.predict(obs, deterministic=False)
            try:
                obs, reward, done, _, info = env_player.step(action)
                episode_reward += reward
                discounted_reward += (gamma ** t) * reward
                t += 1
            except RuntimeError as e:
                print(e)
                env_player.reset()
                break
        total_rewards.append(episode_reward)
        discounted_rewards.append(discounted_reward)
        env_player.reset()
    average_reward = sum(total_rewards) / 100
    average_discounted_reward = sum(discounted_rewards) / 100
    reward_variance = np.var(total_rewards)
    success_rate = env_player.n_won_battles / 100
    with open(f"{logs_path}/execution.log", mode='a', encoding='utf-8') as logfile:
        player = env_player.get_opponent().username.split(' ')[0]
        logfile.write(f'{name}|{player}|{average_reward}|{average_discounted_reward}|{reward_variance}|{success_rate}\n')
    await env_player.close(purge=True)


async def main():
    model_dir = os.environ['MODEL_PATH']
    model_file_names = [f for f in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, f)) and f.endswith(".zip")]
    model_file_names = sorted(model_file_names)
    for model_file in model_file_names:
        model_name = model_file.split('.')[0]
        with open(f"{model_dir}/{model_name}.metadata") as metadata_file:
            metadata = metadata_file.readline().replace('\n', '').split('|')
            reward_values = RewardValues(
                fainted_value=float(metadata[0]),
                hp_value=float(metadata[1]),
                status_value=float(metadata[2]),
                invalid_action_value=float(metadata[3]),
                victory_value=float(metadata[4])
            )
            print('Evaluating model ' + model_file)
            env_player = RLSimpleAgentsEnv(player=RandomPlayer(), reward_values=reward_values)
            await evaluate(model_name, env_player, model_dir + '/' + model_file)
            env_player = RLSimpleAgentsEnv(player=MaxDamagePlayer(), reward_values=reward_values)
            await evaluate(model_name, env_player, model_dir + '/' + model_file)
            env_player = RLSimpleAgentsEnv(player=SimpleHeuristicsPlayer(), reward_values=reward_values)
            await evaluate(model_name, env_player, model_dir + '/' + model_file)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
