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

"""
    This problem can be solved by navigating the tree with a breadth-first search algorithm.
    Every node is visited only once to perform a constant operation so the complexity is O(N)
    being N the number of nodes in the tree.

    (Since, the Queue module implements multi-producer, multi-consumer queues. I have decided to use a deque.)
"""

from collections import deque


# Definition of a tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.children = []


def bfs_print(root):
    if not root:
        return 

    # Append the root to the queue
    dq = deque([root])
    while len(dq): 
        # during every outer iteration the queue has size = # of nodes in the current level
        current_level_size = len(dq)

        # for every node in the current level
        for _ in range(current_level_size):
            node = dq.popleft()
            # append its children to the queue
            for c in node.children:
                dq.append(c)
            # print the value of the node (without a newline)
            print(node.val, end=' ')
        # all nodes from the previous level were processed
        # the queue now only contains the nodes from the next level(or is empty)
        print()


if __name__ == '__main__':

    # Example 1
    root = None

    # Example 2
    # root = TreeNode(97)
    # next_node = TreeNode(100)
    # root.children = [TreeNode(98), TreeNode(99), next_node]
    # next_node.children = [TreeNode(101)]

    bfs_print(root)
