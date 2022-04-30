from Arithmetic import arithmetic, inv_arithmetic
from AdaptiveArithmetic import adaptivearithmetic, inv_adaptivearithmetic

import time
import sys

if __name__ == '__main__':
    while True:
        mode = input('Enter Arithmetic Coding for \'0\' and Adaptive Arithmetic Coding for \'1\': ')
        if mode == '0':
            print('\n===== Arithmetic Coding =====')
            # Default or Customization
            data_set = ['a', 'b']
            probability = [0.8, 0.2]
            # Fool Proof
            if len(data_set) != len(probability) or sum(probability)-1>0.00000000001:
                print('SOMETHING WRONG ABOUT DATA SET OR PROBABILITY')
                sys.exit()
            print('Data Set = {}'.format(data_set))
            print('Probability of Data = {}\n'.format(probability))

            # Arithmetic Coding
            while True:
                # User Input
                text = input('Enter your text message wanted to encoding: ')

                # Quit Commend
                if text == 'quit':
                    print('\n===== See ya !!! ======')
                    sys.exit()

                # Change Mode
                if text == 'change':
                    break
                
                # Fool Proof
                break_while = False
                for t in text:
                    if t not in data_set:
                        print('SOMETHING WRONG IN THE TEXT !!!')
                        sys.exit()
                
                # Computation
                time_start = time.time()
                ciphertext = arithmetic(text, data_set, probability)
                recovered_text = inv_arithmetic(ciphertext, len(text), data_set, probability)
                time_end = time.time()
                print('\nTime Cost = {}'.format(time_end-time_start))
                print('Arithmetic coding of \'{}\' = {}'.format(text, ciphertext))
                print('Recovered text = \'{}\''.format(recovered_text))
                if text == recovered_text: print('Successful Coding\n')
                else: print('Failed Coding\n')

        elif mode == '1':
            print('\n===== Adaptive Arithmetic Coding =====')
            # Default or Customization
            data_set = ['a', 'b']
            print('Data Set = {}\n'.format(data_set))

            # Adaptive Arithmetic Coding
            while True:
                # User Input
                text = input('Enter your text message wanted to encoding: ')

                # Quit Commend
                if text == 'quit':
                    print('\n===== See ya !!! ======')
                    sys.exit()

                # Change Mode
                if text == 'change':
                    break
                
                # Fool Proof
                break_while = False
                for t in text:
                    if t not in data_set:
                        print('SOMETHING WRONG IN THE TEXT !!!')
                        sys.exit()
                
                # Computation
                time_start = time.time()
                ciphertext = adaptivearithmetic(text, data_set)
                recovered_text = inv_adaptivearithmetic(ciphertext, len(text), data_set)
                time_end = time.time()
                print('\nTime Cost = {}'.format(time_end-time_start))
                print('Arithmetic coding of \'{}\' = {}'.format(text, ciphertext))
                print('Recovered text = \'{}\'\n'.format(recovered_text))
                if text == recovered_text: print('Successful Coding\n')
                else: print('Failed Coding\n')
        else:
            print('ONLY 0 OR 1 !!!!!!')