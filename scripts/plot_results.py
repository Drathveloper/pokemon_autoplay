import pandas as pd
from matplotlib import pyplot as plt


def plot_rewards_bar(title, data, axis):
    axis.bar(data['model'], data['avg_reward'], label='Avg Reward', alpha=0.7)
    axis.bar(data['model'], data['avg_discounted_reward'], label='Avg Discounted Reward', alpha=0.7)
    axis.set_title(title)
    axis.set_ylabel('Reward')
    axis.legend()
    axis.grid(True)


def plot_success_bar(title, data, axis):
    axis.bar(data['model'], data['success_rate'], label='Success Rate', alpha=0.7, color='g')
    axis.set_title(title)
    axis.set_ylabel('Win Ratio')
    axis.legend()
    axis.grid(True)


def plot_variance_bar(title, data, axis):
    axis.bar(data['model'], data['variance_reward'], label='Variance Reward', alpha=0.7, color='r')
    axis.set_title(title)
    axis.set_ylabel('Variance')
    axis.legend()
    axis.grid(True)


def main():
    log_path = "../out/logs"
    with open(f"{log_path}/execution.log", mode='r', encoding='utf-8') as logfile:
        df = pd.read_csv(logfile, sep="|")
    random_player = df[df['player'] == 'RandomPlayer']
    max_damage_player = df[df['player'] == 'MaxDamagePlayer']
    simple_heuristics = df[df['player'].str.contains('SimpleHeuristic')]
    fig, axs = plt.subplots(3, 1, figsize=(14, 18), sharex=True)
    plot_rewards_bar("RandomPlayer", random_player, axs[0])
    plot_rewards_bar("MaxDamagePlayer", max_damage_player, axs[1])
    plot_rewards_bar("SimpleHeuristics", simple_heuristics, axs[2])
    plt.xlabel('Rewards')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    fig2, axs2 = plt.subplots(3, 1, figsize=(14, 18), sharex=True)
    plot_success_bar("RandomPlayer", random_player, axs2[0])
    plot_success_bar("MaxDamagePlayer", max_damage_player, axs2[1])
    plot_success_bar("SimpleHeuristics", simple_heuristics, axs2[2])
    plt.xlabel('Model Success')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    fig3, axs3 = plt.subplots(3, 1, figsize=(14, 18), sharex=True)
    plot_variance_bar("RandomPlayer", random_player, axs3[0])
    plot_variance_bar("MaxDamagePlayer", max_damage_player, axs3[1])
    plot_variance_bar("SimpleHeuristics", simple_heuristics, axs3[2])
    plt.xlabel('Rewards Variance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
