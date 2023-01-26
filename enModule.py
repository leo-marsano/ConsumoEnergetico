import sys
import numpy as np


# CLASS MADE FOR ENERGY CONSUMPTION ANALYSIS USED IN 'enFunctions.py', 'enProject.py' and 'enSunPanel.py'
class Sample():
    """
    Classe per rappresentare i campionamenti del consumo energetico.
    
    Paramtri:
    - tempo (min)
    - casa (kW)
    - fotovoltaico (kW)
    - powerwall (kW)
    - rete (kW)
    -------------------------------------------
    Metodi:
    - __str__ per print
    """
    def __init__(self, time, home, panels, powerwall, net):
        self.time      = ((60*int(time[11:13])) + int(time[14:16]))
        self.home      = home
        self.panels   = panels
        self.powerwall = powerwall
        self.net       = net

    def __str__(self):
        return ("{0}, {1}, {2}, {3}, {4}".format(self.time, self.home,
                                        self.panels, self.powerwall, self.net))

class Month():
    """
    Classe per rappresentare i giorni di campionamento del consumo energetico.
    
    Paramtri:
    - numero campionamenti
    - array campionamenti
    -------------------------------------------
    Metodi:
    - addSamp(tempo, casa, solare, powerwall, rete)
    """
    def __init__(self):
        self.nSamp = 0
        self.aSamp = np.empty(0)

    def addSamp(self, s):
        self.aSamp = np.append(self.aSamp, s)
        self.nSamp = len(self.aSamp)
