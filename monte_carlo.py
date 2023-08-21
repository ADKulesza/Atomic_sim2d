import numpy as np
import random

from coordinates import Coordinates
from observer import AbstractObserver


class MonteCarlo:
    def __init__(self, coords: Coordinates, total_en, T: float):
        self.__T = T
        self.__coords = coords
        self.__max_step = 0.1
        self.__en = total_en
        self.__obs = []

    def add_observer(self, obs: AbstractObserver):
        self.__obs.append(obs)

    def sample(self, n_steps):
        for i in range(n_steps):
            for j in range(self.__coords.n_atoms):
                dx = random.uniform(-self.__max_step, self.__max_step)
                dy = random.uniform(-self.__max_step, self.__max_step)
                old_x, old_y = self.__coords[j].x, self.__coords[j].y
                old_en = self.__en.energy()
                self.__coords[j].x = self.__coords[j].x + dx
                self.__coords[j].y = self.__coords[j].y + dy
                new_en = self.__en.energy()
                delta_e = new_en - old_en
                if delta_e > 0 and random.random() > np.exp(-delta_e / self.__T):
                    self.__coords[j].x = old_x
                    self.__coords[j].y = old_y

            for o in self.__obs:
                o.observe()
