import time
import random
import numpy as np
from matplotlib import pyplot as plt

def arithmetic(text, data_length, set, probability):
    # Fool-Proof Mechanism
    if len(set) != len(probability) or sum(probability) != 1:
        print('=== ERROR !!!!! ===')
        return

    # Preprocess - Inteval of Probability 
    inteval, inte = np.zeros(1), 0
    for i in range(len(probability)):
        inte += probability[i]
        inteval = np.append(inteval, inte)

    # Arithmetic Encoding
    # Initial Condition
    idx = set.index(text[0])
    lower = inteval[idx]
    upper = inteval[idx+1]
    # Recursion
    lowers, uppers = [lower], [upper]
    for i in range(1, len(text)):
        idx = set.index(text[i])
        prev = lower
        lower = prev + inteval[idx] * (upper - prev)
        upper = prev + inteval[idx+1] * (upper - prev)

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

def inv_arithmetic(ciphertext, data_length, set, probability):
    # Fool-Proof Mechanism
    if len(set) != len(probability) or sum(probability) != 1:
        print('=== ERROR !!!!! ===')
        return

    # Preprocess - Inteval of Probability 
    inteval, inte = np.zeros(1), 0
    for i in range(len(probability)):
        inte += probability[i]
        inteval = np.append(inteval, inte)
    
    # Find C and b in arithmetic encoding
    b, C = len(ciphertext), int(ciphertext, 2)
    p = C * pow(2, -b)
    p1 = (C+1) * pow(2, -b)

    # Recursively find the range include b and C
    text = []
    for idx in range(len(inteval)-1):
        if inteval[idx] < p and p1 < inteval[idx+1]:
            lower = inteval[idx]
            upper = inteval[idx+1]
            text.append(set[idx])
            break
    prev_len = 0
    while_break = False
    while prev_len != len(text):
        prev_lower = lower
        prev_upper = upper
        for idx in range(len(inteval)-1):
            lower = prev_lower + inteval[idx] * (prev_upper - prev_lower)
            upper = prev_lower + inteval[idx+1] * (prev_upper - prev_lower)
            if lower < p and p1 < upper:
                text.append(set[idx])
                if len(text) == data_length:
                    while_break = True
                break
        if while_break:
            break
        prev_len += 1
    
    return text

if __name__ == '__main__':
    # Error Encoding
    '''
    set = ['a', 'b']
    probability = [.8, .2]
    text = ['a', 'a', 'a', 'b', 'a']
    ciphertext = arithmetic(text, set, probability)
    print('ciphertext = {}'.format(ciphertext))
    text1 = inv_arithmetic(ciphertext, set, probability)
    print('recovered text = {}'.format(text1))
    text = ['a', 'a', 'a', 'b', 'a', 'a']
    ciphertext = arithmetic(text, set, probability)
    print('ciphertext = {}'.format(ciphertext))
    text1 = inv_arithmetic(ciphertext, set, probability)
    print('recovered text = {}'.format(text1))
    '''

    set = ['a', 'b']
    probability = [0.8, 0.2]
    data_length = 10
    print('\nset = {}, probability = {}, data_length = {}'.format(set, probability, data_length))
    print('Each test with 100 random data')
    for i in range(5):
        count = 0
        time_start = time.time()
        for j in range(100):
            text = random.choices(set, weights=tuple(probability), k=data_length)
            ciphertext = arithmetic(text, data_length, set, probability)
            text1 = inv_arithmetic(ciphertext, data_length, set, probability)
            if text != text1:
                count += 1
        time_end = time.time()
        print('Test {} : Spending time = {}'.format(i+1, time_end-time_start))
        print('Test {} : Accuracy = {} %'.format(i+1, (100-count)))
    print('\n')