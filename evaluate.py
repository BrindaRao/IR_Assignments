""" Assignment 2
"""
import abc
from collections import defaultdict
import numpy as np


class EvaluatorFunction:
    """
    An Abstract Base Class for evaluating search results.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, hits, relevant):
        """
        Do not modify.
        Params:
          hits...A list of document ids returned by the search engine, sorted
                 in descending order of relevance.
          relevant...A list of document ids that are known to be
                     relevant. Order is insignificant.
        Returns:
          A float indicating the quality of the search results, higher is better.
        """
        return


class Precision(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute precision.

        >>> Precision().evaluate([1, 2, 3, 4], [2, 4])
        0.5
        """
        ###TODO
        set_hits = set(hits)
        set_relevan = set(relevant)
        final_list = list(set_hits.intersection(set_relevan))
        if(len(final_list) > 0):
            tp = len(final_list)
        else:
            tp = 0
        if(len(set_hits) > 0):
            fp = len(hits) - len(final_list)
        else:
            fp = 0
        if(tp >= 0 and fp >= 0):
            precision_val = tp/(tp+fp)
        else:
            precision_val = 0
        return precision_val
        pass

    def __repr__(self):
        return 'Precision'


class Recall(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute recall.

        >>> Recall().evaluate([1, 2, 3, 4], [2, 5])
        0.5
        """
        ###TODO
        total_kdocs = 10
        set_hits = set(hits)
        set_relevan = set(relevant)
        final_list = list(set_hits.intersection(set_relevan))
        if(len(final_list)> 0):
            tp = len(final_list)
        else:
            tp = 0
        if(len(hits) > 0):
            fn = len(set_relevan) - len(final_list)
        else:
            fn = 0
        if(tp > 0 and fn > 0):
            recall_val = tp/(tp+fn)
        else:
            recall_val = 0
        return recall_val
        pass

    def __repr__(self):
        return 'Recall'


class F1(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute F1.

        >>> F1().evaluate([1, 2, 3, 4], [2, 5])  # doctest:+ELLIPSIS
        0.333...
        """
        ###TODO
        #recall calculation
        recall_val = Recall().evaluate(hits,relevant)
        #precision calculation
        precision_val = Precision().evaluate(hits,relevant)
        #F1 Calculation
        if(precision_val > 0 and recall_val >0):
            f1_value = 2 * precision_val * recall_val / (precision_val + recall_val)
        else:
            f1_value = 0
        return f1_value
        pass

    def __repr__(self):
        return 'F1'


class MAP(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute Mean Average Precision.

        >>> MAP().evaluate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 4, 6, 11, 12, 13, 14, 15, 16, 17])
        0.2
        >>> MAP().evaluate([11, 1, 12, 4, 18], [1, 2, 3, 4, 5])
        0.2
        """
        ###TODO
        total_k_docs = len(relevant)
        set_hits = set(hits)
        set_relevan = set(relevant)
        hitslist = []
        maplist = defaultdict(lambda:0)
        mapvalue = 0
        for index in range(0,len(hits)):
            hitslist.append(hits[index])
            #precision calculation 
            precision_val = Precision().evaluate(hitslist,relevant)
            #recall calculation
            recall_val = Recall().evaluate(hitslist,relevant)
            listdata = []
            #lists of precisions and recall
            listdata.append([precision_val,recall_val])
            maplist[hits[index]] = listdata
        #MAP evaluation
        precisionlist = []
        recisionlst = []
        finallist = []
        for key,value in maplist.items():
            for item in maplist[key]:
                recisionlst.append(item[1])
                precisionlist.append(item[0])
        finallist.append(precisionlist[0])
        compare_val = recisionlst[0]
        for i in range(0,len(recisionlst)):
            if(compare_val < recisionlst[i] and compare_val != recisionlst[i]):
                compare_val = recisionlst[i]
                finallist.append(precisionlist[i])
        for i in range(0,len(finallist)):
            mapvalue = mapvalue + finallist[i]
        mapvalue = mapvalue/total_k_docs
        return mapvalue
        pass

    def __repr__(self):
        return 'MAP'

