#!/bin/python3

import bisect

if __name__ == '__main__':
    n = int(input())
    contacts = []
    for n_itr in range(n):
        opContact = input().split()

        op = opContact[0]

        contact = opContact[1]

        if op == 'add':
            bisect.insort_left(contacts, contact)
        else:
            left = bisect.bisect_left(contacts, contact)
            right = bisect.bisect_left(contacts, contact + 'zzzzzzzzzzz', left)
            print(right - left)
