__author__ = 'indiquant'


from datetime import datetime
import numpy as np


class Option(object):

    def __init__(self, undl, cp, mat, strike, bidpx, askpx, lastpx, volume):
        self._undl = undl
        self._cp = cp
        self._mat = mat
        self._strike = strike
        self._bidpx = bidpx
        self._askpx = askpx
        self._lastpx = lastpx
        self._volume = volume

    @property
    def bidpx(self):
        return self._bidpx

    @property
    def askpx(self):
        return self._askpx

    @property
    def midpx(self):
        if (self._bidpx is not None) and (self._askpx is not None):
            return (self._bidpx + self._askpx) / 2.0

        elif self._bidpx is not None:
            return self._bidpx

        elif self._askpx is not None:
            return self._askpx

        else:
            return None

    @property
    def volume(self):
        return self._volume


class PutCallSurface(object):
    def __init__(self, undl):
        self._undl = undl
        self._surface = {'C': {}, 'P': {}}
        self._mats = np.array([])
        self._strikes = {}
        self._issorted = True

    def add(self, cp, mat, k, bidpx, askpx, lastpx, volume):
        mat = self._datefint(mat)

        self._issorted = False
        self._mats = np.append(self._mats, mat)
        if mat not in self._strikes:
            self._strikes[mat] = np.array([k])

        else:
            self._strikes[mat] = np.append(self._strikes[mat], k)

        op = Option(self._undl, cp, mat, k, bidpx, askpx, lastpx, volume)

        if mat in self._surface[cp]:
            self._surface[cp][mat][k] = op

        else:
            self._surface[cp][mat] = {k: op}

    def get_grid(self, cp='C'):
        self._sort()
        strikes = np.array([])
        for m, _strikes in self._strikes.items():
            strikes = np.append(strikes, _strikes)
        strikes = np.sort(np.unique(strikes))
        px_array, sz_array = [], []
        for m in self._mats:
            px_row, sz_row = [], []
            for k in strikes:
                try:
                    op = self._surface[cp][m][k]
                    px_row.append(op.midpx)
                    sz_row.append(op.volume)

                except KeyError:
                    px_row.append(np.nan)
                    sz_row.append(np.nan)
            px_array.append(px_row)
            sz_array.append(sz_row)

        return np.array(px_array), np.array(sz_array)

    def _datefint(self, dt):
        """
        :type dt: int
        """
        return datetime.strptime(str(dt), '%Y%m%d').date()

    def _sort(self):
        if not self._issorted:
            self._mats = np.sort(np.unique(self._mats))
            for m in self._strikes:
                self._strikes[m] = np.sort(np.unique(self._strikes[m]))
            self._issorted = True


