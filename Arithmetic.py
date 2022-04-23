import sys
import time
import random
import numpy as np
from matplotlib import pyplot as plt

def arithmetic(text, data_length, set, probability):
    # Fool-Proof Mechanism
    if len(set) != len(probability) or round(sum(probability)) != 1 or len(set) != 2:
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
    lower = 0
    upper = 1
    
    # Recursion
    # If upper <= 0.5 or lower > 0.5, we can directly add 0 or 1 into the ciphertext
    ciphertext = ''
    for i in range(len(text)):
        idx = set.index(text[i])
        prev = lower
        lower = prev + inteval[idx] * (upper - prev)
        upper = prev + inteval[idx+1] * (upper - prev)

        while lower > 0.5 or upper <= 0.5:
            if lower > 0.5:
                ciphertext += '1'
                lower = lower * 2 - 1
                upper = upper * 2 - 1
            elif upper <= 0.5:
                ciphertext += '0'
                lower *= 2
                upper *= 2

    # Find C and b s.t. lower < C * k^-b < (C+1) * k^-b < upper where k = 2 in general
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
    if len(set) != len(probability) or round(sum(probability)) != 1 or len(set) != 2:
        print('=== ERROR !!!!! ===')
        return

    # Preprocess - Inteval of Probability
    inteval, inte = [0], 0
    for i in range(len(probability)):
        inte += probability[i]
        inteval.append(inte)

    #
    lower, upper = 0, 1
    lower1, upper1 = 0, 1
    j, times = 1, 0
    recovered_text = []
    for i in range(data_length):
        check = 1
        while check:
            for_break = True
            for n in range(len(inteval)-1):
                if lower + inteval[n] * (upper-lower) <= lower1 and lower + inteval[n+1] * (upper-lower) >= upper1:
                    check = 0
                    for_break = False
                    break
            if for_break:
                prev = lower1
                lower1 = prev + int(ciphertext[j-1]) * pow(2, -j+times)
                upper1 = prev + (int(ciphertext[j-1])+1) * pow(2, -j+times)
                j += 1
        recovered_text.append(set[n])
        lower = lower + inteval[n] * (upper-lower)
        upper = lower + inteval[n+1] * (upper-lower)
        while lower > 0.5 or upper <= 0.5:
            if lower > 0.5:
                lower = lower * 2 - 1
                upper = upper * 2 - 1
                lower1 = lower1 * 2 - 1
                upper1 = upper1 * 2 - 1
                times += 1
            elif upper <= 0.5:
                lower *= 2
                upper *= 2
                lower1 *= 2
                upper1 *= 2
                times += 1
    
    return ''.join(recovered_text)


if __name__ == '__main__':
    set = ['a', 'b']
    probability = [0.8, 0.2]
    data_length = 1000
    text = ''.join(random.choices(set, weights=tuple(probability), k=data_length))
    print('Random text :', text, sys.getsizeof(text))
    ciphertext = arithmetic(text, data_length, set, probability)
    print('Ciphertext :', ciphertext, sys.getsizeof(ciphertext))
    recovered_text = inv_arithmetic(ciphertext, data_length, set, probability)
    print('Recovered text :', recovered_text)
    ciphertext1 = arithmetic(recovered_text, data_length, set, probability)
    print('Coding completion: ', text == recovered_text)

    '''
    set = ['a', 'b']
    probability = [0.8, 0.2]
    number_data = 1000
    for i in range(5):
        data_length = 500 * (i+1)
        original_data = 0
        compression_data = 0
        count = 0
        time_start = time.time()
        for j in range(number_data):
            text = ''.join(random.choices(set, weights=tuple(probability), k=data_length))
            original_data += sys.getsizeof(text)
            ciphertext = arithmetic(text, data_length, set, probability)
            compression_data += sys.getsizeof(ciphertext)
            text1 = inv_arithmetic(ciphertext, data_length, set, probability)
            if text != text1:
                count += 1
        time_end = time.time()
        print('\nset = {}, probability = {}, data_length = {}'.format(set, probability, data_length))
        print('Each test with {} random data'.format(number_data))
        print('Test {} : Compression Rate = {}'.format(i+1, original_data / compression_data))
        print('Test {} : Spending time = {}'.format(i+1, time_end-time_start))
        print('Test {} : Accuracy = {} %'.format(i+1, (number_data-count)/number_data*100))
    print('\n')
    '''