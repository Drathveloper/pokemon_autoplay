import asyncio

from poke_env import RandomPlayer, SimpleHeuristicsPlayer
from stable_baselines3 import DQN

from gym_env.player import MaxDamagePlayer
from gym_env.simple_agents_environment import RLSimpleAgentsEnv


async def evaluate(env_player):
    model = DQN.load("/home/drath/repos/pokemon_tfg/out/new_model_11.zip")
    for i in range(1, 100):
        obs, reward, done, _, info = env_player.step(0)
        while not done:
            action, _ = model.predict(obs, deterministic=False)
            try:
                obs, reward, done, _, info = env_player.step(action)
            except RuntimeError as e:
                print(e)
                env_player.reset()
                break
        env_player.reset()
    print("Won", env_player.n_won_battles, "/ 100 battles against", env_player.get_opponent().username)
    await env_player.close(purge=True)


async def main():
    env_player = RLSimpleAgentsEnv(player=RandomPlayer())
    await evaluate(env_player)
    env_player = RLSimpleAgentsEnv(player=MaxDamagePlayer())
    await evaluate(env_player)
    env_player = RLSimpleAgentsEnv(player=SimpleHeuristicsPlayer())
    await evaluate(env_player)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
