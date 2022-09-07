from quicksort import *


def read_data(filename):
    """ Returns a list of integers read from the file """
    with open(filename) as infile:
        numbers = [int(line) for line in infile]
    return numbers


def common_items(list_x, list_y):
    """ Takes two sorted lists as input (ie, both lists are in ascending order).
    Returns a list containing all the items in list_x that are also in list_y.
    Returns an empty list if there are none.

    The resulting list should be in order and only contain one instance of each
    item that appears in both lists, ie, common items should only be listed once.
    NOTE: You should use a method similar to the merge function in mergesort,
    that is, use a while loop and a couple of indices. Don't use any for loops!

    First write code for dealing with two lists that each contain only uniques values.
    When you have that running, update it so that it deals with lists that don't
    contain all unique values, see the commented doctests below

    NOTES:
    Your function will need to use only one while loop.
    Your function shouldn't use expressions like:
       - item in alist
       - for item in alist

    >>> common_items([0,1,2,3],[1,2,3,4])
    [1, 2, 3]
    >>> common_items([0,1,2,3],[0,1,2,3])
    [0, 1, 2, 3]
    >>> common_items([0,1,2,3],[5,6,7,8])
    []
    >>> common_items([],[5,6,7,8])
    []
    >>> common_items([1,2,3,4],[])
    []
    >>> common_items([],[])
    []
    
    # add the following doctests (and some of your own)
    # when ready for lists of non-unique items
    >>> common_items([0,1,2,3],[0,0,2,4])
    [0, 2]
    >>> common_items([0,1,2,2,5,5,6,6,7],[0,0,2,4,5,5,5,7])
    [0, 2, 5, 7]
    """
    # ---start student section---
    
    common = []
    i = 0
    j = 0
    while i < len(list_x) and j < len(list_y):
        if list_x[i] == list_y[j] and list_x[i] not in common:
            common.append(list_x[i])
            i += 1
            j += 1
        else:
            if list_x[i] > list_y[j]:
                j += 1
            else:
                i += 1
    return common
    # ===end student section===


if __name__ == "__main__":
    doctest.testmod()
    ou_4 = read_data('./data/ordered_4.txt')
    ou_5 = read_data('./data/ordered_5.txt')
    print(len(common_items(ou_4,  ou_5)))