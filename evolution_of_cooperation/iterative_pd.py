import numpy as np


class IterativePrisionerDilemma:
    def __init__(self, N, payoff_CC, payoff_CD, payoff_DC, payoff_DD):
        self.N = N
        self.payoff_CC = payoff_CC
        self.payoff_CD = payoff_CD
        self.payoff_DC = payoff_DC
        self.payoff_DD = payoff_DD

    def _get_outcome(self, move_A, move_B):
        if move_A == 0 and move_B == 0:
            return 0
        elif move_A == 0 and move_B == 1:
            return 1
        elif move_A == 1 and move_B == 0:
            return 2
        elif move_A == 1 and move_B == 1:
            return 3

    def _compute_payoff(self, outcomes):
        payoff_player_A = (self.payoff_CC * np.sum(outcomes == 0)
                           + self.payoff_CD * np.sum(outcomes == 1)
                           + self.payoff_DC * np.sum(outcomes == 2)
                           + self.payoff_DD * np.sum(outcomes == 3))

        payoff_player_B = (self.payoff_CC * np.sum(outcomes == 0)
                           + self.payoff_CD * np.sum(outcomes == 2)
                           + self.payoff_DC * np.sum(outcomes == 1)
                           + self.payoff_DD * np.sum(outcomes == 3))

        return [payoff_player_A, payoff_player_B]

    def run(self, player_A, player_B):
        history = np.nan * np.ones((self.N, 2))
        outcomes = np.nan * np.ones((self.N, ))
        payoff = np.nan * np.ones((self.N, 2))

        for turn in range(self.N):
            move_A = player_A.get_action(turn, history, payoff)
            move_B = player_B.get_action(turn,
                                         np.flip(history, axis=1),
                                         np.flip(payoff, axis=1))
            outcome = self._get_outcome(move_A, move_B)
            history[turn, 0] = move_A
            history[turn, 1] = move_B

            outcomes[turn] = outcome
            payoff[turn] = self._compute_payoff(outcomes[:turn])

        return history, outcomes, payoff
