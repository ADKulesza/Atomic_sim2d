from coordinates import Coordinates
from energy import TotalEnergyFromFile, TotalEnergy, HarmonicMaker, CoulombMaker, RepulsionMaker
from monte_carlo import MonteCarlo
from observer import EnergyObserver

if __name__ == '__main__':
    crds = Coordinates('sim2d-system.txt')
    total_energy = TotalEnergy()
    factory = TotalEnergyFromFile(crds, total_energy)
    factory.register_energy_type("HARMONIC", HarmonicMaker())
    # factory.register_energy_type("ATTACHED_HARMONIC", AttachedHarmonicMaker())
    factory.register_energy_type("COULOMB", CoulombMaker())
    factory.register_energy_type("REPULSION", RepulsionMaker())

    en = factory.from_file("sim2d-energy.txt")
    simulation = MonteCarlo(crds, total_energy, 3.0)
    energy_observer = EnergyObserver(total_energy)
    simulation.add_observer(energy_observer)
    simulation.sample(100)
