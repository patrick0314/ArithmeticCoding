import sys
import time
import random
import numpy as np
from itertools import product
from matplotlib import pyplot as plt

def inteval(dic):
    inte = {}
    prev = 0
    for k in dic.keys():
        if k != 'total':
            inte[k] = [prev, prev + dic[k]/dic['total']]
            prev += dic[k]/dic['total']
    return inte

def modeling(set):
    # dic[0]: previous is consonant
    # dic[1]: previous is vowel
    # dic[2]: the beginning of a sentence or previous is ' '
    # dic[3]: previous is ',' or '.'
    dic = {}
    for i in range(4):
        dic[i] = {'total':29}
        for s in set:
            dic[i][s] = 1
    return dic

def contextmodeling(text, set):
    # Context Modeling
    model = modeling(set)
    
    # Arithmetic Encoding
    # Initial Condition
    lower, upper = 0, 1
    
    # Recursion
    # If upper <= 0.5 or lower > 0.5, we can directly add 0 or 1 into the ciphertext
    ciphertext = ''
    prev_letter = ''
    for t in text:
        # Judge context and select table
        if prev_letter in ['a', 'e', 'i', 'o', 'u']: dic = model[1]
        elif prev_letter == '' or prev_letter == ' ': dic = model[2]
        elif prev_letter == ',' or prev_letter == '.': dic = model[3]
        else: dic = model[0]
        # Update lower & upper bound
        inte = inteval(dic)
        prev = lower
        lower = prev + inte[t][0] * (upper - prev)
        upper = prev + inte[t][1] * (upper - prev)
        # Update context table and prev_letter
        if prev_letter in ['a', 'e', 'i', 'o', 'u']:
            model[1][t] += 1
            model[1]['total'] += 1
            prev_letter = t
        elif prev_letter == '' or prev_letter == ' ':
            model[2][t] += 1
            model[2]['total'] += 1
            prev_letter = t
        elif prev_letter == ',' or prev_letter == '.':
            model[3][t] += 1
            model[3]['total'] += 1
            prev_letter = t
        else:
            model[0][t] += 1
            model[0]['total'] += 1
            prev_letter = t
        # Prevent from floating point error
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

def inv_contextmodeling(ciphertext, data_length, set):
    # Context Modeling
    model = modeling(set)

    # Arithmetic Decoding
    lower, upper = 0, 1
    lower1, upper1 = 0, 1
    j, times = 1, 0
    prev_letter = ''
    recovered_text = []
    for i in range(data_length):
        # Judge context and select table
        if prev_letter in ['a', 'e', 'i', 'o', 'u']: dic = model[1]
        elif prev_letter == '' or prev_letter == ' ': dic = model[2]
        elif prev_letter == ',' or prev_letter == '.': dic = model[3]
        else: dic = model[0]
        # Find which text is in the range
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
        # Update lower & upper bound
        prev = lower
        lower = prev + inte[k][0] * (upper-prev)
        upper = prev + inte[k][1] * (upper-prev)
        # Update context table and prev_letter
        if prev_letter in ['a', 'e', 'i', 'o', 'u']:
            model[1][k] += 1
            model[1]['total'] += 1
            prev_letter = k
        elif prev_letter == '' or prev_letter == ' ':
            model[2][k] += 1
            model[2]['total'] += 1
            prev_letter = k
        elif prev_letter == ',' or prev_letter == '.':
            model[3][k] += 1
            model[3]['total'] += 1
            prev_letter = k
        else:
            model[0][k] += 1
            model[0]['total'] += 1
            prev_letter = k
        # Prevent from floating point error
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
    set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', \
                'r', 's', 't' , 'u', 'v' , 'w', 'x', 'y' ,'z', ',', '.', ' ']
    text = 'this is an apple.'

    print('\n=== Random text : {} ==='.format(text))
    ciphertext = contextmodeling(text, set)
    print('=== Ciphertext : {} ==='.format(ciphertext))
    recovered_text = inv_contextmodeling(ciphertext, len(text), set)
    print('=== Recovered text : {} ==='.format(recovered_text))
    print('=== Coding completion : {} ===\n'.format(text == recovered_text))
    '''

    # 
    print('\n')
    set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', \
                'r', 's', 't' , 'u', 'v' , 'w', 'x', 'y' ,'z', ',', '.', ' ']
    f = open('article.txt', encoding='utf-8')
    idx = 1
    for line in f.readlines():
        text  = line.lower()[:-2]
        ciphertext = contextmodeling(text, set)
        recovered_text = inv_contextmodeling(ciphertext, len(text), set)
        print('=== Article {}: Coding completion = {} ==='.format(idx, (text==recovered_text)))
        print('Compression ratio = {}\n'.format(sys.getsizeof(text)*29/sys.getsizeof(ciphertext)/2))
        idx += 1
