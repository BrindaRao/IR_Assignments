from collections import defaultdict
import tarfile
import tabulate
import re
import index, evaluate, score


def parse_relevance_strings(strings):
    r"""
    Parse lines from TIME.REL.

    Params:
      strings...A list of strings, one per line, from TIME.REL
    Returns:
      A dict from query id to the list of relevant document ids, as ordered in the file.

    >>> strings = '''1  268 288 304
    ...
    ... 2  326 334'''
    >>> result = parse_relevance_strings(strings.split('\n'))
    >>> sorted(result.items())
    [(1, [268, 288, 304]), (2, [326, 334])]
    """
    ###TODO
    parsedict = defaultdict(lambda:0)
    finallist = defaultdict(lambda:0)
    listofstrings = []
    for i in range(0,len(strings)):
        l1 = re.findall('\w+',strings[i]) 
        if(len(l1)>0):
            listofstrings.append(l1)
    for item in listofstrings:
        valuelist = []
        for j in range(1,len(item)):
            valuelist.append(int(item[j]))
        parsedict[int(item[0])] = valuelist
    finallist = sorted(parsedict.items(),key=lambda x: x[0])    
    return dict(finallist)
    pass


def read_relevances(fname):
    """
    Do not modify.
    Read a map from query ID to a list of relevant doc IDs.
    """
    return parse_relevance_strings(open(fname).readlines())


def parse_query_strings(strings):
    r"""
    Parse lines from TIME.QUE.

    Params:
      strings...A list of strings, one per line, from TIME.QUE
    Returns:
      A dict from query id to query text string.
    >>> string = '''*FIND      1
    ...
    ... KENNEDY ADMINISTRATION PRESSURE ON NGO DINH DIEM TO STOP
    ...
    ... SUPPRESSING THE BUDDHISTS .
    ...
    ... *FIND      2
    ...
    ... EFFORTS OF AMBASSADOR HENRY CABOT LODGE TO GET VIET NAM'S
    ...
    ... PRESIDENT DIEM TO CHANGE HIS POLICIES OF POLITICAL REPRESSION .
    ...
    ... *STOP'''
    >>> res = parse_query_strings(string.split('\n'))
    >>> print('%s' % res[1])
    KENNEDY ADMINISTRATION PRESSURE ON NGO DINH DIEM TO STOP SUPPRESSING THE BUDDHISTS . 
    >>> print('%s' % res[2])
    EFFORTS OF AMBASSADOR HENRY CABOT LODGE TO GET VIET NAM'S PRESIDENT DIEM TO CHANGE HIS POLICIES OF POLITICAL REPRESSION . 
    """
    ###TODO
    querydict = defaultdict(lambda:0)
    listarray =[]
    lenarray = []
    finalarray = []
    arraylist =[]
    for i in range(0,len(strings)):
        parsedquerylist = re.split('\*FIND\s+[0-9]+', strings[i])
        if(len(parsedquerylist)>0):
            listarray.append(parsedquerylist)
    for i in range(0,len(listarray)):
        for j in listarray[i]:
            lenarray.append(j.strip())
    #to remove out empty lists
    finalarray = [x for x in lenarray if x != ['\n']]
    arrayval = " ".join(finalarray)
    arra1 = re.split('\s?[.]\s{5,7}',arrayval)
    arra1[0] = arra1[0][1:]
    leng1 = len(arra1)-1
    summ = len(arra1[leng1])-10
    arra1[len(arra1)-1] = arra1[len(arra1)-1][0:summ]
    for i in range(0,len(arra1)):
        querydict[i+1] = arra1[i].strip() + " ."
    return dict(querydict)
    pass


def read_queries(fname):
    """  Do not modify. Read a map from query id to text."""
    return parse_query_strings(open(fname).readlines())


def parse_document_strings(strings):
    r"""
    Parse lines from TIME.ALL.

    Params:
       strings...A list of strings, one per line, from TIME.ALL
    Returns:
       A list of strings, one per document.
    >>> string = '''*TEXT 017 01/04/63 PAGE 020
    ...
    ... THE ALLIES AFTER NASSAU
    ...
    ... *TEXT 020 01/04/63 PAGE 021
    ...
    ... THE ROAD TO JAIL IS PAVED WITH
    ...
    ... *STOP'''
    >>> parse_document_strings(string.split('\n'))
    ['THE ALLIES AFTER NASSAU ', 'THE ROAD TO JAIL IS PAVED WITH ']
    """
    ###TODO
    parsedlist = []
    finalarray = []
    finlist = []
    arrayval = ""
    final_str = " ".join(strings)
    final_st = re.split('\*STOP',final_str)
    parsedlist = re.split('\*TEXT\s+[0-9]{3}\s+\d+/\d+/\d+\s+PAGE\s+[0-9]{3}|\*TEXT\s+[0-9]{3}\s+\d+/\d+\s+[0-9]{2}\s+PAGE\s+[0-9]{3}', str(final_st[0]))
    for i in range(0,len(parsedlist)-1):
        if '\n' in parsedlist[i]:
            parsedlist[i] = re.sub('\n','',parsedlist[i])
        arrayval = "".join(parsedlist[i])
        finalarray.append(arrayval)
    fo = open("RESULTS_txt.txt", 'w')
    for i in range(0,len(finalarray)):
        stringwrite = finalarray[i]
        fo.write(str(stringwrite))
        fo.write('\n')
    return finalarray
    pass


def read_documents(fname):
    """ Do not modify. Read a list of documents."""
    return parse_document_strings(open(fname).readlines())


def read_data():
    """ Do not modify. Read data."""
    tarfile.open('time.tar.gz', mode='r').extractall()
    queries = read_queries('TIME.QUE')
    print('read %d queries.' % len(queries))
    relevances = read_relevances('TIME.REL')
    print('read %d relevance judgements.' % len(relevances))
    #print(relevances)
    docs = read_documents('TIME.ALL')
    print('read %d documents.' % len(docs))
    return queries, relevances, docs


def write_results(all_results, fname):
    """ Do not modify. Write results. """
    evals = sorted(list(all_results.values())[0].keys())
    headers = ['System'] + evals
    systems = sorted(all_results.keys())
    vals = []
    for system in systems:
        results = all_results[system]
        vals.append([system] + [results[e] for e in evals])
    f = open(fname, 'w')
    f.write(tabulate.tabulate(vals, headers, floatfmt=".4f"))
    f.write('\n')

def search(query, scorer, index):
    """
    Retrieve documents matching a query using the specified scorer.

    1) Tokenize the query.
    2) Convert the query tokens to a vector, using Index.query_to_vector.
    3) Call the scorer's score function.
    4) Return the list of document ids in descending order of relevance.

    NB: Due to the inconsistency of floating point arithmetic, when sorting,
    round the scores to 6 decimal places (e.g., round(x, 6)). This will ensure
    replicable results.

    Params:
      query....A string representing a search query.
      scorer...A ScoringFunction to retrieve documents.
      index....A Index storing postings lists.
    Returns:
      A list of document ids in descending order of relevance to the query.
    """
    ###TODO
    #1
    tokenized_query = index.tokenize(query)
    #2
    idf_vector = index.query_to_vector(tokenized_query)
    #3
    scorer_val = scorer.score(idf_vector,index)
    #4
    finallist = sorted(scorer_val,key=scorer_val.__getitem__,reverse=True)
    #finallist = sorted(scorer_val.items(),key=lambda x: x[1],reverse=True) 
    return finallist
    pass


def run_all(queries, relevances, docs, indexer, scorers, evaluators, NHITS):
    """ Do not modify.
    For each query, run all scoring methods and evaluate the results.
    Returns:
      A dict from scoring method to results
    """
    results = defaultdict(lambda: defaultdict(lambda: 0))
    for qid, qtext in queries.items():
        print('\n-------\nQUERY:%d %s' % (qid, qtext))
        relevant = sorted(list(relevances[qid]))
        print('RELEVANT: %s' % relevant)
        for scorer in scorers:
            hits = search(qtext, scorer, indexer)[:NHITS]
            print('\t%s results: %s' % (scorer, hits))
            for evaluator in evaluators:
                evaluation = evaluator.evaluate(hits, relevant)
                results[str(scorer)][str(evaluator)] += evaluation
    for scorer in scorers:
        for evaluator in evaluators:
            results[str(scorer)][str(evaluator)] /= len(queries)
            
        """ fo = open("RESULTS.txt", 'w')
        stringwrite += str(relevances[qid])
        results1 = stringwrite + results
        fo.write(str(results1))
        #fo.write('\n')"""
    return results


def main():
    """ Do not modify.
    Run and evaluate all methods.
    """
    queries, relevances, docs = read_data()
    NHITS = 10
    indexer = index.Index(docs)

    scorers = [score.Cosine(),
               score.RSV(),
               score.BM25(k=1, b=.5),
               score.BM25(k=1, b=1),
               score.BM25(k=2, b=.5),
               score.BM25(k=2, b=1)]

    evaluators = [evaluate.Precision(),
                  evaluate.Recall(),
                  evaluate.F1(),
                  evaluate.MAP()]

    all_results = run_all(queries, relevances, docs, indexer, scorers, evaluators, NHITS)
    write_results(all_results, 'Results.md')


if __name__ == '__main__':
    main()
