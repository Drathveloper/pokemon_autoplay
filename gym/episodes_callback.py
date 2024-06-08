from stable_baselines3.common.callbacks import BaseCallback


class StopTrainingOnEpisodesCallback(BaseCallback):
    def __init__(self, n_episodes: int, verbose=0):
        super(StopTrainingOnEpisodesCallback, self).__init__(verbose)
        self.n_episodes = n_episodes
        self.episode_count = 0

    def _on_step(self) -> bool:
        if self.locals.get('dones') is not None and any(self.locals['dones']):
            self.episode_count += 1
            if self.verbose > 0:
                print(f"Episode {self.episode_count}/{self.n_episodes}")
        if self.episode_count >= self.n_episodes:
            print("Training stopped after reaching the target number of episodes.")
            return False
        return True
