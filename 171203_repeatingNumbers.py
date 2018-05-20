# https://stackoverflow.com/questions/47581326/given-a-string-of-a-million-numbers-return-all-repeating-3-digit-numbers-inter
"""
Question: Given a string of a million numbers (Pi for example), write a function/program
that returns all repeating 3 digit numbers and number of repetition greater than 1
For example: if the string was: 123412345123456 then the function/program would return:

123 - 3 times
234 - 3 times
345 - 2 times

"""

import time

s = '123412345123456'


def cntRpt(str_in):
    d = dict()

    for c in range(len(str_in) - 2):
        seq = str_in[c:c + 3]
        try:
            d[seq] += 1
        except KeyError:
            d[seq] = 1

    for a in d:
        if d[a] > 1:
            print("key: {}, cnt: {}".format(a, d[a]))
    # print(d)
    time.sleep(1)

cntRpt(s)
