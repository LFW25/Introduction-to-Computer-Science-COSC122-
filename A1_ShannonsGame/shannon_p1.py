"""
A simple program that plays Shannon's Game.
Students should enter their name and number below!

PLEASE READ THROUGH ALL THE COMMENTS FOR INSTRUCTIONS!

Author: Lily Williams, 42415299, lfw25
Date: 4/01/2021
"""
import doctest
import sys
import time
import re
from unicodedata import category


DEFAULT_CORPUS = 'corpus.txt'


class Frequency(object):
    """
    Stores a letter:frequency pair.

    >>> test = Frequency('c', 2)
    >>> test.letter
    'c'
    >>> test.frequency
    2
    >>> test
    Frequency('c', 2)
    """

    def __init__(self, letter, frequency):
        self.letter = letter
        self.frequency = frequency
        # The next Frequency object when stored as part of a linked list
        self.next_node = None

    def __repr__(self):
        # return '{%s: %d}' % (self.letter, self.frequency)
        return 'Frequency({}, {})'.format(repr(self.letter), repr(self.frequency))
        # return 'Frequency({}, {})'.format(self.letter, self.frequency)




class FrequencyList(object):
    """Stores a collection of Frequency objects as a linked list."""

    def __init__(self):
        """ Creates an empty FrequencyList """
        self.head = None

    def add(self, letter, frequency=1):
        """
        If the given `letter` is already in the list,
          the given frequency is added to its frequency.
        Otherwise adds the given letter:frequency combination as a Frequency object
        to the end of the list.

        YOU MUST write some more doctests for this method.

        >>> test = FrequencyList()
        >>> test.add('a', 3)
        >>> test
        Frequency List -> Frequency('a', 3) -> None
        >>> test.add('b', 2)
        >>> test
        Frequency List -> Frequency('a', 3) -> Frequency('b', 2) -> None
        >>> test.add('b', 1)
        >>> test
        Frequency List -> Frequency('a', 3) -> Frequency('b', 3) -> None
        >>> test.add('x')
        >>> test
        Frequency List -> Frequency('a', 3) -> Frequency('b', 3) -> Frequency('x', 1) -> None
        >>> test.add('x')
        >>> test.add('a', 2)
        >>> test
        Frequency List -> Frequency('a', 5) -> Frequency('b', 3) -> Frequency('x', 2) -> None
        """
        # ---start student section---
        if self.find(letter) is not None:               # Is the item in the list?
            node_index = self.find(letter)                  # Find the node pertaining to the item
            node_index.frequency += frequency               # Increase the frequency by the given value or 1 (default)
        else:                                           # Item is not in the list
            current = self.head
            if self.head is None:                       # If the list is empty
                new_node = Frequency(letter, frequency) # Make the new node
                self.head = new_node                    # at the head of the list
            else:                                       # Otherwise
                while current.next_node is not None:            # Find the end of the list
                    current = current.next_node             
            
                new_node = Frequency(letter, frequency)         # Initialise a new node for the letter
                current.next_node = new_node                    # Make the end of the list point to the new node
        # ===end student section===

    def remove(self, letter):
        """
        Removes the Frequency object with the given `letter` from the list.
        Does nothing if `letter` is not in the list.

        NOTE: YOU MUST write some doctests for the remove method here!
        >>> f = FrequencyList()
        >>> f.add('a', 3)
        >>> f.add('b', 2)
        >>> f.add('c', 3)
        >>> f
        Frequency List -> Frequency('a', 3) -> Frequency('b', 2) -> Frequency('c', 3) -> None
        >>> f.remove('a')
        >>> f
        Frequency List -> Frequency('b', 2) -> Frequency('c', 3) -> None
        >>> f.remove('c')
        >>> f
        Frequency List -> Frequency('b', 2) -> None
        """
        # ---start student section---
        if self.find(letter) is not None:             # Is the item in the list (it should be)
            if self.head.letter == letter:              # If the item is the head of the list
                current = self.head                     
                self.head = current.next_node           # assign the head to point to the second item in the list
                current.next_node = None                # and remove the redundant link
            else:                                     # otherwise, when the item is not the head
                current = self.head
                previous = self.head
                while current.letter != letter and current.next_node != None:           # Find the item in the linked list ('and' statement is a safety net)
                    previous = current
                    current = current.next_node
            
                previous.next_node = current.next_node   # Change the pointers to skip over the desired node, removing it
                current.next_node = None                 # and remove the redundant link
        # ===end student section===

    def find(self, letter):
        """
        Returns the Frequency object for the given `letter` in the list, or
        None if the `letter` doesn't appear in the list.

        YOU MUST write more doctests for this method!

        >>> f = FrequencyList()
        >>> f.add('a', 3)
        >>> f.find('a')
        Frequency('a', 3)
        >>> f.find('b')
        
        >>> f.add('x', 2)
        >>> f
        Frequency List -> Frequency('a', 3) -> Frequency('x', 2) -> None
        >>> f.find('x')
        Frequency('x', 2)
        >>> f.remove('x')
        >>> f.find('x')
        
        """
        # ---start student section---
        current = self.head
        found =  False
        while current is not None and found == False:          # As long as current isn't pointing to the end of the list, cycle through each node
            if current.letter == letter:      # until a match is found.
                found = True                # Mark as true to break the while loop
                return current              # and return the matching node
            else:  
                current = current.next_node
        if current is None and found == False:                 # If the end of the list has been reached and match is not found
            return None                     # return None, as the item is not in the list
        # ===end student section===

    def __contains__(self, item):
        """ Returns True if item is in this FrequencyList
        Remember self.find(item) will return the index of the item
        if the item is in the list otherwise it returns None.

        >>> f = FrequencyList()
        >>> f.add('a', 3)
        >>> 'a' in f
        True
        >>> 'b' in f
        False

        """
        return self.find(item) is not None

    def __len__(self):
        """ Returns the length of the FrequncyList, zero if empty
        YOU MUST write some more doctests here.
        >>> f = FrequencyList()
        >>> f.add('a', 3)
        >>> len(f)
        1
        >>> f.add('b', 1)
        >>> len(f)
        2
        >>> f.add('c', 1)
        >>> len(f)
        3
        >>> f.remove('b')
        >>> len(f)
        2
        >>> f.add('d', 4)
        >>> f.add('e', 2)
        >>> len(f)
        4
        >>> f.remove('a')
        >>> f.remove('c')
        >>> f.remove('d')
        >>> f.remove('e')
        >>> len(f)
        0
        """
        # ---start student section---
        length = 0                          # Initial length is 0
        current = self.head
        while current is not None:          # Until you reach the end of the list
            length += 1                     # For each node, add one to the length
            current = current.next_node
        return length                       # Once the end is reached, return the length
        # ===end student section===

    def __repr__(self):
        """ Returns a string representation of the list in the form
        Frequency List -> Frequency('a', 2) -> Frequency('b', 10) ... -> None
        """
        current = self.head
        result = 'Frequency List -> '
        while current is not None:
            result += repr(current) + ' -> '
            current = current.next_node
        result += 'None'
        return result





def filter_possible_chars(corpus, last):
    """
    Returns a Python list of all instances of single characters in 'corpus' that
    immediately follow 'last' (including duplicates). The characters should be
    in that same order as they appear in the corpus

    The 'corpus' and 'last' should be all lowercase characters.

    Duplicates are included - see the doctests below.

    YOU MUST write more doctests!

    >>> filter_possible_chars('lazy languid line', 'la')
    ['z', 'n']
    >>> filter_possible_chars('pitter patter batton', 'tt')
    ['e', 'e', 'o']
    >>> filter_possible_chars('pitter pattor batt', 'tt')
    ['e', 'o']
    >>> filter_possible_chars('pitter pattor batt', 'er')
    [' ']
    """
    # ---start student section---
    match_list = []                     # Initialises an empty list
    for i in range(len(corpus) - 1):        # Cycle through the corpus until the second to last letter (to prevent an index error)
        if corpus[i] + corpus[i+1] == last and i+1 != len(corpus) - 1:      # if the current and next letters together are equal to the target AND they're not the final letters in the corpus
            match_list.append(corpus[i+2])                              # add the following letter to the match list
    return match_list                   # returns the completed list
    # ===end student section===


def count_frequencies(items):
    """
    Counts the frequencies of each element in `items` and returns a
    FrequencyList of Frequency objects containing the element and frequency.
    The items in the returned LinkedList should be in the same order as they appear in the 
    items list (they don't need to be sorted by frequency).

    NOTE: You will need to write some more doctests here!

    >>> count_frequencies(['e', 'e', 'o'])
    Frequency List -> Frequency('e', 2) -> Frequency('o', 1) -> None
    >>> count_frequencies(['j', 'i', 'k', 'k', 'k', 'i'])
    Frequency List -> Frequency('j', 1) -> Frequency('i', 2) -> Frequency('k', 3) -> None
    >>> freqs = count_frequencies(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'c', 'b'])
    >>> # Print in order
    >>> current = freqs.head
    >>> while current is not None:
    ...    print(current)
    ...    current = current.next_node
    Frequency('a', 1)
    Frequency('b', 2)
    Frequency('c', 2)
    Frequency('d', 1)
    Frequency('e', 1)
    Frequency('f', 1)
    Frequency('g', 1)
    
    >>> count_frequencies("just one, i'm a few, no family too, who am i?")
    Frequency List -> Frequency('j', 1) -> Frequency('u', 1) -> Frequency('s', 1) -> Frequency('t', 2) -> Frequency(' ', 10) -> Frequency('o', 5) -> Frequency('n', 2) -> Frequency('e', 2) -> Frequency(',', 3) -> Frequency('i', 3) -> Frequency("'", 1) -> Frequency('m', 3) -> Frequency('a', 3) -> Frequency('f', 2) -> Frequency('w', 2) -> Frequency('l', 1) -> Frequency('y', 1) -> Frequency('h', 1) -> Frequency('?', 1) -> None
    >>> count_frequencies("After time adrift among open stars / Among tides of light and to shoals of dust / I will return to where I began.")
    Frequency List -> Frequency('A', 2) -> Frequency('f', 4) -> Frequency('t', 10) -> Frequency('e', 8) -> Frequency('r', 6) -> Frequency(' ', 23) -> Frequency('i', 5) -> Frequency('m', 3) -> Frequency('a', 6) -> Frequency('d', 4) -> Frequency('o', 8) -> Frequency('n', 6) -> Frequency('g', 4) -> Frequency('p', 1) -> Frequency('s', 6) -> Frequency('/', 2) -> Frequency('l', 4) -> Frequency('h', 3) -> Frequency('u', 2) -> Frequency('I', 2) -> Frequency('w', 2) -> Frequency('b', 1) -> Frequency('.', 1) -> None
    """
    # ---start student section---
    count_list = FrequencyList()        # Initialise an empty linked list
    for character in items:             # For each letter in the given string or list
        count_list.add(character)       # Use the FrequencyList add method to add it to the list
    return count_list                   # Return the linked list at the end
    # ===end student section===
    
def select_next_guess(possibles):
    """
    Removes and returns the letter with the highest frequency from the
    'possibles' FrequencyList.
    If more than one letter has the highest frequency then the first
    letter in the list with that frequency is returned.
    Returns None if there are no more guesses.

    YOU MUST write some more doctests!

    >>> p = FrequencyList()
    >>> p.add('a', 2)
    >>> p.add('b', 4)
    >>> p.add('c', 1)
    >>> p.add('d', 4)
    >>> p
    Frequency List -> Frequency('a', 2) -> Frequency('b', 4) -> Frequency('c', 1) -> Frequency('d', 4) -> None
    >>> select_next_guess(p)
    'b'
    >>> p
    Frequency List -> Frequency('a', 2) -> Frequency('c', 1) -> Frequency('d', 4) -> None
    >>> p.add('z', 54)
    >>> p
    Frequency List -> Frequency('a', 2) -> Frequency('c', 1) -> Frequency('d', 4) -> Frequency('z', 54) -> None
    >>> select_next_guess(p)
    'z'
    >>> selext_next_guess(p)
    'd'
    >>> p
    Frequency List -> Frequency('a', 2) -> Frequency('c', 1) -> None
    """
    # ---start student section---
    if possibles.head is None:                                          # If the given list is empty
        return None                                                     # return None.
    else:                                                               # Otherwise
        current_highest = possibles.head                                # make the head item the initial highest frequency
        current_node = possibles.head
        while current_node is not None:                                 # and cycle through the list
            if current_node.frequency > current_highest.frequency:      # comparing the highest frequency with the current item's frequency
                current_highest = current_node                          # and taking the higher frequency
            else:                                                       # or moving on if the current item is lower
                current_node = current_node.next_node
        possibles.remove(current_highest.letter)                        # Once the list has been checked, remove the highest frequency item from the list
        return current_highest.letter                                   # and return it
    
    # ===end student section===




###############################################################################
#################### DO NOT MODIFY ANYTHING INSIDE THE BLOCK BELOW ############
################# There is some code below this block you should read #########
###############################################################################

def fallback_guesses(possibles):
    """
    Returns all characters from a--z, and some punctuation that don't appear in
    `possibles`.
    """
    all_fallbacks = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
                    [' ', ',', '.', "'", '"', ';', '?', '!']
    fallbacks = [x for x in all_fallbacks if x not in possibles]
    return fallbacks


def format_document(doc):
    """
    Re-formats `doc` by collapsing all whitespace characters into a space and
    stripping all characters that aren't letters or punctuation.
    """
    # http://www.unicode.org/reports/tr44/#General_Category_Values
    allowed_categories = ('Lu', 'Ll', 'Lo', 'Po', 'Zs')
    # d = unicode(d, 'utf-8')
    # d = str(d, 'utf-8')
    # Collapse whitespace
    doc = re.compile(r'\s+', re.UNICODE).sub(' ', doc)
    doc = u''.join([c.lower() for c in doc if category(c) in allowed_categories])
    # Disable the encode to properly process a unicode corpus
    return doc


def confirm(prompt):
    """
    Asks the user to confirm a yes/no question.
    Returns True/False based on their answer.
    """
    answer = ' '
    while len(answer) == 0 or answer[0].lower() not in ('y', 'n'):
        answer = input(prompt + ' (y/n) ')
    return answer[0].lower() == 'y'


def check_guess(next_char, guess):
    """
    Returns True if `guess` matches `next_char`, or asks the user if
    `next_char` is None.
    """
    if next_char is not None:
        return next_char == guess
    else:
        return confirm(" '{}'?".format(guess))


def check_guesses(next_char, guesses):
    """
    Runs through `guesses` to check against `next_char` (or asks the user if
    `next_char` is None).
    If a correct guess is found, (guess, count) is returned; otherwise
    (None, count) is returned. Where `count` is the number of guesses
    attempted.
    """
    guess = select_next_guess(guesses)
    guess_count = 0
    while guess is not None:
        guess_count += 1
        if check_guess(next_char, guess):
            return guess, guess_count
        guess = select_next_guess(guesses)
    # Wasn't able to find a guess
    return None, guess_count


def check_fallback_guesses(next_char, guesses):
    """
    Runs through 'guesses' to check against 'next_char' (or asks the user if
    'next_char' is None).
    If a correct guess is found, (guess, count) is returned; otherwise
    (None, count) is returned. Where 'count' is the number of guesses
    attempted.
    """
    guess_count = 0
    for guess in guesses:
        guess_count += 1
        if check_guess(next_char, guess):
            return guess, guess_count

    # If that failed, we're screwed!
    print('Exhaused all fallbacks! Failed to guess phrase.')
    sys.exit(1)


def get_guesses_list(corpus, progress):
    """ Returns the frequency list of guesses
    Guesses should appear in the same order in the input file
    """
    pair = progress[-2:]  #.lower()
    possibles = filter_possible_chars(corpus, pair)
    if possibles is None:
        sys.stderr.write('filter_possible_chars has not been ' +
                         'implemented!\n')
        sys.exit(1)

    guesses = count_frequencies(possibles)
    if guesses is None:
        sys.stderr.write('count_frequencies has not been implemented!\n')
        sys.exit(1)
    return guesses


def find_next_char(corpus, phrase, progress, is_auto):
    """ Keeps guessing until the right character is chosen.
    With crash and burn if can't guess it.
    """
    guesses = get_guesses_list(corpus, progress)
    fallbacks = fallback_guesses(guesses)
    # Figure out what the next character to guess is
    next_char = phrase[len(progress)].lower() if is_auto else None
    # Try to guess it from the corpus
    (guess, char_guess_count) = check_guesses(next_char, guesses)
    # If guessing from the corpus failed, try guessing from the fallbacks
    if guess is None:
        print('Exhausted all guesses from the corpus! Just guessing...')
        (guess, fb_count) = check_fallback_guesses(next_char, fallbacks)
        char_guess_count += fb_count
    return guess, char_guess_count


def play_game(corpus, phrase, phrase_len=0):
    """
    Plays the game.
      'corpus' is the complete corpus to use for finding guesses.
      'phrase' is the phrase to match, or part of the phrase.
      'phrase_len' is the total length of the phrase or 0 for auto mode
    If 'phrase_len' is zero, then the game is played automatically and
    the phrase is treated as the whole phrase. Otherwise the phrase is
    the start of the phrase and the function will ask the user whether
    or not it's guesses are correct - and keep going until phrase_len
    characters have been guessed correctly.

    Given phrase_len is 0 by default leaving out phrase_len from
    calls will auto-run, eg, play_game(corpus, 'eggs') will auto-run

    Returns the total number of guesses taken and the total time taken
    If in interactive mode the time taken value will be 0.
    """
    is_auto = phrase_len == 0
    if is_auto:
        phrase_len = len(phrase)
    progress = phrase[0:2]
    total_guesses = 0

    start = time.perf_counter()
    gap_line = '_' * (phrase_len - len(progress))
    print('{}{}  (0)'.format(progress, gap_line))
    while len(progress) != phrase_len:
        next_char, guesses = find_next_char(corpus, phrase, progress, is_auto)
        total_guesses += guesses
        progress += next_char
        gap_line = '_' * (phrase_len - len(progress))
        print('{}{}  ({})'.format(progress, gap_line, guesses))
    end = time.perf_counter()

    print(' Solved it in {} guesses!'.format(total_guesses))
    # return zero if in interactive mode
    time_taken = end - start if is_auto else 0
    return total_guesses, time_taken


def load_corpus_and_play(corpus_filename, phrase, length=0):
    """ Loads the corpus file and plays the game with the given setttings
    >>> filename = 'the-yellow-wall-paper.txt'
    >>> phrase = 'document test phrase'
    >>> load_corpus_and_play(filename, phrase)  # doctest: +ELLIPSIS
    Loading corpus... the-yellow-wall-paper.txt
    Corpus loaded. (49812 characters)
    do__________________  (0)
    doc_________________  (10)
    Exhausted all guesses from the corpus! Just guessing...
    docu________________  (21)
    Exhausted all guesses from the corpus! Just guessing...
    docum_______________  (18)
    docume______________  (3)
    documen_____________  (2)
    document____________  (3)
    document ___________  (1)
    document t__________  (2)
    document te_________  (4)
    document tes________  (5)
    document test_______  (3)
    document test ______  (1)
    document test p_____  (15)
    document test ph____  (7)
    document test phr___  (3)
    document test phra__  (3)
    document test phras_  (12)
    document test phrase  (2)
     Solved it in 115 guesses!
    ...
    """
    with open(corpus_filename, encoding='utf-8') as infile:
        print('Loading corpus... ' + corpus_filename)
        corpus = format_document(infile.read())
        print('Corpus loaded. ({} characters)'.format(len(corpus)))
        _, time_taken = play_game(corpus, phrase, length)
        if length == 0:
            print('Took {:0.6f} seconds'.format(time_taken))


###############################################################################
#################### DO NOT MODIFY ANYTHING INSIDE THE BLOCK ABOVE ############
###############################################################################




################### Your Testing Code Goes in here ############################

def run_time_trials():
    """ A good place to write code for time trials.
    We have given you some example code to get you started.
    Make sure you use this docstring to explain your code and that
    you write comments in your code to help explain the process.
    """
    corpus_filename = 'war-and-peace.txt'  # try others if you want
    with open(corpus_filename, encoding='utf-8') as infile:
        print('Loading corpus ... ' + corpus_filename)
        full_corpus = format_document(infile.read())
    results = []
    phrase = 'your test phrase should go here'
    # we go up to 50000 in steps of 2000 for a start
    # you may want to go all the way to the lenght of the corpus
    # to see what happens.
    for size in range(1000, 50000, 2000):
        slice_of_corpus = full_corpus[0:size]  # then try [0:2000] etc
        num_guesses, time_taken = play_game(slice_of_corpus, phrase)  # play with autorun
        print('With corpus size {:4} time taken = {}'.format(size, time_taken))
        results.append((size, num_guesses, time_taken))
    print('{:>6}  {:^12} {:^10}'.format('size', 'num_guesses', 'time_taken'))
    for size, num_guesses, time_taken in results:
        print('{:6}  {:^12}  {:^10.4f}'.format(size, num_guesses, time_taken))

    # As the corpus size increases the number of guesses generally falls
    # but why does the time increase?



def run_some_trials():
    """ Play some games with various test phrases and settings """
    # play game using whatever you like
    # maybe put an input statement here
    # so you can enter the corpus
    # and settings
    # or just run various games with various settings

    # MAKE SURE you test with various phrases!
    test_phrases = ["is it weird to have  two spaces in here?",
                    'dead war',
                    # 'Extreme emotional experiment',
                    ]
    test_files = [DEFAULT_CORPUS,
                  # Some other file names
                  # 'the-yellow-wall-paper.txt',
                  # 'hamlet.txt',
                  # 'le-rire.txt',
                  # 'war-of-the-worlds.txt',
                  # 'ulysses.txt',
                  # 'war-and-peace.txt'
                  ]

    #Uncomment the block below to run trials based on the lists of phrases and files above
    for test_phrase in test_phrases:
        for corpus_filename in test_files:
            phrase_length = 0  # for auto-run
            load_corpus_and_play(corpus_filename, test_phrase, phrase_length)
            print('\n' * 3)
    # check out https://www.gutenberg.org/ for more free books!



def test():
    """ Runs doctests and other trials"""

    # Doctests
    # -----------------
    # Uncomment various doctest runs to check each method/function
    # MAKE sure your submitted code doesn't run tests - we will do this.
    # MAKE SURE you add some doctests of your own to the docstrings

    # doctest.run_docstring_examples(Frequency, globs=None)
    # doctest.run_docstring_examples(FrequencyList.add, globs = None)
    # doctest.run_docstring_examples(FrequencyList.remove, globs = None)
    # doctest.run_docstring_examples(FrequencyList.find, globs = None)

    # doctest.run_docstring_examples(filter_possible_chars, globs = None)
    # doctest.run_docstring_examples(count_frequencies, globs = None)
    # doctest.run_docstring_examples(select_next_guess, globs = None)


    # Uncomment the line below to run all doctests - this is helpful before you submit
    # doctest.testmod()


    # Running trials
    # -----------------
    # Uncomment the call to run_some_trials below to run
    # whatever trials you have setup in that function
    # IMPORTANT: comment out the run_some_trials() line below
    # before you submit your code
    # run_some_trials()

    # Time trials
    # -----------------
    # Running time trials will give you a feel for how the speed
    # is affected by the corpus size
    # run_time_trials()

    # interactive trial
    # -----------------
    # see how long the program takes to guess 'bat man'
    # it will get the first two characters and start asking you
    # if it has the third character correct etc...
    #load_corpus_and_play('test_file.txt', 'Big boy')
    #load_corpus_and_play('le-rire.txt', 'ba', 7)
    

################# End of Testing Code ########################################





def main():
    """ Put your calls to testing code here.
    The quiz server will not run this function.
    It will test directly
    """
    test()


# run this code if not being imported
if __name__ == '__main__':
    main()
    # don't add any code here
