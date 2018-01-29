#!/usr/bin/python3

# Prepare a function that displays nodes values of a tree passed to it as an argument. The passed element is the root node of the tree.
# All values should be displayed by tree levels (one tree level per line), i.e. root node in the first line, all nodes from the 2nd level in the second line, etc.
# Below example presents the behaviour:

#             A
#            / \
#          B    C
#        / | \    \
#      D   E  F    G

# For the above tree, the following result should be displayed on the screen:
# A
# B C
# D E F G

# You are allowed to decide on the data structure of the tree in the program memory.

from collections import deque

# Definition of a tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.children = []

def bfs_print(root):
    if not root:
        return 

    dq = deque([root])
    while len(dq): 
        current_level_size = len(dq)
        for _ in range(current_level_size):
            node = dq.popleft()
            for c in node.children:
                dq.append(c)
            print(node.val, end=' ')
        print()

if __name__ == '__main__':
    # root = TreeNode(97)
    # next_node = TreeNode(100)
    # root.children = [TreeNode(98), TreeNode(99), next_node]
    # next_node.children = [TreeNode(101)]
    root = None
    bfs_print(root)
