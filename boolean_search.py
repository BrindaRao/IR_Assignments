""" Assignment 0

You will implement a simple in-memory boolean search engine over the jokes
from http://web.hawkesnest.net/~jthens/laffytaffy/.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Your search engine will only need to support AND queries. A multi-word query
is assumed to be an AND of the words. E.g., the query "why because" should be
processed as "why AND because."
"""
from collections import defaultdict
import re


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    Here is a doctest: 
    >>> tokenize("Hi  there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """
    """First convert the document to lowercase, find all the alphanumeric words,hence split on the non-alphanumeric words and store the         result to a local variable called result. And finally return the result
    """
    result = re.findall('\w+',document.lower())
    #print(result)
    return result
    ###TODO
    pass


def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    Params:
      tokens...A list of lists of strings
    Returns:
      An inverted index. This is a dict where keys are words and values are
      lists of document indices, sorted in increasing order.
    Below is an example, where the first document contains the tokens 'a' and
    'b', and the second document contains the tokens 'a' and 'c'.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    """
    """
    Create a default dictionary called list_of_indexes , which will return a new empty list as list is the parameter sent to the defaultdict. Using the enumerate function, we will find the index of the inner tokens looping through outer tokens as specified in the first and second for loops respectively. On finding, we will append the value of the outer index that is found on looping through the inner tokens. And finally,returning the result.
    """
    list_of_indexes = defaultdict(list)
    for i, token in enumerate(tokens):
        for inner_token in token:
            list_of_indexes[inner_token].append(i)
    return list_of_indexes
    ###TODO
    pass


def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text. Your implementation should be
    linear in the sizes of list1 and list2. That is, you should only loop once
    through each list.
    Params:
      list1....A list of document indices, sorted in ascending order.
      list2....Another list of document indices, sorted in ascending order.
    Returns:
      The list of document ids that appear in both lists, sorted in ascending order.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    """
    Followed the algorthim to intersect two posting lists"""
    intersection_list = []
    m = 0
    n = 0
    while(m < len(list1) and n < len(list2)): 
        if(list1[m]==list2[n]):
            intersection_list.append(list1[m])
            m = m + 1
            n = n + 1
        else:
            if(list1[m] < list2[n]):
                m = m + 1
            else:
                n = n + 1
    return intersection_list
   
        

def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index. You may use Python's builtin sorted method.
    Params:
      words....a list of strings.
      index....An inverted index; a dict mapping words to lists of document
      ids, sorted in ascending order.
    Returns:
      A list of words, sorted in ascending order by the number of document ids
      in the index.

    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    """ 
    Define a dictionary variable:length_list. Then on looping each of the words in the first parameter, found the length of the same with the help of the index as the word. And save the word and its corresponding length into the dict variable. Post that, use the sorted() function with the value to be arranged as the dict's value and not key. And display the result of the same.
    """
    length_list = {}
    for wordlist in words:
        countword = len(index[wordlist])
        length_list[wordlist] = countword
    length_list = sorted(length_list,key=length_list.__getitem__)
    #print(length_list)
    return length_list
    ###TODO
    pass


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that
    query is a single string, possibly containing multiple words. The steps
    are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.

    If a query term is not in the index, then an empty list should be returned.

    Params:
      index...An inverted index (dict mapping words to document ids)
      query...A string that may contain multiple search terms. We assume the
      query is the AND of those terms by default.

    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """
    """At first, query has been tokenized and then for each of these tokens, using the while loop find the interect of the first element with the rest of the elements. Using interesct solution and return the final_search value as the result for the search
    """
    
    final_search = []
    if(len(query) > 0):
        tokenised_data = tokenize(query)
        sorted_num_postings = sort_by_num_postings(tokenised_data,index)
        #print(sorted_num_postings)
        indice = 1
        #print(index[sorted_num_postings[0]])
        final_search = index[sorted_num_postings[0]]
        while indice < len(sorted_num_postings):
            # print(index[sorted_num_postings[indice]])
            final_search = intersect(final_search,index[sorted_num_postings[indice]])
            #print(final_search)
            indice+= 1
    return final_search
    ###TODO
    pass


def main():
    """ Main method. You should not modify this. """
    documents = open('documents.txt').readlines()
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = open('queries.txt').readlines()
    for query in queries:
        results = search(index, query)
        print('\n\nQUERY:%s\nRESULTS:\n%s' % (query, '\n'.join(documents[r] for r in results)))


if __name__ == '__main__':
    main()
