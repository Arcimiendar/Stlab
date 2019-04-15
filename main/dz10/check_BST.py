""" Node is defined as
class node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
"""
data = []
parents = []
main_root = []


def check_len(root):
    if root is None:
        return 0
    else:
        return check_len(root.right) + check_len(root.left) + 1


def check_path(value):
    temp_root = main_root[0]
    for parent in parents:
        if parent != temp_root.data:
            return False
        if value > temp_root.data:
            temp_root = temp_root.right
        else:
            temp_root = temp_root.left

    return True

def checkBST(root):
    main_root.append(root) if not len(main_root) else 0

    if root is None:
        return True
    if root.right is not None:
        if root.right.data <= root.data:
            return False
    if root.left is not None:
        if root.left.data >= root.data:
            return False
    if root.data in data:
        return False

    len_right = check_len(root.right)
    len_left = check_len(root.left)

    if len_left > len_right + 1:
        return False

    if len_right > len_left + 1:
        return False

    if not check_path(root.data):
        return False

    data.append(root.data)
    parents.append(root.data)
    right = checkBST(root.right)
    left = checkBST(root.left)
    parents.pop()
    return right and left
