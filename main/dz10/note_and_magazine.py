# !/bin/python3

import math
import os
import random
import re
import sys


# Complete the checkMagazine function below.
def checkMagazine(magazines, notes):
    dict_count = {}

    for magazine in magazines:
        if magazine in dict_count.keys():
            dict_count[magazine] += 1
        else:
            dict_count[magazine] = 1

    breaked = False
    for note in notes:
        if note not in dict_count.keys():
            breaked = True
            break
        elif dict_count[note] == 0:
            breaked = True
            break
        else:
            dict_count[note] -= 1

    if breaked:
        print("No")
    else:
        print("Yes")


if __name__ == '__main__':
    mn = input().split()

    m = int(mn[0])

    n = int(mn[1])

    magazine = input().rstrip().split()

    note = input().rstrip().split()

    checkMagazine(magazine, note)
