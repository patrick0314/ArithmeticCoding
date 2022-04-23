import sys
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
    inteval, inte = [0], 0
    for i in range(len(probability)):
        inte += probability[i]
        inteval.append(inte)

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
    figure = plt.figure(figsize=(10, 2*len(text)))
    for i, (l, u) in enumerate(zip(lowers, uppers)):
        print(l, u)
        figure.add_subplot(len(text), 1, i+1)
        x = np.arange(l, u, 0.0000001)
        y = np.ones(x.shape)
        plt.plot(x, y, color='Red', lw=30)
        plt.xlim(0, 1), plt.ylim(0.9, 1.1)
        ax = plt.gca()
        ax.get_yaxis().set_visible(False)
    plt.show()

    # Find C and b s.t. lower < C * k^-b < (C+1) * k^-b < upper where k = 2 in general
    # If upper <= 0.5 or lower > 0.5, we can directly add 0 or 1 into the ciphertext
    ciphertext = ''
    count = 0
    while upper <= 0.5 or lower > 0.5:
        if upper <= 0.5:
            ciphertext += '0'
            lower *= 2
            upper *= 2
        elif lower > 0.5:
            ciphertext += '1'
            lower = lower * 2 - 1
            upper = upper * 2 - 1
        count += 1
        if count > 100:
            break

    #return
    # Traditional method to find b and C
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

    return ciphertext + str(bin(C)[2:]).zfill(b)

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
    # This algorithm only can encoding the text whose long less than 20
    # Otherwise, the float precision will overflow
    set = ['a', 'b']
    probability = [0.8, 0.2]
    #data_length = 10
    #text = random.choices(set, weights=tuple(probability), k=data_length)
    data_length = 6
    text = 'aaabaa'
    ciphertext = arithmetic(text, data_length, set, probability)
    recovered_text = inv_arithmetic(ciphertext, data_length, set, probability)

    print('Random text :', text)
    print('Ciphertext :', ciphertext)
    print('Recovered text :', recovered_text)

    set = ['a', 'b', 'c', 'd', 'e']
    probability = [0.15, 0.35, 0.05, 0.25, 0.2]
    data_length = 3
    text = 'bdb'
    ciphertext = arithmetic(text, data_length, set, probability)
    recovered_text = inv_arithmetic(ciphertext, data_length, set, probability)

    print('Random text :', text)
    print('Ciphertext :', ciphertext)
    print('Recovered text :', recovered_text)