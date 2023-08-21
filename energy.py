import re
from abc import ABC, abstractmethod

from coordinates import Coordinates


class AbstractEnergy(ABC):

    @abstractmethod
    def energy(self):
        pass


class AbstractMaker(ABC):

    @abstractmethod
    def make(self, coords: Coordinates, *args):
        pass


class HarmonicMaker(AbstractMaker):

    def make(self, coords: Coordinates, *args):
        atom_i = coords[int(args[0])]
        atom_j = coords[int(args[1])]
        d0, k = args[2:]
        return Harmonic(atom_i, atom_j, d0, k)


class RepulsionMaker(AbstractMaker):

    def make(self, coords, *args):
        return Repulsion(coords, args[0])


class CoulombMaker(AbstractMaker):

    def make(self, coords, *args):
        return Coulomb(coords, args[0])


class Harmonic(AbstractEnergy):
    def __init__(self, atom_i, atom_j, d0, k):
        self.__atom_i = atom_i
        self.__atom_j = atom_j
        self.__d0 = float(d0)
        self.__k = float(k)

    def energy(self):
        distance = self.__atom_i.distance_to(self.__atom_j)
        harmonic_energy = self.__k * (self.__d0 - distance) ** 2
        return harmonic_energy


class Repulsion(AbstractEnergy):
    def __init__(self, coords: Coordinates, c):
        self.__coords = coords
        self.__c = float(c)

    def energy(self):
        repulsion_energy = 0
        for i, atom_i in enumerate(self.__coords):
            for j in range(i + 1, self.__coords.n_atoms):
                atom_j = self.__coords[j]
                distance = atom_i.distance_to(atom_j)
                repulsion_energy += self.__c * (atom_i.radius + atom_j.radius - distance) ** 6
        return repulsion_energy


class Coulomb(AbstractEnergy):
    def __init__(self, coords: Coordinates, c):
        self.__coords = coords
        self.__c = float(c)

    def energy(self):
        coulomb_energy = 0
        for i, atom_i in enumerate(self.__coords):
            for j in range(i + 1, self.__coords.n_atoms):
                atom_j = self.__coords[j]
                distance = atom_i.distance_to(atom_j)
                coulomb_energy += self.__c * atom_i.q * atom_j.q / (distance ** 2)
        return coulomb_energy


class TotalEnergy(AbstractEnergy):
    def __init__(self):
        self.__energies = []

    def energy(self):
        energy = 0
        for en in self.__energies:
            energy += en.energy()
        return energy

    def add_component(self, en: AbstractEnergy):
        self.__energies.append(en)


class TotalEnergyFromFile:
    def __init__(self, coords: Coordinates,
                 total_energy: TotalEnergy):
        self.__coords = coords
        self.__energy_dispatch = {}
        self.__total_energy = total_energy

    def from_file(self, fname):
        f = open(fname)
        for line in f.readlines():
            if line.startswith('#') or len(line) < 3:
                continue
            replacement = re.findall(r'#.*', line)
            if len(replacement) > 0:
                tokens = line.replace(*replacement, '').strip().split(' ')
            else:
                tokens = line.strip().split(' ')
            energy = self.__energy_dispatch[tokens[0]].make(self.__coords, *tokens[1:])
            self.__total_energy.add_component(energy)

    def register_energy_type(self, energy_type, maker_type):
        self.__energy_dispatch[energy_type] = maker_type
