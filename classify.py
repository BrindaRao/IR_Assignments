"""
Assignment 3. Implement a Multinomial Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

from collections import defaultdict
import glob
import math
import os
import collections


class Document(object):
    """ A Document. Do not modify.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename=None, label=None, tokens=None):
        """ Initialize a document either from a file, in which case the label
        comes from the file name, or from specified label and tokens, but not
        both.
        """
        if label: # specify from label/tokens, for testing.
            self.label = label
            self.tokens = tokens
        else: # specify from file.
            self.filename = filename
            self.label = 'spam' if 'spmsg' in filename else 'ham'
            self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):

    def get_word_probability(self, label, term):
        """
        Return Pr(term|label). This is only valid after .train has been called.

        Params:
          label: class label.
          term: the term
        Returns:
          A float representing the probability of this term for the specified class.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_word_probability('spam', 'a')
        0.25
        >>> nb.get_word_probability('spam', 'b')
        0.375
        """
        ###TODO
        """print('Has lable value %s' % label)
        print('Has term value %s' % term)
        print('Doc count %s' % self.docCount)
        print('Vocab = %s' % self.Vocab)
        print('Label count = %s' % self.label_count)
        #print(self.prior)
        print(self.count_tokens_spamm)
        print(self.count_tokens_hamm)"""
        if label == 'spam':
            if term in self.count_tokens_spamm:
                numerator = self.count_tokens_spamm[term] + 1
                denominator = len(self.unique_vocab) + self.length_spam
                wordprobability = numerator/denominator
        else:
            if term in self.count_tokens_hamm:
                numerator = self.count_tokens_hamm[term] + 1
                denominator = len(self.unique_vocab) + self.length_ham
                wordprobability = numerator/denominator
        return wordprobability
        pass

    def get_top_words(self, label, n):
        """ Return the top n words for the specified class, using the odds ratio.
        The score for term t in class c is: p(t|c) / p(t|c'), where c'!=c.

        Params:
          labels...Class label.
          n........Number of values to return.
        Returns:
          A list of (float, string) tuples, where each float is the odds ratio
          defined above, and the string is the corresponding term.  This list
          should be sorted in descending order of odds ratio.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_top_words('spam', 2)
        [(2.25, 'b'), (1.5, 'a')]
        """
        ###TODO
        oddsration = []
        result = []
        condprop_spam = defaultdict(lambda:0)
        condprop_ham = defaultdict(lambda:0)
        #print(self.unique_vocab)
        #finding the condtional probabilities
        for word in self.unique_vocab:
            condprop_spam[word] = float(self.count_tokens_spamm[word] + 1) / float (self.length_spam + len(self.unique_vocab))
            condprop_ham[word] = float(self.count_tokens_hamm[word] + 1) / float (self.length_ham + len(self.unique_vocab))
        #print(condprop_spam)
        #print(condprop_ham)
        if label == 'spam':
            for word in  self.unique_vocab:
                ratio = condprop_spam[word]/condprop_ham[word]
                value = (ratio,word)
                result.append(value)
        if label == 'ham':
            for word in  self.unique_vocab:
                ratio = condprop_ham[word]/condprop_spam[word]
                value = (ratio,word)
                result.append(value)
        result = sorted(result, key=lambda tup: tup[0],reverse = True)
        #print(result)
        oddsration = result[:n]
        return oddsration
        pass

    def train(self, documents):
        """
        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your
        book. Store these as instance variables, to be used by the classify
        method subsequently.
        Params:
          documents...A list of training Documents.
        Returns:
          Nothing.
        """
        ###TODO
        V = []
        unique_vocab = []
        self.Vocab = []
        countdocs = len(documents)
        self.docCount = countdocs
        self.label_count = defaultdict(int)
        self.prior = defaultdict(float)
        concat_spam = []
        concat_ham = []
        self.length_spam = 0
        self.length_ham = 0
        for fname in documents:
            self.label_count[fname.label] += 1
            if fname.label == "spam":
                for doc in fname.tokens:
                    concat_spam.append(doc)
            elif fname.label == "ham":
                for doc in fname.tokens:
                    concat_ham.append(doc)
            for doc in fname.tokens:
                V.append(doc)
        self.Vocab = V
        self.unique_vocab = list(set(V))
        #self.length_document = len(document)
        for label in self.label_count:
            self.prior[label] = float(self.label_count[label]) / countdocs
  
        self.cond_prob_spam = defaultdict(lambda:0)
        self.cond_prob_ham = defaultdict(lambda:0)
        self.spam_cnd = defaultdict(lambda:0)
        self.ham_cnd = defaultdict(lambda:0)
        count_tokens_spam = collections.Counter(concat_spam)
        count_tokens_ham = collections.Counter(concat_ham)
        self.count_tokens_spamm = count_tokens_spam
        self.count_tokens_hamm = count_tokens_ham
        for word in unique_vocab:
            self.cond_prob_spam[word] = count_tokens_spam[word] + 1 /len(concat_spam) + len(unique_vocab)
            #print("%s = %s" % (self.spam_cnd[word] , float (count_tokens_spam[word] + 1) / float ( len(concat_spam) + len(unique_vocab))))
            self.cond_prob_ham[word] = count_tokens_ham[word] + 1 /len(concat_ham) + len(unique_vocab)
            #self.ham_cnd[word] = float (count_tokens_ham[word] + 1) / float ( len(concat_ham) + len(unique_vocab))
        self.length_spam = len(concat_spam)
        self.length_ham = len(concat_ham)
        #print(self.cond_prod_spam)
        pass

    def classify(self, documents):
        """ Return a list of strings, either 'spam' or 'ham', for each document.
        Params:
          documents....A list of Document objects to be classified.
        Returns:
          A list of label strings corresponding to the predictions for each document.
        """
        ###TODO
        returnlist = []
        value = ''
        score = defaultdict(lambda:0)
        for doc_value in documents:
            for key in self.label_count:
                score[key] = math.log(self.prior[key],10)
            for item in list(set(doc_value.tokens)):
                   if (self.cond_prob_spam[item] > 0 and self.cond_prob_ham[item] > 0):
                        score["spam"] += math.log(self.cond_prob_spam[item],10) * doc_value.tokens.count(item)
                        score["ham"] += math.log(self.cond_prob_ham[item],10) * doc_value.tokens.count(item)
            value = max(score, key=score.get) 
            returnlist.append(value)
        return returnlist
        pass

def evaluate(predictions, documents):
    """ Evaluate the accuracy of a set of predictions.
    Return a tuple of three values (X, Y, Z) where
    X = percent of documents classified correctly
    Y = number of ham documents incorrectly classified as spam
    X = number of spam documents incorrectly classified as ham

    Params:
      predictions....list of document labels predicted by a classifier.
      documents......list of Document objects, with known labels.
    Returns:
      Tuple of three floats, defined above.
    """
    ###TODO
    spam_incorrect = 0
    ham_incorrect = 0
    classified_correct = 0
    for i in range(0,len(documents)):
        if documents[i].label == predictions[i]:
            classified_correct += 1
        else:
            if predictions[i] == 'spam':
                spam_incorrect += 1
            else:
                ham_incorrect += 1
    percent_value = float(classified_correct/len(documents))
    #print(percent_value,spam_incorrect,ham_incorrect
    return(percent_value,float(spam_incorrect),float(ham_incorrect))
    pass

def main():
    """ Do not modify. """
    if not os.path.exists('train'):  # download data
        from urllib.request import urlretrieve
        import tarfile
        urlretrieve('http://cs.iit.edu/~culotta/cs429/lingspam.tgz', 'lingspam.tgz')
        tar = tarfile.open('lingspam.tgz')
        tar.extractall()
        tar.close()
    train_docs = [Document(filename=f) for f in glob.glob("train/*.txt")]
    print('read', len(train_docs), 'training documents.')
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(filename=f) for f in glob.glob("test/*.txt")]
    print('read', len(test_docs), 'testing documents.')
    predictions = nb.classify(test_docs)
    results = evaluate(predictions, test_docs)
    print('accuracy=%.3f, %d false spam, %d missed spam' % (results[0], results[1], results[2]))
    print('top ham terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('ham', 10)))
    print('top spam terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('spam', 10)))

if __name__ == '__main__':
    main()
