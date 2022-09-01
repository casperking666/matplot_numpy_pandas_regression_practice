import csv
import plantDynamics as pD
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
import parameter_relationship as pr
import numpy as np

"""
This script is mainly designed as an automation tool to automate the process of 
writing data to excel and csv file, as well as plotting different runToSteadyState graphs.
"""


def newExcel(path):
    df_empty = pd.DataFrame()
    df_empty.to_excel(path)


def plotSteadyState(inputTime, inputVoltage, inputCurrent, value, save):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(inputTime, inputVoltage, 'g-')
    ax2.plot(inputTime, inputCurrent, color='b')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage', color='g')
    ax2.set_ylabel('Inductor Current', color='b')
    plt.title('commutations voltage={} vOS={} res={} tEn={} tP={}'.format(0, value, 5000, 200, 33333))

    if save:
        plt.savefig('tE{} tP{} vOS{} vIn{}.png'.format(200, 33333, value, 0))
    else:
        plt.show()


def writeToExcel(inputTime, inputVoltage, inputCurrent, value, path):
    df = pd.DataFrame({'time': inputTime, 'voltage': inputVoltage, 'current': inputCurrent})

    # append mode
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
        writer.book = openpyxl.load_workbook(path)
        df.to_excel(writer, sheet_name='tE200, tP{} vOS{} vIn{}'.format(33333, value, 0))


def multiSteadyState(changes, changeType, path, vin=0, vos=6, resistance=5000, tE=200, tP=33333, save=False):
    """
    Generating a set of Excel sheets and plots with one plot being one value of the changeType
    e.g. vin = 2, of that runToSteadyState plot
    :param changes: a list of values, could be vin, vos etc.
    :param changeType: the type of the changes
    :param path: path of the Excel sheet
    :param save: boolean that tells if the plots need to be saved
    :return: x_axis, y_axis list
    """
    commutations = list()
    values = []

    for value in changes:
        if changeType == 'vin':
            vin = value
        elif changeType == 'vos':
            vos = value
        elif changeType == 'resistance':
            resistance = value
        elif changeType == 'tP':
            tP = value

        PD = pD.inputChannel_class(channelNumber=1, voltage=vin, capacitance=10e-6, energiseClocks=tE
                                   , periodClocks=tP, eGearFast=0, dGearFast=0, lastEnergizeEndClock=0,
                                   channelType=pD.HarvesterType_t.THEVENIN, vOpenSource=vos, resistance=resistance, frequency=0)

        # drawing graphs
        result = PD.RunToSteadyState()
        inputTime = result[0]
        inputVoltage = result[1]
        inputCurrent = result[2]

        plotSteadyState(inputTime, inputVoltage, inputCurrent, value, save)
        # writeToExcel(inputTime, inputVoltage, inputCurrent, value, path)

        commutations.append(len(inputCurrent) / 2)
        values.append(value)

    return values, commutations


def write_csv(type, variable, commutations):
    np.savetxt(f'data-{type}.csv', [p for p in zip(variable, commutations)], delimiter=',')


if __name__ == '__main__':
    tPs = np.arange(300, 75000, 100)
    vOpenSrc = np.arange(0.2, 12, 0.1)
    # vIn = [i / 2 for i in range(0, 25)] step of 0.5 using this way
    vIn = np.arange(0, 12, 0.1)
    resist = np.arange(50, 50000, 50)

    path = 'changeVosCounter10.xlsx'
    path2 = 'changeVinCounter10.xlsx'
    path3 = 'changeRinCounter10.xlsx'

    # newExcel(path3)

    # changing vos
    changeType = 'tP'
    values, commutations = multiSteadyState(tPs, changeType, path)
    np.savetxt('data-tp.csv', [p for p in zip(values, commutations)], delimiter=',')
    # pr.plotRelationship(commutations, values, 'tP')

    # changing resistance
    # changeType = 'resistance'
    # values, commutations = multiSteadyState(resist, changeType, path)
    # write_csv(changeType, values, commutations)
    #
    # changeType = 'vos'
    # values, commutations = multiSteadyState(vOpenSrc, changeType, path)
    # write_csv(changeType, values, commutations)
    #
    # changeType = 'vin'
    # values, commutations = multiSteadyState(vIn, changeType, path)
    # write_csv(changeType, values, commutations)
