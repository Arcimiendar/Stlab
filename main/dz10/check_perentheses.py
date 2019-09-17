#!/bin/python3

import math
import os
import random
import re
import sys

if __name__ == '__main__':
    t = int(input())

    for t_itr in range(t):
        expression = input()

        stack = []

        breaked = False

        for letter in expression:
            if letter in ["(", "[", "{"]:
                stack.append(letter)
            else:
                if not len(stack):
                    breaked = True
                    break
                last = stack.pop()
                if not ((letter == "]" and last == "[") or
                        (letter == ")" and last == "(") or
                        (letter == "}" and last == "{")):
                    breaked = True
                    break

        if breaked or len(stack):
            print("NO")
        else:
            print("YES")

