from Arithmetic import arithmetic, inv_arithmetic

import time

if __name__ == '__main__':
    print('\n= = = = = = = = = = = = = = = = = = =')
    print('default data set is [\'a\', \'b\']')
    print('default probability is [0.5, 0.5]')
    print('= = = = = = = = = = = = = = = = = = =')

    # Customization
    data_set = ['a', 'b']
    probability = [0.5, 0.5]

    while True:
        # User Input
        text = input('Enter your text wanted to encoding like \'aba\': ')

        if text == 'quit':
            print('\n=== See ya !!! ===')
            break

        # Computation of Arithmetic Coding
        time_start = time.time()
        ciphertext = arithmetic(text, data_set, probability)
        recovered_text = inv_arithmetic(ciphertext, data_set, probability)
        time_end = time.time()

        # Output
        print('\nAfter {} (sec), encoding and decoding are completely finished'.format(time_end-time_start))
        print('Arithmetic coding of \'{}\' = {}'.format(text, ciphertext))
        print('Recovered text = \'{}\'\n'.format(''.join(recovered_text)))