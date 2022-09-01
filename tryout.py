import enum
import numpy as np
import parameter_relationship as pr
import matplotlib.pyplot as plt

class Arguments(enum.Enum):
    vin = 1
    vos = 2
    r = 3
    tP = 4
    tE = 5


def shabi():
    return [x for x in range(length) if x % 2 == 1]


def cheb(xs, c):
    coefs = c*[0] + [1]
    return np.polynomial.chebyshev.chebval(xs, coefs)


if __name__ == '__main__':
    # length = 'shabi'
    # myVars = vars()
    # myVars['length'] = 'wanghaozeshidmztadie'
    # print(length)
    # xs = np.linspace(-1, 1, 100)
    # pr.plotRelationship(cheb(xs, 3), xs, 'goba')
    # print(sum([x for x in range(5)]))
    # a = np.arange(4)
    # b = np.array([5, 4, 3, 2]).reshape(4, 1)
    # print(np.dot(a, b))
    # print(a @ b)  # all of those three methods do matrix multiplication the same way
    # print(a.dot(b))  # but can also use for dot product for vectors, weird
    # print(a * b)

    test = np.array([[[[[0]]]]])
    test[0,0,0,0,0] = 1
    print(test)

    # i fucking hate numpy arrays, they are so bad and counterintuitive
    # a = np.empty((0, 3, 3), int)  # honestly no idea what to do here with 3D
    # print(a)
    # a = np.append(a, [[[1, 1, 1]]], axis=0)
    # print(a)

    a = [[2,2],[2,2]]
    b = np.array(a)
    print(b[1,1])
    # a[0,0] = 2
    print(a[1][1])


