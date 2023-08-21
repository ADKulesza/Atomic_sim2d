from abc import ABC
from energy import TotalEnergy


class AbstractObserver(ABC):
    def observe(self):
        pass


class EnergyObserver(AbstractObserver):
    def __init__(self, total_energy: TotalEnergy):
        self._total_en = total_energy

    def observe(self):
        energy = self._total_en.energy()
        print(energy)
