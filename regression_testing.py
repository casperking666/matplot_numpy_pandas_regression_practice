import numpy as np
import matplotlib.pyplot as plt


# basically, there are two ideas I have atm to implement regression
# one is by just manually try with different orders of functions
# I might be able to do chebyshev with automation tho, but I wanna do the
# simpler one first just to familiarize myself with numpy again
# the second approach is to use gradient descent, it should be quite fun.
# one other thing to note is that there are also 3d regression in Lawrence's lecture
# could try that in the future.
# I mean, still, it's a tough job, but I might actually be able to find sth out.
def add_order(X, order):
    temp = np.ones(X.shape)
    for i in range(order):
        temp = np.column_stack((X**(i + 1), temp))
    return temp


def fit_wh(X, Y):
    return np.linalg.inv(X.T @ X) @ X.T @ Y


# abandoned method
def cubic(a, b, c, d):
    x = np.linspace(300, 50000, 10000).reshape(10000, 1)
    y = a*x**3 + b*x**2 + c*x + d
    return x, y


def cost_function(y_predict, y_actual):
    sum = 0
    length = len(y_actual)
    for i in range(length):
        diff = y_predict[i] - y_actual[i]
        square = diff**2
        sum += square
    cost = sum / (2 * length)
    return cost


def automate_order(ord_num, xs, ys):
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
    # xs, ys = quadratic(2, 3, 5)
    # result = least_squares(xs, ys)
    data = np.loadtxt('data-tp.csv', delimiter=',')
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
    # ax.set_xlim([-2, 20])
    plt.show()

# seems like tE affects a lot on number of commutations
# could kinda try a brute force approach

# let me try one thing first, this would be kinda fun
# so let's calculate the cost function for different orders first


# 写得很爽 这几个方法我算是彻底玩儿明白了 下一个要干的活儿有点儿无聊
# 感觉像是重复性工作 我暂时兴趣不大 想看下吴恩达下部分的内容 但是又有点儿累
# 想去跟她得波几句去 但又没啥好说的 好想等着领钱啊 最好工资多点儿 虽说我确实不太配
# 但是又还算配 毕竟我现在搞得可是高级货 这玩意儿可算有难度的 我可不只是调包侠
