import numpy as np


class IterativePrisionerDilemma:
    def __init__(self, N, payoff_CC, payoff_CD, payoff_DC, payoff_DD):
        self.N = N
        self.payoff_CC = payoff_CC
        self.payoff_CD = payoff_CD
        self.payoff_DC = payoff_DC
        self.payoff_DD = payoff_DD
        self.history = np.nan * np.ones((self.N, 3))

    def _get_outcome(self, move_A, move_B):
        if move_A == 0 and move_B == 0:
            return 0
        elif move_A == 0 and move_B == 1:
            return 1
        elif move_A == 1 and move_B == 0:
            return 2
        elif move_A == 1 and move_B == 1:
            return 3

    def _compute_payoff(self, player_A, player_B):
        player_A.payoff = (self.payoff_CC * np.sum(self.history[:, 2] == 0)
                           + self.payoff_CD * np.sum(self.history[:, 2] == 1)
                           + self.payoff_DC * np.sum(self.history[:, 2] == 2)
                           + self.payoff_DD * np.sum(self.history[:, 2] == 3))

        player_B.payoff = (self.payoff_CC * np.sum(self.history[:, 2] == 0)
                           + self.payoff_CD * np.sum(self.history[:, 2] == 2)
                           + self.payoff_DC * np.sum(self.history[:, 2] == 1)
                           + self.payoff_DD * np.sum(self.history[:, 2] == 3))

    def run(self, player_A, player_B):
        for turn in range(self.N):
            move_A = player_A.get_action(self.history[:turn, 1])
            move_B = player_B.get_action(self.history[:turn, 0])
            outcome = self._get_outcome(move_A, move_B)
            self.history[turn, 0] = move_A
            self.history[turn, 1] = move_B
            self.history[turn, 2] = outcome

        self._compute_payoff(player_A, player_B)
