import plantDynamics as PD
import matplotlib.pyplot as plt
import numpy as np


"""
This file could generate a 5 dimensional commutation dataset
where given tE, tP_start, tP_end, resistance and vOS,
the number of commutations those set of parameters will take
can be retrieved from the dataset.
"""


def generate_5d_dataset(tP_start, tP_end, tE, resistance, vOpenSrc):
    """
    Iterating through all 5 parameter's list, record the number of commutations
    this particular set of parameters will take
    :param tP_start:
    :param tP_end:
    :param tE:
    :param resistance:
    :param vOpenSrc:
    :return: 5D numpy array
    """
    commutations_dataset = np.zeros([len(resistance), len(vOpenSrc), len(tE), len(tP_start), len(tP_end)])
    InputChan = PD.inputChannel_class(channelNumber=1, voltage=0, capacitance=10e-6,
                                      energiseClocks=0,
                                      periodClocks=0, eGearFast=0, dGearFast=0,
                                      lastEnergizeEndClock=0,
                                      channelType=PD.HarvesterType_t.THEVENIN, vOpenSource=0,
                                      resistance=0, frequency=0)
    count = 0
    for res in range(len(resistance)):
        for vos in range(len(vOpenSrc)):
            print(f'this is count {count}')
            count += 1
            for te in range(len(tE)):
                for tps in range(len(tP_start)):
                    if te >= tps:
                        continue
                    InputChan.voltage = 0
                    InputChan.energiseClocks = tE[te]
                    InputChan.periodClocks = tP_start[tps]
                    InputChan.vOpenSource = vOpenSrc[vos]
                    InputChan.resistance = resistance[res]
                    InputChan.lastEnergizeEndClock = 0

                    result = InputChan.RunToSteadyState()
                    newVin = result[1][len(result[1]) - 1]
                    for tpe in range(len(tP_end)):
                        InputChan.voltage = newVin
                        InputChan.energiseClocks = tE[te]
                        InputChan.periodClocks = tP_end[tpe]
                        InputChan.vOpenSource = vOpenSrc[vos]
                        InputChan.resistance = resistance[res]
                        InputChan.lastEnergizeEndClock = 0

                        result = InputChan.RunToSteadyState()
                        num_of_comms = len(result[1]) / 2
                        commutations_dataset[res, vos, te, tps, tpe] = num_of_comms
    return commutations_dataset


if __name__ == '__main__':
    # testing set
    # tp_s = [500, 2000, 10000, 40000, 80000]
    # tp_e = [500, 2000, 10000, 40000, 80000]
    # te_test = [10, 50, 150, 300]
    # resist = [200, 2000, 20000]
    # vos = [1, 4, 10]

    tP_start = np.logspace(2.477, 5.176, 20)  # 300 - 150000
    tP_end = np.logspace(2.477, 5.176, 20)
    tE = np.logspace(1, 2.544, 15)  # 10 - 350
    resistance = np.logspace(1.7, 4.699, 18)  # 50 - 50k
    vOpenSrc = np.logspace(-0.699, 1.0792, 15)  # 0.2 - 12

    results = generate_5d_dataset(tP_start, tP_end, tE, resistance, vOpenSrc)
    np.save('commutation_dataset', results)
    
