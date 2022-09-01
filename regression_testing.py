import numpy as np
import matplotlib.pyplot as plt


"""
This file implements a regression model that automate testing with different orders
to find the minimum cost following a cost function.
"""


def add_order(X, order):
    """
    Adding columns of different order of xs for matrix multiplication
    :param X:
    :param order:
    :return:
    """
    temp = np.ones(X.shape)
    for i in range(order):
        temp = np.column_stack((X**(i + 1), temp))
    return temp


def fit_wh(X, Y):
    """
    Adopted normal equation
    :param X:
    :param Y:
    :return: list of weights
    """
    return np.linalg.inv(X.T @ X) @ X.T @ Y


# abandoned method
def cubic(a, b, c, d):
    x = np.linspace(300, 50000, 10000).reshape(10000, 1)
    y = a*x**3 + b*x**2 + c*x + d
    return x, y


def cost_function(y_predict, y_actual):
    """
    Mean squared error cost function
    :param y_predict:
    :param y_actual:
    :return:
    """
    sum = 0
    length = len(y_actual)
    for i in range(length):
        diff = y_predict[i] - y_actual[i]
        square = diff**2
        sum += square
    cost = sum / (2 * length)
    return cost


def automate_order(ord_num, xs, ys):
    """
    Automating different orders to find the order
    that has the minimum cost
    :param ord_num:
    :param xs:
    :param ys:
    :return:
    """
    cost = 10000
    index = 0
    temp_x = list()
    temp_w = list()
    for i in range(1, ord_num + 1):
        x_matrix = add_order(xs, i)
        weights = fit_wh(x_matrix, ys)
        y_predict = x_matrix@weights
        newCost = cost_function(y_predict, ys)
        if cost > newCost:
            cost = newCost
            temp_w = weights
            temp_x = x_matrix
            index = i
    return [index, cost, temp_x, temp_w]


if __name__ == '__main__':
    data = np.loadtxt('data-tp.csv', delimiter=',')  # generated from steadyStateResearch.py file
    # data = np.loadtxt('data-vos.csv', delimiter=',')
    print(data.shape)
    length = len(data[:, 0])
    xs = data[:, 0]
    ys = data[:, 1]

    result = automate_order(20, xs, ys)
    print(result)
    y_prediction = result[2]@result[3]

    fig, ax = plt.subplots()
    ax.scatter(xs, ys, c='blue')
    ax.plot(xs, y_prediction, 'g-')
    plt.xlabel('tPeriod')
    plt.ylabel('Number of commutations', color='g')
    title = 'vin = 0, vos = 6, resistance = 5000, tE = 200, tP = 300-75000'
    plt.title('Commutations vs tP {}'.format(title))
    plt.show()
    
