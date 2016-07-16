"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
from collections import defaultdict
import gzip
import math

import numpy as np


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector), rounded to 2 decimal places.
        See Log.txt for expected output.
        The order of operations is:
        1) initialize means
        2) Loop
          2a) compute_clusters
          2b) compute_means
          2c) print sizes and error
        """
        ###TODO
 
        #decalrations:
        self.vectorformeans = []
        self.clusters_list = defaultdict(list)
        #Final:
        maxvalue = self.k
        #intitialise means
        self.means_doclist = documents[0:maxvalue] #initialize
        #creating global document list
        self.doc_list = documents #reinitialise to global doclist of documents

        for i in self.means_doclist:
            result = 0
            for value in i:
                result = result + math.pow(i[value],2)
            self.vectorformeans.append(result)
            
        
        for i in range(0, iters):
            #create new clusters for every iteration
            self.clusters_list = defaultdict(list)
            #compute clusters
            result_list = self.compute_clusters(documents)
            #print the cluster list
            print(result_list)
            #compute means
            self.means_doclist = self.compute_means()
            #print error
            errorvalue = self.error(documents)
            print("%.2f" % errorvalue)

        self.clusters = defaultdict(list)
        self.compute_clusters(documents)

        pass

    def compute_means(self):
        """ Compute the mean vectors for each cluster (results stored in an
        instance variable of your choosing)."""
        ###TODO
       
        #decalartion
        self.vectorformeans = []

        for doc in self.means_doclist:
            resul = list(doc.values())
            self.vectorformeans.append(float(np.dot(resul, resul)))

        for key, val in self.clusters_list.items():
            result = Counter()
            for values_id, values_val in val:
                result.update(self.doc_list[values_id])
            for keys, value in result.items():
                result[keys] = float(value) / float(len(val))
            self.means_doclist[key] = result

        return self.means_doclist
        
        

        pass

    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable of your choosing). """
        ###TODO
        
        self.clusters_list=defaultdict(list) 
        idval = 0
        for doc in documents:
            for i in range(self.k):
                result = self.distance(doc,self.means_doclist[i],self.vectorformeans[i])
                if (i==0):
                    min_id =i
                    minimum_distance= result
                else:
                    if (result< minimum_distance):
                        min_id=i
                        minimum_distance= result
            self.clusters_list[min_id].append(idval)
            idval +=1
            
        return self.clusters_list
   
        pass

    def sqnorm(self, d):
        """ Return the vector length of a dictionary d, defined as the sum of
        the squared values in this dict. """
        ###TODO
        sum_calculated = 0
        for doclist in d.keys():
             sum_calculated = sum_calculated + math.pow(doclist[value],2)
        return sum_calculated
        pass

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        ###TODO
        
        meannorm = mean_norm

        valueslist = doc.values()
        prod_val = np.dot(list(valueslist),list(valueslist))
       
       
        res = 0.0
        for values in doc.keys():
            if values in mean:
                res =res + mean[values]*doc[values]
        value = meannorm + prod_val - 2.0 * res
        
        res = math.sqrt(value)
        
        return res
        pass

    def error(self, documents):
        """ Return the error of the current clustering, defined as the total
        Euclidean distance between each document and its assigned mean vector."""
        ###TODO
       
        result = 0.0
        self.mean_vector = []

        for doc in self.means_doclist:
            value = list(doc.values())
            self.vectorformeans.append(float(np.dot(value, value)))

        for key, values in self.clusters_list.items():
            for i, j in values:
                result += self.distance(documents[i], self.means_doclist[key], self.vectorformeans[key])
        return result
    
        pass

    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster. These are the
        documents that are the closest to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (sorted alphabetically).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        ###TODO
        
        for key,values in self.clusters_list.items():
            lsit = sorted(values, key=lambda x: x[1])
            print('CLUSTER ' + str(key))
            iter = 0
            if len(lsit) > n:
                iter = n
            else:
                iter = len(lsit)
            i = 0
            while i < iter:
                if len(self.documents[lsit[i][0]]) > 3:
                    print(' '.join(sorted([k for k in self.documents[lsit[i][0]]], key=lambda x: x)))
                else:
                    iter += 1
                i += 1

        pass


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    ###TODO
    counterlist = []
    totalcounterlist = []
    listvalues = []
    resultlist = []
    
    
    for docsval in docs:
        result = Counter(docsval.keys())
        counterlist = counterlist + [result]
    diclist = defaultdict(lambda:0)
    
    
    for value in counterlist:
        for item in value:
            count = len(value)
            diclist[item] = value[item]
            
    totalcounterlist = sum(counterlist, Counter()) 
    
    
    for keys,item in totalcounterlist.items():
        if(item >= min_df):
            listvalues.append(keys)
    listvalues = set(listvalues)
    diclist = defaultdict(lambda:0)
    
    
    for docsval in docs:
        for keys,valu in docsval.items():
            if keys in listvalues:
                diclist[keys] = valu
                resultlist = resultlist + [Counter(diclist)]
    return resultlist


    pass

def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with gzip.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles


def main():
    profiles = read_profiles('profiles.txt.gz')
    print('read', len(profiles), 'profiles.')
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
