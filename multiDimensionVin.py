import plantDynamics as pD
import matplotlib.pyplot as plt
import parameter_relationship as pr
import numpy as np
import steadyStateResearch as ssr
from dataclasses import dataclass


"""
This script creates 3-dimensional plots with commutations on the z-axis
the other two variable parameters on the x and y axis.
"""


# C like struct
@dataclass
class Variables:
    changeType1: str
    changeType2: str
    changes1: []
    changes2: []
    result1: []
    result2: []
    commutations: []


def plotMultiRelationship(commutations, xAxis, yAxis, typeX, typeY):
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.scatter(xAxis, yAxis, commutations, c='blue')

    ax.set_xlabel(typeX)
    ax.set_ylabel(typeY)
    ax.set_zlabel('Number of commutations', color='r')
    plt.title(f'commutations type={typeX} {typeY}')
    ax.grid(True)

    plt.show()


def threeDSteadyState(variable, vin=0, vos=6, resistance=5000, tE=200, tP=33333):
    """
    This function creates a 3D dataset, the parameters can be dynamically set
    :param variable:
    :param vin:
    :param vos:
    :param resistance:
    :param tE:
    :param tP:
    :return:
    """
    for var1 in variable.changes1:
        for var2 in variable.changes2:
            PD = pD.inputChannel_class(channelNumber=1, voltage=vin, capacitance=10e-6, energiseClocks=tE
                                       , periodClocks=tP, eGearFast=0, dGearFast=0, lastEnergizeEndClock=0,
                                       channelType=pD.HarvesterType_t.THEVENIN, vOpenSource=vos, resistance=resistance,
                                       frequency=0)

            setattr(PD, getattr(variable, 'changeType1'), var1)  # interesting method
            setattr(PD, variable.changeType2, var2)

            result = PD.RunToSteadyState()
            variable.result1.append(var1)
            variable.result2.append(var2)
            commutationsRes.append(len(result[0]) / 2)


# merely a tryout, testing the 4D space
def sthDodgy():
    variable = Variables('vin', 'resistance', vins, resist, vinRes, resistRes, commutationsRes)
    count = 0
    for var0 in vOpenSrc:
        print(f'number of times{count}')
        threeDSteadyState(variable, vos=var0)
        count += 1
    print(max(commutationsRes))


if __name__ == '__main__':
    tPs = [300, 500, 1000, 2000, 4000, 6000, 8000, 10000, 15000, 20000, 33333, 45000, 60000, 80000, 100000, 120000, 150000]
    vOpenSrc = np.arange(1, 12.5, 0.5)
    vins = [i / 2 for i in range(0, 17)]
    resist = [400, 600, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 20000, 30000, 50000]
    resistRes = []
    vinRes = []
    commutationsRes = []
    vosRes = []

    # sthDodgy()
    variable = Variables('voltage', 'resistance', vins,  resist,  vinRes, resistRes, commutationsRes)
    threeDSteadyState(variable)
    plotMultiRelationship(commutationsRes, variable.result1, variable.result2, "vin", "resistance")
    print(max(commutationsRes))

    commutationsRes = []
    vinRes = []
    variable2 = Variables('voltage', 'vOpenSource', vins,  vOpenSrc,  vinRes, vosRes, commutationsRes)
    threeDSteadyState(variable2)
    print(max(commutationsRes))
    plotMultiRelationship(commutationsRes, variable2.result1, variable2.result2, "vin", "vos")


