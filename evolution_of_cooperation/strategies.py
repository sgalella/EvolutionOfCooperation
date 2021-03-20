from abc import ABC, abstractmethod

import numpy as np


class Strategy(ABC):
    def __init__(self):
        self.payoff = None

    @abstractmethod
    def get_action(self):
        pass


class TitForTat(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, history):
        if history.size != 0:
            if history[-1] == 1:
                return 1
            return 0
        else:
            return 0


class AlwaysDefect(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, history):
        return 1


class AlwaysCooperate(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, history):
        return 0


class Random(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, history):
        if np.random.random() > 0.5:
            return 0
        return 1


class Friedman(Strategy):
    def __init__(self):
        super().__init__()
        self.cooperate = True

    def get_action(self, history):
        if self.cooperate:
            if 1 not in history:
                return 0
            self.cooperate = False
        return 1


class DavisCuny(Strategy):  # Check
    def __init__(self):
        super().__init__()
        self.counter = 10
        self.cooperate = True

    def get_action(self, history):
        if self.counter > 0:
            self.counter -= 1
            if self.counter == 0 and 1 in history:
                self.cooperate = False
                return 1
            return 0
        if not self.cooperate:
            return 1
        return 0


class Shubik(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, history):
        if history.size == 0:
            return 0
        if history[-1] == 0:
            return 0
        else:
            return 1


class Joss(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, history):
        if history.size == 0:
            return 0
        if history[-1] == 0:
            return 0 if np.random.random() > 0.1 else 1
        return 1


class Feld(Strategy):
    def __init__(self):
        super().__init__()
        self.p_coop = 1

    def get_action(self, history):
        if history.size == 0:
            return 0
        self.p_coop -= self.p_coop / 200
        if history[-1] == 1:
            return 1
        return 0 if np.random.random() > (1 - self.p_coop) else 1
