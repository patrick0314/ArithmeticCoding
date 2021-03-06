import sys
import time
import random
import numpy as np
from matplotlib import pyplot as plt

def inteval(dic):
    inte = {}
    prev = 0
    for k in dic.keys():
        if k != 'total':
            inte[k] = [prev, prev + dic[k]/dic['total']]
            prev += dic[k]/dic['total']
    return inte

def adaptive(text, set):
    # Preprocess - Number of Element
    dic = {'total':0}
    for s in set:
        dic[s] = 1
        dic['total'] += 1
    
    # Arithmetic Encoding
    # Initial Condition
    lower, upper = 0, 1
    
    # Recursion
    # If upper <= 0.5 or lower > 0.5, we can directly add 0 or 1 into the ciphertext
    ciphertext = ''
    for t in text:
        inte = inteval(dic)
        prev = lower
        lower = prev + inte[t][0] * (upper - prev)
        upper = prev + inte[t][1] * (upper - prev)
        dic[t] += 1
        dic['total'] += 1
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

def inv_adaptive(ciphertext, data_length, set):
    # Preprocess - Number of Element
    dic = {'total':0}
    for s in set:
        dic[s] = 1
        dic['total'] += 1

    # Arithmetic Decoding
    lower, upper = 0, 1
    lower1, upper1 = 0, 1
    j, times = 1, 0
    recovered_text = []
    for i in range(data_length):
        inte = inteval(dic)
        check = 1
        while check:
            for_break = True
            for k in inte.keys():
                if lower + inte[k][0] * (upper-lower) <= lower1 and lower + inte[k][1] * (upper-lower) >= upper1:
                    check = 0
                    for_break = False
                    break
            if for_break:
                prev = lower1
                lower1 = prev + int(ciphertext[j-1]) * pow(2, -j+times)
                upper1 = prev + (int(ciphertext[j-1])+1) * pow(2, -j+times)
                j += 1

        recovered_text.append(k)
        dic[k] += 1
        dic['total'] += 1
        prev = lower
        lower = prev + inte[k][0] * (upper-prev)
        upper = prev + inte[k][1] * (upper-prev)
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

def random_data(set, probability, data_length):
    text = []
    for _ in range(data_length):
        text += random.choices(set, weights=tuple(probability), k=1)
    text = ''.join(text)
    return text

if __name__ == '__main__':
    '''
    '''
    set = ['a', 'b']
    text = 'aaabaa'
    print('\n=== Random text : {} ==='.format(text))
    ciphertext = adaptive(text, set)
    print('=== Ciphertext : {} ==='.format(ciphertext))
    recovered_text = inv_adaptive(ciphertext, len(text), set)
    print('=== Recovered text : {} ==='.format(recovered_text))
    print('=== Coding completion : {} ==='.format(text == recovered_text))
    print('=== {} bits compressed to {} bits, ratio {} ===\n'.format(len(text)*8, len(ciphertext), len(ciphertext)/(len(text)*8)))

    # Comparison with data length
    '''
    set = ['a', 'b', 'c', 'd', 'e']
    probability = [0.8, 0.05, 0.1, 0.025, 0.025]
    number_data = 1000
    for i in range(5):
        data_length = 1000 * (i+1)
        original_data = 0
        compression_data = 0
        count = 0
        time_start = time.time()
        for j in range(number_data):
            text = random_data(set, probability, data_length)
            original_data += sys.getsizeof(text)
            ciphertext = adaptive(text, set)
            compression_data += sys.getsizeof(ciphertext)
            text1 = inv_adaptive(ciphertext, data_length, set)
            if text != text1:
                count += 1
        time_end = time.time()
        print('\nset = {}, data_length = {}'.format(set, data_length))
        print('Each test with {} random data'.format(number_data))
        print('Spending time = {}'.format(time_end-time_start))
        print('Accuracy = {} %'.format((number_data-count)/number_data*100))
        print('{} bits compressed to {} bits, ratio {}'.format(len(text)*8, len(ciphertext), len(ciphertext)/(len(text)*8)))
    print('\n')
    '''

    # Comparison with set length and different distribution of data
    '''
    set1 = ['a', 'b']
    probability1 = [0.5, 0.5]
    set2 = ['a', 'b']
    probability2 = [0.8, 0.2]
    set3 = ['a', 'b', 'c', 'd', 'e']
    probability3 = [0.2, 0.2, 0.2, 0.2, 0.2]
    set4 = ['a', 'b', 'c', 'd', 'e']
    probability4 = [0.8, 0.05, 0.1, 0.025, 0.025]
    set5 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    probability5 = [0.8, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.0125, 0.0125]
    number_data = 1000
    sets = [set1, set2, set3, set4, set5]
    probabilitys = [probability1, probability2, probability3, probability4, probability5]
    for set, probability in zip(sets, probabilitys):
        data_length = 5000
        original_data = 0
        compression_data = 0
        count = 0
        time_start = time.time()
        for j in range(number_data):
            text = random_data(set, probability, data_length)
            original_data += sys.getsizeof(text)
            ciphertext = adaptive(text, set)
            compression_data += sys.getsizeof(ciphertext)
            text1 = inv_adaptive(ciphertext, data_length, set)
            if text != text1:
                count += 1
        time_end = time.time()
        print('\nset = {}, probability = {}, data_length = {}'.format(set, probability, data_length))
        print('Each test with {} random data'.format(number_data))
        print('Spending time = {}'.format(time_end-time_start))
        print('Accuracy = {} %'.format((number_data-count)/number_data*100))
        print('{} bits compressed to {} bits, ratio {}'.format(len(text)*8, len(ciphertext), len(ciphertext)/(len(text)*8)))
    print('\n')
    '''