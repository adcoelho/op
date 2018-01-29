#!/usr/bin/python3

# Note: If tasks descriptions below don't specify some behaviour in details
# (e.g. you miss some information) you are allowed to make your own assumptions.
# In such cases, please describe (e.g. in the code) what assumptions were taken by you.

# Task 1.

# Suppose you have rectangular area of size M x N. On each field you have 0 or 1.
# Your task is to design algorithm and write Python function for marking the
# largest 8-connected area of ones. Fields from the largest area should have the value 2.

# |1|0|1|0|1|    |2|0|2|0|1|
# |1|1|1|0|0| => |2|2|2|0|0|
# |0|1|0|1|0|    |0|2|0|2|0|
# |0|1|0|0|0|    |0|2|0|0|0|

# |1|0|1|     |2|0|2|
# |0|1|0| =>  |0|2|0|
# |0|0|0|     |0|0|0|

# If there will be more than one such area then all should be marked:

# |1|0|0|1|     |2|0|0|2|
# |1|1|0|1| =>  |2|2|0|2|
# |0|0|0|1|     |0|0|0|2|

# With the code please provide time complexity of your algorithm (use big O notation - http://en.wikipedia.org/wiki/Big_O_notation).

# Your function should have the following signature:

# - as a parameter it gets list of lists like:
#     [
#         [1,0,1,0,1],
#         [1,1,1,0,0],
#         [0,1,0,1,0]
#     ]

# - returns list of lists like:
#     [
#         [2,0,2,0,1],
#         [2,2,2,0,0],
#         [0,2,0,2,0]
#     ]

# The input parameter can be modified.

"""
    # Algorithm

    This problem is a variation of Connected-component labeling(see, https://en.wikipedia.org/wiki/Connected-component_labeling)
    that is commonly used in image processing.

    To solve it, I have adapted the watershed segmentation algorithm to the specifics of the task at hand.

    1. Start from the cell of the matrix. Set current label to 2(The values 0 and 1 are reserved). Go to (2).
    2. 
        2.1 If this cell has value 1 give it the current label and add it as the first element in a queue, then go to (3).
        2.2 If this cell has value 0 or it was already labeled, then repeat (2) for the next cell in the matrix.
    3. * Flooding/Watershed phase *
        Pop out an element from the queue, and look at its neighbours - based on the type of connectivity, in this case 8-connected.
        3.1 If a neighbour has value 1, give it the current label and add it to the queue.
        3.2 Else, check the next neighbour.
        3.3 Repeat (3) until there are no more elements in the queue - The full group has been labeled.
    4. Go to (2) for the next cell in the matrix and increment the current label by 1.

    During the labeling fase I always keep track of the size of the current group. After flooding, if new_group_size > max_group_size
    I update the max value and store the label. If the size is the same as the current max, both labels are stored.

    The final step is to iterate over the matrix one last time and update the cell values.
    1. The cells with a label from the biggest groups get value 2
    2. Cells with value 0 remain the same
    3. All other cells are have value 1

    # Time complexity

    Having broken down the algorithm in steps we can analyze their time complexity independently and merge them to reach the final value.
    
    This problem involves visiting all nodes in a matrix. It is impossible to judge what the contents of the matrix are without visiting the nodes
    so the best we can achieve in this case is a time complexity of O(N x M), linear complexity on the size of the matrix.


    We pass over the matrix 2 times. If both are linear the complexity will be O1(M x N) + O2(M x N) = O(M x N)

    The second pass is easy, every step does a constant operation so it is indeed O(M x N).

    But in the case of the first pass over the matrix the operations are not always constant. In particular, the step 3 takes some consideration.
    What is the worst case scenario here? If every cell in the matrix has value 1 then all of them will be queued.
    For every queued cell we check it's 8 neighbours(+ itself albeit unnecessarily). So we would do those 9 operations M x N times. This is O(9 x M x N).
    But can any cell be flooded twice? Actually no. The step 2.2 prevents that.

    Therefore, the worst case scenario would be:
        O(9 x M x N) - visit of the first cell
        +
        O((M - 1) x N) - visiting all other cells without entering the step 3

    This can be simplified down to O(M x N) by first using the "Multiplication by a constant" property and then the "Sum" property.

    O(9 x M x N) + O((M - 1) x N) + O(M x N) =
    O(M x N) + O((M - 1) x N) + O(M x N) =
    O(M x N) + O(M x N) =
    O(M x N)

"""


from collections import deque


def area_labeling(data):
    M = len(data)
    
    if M:
        N = len(data[0])
    else:
        return data

    current_label = 2
    max_value = 0
    max_labels = []        

    # First Pass:

    # Iterate over the the positions in the matrix
    for row in range(M):
        for column in range(N):

            # If the current position is a 1 we are going to:
            if data[row][column] == 1:

                # label the position
                data[row][column] = current_label

                # flood all neighbours with the same label
                dq = deque([(row, column)])
                current_max = 1

                while len(dq): 
                    row, column = dq.popleft()
                    for r in range(max(row - 1, 0), min(row + 2, M)):
                        for c in range(max(column - 1, 0), min(column + 2, N)):
                            if data[r][c] == 1:
                                data[r][c] = current_label
                                dq.append((r,c))
                                current_max += 1

                # Here is a key difference to the original algorithm.
                # Some logic is necessary to identify what is the biggest group.
                # this is done using the labels and the number of elements that each label has.
                if current_max > max_value:
                    max_labels = [current_label]
                    max_value = current_max
                elif current_max == max_value:
                    max_labels.append(current_label)
                
                current_label += 1
            
            # If the position was a 0 or previously labeled we move on to the next cell
            else:
                pass

    # Second pass:
    for row in range(M):
        for column in range(N):
            # Change the values of the cells with a label from the biggest groups to 2
            if data[row][column] in max_labels:
                data[row][column] = 2
            # All other labeled cells should have 1
            elif data[row][column] != 0:
                data[row][column] = 1
    
    return data


if __name__=='__main__':

    # example 1
    data = [[]]
    
    # example 2
    # data = [
    #     [1,0],
    #     [1,0]
    # ]

    # example 3
    # data = [
    #     [1,0,1,0,1],
    #     [1,0,1,0,0],
    #     [0,1,0,1,0]
    # ]

    # example 4
    # data = [
    #     [1,0,1,0,1,0,1,0,1],
    #     [0,1,0,1,0,1,0,1,0],
    #     [1,0,1,0,0,0,1,0,1],
    #     [0,1,0,1,0,1,0,1,0]
    # ]

    # example 5
    # data = [
    #     [1,0,1,0,1,0,1,0,1],
    #     [0,0,0,0,0,0,0,0,0],
    #     [1,0,1,0,1,0,1,0,1],
    #     [0,0,0,0,0,0,0,0,0],
    #     [1,0,1,0,1,0,1,0,1],
    #     [0,0,0,0,0,0,0,0,0],
    #     [1,0,1,0,1,0,1,0,1]
    # ]

    area_labeling(data)
    print(data)
