class Atom:
    def __init__(self, x, y, radius, q):
        self.__x = float(x)
        self.__y = float(y)
        self.__r = float(radius)
        self.__q = float(q)

    def __str__(self):
        return '%0.1f, %0.1f, %0.1f, %0.1f' % \
               (self.__x, self.__y, self.__r, self.__q)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def radius(self):
        return self.__r

    @property
    def q(self):
        return self.__q

    @x.setter
    def x(self, value):
        self.__x = value

    @y.setter
    def y(self, value):
        self.__y = value

    def distance_to(self, other_atom):
        x_distnace = self.__x - other_atom.x
        y_distance = self.__y - other_atom.y
        distance = (x_distnace ** 2 + y_distance ** 2) ** 0.5
        return distance
