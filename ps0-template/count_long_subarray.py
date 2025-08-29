def count_long_subarray(A):
    '''
    Input:  A     | Python Tuple of positive integers
    Output: count | number of longest increasing subarrays of A
    '''
    count = 0
    last = -float('inf')
    length = 0
    current = 0
    ##################
    # YOUR CODE HERE #
    ##################
    for a in A:
        if a > last:
            current += 1
        else:
            current = 1
        if current == length:
            count += 1
        if current > length:
            length = current
            count = 1
    

    return count

#  (11, 16, 10, 19, 20, 18, 3, 19, 2, 1, 8, 17, 7, 13, 1, 11, 1, 18, 19, 9, 7, 19, 24, 2, 12),
#         4,