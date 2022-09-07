"""
An improved program that plays Shannon's Game.
Students should enter their name and number below!

PLEASE READ THROUGH ALL THE COMMENTS FOR INSTRUCTIONS!

Author: Lily Williams
Date: 25 January 2021
"""
import doctest
import re
import time
import sys
# import matplotlib.pyplot as plt


DEFAULT_CORPUS = 'corpus.txt'


def _c_mul(num_a, num_b):
    '''Substitute for c multiply function'''
    return (int(num_a) * int(num_b)) & 0xFFFFFFFF


def nice_hash(input_string):
    """ Takes a string name and returns a hash for the string. This hash value
    will be os independent, unlike the default Python hash function.
    It will also be stable across runs of Python, unlike the default.
    """
    if input_string is None:
        return 0  # empty
    value = ord(input_string[0]) << 7
    for char in input_string:
        value = _c_mul(1000003, value) ^ ord(char)
    value = value ^ len(input_string)
    if value == -1:
        value = -2
    return value


class Frequency(object):
    """
    DO NOT MODIFY THIS CLASS.
    Stores a letter:frequency pair.
    The repr for printing will be of the form <item, frequency>
    See the example below
    >>> f = Frequency('c', 2)
    >>> f.letter
    'c'
    >>> f.frequency
    2
    >>> print(f)
    <'c': 2>
    """

    def __init__(self, letter, frequency):
        self.letter = letter
        self.frequency = frequency
        self.next = None

    def __repr__(self):
        return ('<' +
                repr(self.letter) + ': ' + str(self.frequency) +
                '>')


class SortedFrequencyList(object):
    """
    Stores a collection of Frequency objects as a sorted linked list.
    Items are sorted from the highest frequency to the lowest.
    """

    def __init__(self):
        self.head = None

    def add(self, letter, frequency=1):
        """
        Adds the given letter and frequency combination as a Frequency object
        to the list. If the given letter is already in the list, the given
        frequency is added to its frequency.

        If the updated frequency is greater than the frequency of the previous
        node then it should be moved into order, ie, so that it is after
        all items with the same or greater frequency.

        If the letter is not in the list then the new frequency object should be
        added to the list so that it is after all letters
        with the same or higher frequency.

        Adding new letters with frequency 1 should be the sole usage case in
        this assignment and you can make your code more efficient if you treat
        letters with frequency of 1 as a special case. But, your code should
        still deal with the more general case, eg, my_list.add('a', 4)

        Of course, if there are no letters in the list
        then the new item should be added at the head.

        The doctests below should make it clear how this method should work.
        Hint: you should have code similar to this in your answers to lab 3 :)

        You will probably want to use a helper function.
        YOU MUST write some more doctests for this method.
        >>> f = SortedFrequencyList()
        >>> f.add('a', 1)
        >>> f
        SFL(<'a': 1>)
        >>> f.add('b', 1)
        >>> f
        SFL(<'a': 1>, <'b': 1>)
        >>> f.add('c', 1)
        >>> f
        SFL(<'a': 1>, <'b': 1>, <'c': 1>)
        >>> f.add('d', 1)
        >>> f
        SFL(<'a': 1>, <'b': 1>, <'c': 1>, <'d': 1>)
        >>> f.add('d', 1)
        >>> f
        SFL(<'d': 2>, <'a': 1>, <'b': 1>, <'c': 1>)
        >>> f.add('c', 1)
        >>> f
        SFL(<'d': 2>, <'c': 2>, <'a': 1>, <'b': 1>)
        >>> f.add('d', 1)
        >>> f
        SFL(<'d': 3>, <'c': 2>, <'a': 1>, <'b': 1>)
        >>> f.add('a', 1)
        >>> f
        SFL(<'d': 3>, <'c': 2>, <'a': 2>, <'b': 1>)
        >>> f.add('b', 2)
        >>> f
        SFL(<'d': 3>, <'b': 3>, <'c': 2>, <'a': 2>)
        >>> f.add('a', 4)
        >>> f
        SFL(<'a': 6>, <'d': 3>, <'b': 3>, <'c': 2>)
        >>> f.add('r', 4)
        >>> f
        SFL(<'a': 6>, <'r': 4>, <'d': 3>, <'b': 3>, <'c': 2>)
        >>> f.add('t', 3)
        >>> f
        SFL(<'a': 6>, <'r': 4>, <'d': 3>, <'b': 3>, <'t': 3>, <'c': 2>)
        >>> f.add('z', 1)
        >>> f
        SFL(<'a': 6>, <'r': 4>, <'d': 3>, <'b': 3>, <'t': 3>, <'c': 2>, <'z': 1>)
        >>> sflist = SortedFrequencyList()
        >>> sflist.add('z', 32)
        >>> sflist
        SFL(<'z': 32>)
        >>> sflist.add('y', 44)
        >>> sflist
        SFL(<'y': 44>, <'z': 32>)
        >>> sflist.add('x', 2)
        >>> sflist
        SFL(<'y': 44>, <'z': 32>, <'x': 2>)
        >>> sflist.add('x', 31)
        >>> sflist
        SFL(<'y': 44>, <'x': 33>, <'z': 32>)
        >>> sflist.add('w', 1)
        >>> sflist.add('x', 12)
        >>> sflist
        SFL(<'x': 45>, <'y': 44>, <'z': 32>, <'w': 1>)
        """
        # ---start student section---
        if self.head == None:                               # If the list is empty
            new_node = Frequency(letter, frequency)         # make the new node the head
            self.head = new_node
            return                                          # return early

        current = self.head                                 # otherwise        
        prev = current                                  
        super_prev = prev
        while current is not None:    # cycle through the list
            if current.letter == letter:    # to find an existing node
                current.frequency += frequency              # and increase the frequency
                
                if current.frequency > prev.frequency:      # If reordering is necessary
                    shifting = current                      # store the moving node in a variable
                    prev.next = current.next                # remove the moving node from the linked list
                    
                    current = self.head                     # starting a new list search
                    prev = current
                    while current is not None:              # As long as it hasn't been switched yet and you having reached the end of the loop
                        if current.frequency < shifting.frequency and self.head == current:  # Is the head the correct location?
                            self.head = shifting                                                # Insert the moving node the head
                            shifting.next = current                                             # attach the list to the node
                            return                                                              # finished!
                            
                        elif current.frequency < shifting.frequency and self.head != current: # Nope, not the head but still correct?
                            prev.next = shifting                        # Plug the node into the list
                            shifting.next = current
                            return                                      #finished!

                        else:                                       # Not the correct location!
                            prev = current                              # Keep the cycling
                            current = current.next
                return
                            
                            
                                                           # you haven't found the correct node so keep cycling
            super_prev = prev
            prev = current
            current = current.next
# if a match was not found
        new_node = Frequency(letter, frequency)         # make a new node
        current = self.head
        prev = current
        super_prev = prev
        inserted = False
        while current is not None and inserted == False:    # find the correct place for it
            if current.frequency >= frequency and current.next is None:     # if the current item goes ahead in the order and new node goes last
                current.next = new_node                                         # insert at the end
                inserted = True                                                 # break the loop

            elif current.frequency >= frequency and current.next is not None:   # you havent found the right place and havent reached the end of the list
                prev = current                                                      # keep searching
                current = current.next
                
            elif self.head == current:                  # you're inserting at the head?
                self.head = new_node                        # Yes! New node is the new head
                new_node.next = current                     # The list is linked onto it
                inserted = True                             # and the loop is broken
            else:                                       # you're not inserting at the head or the tail.
                prev.next = new_node                        # insert in in its place
                new_node.next = current                     # link into the list
                inserted = True                             # and the loop is broken
                        
                        
        # ===end student section===

    def remove(self, letter):
        """
        Removes the Frequency object with the given `letter` from the list.
        Does nothing if `letter` is not in the list.
        YOU MUST write some more doctests for this method.

        >>> f = SortedFrequencyList()
        >>> f.add('a', 3)
        >>> f.add('b', 2)
        >>> f.add('c', 1)
        >>> f
        SFL(<'a': 3>, <'b': 2>, <'c': 1>)
        >>> f.remove('b')
        >>> f
        SFL(<'a': 3>, <'c': 1>)
        >>> f.add('d', 2)
        >>> f.add('e', 5)
        >>> f
        SFL(<'e': 5>, <'a': 3>, <'d': 2>, <'c': 1>)
        >>> f.remove('y')
        >>> f
        SFL(<'e': 5>, <'a': 3>, <'d': 2>, <'c': 1>)
        >>> f.remove('c')
        >>> f
        SFL(<'e': 5>, <'a': 3>, <'d': 2>)
        >>> f.remove('e')
        >>> f
        SFL(<'a': 3>, <'d': 2>)
        >>> f.remove('a')
        >>> f
        SFL(<'d': 2>)
        >>> f.remove('d')
        >>> f
        SFL()
        >>> f.remove('d')
        >>> f
        SFL()
        """
        # ---start student section---
        if self.head == None:                   # Is the list empty?
            return                                          
        else:                                       # The list is not empty
            current = self.head                         # Prepare to cycle
            prev = current
            while current is not None:                  # Begin searching the list
                if current.letter == letter:                # Is the current item the one you're searching for?
                    if self.head == current:                    # Yes, is the desired item the head?
                        self.head = current.next                    # Yes. Bypass the node and reassign the head
                        current.next = None
                        return
                    elif current.next == None:                  # No, is the desired item the tail?
                        prev.next = None                            # Yes. Bypass the node and remove links
                        current.next = None
                        return
                    else:                                       # No, its in the  middle somewhere.                                       
                        prev.next = current.next                    #  Link around the node
                        current.next = None
                        return
                else:                                       # Not the correct one, keep cycling.
                    prev = current
                    current = current.next
            if current is None:                     # The letter is not in the list
                return                                  # so do nothing
        # ===end student section===

    def find(self, letter):
        """
        Returns the Frequency object for the given `letter` in the list, or
        None if the `letter` doesn't appear in the list.
        YOU MUST write some more doctests for this method.

        >>> f = SortedFrequencyList()
        >>> f.add('a', 3)
        >>> f.find('a')
        <'a': 3>
        >>> print(f.find('b'))
        None
        >>> f.add('b', 2)
        >>> f.add('c', 5)
        >>> f.add('d', 1)
        >>> f.find('d')
        <'d': 1>
        >>> f.find('c')
        <'c': 5>
        >>> f.find('b')
        <'b': 2>
        >>> print(f.find('x'))
        None
        >>> g = SortedFrequencyList()
        >>> print(g.find('a'))
        None
        """
        # ---start student section---
        if self.head == None:                   #  Is the list empty?
            return None
        else:                                   # Nope!
            current = self.head
            while current is not None:          # Cycle through the list until the end
                if current.letter == letter:        #Is it a match?
                    return current                      #Return the matching node
                else:                               # Not a match
                    current = current.next              # Keep cycling
            if current == None:                 # The item is not in the list
                return None                         
        # ===end student section===

    def __contains__(self, item):
        # you should use the find method here
        # ---start student section---
        if self.find(item) is not None:         # Uses the find method
            return True                             # It is present in the list
        else:
            return False                            #  It is not present in the list
        # ===end student section===

    def __iter__(self):
        """ Note this will be used to return a simple list of Frequency items
        eg, list(my_sorted_frequency_list)
        Students shouldn't change this method and don't need to understand it.
        """
        current = self.head
        while current is not None:
            yield current.letter
            current = current.next

    def __repr__(self):
        """ Returns a string representation of the list, eg, SFL(<'e': 2>, <'d': 1>))
        """
        item_strs = []
        current = self.head
        while current is not None:
            item_strs.append(repr(current))
            current = current.next
        return 'SFL(' + ', '.join(item_strs) + ')'



class PrefixItem(object):
    """
    DO NOT MODIFY THIS CLASS.
    Stores a prefix:possibles pair.

    >>> p = PrefixItem('th', SortedFrequencyList())
    >>> p.possibles.add('e', 40)
    >>> p.possibles.add('o', 10)
    >>> p
    PfI('th': SFL(<'e': 40>, <'o': 10>))
    """

    def __init__(self, prefix, possibles):
        """
        Initialises a new PrefixItem with the given letter `prefix` and
        SortedFrequencyList of `possibles`.
        """
        self.prefix = prefix
        self.possibles = possibles

    def __hash__(self):
        return nice_hash(self.prefix)

    def __repr__(self):
        return 'PfI(' + repr(self.prefix) + ': ' + repr(self.possibles) + ')'


class PrefixTable(object):
    """
    A simple hash table for storing prefix:possible combinations using
    PrefixItems internally.
    """

    def __init__(self, slots):
        """
        Initialises the PrefixTable with a number of `slots`. The table cannot
        store more items than the number of slots specified here.
        """
        self.data = [None] * slots

    def store(self, prefix, possibles):
        """
        Stores the given letter `prefix` and list of `possibles` (a
        SortedFrequencyList) in the hash table using a PrefixItem. If the
        item is successfully stored in the table, this method returns
        True, otherwise (for example, if there is no more room left in the
        table) it returns False.
        Make sure you use nice_hash to get the initial hash
        and remember you are using linear probing for clashes.
        YOU MUST write some more doctests for this method.

        >>> p = PrefixTable(1)
        >>> p.store('th', SortedFrequencyList())
        True
        >>> p
        Prefix hash Table
        -----------------
            0: PfI('th': SFL())
        >>> p.store('ca', SortedFrequencyList())
        False
        >>> t = PrefixTable(0)
        >>> t.store('yo', SortedFrequencyList())
        False
        >>> f = PrefixTable(4)
        >>> f.store('ab', SortedFrequencyList())
        True
        >>> f
        Prefix hash Table
        -----------------
            0: None
            1: None
            2: None
            3: PfI('ab': SFL())
        >>> f.store('bc', SortedFrequencyList())
        True
        >>> f
        Prefix hash Table
        -----------------
            0: PfI('bc': SFL())
            1: None
            2: None
            3: PfI('ab': SFL())
        >>> f.store('cd', SortedFrequencyList())
        True
        >>> f
        Prefix hash Table
        -----------------
            0: PfI('bc': SFL())
            1: PfI('cd': SFL())
            2: None
            3: PfI('ab': SFL())
        >>> f.store('de', SortedFrequencyList())
        True
        >>> f
        Prefix hash Table
        -----------------
            0: PfI('bc': SFL())
            1: PfI('cd': SFL())
            2: PfI('de': SFL())
            3: PfI('ab': SFL())
        >>> f.store('ef', SortedFrequencyList())
        False
        """
        # ---start student section---
        if len(self.data) == 0:                                                         # If the number of slots is 0
            return False                                                                    # Nothing can be stored.
        else:                                                                           # Otherwise
            new_item = PrefixItem(prefix, possibles)                                        # Initialise a new prefix item,
            index = nice_hash(prefix) % len(self.data)                                      # locate an initial hash using nice_hash,
            slots_checked = 0                                                               # start a count of the number of slots checked
            while self.data[index] is not None and slots_checked <= len(self.data):         # until you find a free slot OR youve checked them all
                if self.data[index] is not None:                                                #does the slot have something in it?
                    if self.data[index].prefix == prefix:                                           # yes, is it the prefix you're trying to store?
                        new_item = PrefixItem(prefix, possibles)                                        # same prefix, updated list of possibles
                        self.data[index] = new_item                                                     # replace the old item in the list
                        return True                                                                     # job done
                    else:                                                                           # no, it's not a match
                        index = (index + 1) % len(self.data)                                            # increment the index
                        slots_checked += 1                                                              # and add 1 to the check count        
        
            if self.data[index] is not None:                                                # If all the slots are full
                return False                                                                    # nothing can be stored.
            else:                                                                           # Otherwise an empty slot has been found
                new_item = PrefixItem(prefix, possibles)
                self.data[index] = new_item                                                     # the new item is stored in the table
                return True                                                                     # and the method returns true    
        # ===end student section===

    def fetch(self, prefix):
        """"
        Returns the SortedFrequencyList of possibles associated with the given
        letter `prefix', or None if the `prefix` isn't stored in the table.
        Make sure you use nice_hash to get the initial hash
        and remember you are using linear probing for clashes
        YOU MUST write some more doctests for this method.

        >>> prefix = 'th'
        >>> possibles = SortedFrequencyList()
        >>> possibles.add('e', 40)
        >>> possibles.add('o', 10)
        >>> p = PrefixTable(1)
        >>> p.store(prefix, possibles)
        True
        >>> p.fetch('th')
        SFL(<'e': 40>, <'o': 10>)
        >>> print(p.fetch('ca'))
        None
        >>> prefix = 'ca'
        
        >>> possibles = SortedFrequencyList()
        >>> possibles.add('a', 3)
        >>> possibles.add('z', 7)
        >>> f = PrefixTable(4)
        >>> f.store('ab', possibles)
        True
        >>> f.fetch('ab')
        SFL(<'z': 7>, <'a': 3>)
        >>> print(f.fetch('bc'))
        None
        >>> f.store('bc', possibles)
        True
        >>> f.fetch('bc')
        SFL(<'z': 7>, <'a': 3>)
        >>> f.store('cd', possibles)
        True
        >>> f.fetch('cd')
        SFL(<'z': 7>, <'a': 3>)
        >>> f.store('de', possibles)
        True
        >>> f.store('ef', possibles)
        False
        >>> print(f.fetch('ef'))
        None
        
        >>> g = PrefixTable(0)
        >>> print(g.fetch('gg'))
        None
        >>> f.store('gg', possibles)
        False
        >>> print(g.fetch('gg'))
        None
        
        """
        # ---start student section---
        if len(self.data) == 0:                                         # Ensure you're not checking a length 0 table
            return None                                                     # in which case, do nothing
        else:                                                           # not length 0!
            index = nice_hash(prefix) % len(self.data)                      # create an initial hash guess (modulated of course)
            slots_checked = 0                                               # create a variable to ensure the checking has an end point
            found = False                                                   # a while loop break out clause
            while found == False and slots_checked <= len(self.data):       # search the list until you find it or until youve searched the whole list
                if self.data[index] is None:                                    # is the slot empty?
                    index = (index + 1) % len(self.data)                            # check the next slot (linear probing)
                    slots_checked += 1                                              # keep count of the slots youve checked
                else:                                                           # the slot isn't empty
                    if self.data[index].prefix == prefix:                           # does the slot have the prefix youre searching for?
                        found = True                                                        # break the while loop
                        return self.data[index].possibles                                   # it do. print the desired information

                    else:                                                           # this is not the prefix youre searching for
                        index = (index + 1) % len(self.data)                            # check the next slot (linear probing)
                        slots_checked += 1                                              # keep count of the slots youve checked
            if found == False and slots_checked >= len(self.data):                  # you havent found it and checked every slot?
                return None                                                             # give up! (jk just say its not there)
        # ===end student section===

    def __contains__(self, prefix):
        """ Returns True if prefix is in the table, otherwise False"""
        # ---start student section---
        if len(self.data) == 0:                                         # Ensure you're not checking a length 0 table
            return False                                                    # in which case, say its not there
        else:                                                           # not length 0!
            index = nice_hash(prefix) % len(self.data)                      # create an initial hash guess (modulated of course)
            slots_checked = 0                                               # create a variable to ensure the checking has an end point
            while slots_checked <= len(self.data):                          # search the list until you find it or youve searched the whole list
                if self.data[index] is None:                                    # is the slot empty?
                    index = (index + 1) % len(self.data)                            # check the next slot (linear probing)
                    slots_checked += 1                                              # keep count of the slots youve checked
                else:                                                           # the slot isn't empty
                    if self.data[index].prefix == prefix:                           # does the slot have the prefix youre searching for?
                        return True                                                     # say youve got it
                    else:                                                           # this is not the prefix youre searching for
                        index = (index + 1) % len(self.data)                            # check the next slot (linear probing)
                        slots_checked += 1                                              # keep count of the slots youve checked
            if slots_checked >= len(self.data):                                     # you havent found it and checked every slot?
                return False                                                             # say its not there

                    
        # ===end student section===

    def __repr__(self):
        ans = 'Prefix hash Table\n'
        ans += '-----------------'
        for i, item in enumerate(self.data):
            ans += '\n{:5}: {}'.format(i, repr(item))
        return ans



def process_corpus(corpus, unique_chars):
    """
    Returns a PrefixTable populated with the possible characters that follow
    each character pair in `corpus`. `unique_chars` is the number of unique
    characters in `corpus`.

    The size of the PrefixTable should be chosen by calculating the maximum
    number of character pairs (the square of `unique_chars`). In practice,
    the actual number of unique pairs in the corpus will be considerably less
    than this, so we are guaranteed a low load factor.

    WARNING: Clashes may still occur and you must use linear probing
    to resolve clashes

    Note: The ...'s below indicate lines have been chopped out to save space
          Usually the lines will just contain None

    NOTE: YOU MUST write some doctests for the method here! Ones that
    produce more interesting SFL's would be good.


    >>> process_corpus('lazy languid line', 11) #doctest: +ELLIPSIS
    Prefix hash Table
    -----------------
        0: None
       ...
       19: None
       20: PfI('ui': SFL(<'d': 1>))
       21: None
       ...
       41: None
       42: PfI('la': SFL(<'z': 1>, <'n': 1>))
       43: None
       44: PfI('an': SFL(<'g': 1>))
       45: None
       ...
       49: None
       50: PfI('li': SFL(<'n': 1>))
       51: None
       ...
       55: None
       56: PfI('az': SFL(<'y': 1>))
       57: PfI('y ': SFL(<'l': 1>))
       58: None
       59: None
       60: None
       61: PfI('ng': SFL(<'u': 1>))
       62: None
       63: None
       64: PfI('gu': SFL(<'i': 1>))
       65: None
       66: None
       67: None
       68: None
       69: PfI(' l': SFL(<'a': 1>, <'i': 1>))
       70: None
       ...
       93: None
       94: PfI('d ': SFL(<'l': 1>))
       95: None
       96: PfI('in': SFL(<'e': 1>))
       97: None
       98: None
       99: None
      100: None
      101: PfI('zy': SFL(<' ': 1>))
      102: PfI('id': SFL(<' ': 1>))
      103: None
      ...
      120: None
    >>> process_corpus('pitter patter', 7) #doctest: +ELLIPSIS
    Prefix hash Table
    -----------------
        0: None
        1: None
        2: None
        3: PfI('tt': SFL(<'e': 2>))
        4: None
       ...
       19: None
       20: PfI('te': SFL(<'r': 2>))
       21: None
       ...
       29: None
       30: PfI('er': SFL(<' ': 1>))
       31: None
       ...
       33: None
       34: PfI('pa': SFL(<'t': 1>))
       35: None
       ...
       37: None
       38: PfI(' p': SFL(<'a': 1>))
       39: PfI('it': SFL(<'t': 1>))
       40: PfI('r ': SFL(<'p': 1>))
       41: None
       42: PfI('pi': SFL(<'t': 1>))
       43: PfI('at': SFL(<'t': 1>))
       44: None
       ...
       48: None
    >>> process_corpus('riff raff', 5)  #doctest: +ELLIPSIS
    Prefix hash Table
    -----------------
        0: PfI(' r': SFL(<'a': 1>))
        1: None
        2: PfI('ra': SFL(<'f': 1>))
        3: None
        4: None
        5: None
        6: PfI('if': SFL(<'f': 1>))
        7: None
        8: None
        9: None
       10: PfI('ri': SFL(<'f': 1>))
       11: PfI('af': SFL(<'f': 1>))
       12: None
       13: None
       14: None
       15: None
       16: PfI('ff': SFL(<' ': 1>))
       17: None
       18: None
       19: None
       20: None
       21: PfI('f ': SFL(<'r': 1>))
       22: None
       23: None
       24: None
    >>> process_corpus('ppppppppp', 1) #doctest: +ELLIPSIS
    Prefix hash Table
    -----------------
        0: PfI('pp': SFL(<'p': 7>))
    >>> process_corpus('wrgipj gjriwpdkjgqe tuiepqutioeoqutioqe gdnjksowodngfei', 10) #doctest: +ELLIPSIS
    Prefix hash Table
    -----------------
        0: None
        1: None
        2: None
        3: PfI('ti': SFL(<'o': 2>))
        4: None
        5: PfI('gj': SFL(<'r': 1>))
        6: PfI('gi': SFL(<'p': 1>))
        7: PfI('jr': SFL(<'i': 1>))
        8: PfI(' t': SFL(<'u': 1>))
        9: PfI('ip': SFL(<'j': 1>))
       10: PfI('oe': SFL(<'o': 1>))
       11: PfI('nj': SFL(<'k': 1>))
       12: PfI('od': SFL(<'n': 1>))
       13: None
       14: PfI('iw': SFL(<'p': 1>))
       15: PfI('jk': SFL(<'s': 1>))
       16: None
       17: None
       18: None
       19: PfI('jg': SFL(<'q': 1>))
       20: PfI('dn': SFL(<'j': 1>, <'g': 1>))
       21: PfI('ow': SFL(<'o': 1>))
       22: PfI('io': SFL(<'e': 1>, <'q': 1>))
       23: PfI('ng': SFL(<'f': 1>))
       24: PfI('qu': SFL(<'t': 2>))
       25: PfI('dk': SFL(<'j': 1>))
       26: PfI('oq': SFL(<'u': 1>, <'e': 1>))
       27: None
       28: PfI('ie': SFL(<'p': 1>))
       29: PfI('e ': SFL(<'t': 1>, <'g': 1>))
       30: None
       ...
       34: None
       35: PfI('pq': SFL(<'u': 1>))
       36: None
       37: None
       38: None
       39: None
       40: PfI('qe': SFL(<' ': 2>))
       41: None
       ...
       53: None
       54: PfI('pd': SFL(<'k': 1>))
       55: PfI('eo': SFL(<'q': 1>))
       56: PfI('pj': SFL(<' ': 1>))
       57: PfI('j ': SFL(<'g': 1>))
       58: PfI('kj': SFL(<'g': 1>))
       59: None
       ...
       63: None
       64: PfI('ks': SFL(<'o': 1>))
       65: PfI('so': SFL(<'w': 1>))
       66: PfI('fe': SFL(<'i': 1>))
       67: None
       68: PfI('wo': SFL(<'d': 1>))
       69: None
       ...
       74: None
       75: PfI('rg': SFL(<'i': 1>))
       76: None
       77: PfI('ut': SFL(<'i': 2>))
       78: None
       79: None
       80: None
       81: PfI('wr': SFL(<'g': 1>))
       82: PfI('gq': SFL(<'e': 1>))
       83: PfI('wp': SFL(<'d': 1>))
       84: PfI('ep': SFL(<'q': 1>))
       85: PfI('ri': SFL(<'w': 1>))
       86: None
       87: None
       88: PfI('ui': SFL(<'e': 1>))
       89: PfI(' g': SFL(<'j': 1>, <'d': 1>))
       90: None
       91: PfI('tu': SFL(<'i': 1>))
       92: None
       93: PfI('gf': SFL(<'e': 1>))
       94: None
       95: PfI('gd': SFL(<'n': 1>))
       ...
       99: None
       >>> process_corpus('ggqggwgge ', 4) #doctest: +ELLIPSIS
       Prefix hash Table
       -----------------
           0: PfI('gg': SFL(<'q': 1>, <'w': 1>, <'e': 1>))
           1: PfI('gw': SFL(<'g': 1>))
           2: PfI('wg': SFL(<'g': 1>))
           3: PfI('ge': SFL(<' ': 1>))
           4: None
           5: None
           6: PfI('gq': SFL(<'g': 1>))
           7: PfI('qg': SFL(<'g': 1>))
           8: None
           ...
          15: None
        >>> process_corpus('what we owe to each other', 10) #doctest: +ELLIPSIS
        Prefix hash Table
        -----------------
            0: None
            1: None
            2: PfI('th': SFL(<'e': 1>))
            3: None
            4: None
            5: PfI(' w': SFL(<'e': 1>))
            6: PfI(' t': SFL(<'o': 1>))
            7: PfI('ac': SFL(<'h': 1>))
            ...
           19: None
           20: PfI('ow': SFL(<'e': 1>))
           21: None
           22: None
           23: PfI('ot': SFL(<'h': 1>))
           24: None
           25: PfI('at': SFL(<' ': 1>))
           ...
           28: None
           29: PfI('e ': SFL(<'o': 1>, <'t': 1>))
           30: PfI('h ': SFL(<'o': 1>))
           31: PfI('ch': SFL(<' ': 1>))
           ...
           46: None
           47: PfI('o ': SFL(<'e': 1>))
           ...
           61: None
           62: PfI('we': SFL(<' ': 2>))
           63: None
           64: PfI('ea': SFL(<'c': 1>))
           ...
           73: None
           74: PfI('t ': SFL(<'w': 1>))
           75: PfI('wh': SFL(<'a': 1>))
           ...
           90: None
           91: PfI(' e': SFL(<'a': 1>))
           92: None
           93: None
           94: None
           95: PfI('ha': SFL(<'t': 1>))
           96: None
           97: PfI(' o': SFL(<'w': 1>, <'t': 1>))
           98: PfI('to': SFL(<' ': 1>))
           99: PfI('he': SFL(<'r': 1>))
        >>> process_corpus('', 0) #doctest: +ELLIPSIS
        Prefix hash Table
        -----------------
        >>> process_corpus('                 ', 1) #doctest: +ELLIPSIS
        Prefix hash Table
        -----------------
            0: PfI('  ': SFL(<' ': 15>))

    """
    # ---start student section---
    table = PrefixTable(unique_chars*unique_chars)      # Create the table
    i = 0                                               # Create the index
    while i <= (len(corpus) - 3):                      # check each pair of characters in the corpus
        prefix = corpus[i] + corpus[i+1]                    # identify the prefix
        following_char = str(corpus[i+2])                   # identify the proceeding character to the prefix
        if table.fetch(prefix) is not None:                 # if the prefix is already in the table
            possibles = table.fetch(prefix)                     # take the existing possibles list
            possibles.add(following_char)                       # add the new character
            table.store(prefix, possibles)                      # store the updated prefix:possibles pair
        else:                                               # the prefix is not in the table
            possibles = SortedFrequencyList()                   # create an empty possibles list
            possibles.add(following_char)                       # add the proceeding character
            table.store(prefix, possibles)                      # store the new prefix:possibles pair
        i += 1                                              # iterate onwards
    return table    
        
    # ===end student section===


def run_time_trials():
    """ A good place to write code for time trials
    Make sure you use this docstring to explain your code and that
    you write comments in your code to help explain the process.
    """
    pass
    
    

def run_some_trials():
    """ Play some games with various test phrases and settings """
    # play game using whatever you like
    # maybe put an input statement here
    # so you can enter the corpus
    # and settings
    # or just run various games with various settings

    # test_phrases = ['dead war']

    #'Hello isn\'t it a lovely day today.']
    # MAKE SURE you test with various phrases!

    #test_files = [DEFAULT_CORPUS]

    # 'the-yellow-wall-paper.txt',
    # 'hamlet.txt',
    # 'le-rire.txt',
    # 'war-of-the-worlds.txt',
    # 'ulysses.txt',
    # 'war-and-peace.txt']

    #Uncomment the block below to run trials based on the lists of phrases and files above
    #for test_phrase in test_phrases:
        #for corpus_filename in test_files:
            #phrase_length = 0   # for auto-run
            #load_corpus_and_play(corpus_filename, test_phrase, phrase_length)
            #print('\n'*3)

    # check out https://www.gutenberg.org/ for more free books!

    # interactive trial
    # see how long the program takes to guess 'bat man'
    # it will get the first two characters and start asking you
    # if it has the third character correct etc...
    # load_corpus_and_play(corpus_filename, 'ba', 7)
    pass


def test():
    """ Runs doctests """
    # uncomment various doctest runs to check each method/function
    # MAKE sure your submitted code doesn't run tests except
    # MAKE SURE you add some doctests of your own to the docstrings
    #doctest.run_docstring_examples(SortedFrequencyList.add, globs=None)
    #doctest.run_docstring_examples(SortedFrequencyList.remove, globs=None)
    #doctest.run_docstring_examples(SortedFrequencyList.find, globs=None)

    #doctest.run_docstring_examples(PrefixTable.store, globs=None)
    #doctest.run_docstring_examples(PrefixTable.fetch, globs=None)
    
    #doctest.run_docstring_examples(process_corpus, globs=None)

    # you can leave the following line uncommented as long as your code
    # passes all the tests the line won't produce any output
    doctest.testmod()  # run all doctests - this is helpful before you submit

    # Uncomment the call to run_some_trials below to run
    # whatever trials you have setup in that function
    # IMPORTANT: comment out the run_some_trials() line below
    # before you submit your code
    # run_some_trials()

    # IMPORTANT: comment out the run_time_trials() line below
    # before you submit your code
    # run_time_trials()






###############################################################################
################# DO NOT MODIFY ANYTHING INSIDE THE BLOCK BELOW ###############
################## YOU MUST INCLUDE THIS CODE IN YOUR SUBMISSION ##############
###############################################################################
################# There is some code below this block you should read #########
###############################################################################

def fallback_guesses(possibles):
    """
    Returns all characters from a--z, and some punctuation that don't appear in
    `possibles`.
    """
    all_fallbacks = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
                    [' ', ',', '.', "'", '"', ';', '!', '?']
    return [x for x in all_fallbacks if x not in possibles]


def format_document(doc):
    """
    Re-formats `d` by collapsing all whitespace characters into a space and
    stripping all characters that aren't letters or punctuation.
    """
    from unicodedata import category
    # http://www.unicode.org/reports/tr44/#General_Category_Values
    allowed_types = ('Lu', 'Ll', 'Lo', 'Po', 'Zs')
    #d = unicode(d, 'utf-8')
    #d = str(d, 'utf-8')
    # Collapse whitespace
    doc = re.compile(r'\s+', re.UNICODE).sub(' ', doc)
    doc = u''.join([cat.lower()
                    for cat in doc if category(cat) in allowed_types])
    # Remove .encode() to properly process a unicode corpus
    return doc


def confirm(prompt):
    """
    Asks the user to confirm a yes/no question.
    Returns True/False based on their answer.
    """
    ans = ' '
    while ans[0] not in ('Y', 'y', 'n', 'N'):
        ans = input(prompt + ' (y/n) ')
    return True if ans[0] in ('Y', 'y') else False


def check_guess(next_char, guess):
    """
    Returns True if `guess` matches `next_char`, or asks the user if
    `next_char` is None.
    """
    if next_char is not None:
        return next_char == guess
    else:
        return confirm(" '{}'?".format(guess))


def next_guess(guesses):
    """ Returns the next guess """
    return guesses.pop(0) if len(guesses) else None


def check_guesses(next_char, guesses):
    """
    Runs through `guesses` to check against `next_char` (or asks the user if
    `next_char` is None).
    If a correct guess is found, (guess, count) is returned; otherwise
    (None, count) is returned. Where `count` is the number of guesses
    attempted.
    """
    guess = next_guess(guesses)
    guess_count = 1
    while guess is not None:
        if check_guess(next_char, guess):
            return (guess, guess_count)
        guess = next_guess(guesses)
        guess_count += 1
    # Wasn't able to find a guess
    return (None, guess_count)


def guess_next_char(phrase, progress, table, is_auto):
    """ Takes the full phrase, the progress string, the hash table
    and the is_auto flag and returns the next character once it has
    been guessed successfully. Also returns the number of guesses
    used in this guessing.
    """
    # Figure out what the next character to guess is
    # set it to None if not doing auto
    next_char = phrase[len(progress)].lower() if is_auto else None

    # Find possible guesses
    last_two_chars = progress[-2:].lower()
    guesses = table.fetch(last_two_chars)
    if guesses is None:
        guesses = []
    # Convert guesses into a list
    guesses = list(guesses)

    fallbacks = fallback_guesses(guesses)
    fallbacks = list(fallbacks)

    # Try to guess it from the table
    (guess, guess_count) = check_guesses(next_char, guesses)

    if guess is None:
        # If guessing from the corpus failed, try to guess from the
        # fallbacks
        print(' Exhausted all guesses from the corpus! Just guessing...')
        (guess, current_guess_count) = check_guesses(next_char, fallbacks)
        if guess is None:
            # If that failed, we're screwed!
            print(' Exhaused all fallbacks! Failed to guess phrase.')
            # Give up and exit the program
            sys.exit(1)
        guess_count += current_guess_count
    return guess, guess_count


def play_game(table, phrase, phrase_len=0):
    """
    Plays the game.
      `table` is the table mapping keys to lists of character frequencies.
      `phrase` is the phrase to match, or part of the phrase.
      `phrase_len` is the total length of the phrase or 0 for auto mode
    If `phrase_len` is zero, then the game is played automatically and
    the phrase is treated as the whole phrase. Otherwise the phrase is
    the start of the phrase and the function will ask the user whether
    or not it's guesses are correct - and keep going until phrase_len
    characters have been guessed correctly.

    Given phrase_len is 0 by default leaving out phrase_len from
    calls will auto-run, eg, play_game(table, 'eggs') will auto-run

    Returns the total number of guesses taken and the total time taken
    If in interactive mode the time taken value will be 0.
    """
    start = time.perf_counter()
    # Play the game automatically if phrase_len is 0
    is_auto = phrase_len == 0

    # Set phrase length to length of supplied phrase
    if is_auto:
        phrase_len = len(phrase)

    progress = phrase[0:2]
    gap_line = '_' * (phrase_len - len(progress))
    total_guesses = 0
    print('{}{}  (0)'.format(progress, gap_line))
    while len(progress) < phrase_len:
        guess, count = guess_next_char(phrase, progress, table, is_auto)
        progress += guess
        total_guesses += count
        # Print current progress and guess count for the last letter
        gap_line = '_' * (phrase_len - len(progress))
        print('{}{}  ({})'.format(progress, gap_line, count))
    end = time.perf_counter()
    #print('{}  ({})'.format(progress, count))
    print(' Solved it in {} guesses!'.format(total_guesses))

    # return zero time taken if in interactive mode
    time_taken = end - start if is_auto else 0

    return total_guesses, time_taken


def load_corpus_and_play(corpus_filename, phrase, length=0):
    """ Loads the corpus file and plays the game with the given setttings """
    with open(corpus_filename) as infile:
        print('Loading corpus... ' + corpus_filename)
        corpus = format_document(infile.read())
        print('Corpus loaded. ({} characters)'.format(len(corpus)))
        unique_chars = len(set(corpus))
        table = process_corpus(corpus, unique_chars)
        # print(table)
        _, time_taken = play_game(table, phrase, length)
        if length == 0:
            print('Took {:0.6f} seconds'.format(time_taken))


###############################################################################
#################### DO NOT MODIFY ANYTHING INSIDE THE BLOCK ABOVE ############
############ YOU MUST STILL INCLUDE THE BLOCK ABOVE IN YOUR SUBMISSION ########
###############################################################################



# IMPORTANT - Read all the comments below!!!
# ---------


def main():
    """ Put your calls to testing code here.
    The quiz server will not run this function.
    It will test other functions directly.
    NOTE: also comment out all your tests before submitting
    """
    test()


def random_string(size):
    """Remove me before submission, I might be helpful in for answering the
    short answer questions"""
    from random import randint
    return "".join(
            chr(ord('a') + randint(0, 25)) for _ in range(size)
            )


    # run this code if not being imported
if __name__ == '__main__':
    main()
    # IMPORTANT
    # Your submitted code should output nothing when you run it from Wing
    # Our tests will call functions themselves :)
