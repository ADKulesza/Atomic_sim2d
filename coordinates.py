from atom import Atom


class Coordinates:
    def __init__(self, atom_prop_fname):
        self.__atoms_data = {}
        self.__load_atoms(atom_prop_fname)
        self.__n_atoms = len(self.__atoms_data)

    def __load_atoms(self, fname):
        f = open(fname, 'r')
        for atom_prop in f.readlines():
            if atom_prop[0] == '#':
                continue

            properties = []
            for i, prp in enumerate(atom_prop.split(' ')):
                if i == 0:
                    key = prp
                else:
                    if len(prp) > 0:
                        prp = prp.replace('\n', '')
                        properties.append(prp)

            atom = Atom(*properties)
            self.__atoms_data[int(key)] = atom

    def __getitem__(self, i):
        return self.__atoms_data[i]

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < self.__n_atoms:
            self.__i += 1
            return self.__atoms_data[self.__i - 1]
        else:
            raise StopIteration

    def __len__(self):
        return len(self.__atoms_data)

    @property
    def n_atoms(self):
        return self.__n_atoms
