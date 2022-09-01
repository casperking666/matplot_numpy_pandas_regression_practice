import plantDynamics as pD
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl


"""
An automation tool to extract data from Excel sheets and generate plots
to show the relationship between commutations and a particular parameter
"""


def plotRelationship(commutations, values, type):
    plt.scatter(values, commutations, c='green')

    plt.xlabel(type)
    plt.ylabel('Number of commutations', color='g')
    plt.title('commutations type={}'.format(type))

    plt.show()


def parseString(name, type):
    """
    find the particular value from the sheet name
    e.g. vIn3 -> 3
    :param name:
    :param type:
    :return:
    """
    length = len(type)
    index = name.find(type)
    value = name[index + length:]
    for s in value.split():
        return float(s)


def readExcel(path, type):
    """
    read in each Excel sheet, extract the information we want
    and store it in a list
    :param path:
    :param type:
    :return:
    """
    values = []
    commutations = []
    df = pd.read_excel(path, sheet_name=None, index_col=0)
    for name in df.keys():
        values.append(parseString(name, type))
        commutations.append(len(df[name].index))
    return commutations, values


def plotMultiExcel(paths, types):
    for i in range(len(paths)):
        commutations, values = readExcel(paths[i], types[i])
        print(commutations)
        print(values)
        plotRelationship(commutations, values, types[i])


if __name__ == '__main__':
    paths = ['changeVinCounter10.xlsx', 'changeVosCounter10.xlsx']
    types = ['vIn', 'vIn']  # these strings must match the strings in the Excel sheet
    plotMultiExcel(paths, types)
