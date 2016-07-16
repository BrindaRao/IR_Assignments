""" Assignment 2
"""
import abc
from collections import defaultdict
import math

import index


def idf(term, index):
    """ Compute the inverse document frequency of a term according to the
    index. IDF(T) = log10(N / df_t), where N is the total number of documents
    in the index and df_t is the total number of documents that contain term
    t.

    Params:
      terms....A string representing a term.
      index....A Index object.
    Returns:
      The idf value.

    >>> idx = index.Index(['a b c a', 'c d e', 'c e f'])
    >>> idf('a', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('d', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('e', idx) # doctest:+ELLIPSIS
    0.176...
    """
    ###TODO
    total_doc_length = len(index.documents)
    dft = index.doc_freqs[term]
    idf = math.log((total_doc_length/dft),10)
    return idf
    pass


class ScoringFunction:
    """ An Abstract Base Class for ranking documents by relevance to a
    query. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def score(self, query_vector, index):
        """
        Do not modify.

        Params:
          query_vector...dict mapping query term to weight.
          index..........Index object.
        """
        return


class RSV(ScoringFunction):
    """
    See lecture notes for definition of RSV.

    idf(a) = log10(3/1)
    idf(d) = log10(3/1)
    idf(e) = log10(3/2)
    >>> idx = index.Index(['a b c', 'c d e', 'c e f'])
    >>> rsv = RSV()
    >>> rsv.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.4771...
    """

    def score(self, query_vector, index):
        ###TODO
        #Find no of documents
        total_doc_length = len(index.documents)
        totalidf = 0
        rsvdict = defaultdict(lambda:0)
        for i in range(1,len(index.documents)):
            totalidf = 0
            for key in query_vector:
                #totalidf = 0
                if key in index.documents[i]:
                    idfval = math.log((total_doc_length/index.doc_freqs[key]),10)
                    totalidf += idfval
            rsvdict[i] = totalidf
                #else:
                    #rsvdict[i+1]= totalidf
        return dict(rsvdict)
        pass

    def __repr__(self):
        return 'RSV'


class BM25(ScoringFunction):
    """
    See lecture notes for definition of BM25.

    log10(3) * (2*2) / (1(.5 + .5(4/3.333)) + 2) = log10(3) * 4 / 3.1 = .6156...
    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> bm = BM25(k=1, b=.5)
    >>> bm.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.61564032...
    """
    def __init__(self, k=1, b=.5):
        self.k = k
        self.b = b

    def score(self, query_vector, index):
        ###TODO
        bm25dict = defaultdict(lambda:0)
        totalVal = 0
        for i in range(1,len(index.documents)):
            totalVal = 0
            for key in query_vector:
                #totalVal = 0
                if key in index.documents[i]:
                    idfcal = idf(key,index)
                    tfindex = index.documents[i].count(key)
                    calulatedVal = idfcal * ((self.k + 1) * tfindex) / (self.k * ((1-self.b) + self.b * len(index.documents[i])/index.mean_doc_length) + tfindex)
                    totalVal = totalVal + calulatedVal
            bm25dict[i] = totalVal
                #else:
                    #bm25dict[i+1] = 0
        return dict(bm25dict)
        pass

    def __repr__(self):
        return 'BM25 k=%d b=%.2f' % (self.k, self.b)


class Cosine(ScoringFunction):
    """
    See lecture notes for definition of Cosine similarity.  Be sure to use the
    precomputed document norms (in index), rather than recomputing them for
    each query.

    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> cos = Cosine()
    >>> cos.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.792857...
    """
    def score(self, query_vector, index):
        ###TODO
        cosinedict = defaultdict(lambda:0)
        for i in range(1,len(index.documents)):
            tfidfprod = 0
            norms = 1.0
            for key in query_vector:
                #tfidfprod = 0
                #norms = 1.0
                if key in index.documents[i]:
                    #document frequency
                    docfreq = index.doc_freqs[key]
                    #term frequency
                    termfrequency = index.documents[i].count(key)
                    #tfidf vector
                    #print('Valueofi is %s' % i)
                    t1 = 1 + math.log(termfrequency,10)
                    #print(t1)
                    t2 = math.log(len(index.documents)/docfreq,10)
                    #print(t2)
                    tfidf = t1 * t2
                    #print(tfidf)
                    tfidfprod += tfidf * query_vector[key]
                    norms = index.doc_norms[i+1]
            cosineprd = tfidfprod/norms
            cosinedict[i] = cosineprd
        #print (dict(cosinedict).keys())    
        return dict(cosinedict)
        pass

    def __repr__(self):
        return 'Cosine'
