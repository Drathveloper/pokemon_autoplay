import copy
import os

from stable_baselines3.dqn import MlpPolicy

from gym_env.custom_dqn import CustomDQN
from gym_env.replay_environment import ReplayEnv
from gym_env.episodes_callback import StopTrainingOnEpisodesCallback
from gym_env.reward import RewardValues
from gym_env.simple_agents_environment import RLSimpleAgentsEnv
from replays.replay_processor import ReplayProcessor


def main():
    replay_agent_episodes = int(os.environ['NUM_REPLAY_EPISODES'])
    replay_agent_steps = replay_agent_episodes * 50
    simple_agent_episodes = int(os.environ['NUM_SIMPLE_AGENTS_EPISODES'])
    simple_agent_steps = simple_agent_episodes * 50
    processed_dir = os.environ['REPLAYS_PATH']
    out_dir = os.environ['MODEL_PATH']
    reward_values = RewardValues(
        fainted_value=float(os.environ['REWARD_FAINTED_VALUE']),
        hp_value=float(os.environ['REWARD_HP_VALUE']),
        status_value=float(os.environ['REWARD_STATUS_VALUE']),
        invalid_action_value=float(os.environ['REWARD_INVALID_ACTION_VALUE']),
        victory_value=float(os.environ['REWARD_VICTORY_VALUE']))
    replay_file_names = [f for f in os.listdir(processed_dir) if os.path.isfile(os.path.join(processed_dir, f))]
    replays = []
    print("loading replays...")
    for file_name in replay_file_names:
        processor = ReplayProcessor()
        processor.load_replay(processed_dir + '/' + file_name)
        processor.process_replay()
        replays.append(copy.deepcopy(processor.to_data()))
    print("replays loaded, start learning phase")
    replay_env = ReplayEnv(replays=replays, reward_values=reward_values)
    model = CustomDQN(MlpPolicy, replay_env, verbose=1)
    model.learn(
        total_timesteps=replay_agent_steps,
        callback=StopTrainingOnEpisodesCallback(
            n_episodes=replay_agent_episodes,
            verbose=1))
    simple_agent_env = RLSimpleAgentsEnv(reward_values=reward_values)
    model.set_env(simple_agent_env)
    model.learn(
        total_timesteps=simple_agent_steps,
        callback=StopTrainingOnEpisodesCallback(
            n_episodes=simple_agent_episodes,
            verbose=1))
    simple_agent_env.close(purge=True)
    print("learning phase ended, saving trained model")
    model.save(path=out_dir + '/model.zip')


if __name__ == "__main__":
    main()
