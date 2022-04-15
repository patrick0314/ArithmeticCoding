from operator import inv
from matplotlib import pyplot as plt
from matplotlib.ft2font import LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH
import numpy as np
import random
import cv2
import matplotlib

def arithmetic(test, set, probability):
    # Fool-Proof Mechanism
    if len(set) != len(probability) or sum(probability) != 100:
        print('=== ERROR !!!!! ===')
        return

    # Preprocess - Inteval of Probability 
    inteval, inte = np.zeros(1), 0
    for i in range(len(probability)-1):
        inte += probability[i] / 100
        inteval = np.append(inteval, inte)

    # Arithmetic Encoding
    # Initial Condition
    idx = set.index(test[0])
    lower = inteval[idx]
    upper = inteval[idx] + probability[idx] / 100
    # Recursion
    lowers, uppers = [lower], [upper]
    for i in range(1, len(test)):
        idx = set.index(test[i])
        prev = lower
        lower = prev + inteval[idx] * (upper - prev)
        upper = prev + (inteval[idx] + probability[idx] / 100) * (upper - prev)

        lowers.append(lower)
        uppers.append(upper)
    
    # Plot Encoding Procedure
    '''
    figure = plt.figure(figsize=(10, 2*len(test)))
    for i, (l, u) in enumerate(zip(lowers, uppers)):
        print(l, u)
        figure.add_subplot(len(test), 1, i+1)
        x = np.arange(l, u, 0.0000001)
        y = np.ones(x.shape)
        plt.plot(x, y, color='Red', lw=30)
        plt.xlim(0, 1), plt.ylim(0.9, 1.1)
        ax = plt.gca()
        ax.get_yaxis().set_visible(False)
    plt.show()
    '''

    # Find C and b s.t. lower < C * k^-b < (C+1) * k^-b < upper where k = 2 in general
    b = 2
    while_break = False
    while True:
        if pow(2, -b) > (upper - lower):
            b += 1
        else:
            for C in range(pow(2, b)):
                if lower < C * pow(2, -b) and (C+1) * pow(2, -b) < upper:
                    while_break = True
                    break
            if while_break:
                break
            b += 1

    return str(bin(C)[2:]).zfill(b)

def inv_arithmetic(en, set, probability):
    # Find C and b in arithmetic encoding
    b, C = len(en), int(en, 2)

    # According 

    return

if __name__ == '__main__':
    s = ['a', 'b']
    p = [80, 20]

    t = random.choices(s, weights=tuple(p), k=5)
    t = ['a', 'a', 'a', 'b', 'a', 'a']

    en = arithmetic(t, s, p)
    de = inv_arithmetic(en, s, p)
