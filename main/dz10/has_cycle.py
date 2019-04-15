"""
Detect a cycle in a linked list. Note that the head pointer may be 'None' if the list is empty.

A Node is defined as:

    class Node(object):
        def __init__(self, data = None, next_node = None):
            self.data = data
            self.next = next_node
"""


def has_cycle(head):
    data_map = []
    while True:
        if head is None:
            break
        if head.data in data_map:
            return True
        data_map.append(head.data)
        head = head.next
    return False
