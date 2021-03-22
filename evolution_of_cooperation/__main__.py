import matplotlib.pyplot as plt
import numpy as np

import strategies
from iterative_pd import IterativePrisionerDilemma

# Initialize strategies
player1 = strategies.TitForTat()
player5 = strategies.Shubik()
player7 = strategies.Friedman()
player8 = strategies.DavisCuny()
player11 = strategies.Feld()
player12 = strategies.Joss()
player15 = strategies.Random()

players = [player1, player5, player7, player8, player11, player12, player15]
names = ['TitForTat', 'Shubik', 'Friedman', 'DavisCuny', 'Feld',
         'Joss', 'Random']
num_players = len(players)
results = np.nan * np.ones((num_players, num_players))

# Tournament (N iterations)
game = IterativePrisionerDilemma(N=200, payoff_CC=3, payoff_CD=0, payoff_DC=5, payoff_DD=1)
for i in range(num_players):
    for j in range(i, num_players):
        game.run(players[i], players[j])
        results[i, j] = players[i].payoff
        results[j, i] = players[j].payoff
cumulative = results.sum(axis=1) / len(players)

# Plot scores
plt.figure(figsize=(8, 5))
plt.bar(names, cumulative)
plt.ylabel('Avg. Score', fontsize=12)
plt.xticks(fontsize=8, rotation=70)
plt.tight_layout()
plt.show()
