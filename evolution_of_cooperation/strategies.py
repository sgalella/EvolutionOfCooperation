from abc import ABC, abstractmethod

import numpy as np


class Strategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, turn, history, payoff):
        pass


class TitForTat(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        if turn != 0:
            if history[turn-1, 1] == 1:
                return 1
            return 0
        else:
            return 0


class AlwaysDefect(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        return 1


class AlwaysCooperate(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        return 0


class Random(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        return int(np.random.random() > 0.5)


class Friedman(Strategy):
    def __init__(self):
        super().__init__()
        self.cooperate = True

    def get_action(self, turn, history, payoff):
        if self.cooperate:
            if 1 not in history[:, 1]:
                return 0
            self.cooperate = False
        return 1


class DavisCuny(Strategy):  # Check
    def __init__(self):
        super().__init__()
        self.counter = 10
        self.cooperate = True

    def get_action(self, turn, history, payoff):
        if self.counter > 0:
            self.counter -= 1
            if self.counter == 0 and 1 in history[:, 1]:
                self.cooperate = False
                return 1
            return 0
        if not self.cooperate:
            return 1
        return 0


class Shubik(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        if turn == 0:
            return 0
        if history[turn-1, 1] == 0:
            return 0
        else:
            return 1


class Joss(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        if turn == 0:
            return 0
        if history[turn-1, 1] == 0:
            return int(np.random.random() < 0.1)
        return 1


class Feld(Strategy):
    def __init__(self):
        super().__init__()
        self.p_coop = 1

    def get_action(self, turn, history, payoff):
        if turn == 0:
            return 0
        self.p_coop -= self.p_coop / 200
        if history[turn-1, 1] == 1:
            return 1
        return int(np.random.random() > self.p_coop)


class Tullock(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, turn, history, payoff):
        if turn < 10:
            return 0
        else:
            p_coop_op = (1 - history[turn-10:turn, 1]).sum() / 10
            if np.random.random() > p_coop_op * 0.9:
                return 1
            else:
                return 0


class TidemanChieruzzi(Strategy):
    def __init__(self):
        super().__init__()
        self.defections = 0
        self.fresh_start = False
        self.fresh_start_counter = 2
        self.last_fresh_start = 0

    def _check_fresh_start(self, turn, history, payoff):
        is_payoff = payoff[turn, 0] - payoff[turn, 1] > 10
        is_last_fresh_start = self.last_fresh_start == 20
        is_ten_moves = len(history) - turn <= 10

        if is_payoff or is_last_fresh_start or is_ten_moves:
            self.fresh_start = True
            self.fresh_start_counter = 2
            self.last_fresh_start = 0

    def get_action(self, turn, history, payoff):
        if turn == 0:
            return 0
        if turn >= len(history) - 2:
            return 1

        self._check_fresh_start(turn, history, payoff)

        if self.fresh_start:
            self.fresh_start_counter -= 1
            if self.fresh_start_counter == 0:
                self.fresh_start = False
            return 0

        self.fresh_start += 1

        if history[turn-1, 1] == 1:
            self.defections += 1
            return 1
        if self.defections >= 2:
            self.defections -= 1
            return 1
        else:
            return 0
