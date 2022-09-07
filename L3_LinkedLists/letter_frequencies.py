"""FrequencyList classes and testing routines.
Work through the lab handout to find out what you are doing..."""

import time
import re
from unicodedata import category
import doctest
import os

os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h


#-------------------------------------------------------------------------
class FreqNode(object):
    """Stores an item, frequency pair.

    Basically a FreqNode object is a node in the frequency list.
    Each FreqNode holds an item, the frequency for the item,
    and a pointer to the next FreqNode object (or None).

    >>> f = FreqNode('c', 2)
    >>> f.item
    'c'
    >>> f.frequency
    2
    >>> print(f)
    'c' = 2
    """

    def __init__(self, item, frequency=1):
        self.item = item
        self.frequency = frequency
        self.next_node = None

    def increment(self):
        """ Add one to the frequency count for this item """
        self.frequency += 1

    def __str__(self):
        return "'{}' = {}".format(self.item, self.frequency)


#-------------------------------------------------------------------------
class FreqList(object):
    """Stores a linked list of FreqNode objects.
    NOTE: This is a parent class for Unsorted, NicerUnSorted & Sorted FreqLists
    """

    def __init__(self):
        self.head = None
        self.freq_list_type = 'Generic parent'

    def add(self, item):
        """Will be implemented by child classes. Don't write anything here.
        There is will add an item with frequency=1 if item not in list,
        otherwise it will increment the frequency count for the item.
        """
        pass

    def get_item_frequency(self, item):
        """Returns Frequency of item, if found else returns 0.

        **** NOTE: Don't use this when writing your add methods. ****

        That is, you should scan through the list directly when adding.
        Using this method to check for existence of an item will be
        very inefficient... think about why.
        """
        current = self.head
        while current is not None:
            if current.item == item:
                return current.frequency
            current = current.next_node
        return 0

    def get_xy_for_plot(self):
        """ Returns two lists that can be used for plotting
        items and frequencies.
        The first contains the items and the second contains the frequecies.
        """
        x_values = []
        y_values = []
        curr_item = self.head
        while curr_item is not None:
            # use repr of items so that spaces show, eg, 'e '
            x_values.append(repr(curr_item.item))
            y_values.append(curr_item.frequency)
            curr_item = curr_item.next_node
        return x_values, y_values

    def _max_index_width(self):
        """
        Returns widest index width + 2
        For example, if there are 100 items in the list
        then 100 is the maximum item number and it is 3 characters wide,
        so set the width for the index column to 5
        """
        length = len(self)
        return len(str(length)) + 2

    def __len__(self):
        """Returns the number of nodes in the freq. list. Zero if empty."""
        current = self.head
        length = 0
        while current is not None:
            length += 1
            current = current.next_node
        return length

    def __str__(self):
        """Returns the items together with their letter frequencies."""
        result = self.freq_list_type + '\n'
        result += '-' * 35 + '\n'
        line_strs = []
        current_node = self.head
        max_index_width = self._max_index_width()
        node_num = 1
        while current_node is not None:
            line_str = '{:>{width}}:  {}'.format(node_num,
                                                 str(current_node),
                                                 width=max_index_width)
            line_strs.append(line_str)
            current_node = current_node.next_node
            node_num += 1
        return result + '\n'.join(line_strs)


#-------------------------------------------------------------------------
class UnsortedFreqList(FreqList):
    """FreqList that adds new items to the front/head of the linked list.
    UnsortedFreqList objects get to use the __len__  methods etc,
    of the FreqList class, because this class is inheriting from FreqList.
    This save you having to define them again.

    TO DO -------> All you need to do is write an add method
    """

    def __init__(self):
        FreqList.__init__(self)
        self.freq_list_type = 'Unsorted Frequency List'

    def add(self, new_item):
        """
        Updates the count for a given item/letter.
        If the given new_item is already in the list, the frequency for that
        item is incremented by 1.
        If not in the list then the item is put into a new node (with freq 1)
        and the node is inserted at the start of the frequency list.

        >>> f = UnsortedFreqList()
        >>> f.add('a')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'a' = 1
        >>> f.add('b')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'b' = 1
          2:  'a' = 1
        >>> f.add('a')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'b' = 1
          2:  'a' = 2
        >>> f.add('c')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'c' = 1
          2:  'b' = 1
          3:  'a' = 2
        """
        # ---start student section---
        pass
        # ===end student section===


#-------------------------------------------------------------------------
class NicerUnsortedFreqList(FreqList):
    """FreqList that adds new items at the end of the list"""

    def __init__(self):
        FreqList.__init__(self)
        self.freq_list_type = 'Nicer Unsorted Frequency List'

    def add(self, new_item):
        """
        If the given `letter` is already in the list, the frequency is
        incremented by 1.  If not in list, the item is added to the end of the
        list with a frequency of 1.

        >>> f = NicerUnsortedFreqList()
        >>> f.add('a')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 1
        >>> f.add('b')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 1
          2:  'b' = 1
        >>> f.add('a')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 2
          2:  'b' = 1
        >>> f.add('c')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 2
          2:  'b' = 1
          3:  'c' = 1
        """
        # ---start student section---
        pass
        # ===end student section===


#-------------------------------------------------------------------------
class SortedFreqList(FreqList):
    """FreqList that keeps items in order, sorted by their frequencies"""

    def __init__(self):
        FreqList.__init__(self)
        self.freq_list_type = 'Sorted Frequency List'

    def _insert_in_order(self, freq_node):
        """ Takes a FreqNode and inserts in to the list so that
        items are sorted from largest to smallest.
        NOTE: The list must contain something for this method to work.
        In general this method should only be called from the add method,
        see the add method docstring for information on how to use this method.
        ***** DON'T change this method *****
        """
        # so we don't have to lookup each time
        freq_of_item = freq_node.frequency

        # check to see if larger than first freq in list
        if freq_of_item > self.head.frequency:
            freq_node.next_node = self.head
            self.head = freq_node
        else:
            curr_freq = self.head
            inserted = False
            while curr_freq.next_node is not None and not inserted:
                if freq_of_item > curr_freq.next_node.frequency:
                    # insert here
                    freq_node.next_node = curr_freq.next_node
                    curr_freq.next_node = freq_node
                    inserted = True
                else:
                    curr_freq = curr_freq.next_node
            # got to end and didn't find
            if not inserted:
                freq_node.next_node = None  # as now at end of list
                curr_freq.next_node = freq_node

    def add(self, new_item):
        """
        If the list is empty then make a new FreqNode and insert it at head.
        If the new_item is not already in freq list then adds the given
        item with a frequency of 1 as a FreqNode object to the end of the list.

        If the given new item is already in the list,
           the frequency is incremented by 1.
           If needed (ie, the freq is now greater than the previous node),
             the node is removed and then inserted
             in to its sorted position - using _insert_in_order.

        >>> x = SortedFreqList()
        >>> x.add('t')
        >>> x.add('t')
        >>> print(x)
        Sorted Frequency List
        -----------------------------------
          1:  't' = 2
        >>> f = SortedFreqList()
        >>> f.add('a')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'a' = 1
        >>> f.add('b')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'a' = 1
          2:  'b' = 1
        >>> f.add('b')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 1
        >>> f.add('c')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 1
          3:  'c' = 1
        >>> f.add('a')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 2
          3:  'c' = 1
        >>> f.add('c')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 2
          3:  'c' = 2
        >>> f.add('c')
        >>> f.add('d')
        >>> f.add('d')
        >>> f.add('e')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'c' = 3
          2:  'b' = 2
          3:  'a' = 2
          4:  'd' = 2
          5:  'e' = 1
        >>> f.add('e')
        >>> f.add('e')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'c' = 3
          2:  'e' = 3
          3:  'b' = 2
          4:  'a' = 2
          5:  'd' = 2
        >>> f.add('c')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'c' = 4
          2:  'e' = 3
          3:  'b' = 2
          4:  'a' = 2
          5:  'd' = 2
        """
        # make sure you read the docstring for this method!
        # ---start student section---
        pass
        # ===end student section===

#-------------------------------------------------------------------------
# End of Class definitions
#=========================================================================


def time_freq_build(doc, freq_list_class, n_chars):
    """Calculate the letter frequencies using the supplied freq_list_class and
    document (in the form of a string called doc).
    Returns a freq_list and the time_taken in seconds.
    """
    # create a new freq_list instance of the given class
    freq_list = freq_list_class()
    if n_chars == 1:
        # do a simple scan for single characters
        start = time.perf_counter()
        for char in doc:
            freq_list.add(char)
        end = time.perf_counter()
    elif n_chars > 1:
        # do a scan for given multiples of characters
        start = time.perf_counter()
        for i in range(0, len(doc) - n_chars):
            chars = doc[i:i + n_chars]
            freq_list.add(chars)
        end = time.perf_counter()
    else:
        raise ValueError("Number of characters must be a positive integer")
    time_taken = end - start
    return freq_list, time_taken


def plot_freq_list(freq_list):
    """ Plots a bar chart showing item frequency.
    Will take any of the various freq_list classes, eg, unsorted, sorted etc
    """
    from matplotlib import pyplot
    (xvals, yvals) = freq_list.get_xy_for_plot()
    item_list_nums = list(range(len(xvals)))
    width = 0.8
    pyplot.bar(item_list_nums, yvals, width)
    pyplot.title("Frequency Distribution")
    pyplot.xlabel('Item')
    tick_positions = [i + width / 2 for i in item_list_nums]
    pyplot.xticks(tick_positions, xvals)
    pyplot.ylabel('Frequencies')
    pyplot.draw()
    pyplot.show()


def plot_truncated_freq_list(freq_list, n_items=26):
    """Plots a bar chart showing item frequency for the top n items.
    Will take any of the various freq_list classes, eg, unsorted, sorted etc
    """
    from matplotlib import pyplot
    (raw_x, raw_y) = freq_list.get_xy_for_plot()
    # only use the first n items
    xvals = raw_x[:n_items]
    yvals = raw_y[:n_items]

    # show with ' marks so spaces can be seen
    if len(xvals[0]) > 1:
        xvals = [repr(item) for item in xvals]

    item_list_nums = list(range(len(xvals)))
    width = 0.8
    pyplot.bar(item_list_nums, yvals, width)
    pyplot.title("Frequency Distribution (top " + str(n_items) + " items)")
    pyplot.xlabel('Item')
    tick_positions = [i + width / 2 for i in item_list_nums]
    pyplot.xticks(tick_positions, xvals)
    pyplot.ylabel('Frequencies')
    pyplot.draw()
    pyplot.show()


def print_test_header(filename, doc):
    """Does what it says."""
    print('\n' * 2)
    print('-' * 50)
    print('Tests for: ' + filename)
    print('Doc size:  {} chars'.format(len(doc)))
    print('-' * 50)




def run_a_test(doc, freq_class, n_chars, verbose=True):
    """Calls the freq_list builder for the given doc and n_chars.
    Times how long it takes and prints the time taken.
    If verbose == True then prints out the resulting freq list.
    """
    freq_list, total_time = time_freq_build(doc, freq_class, n_chars)
    n_items = len(freq_list)
    template = '   {} char(s) -> t = {:>.4f}s  ({} items)'
    print(template.format(n_chars, total_time, n_items))
    if verbose:
        print()
        print(freq_list)

    # use something like the following for showing graphs
    # you will need matplotlib installed...
    # plot_truncated_freq_list(freq_list, 10)
    # plot_freq_list(freq_list)



def run_tests(filename, verbose=True):
    """
    Runs sorted/unsorted * n char tests
    If verbose == True then prints out the resulting freq list.
    """
    # to save reloading the corpus for each test simply pre load and send
    # it off to be analysed
    with open(filename, 'r', encoding='utf-8') as infile:
        doc = format_document(infile.read())

    # feel free to print doc here to see what it looks like
    # maybe only for the smallest file:)
    # print(doc)

    print_test_header(filename, doc)
    run_settings = []

    # Uncomment lines for tests that you want to run
    # you can run one after the other if you like...
    run_settings.append((UnsortedFreqList, 1, verbose))
    # run_settings.append((NicerUnsortedFreqList, 1, verbose))
    # run_settings.append((SortedFreqList, 1, verbose))
    # run_settings.append((UnsortedFreqList, 2, verbose))
    # run_settings.append((NicerUnsortedFreqList, 2, verbose))
    # run_settings.append((SortedFreqList, 2, verbose))
    # run_settings.append((SortedFreqList, 3, verbose))

    for list_type, num_chars, verbose in run_settings:
        run_a_test(doc, list_type, num_chars, verbose)
    print('\n\n')
    # print('=' * 50)


##########################################################################
# DO NOT MODIFY ANYTHING in this area
#-------------------------------------------------------------------------
def format_document(input_doc):
    """ Re-formats `input_doc` by collapsing all whitespace characters into a
    space and stripping all characters that aren't letters or punctuation.
    Converts all uppercase characters in the file to lower case.
    """
    # Collapse whitespace
    reduced_doc = re.compile(r'\s+', re.UNICODE).sub(' ', input_doc)
    # http://www.unicode.org/reports/tr44/#General_Category_Values
    allowed_categories = ('Lu', 'Ll', 'Lo', 'Po', 'Zs')
    new_doc = ''.join([c.lower() for c in reduced_doc
                       if category(c) in allowed_categories])
    return new_doc
##########################################################################
##########################################################################


def main():
    """ The place to run doctests and other tests """
    # Uncomment doctests as needed...
    # If everything passes you just get a quick summary
    # otherwise failures will be printed.

    # Note: the doctests test your classes with some simple examples
    # To process txt files use the run_tests function.

    # change to False to get less doctest output
    with_verbose = True

    # Individual tests:
    # doctest.run_docstring_examples(UnsortedFreqList.add, None, verbose=with_verbose)
    # doctest.run_docstring_examples(NicerUnsortedFreqList.add, None, verbose=with_verbose)
    # doctest.run_docstring_examples(SortedFreqList.add, None, verbose=with_verbose)

    # run all the doctests  -- comment this out if you are running individual
    # tests
    result = doctest.testmod()
    if with_verbose:
        print(result)

    # Can enter an infinite loop if something isn't implemented correctly
    # So test on small data file first

    # **** Be sure to look at run_tests and run_a_test to see how the tests work! ****
    # Uncomment the files you want to test
    # ------------------------------------
    #run_tests("le_rire.txt", verbose=True)         # smallest corpus
    #run_tests("ulysses.txt", verbose=True)         # medium corpus
    #run_tests("war_and_peace.txt", verbose=True)   # one of the longest books in english
    #



if __name__ == '__main__':
    main()
