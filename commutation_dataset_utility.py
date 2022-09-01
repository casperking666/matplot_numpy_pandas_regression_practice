import numpy as np

"""
Utility functions for accessing the 5D dataset
"""


def readDataset(path):
    """
    :param path: file path
    :return: 5d lists of commutations
    """
    data = np.load(path)
    return data


def findMaxOfAll(data):
    return max(data.flatten())


def findMax_tE(data, tE_index):
    """
    Find the worst-case commutations for a given tE with the rest of
    variables being unknown
    :param data: 5d dataset
    :param tE_index:
    :return: maximum commutations
    """
    data_4d = data[:, :, tE_index, :, :]
    flat = data_4d.flatten()
    return max(flat)


def findMax_tP_end(data, tP_index):
    """
    Find the worst-case commutations for a given tP_end with the rest of
    variables being unknown
    :param data: 5d dataset
    :param tP_index:
    :return: maximum commutations
    """
    data_4d = data[:, :, :, :, tP_index]
    flat = data_4d.flatten()
    return max(flat)


if __name__ == '__main__':
    tP_start = np.logspace(2.477, 5.176, 20)  # 300 - 150000
    tP_end = np.logspace(2.477, 5.176, 20)
    tEs = np.logspace(1, 2.544, 15)  # 10 - 350
    resistance = np.logspace(1.7, 4.699, 18)  # 50 - 50k
    vOpenSrc = np.logspace(-0.699, 1.0792, 15)  # 0.2 - 12

    dataset = readDataset('commutation_dataset.npy')
    test0 = findMax_tE(dataset, 8)
    print(findMaxOfAll(dataset))
    print(test0)
