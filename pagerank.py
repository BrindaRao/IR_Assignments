""" Assignment 6: PageRank. """
from bs4 import BeautifulSoup
from sortedcontainers import SortedList, SortedSet, SortedDict
from collections import Counter
from collections import defaultdict
import glob
import os
import re


def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = (1/N)(1-b) + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0.

    Params:
      urls.......SortedList of urls (names)
      inlinks....SortedDict mapping url to list of in links (backlinks)
      outlinks...Sorteddict mapping url to list of outlinks
    Returns:
      A SortedDict mapping url to its final PageRank value (float)

    >>> urls = SortedList(['a', 'b', 'c'])
    >>> inlinks = SortedDict({'a': ['c'], 'b': set(['a']), 'c': set(['a', 'b'])})
    >>> outlinks = SortedDict({'a': ['b', 'c'], 'b': set(['c']), 'c': set(['a'])})
    >>> sorted(compute_pagerank(urls, inlinks, outlinks, b=.5, iters=0).items())
    [('a', 1.0), ('b', 1.0), ('c', 1.0)]
    >>> iter1 = compute_pagerank(urls, inlinks, outlinks, b=.5, iters=1)
    >>> iter1['a']  # doctest:+ELLIPSIS
    0.6666...
    >>> iter1['b']  # doctest:+ELLIPSIS
    0.333...
    """
    ###TODO
        
    rw = defaultdict(lambda:0.0)
    pageRank = defaultdict(lambda:1.0)
   
    for outlink in outlinks:
        rw[outlink]=len(outlinks[outlink])
        
    #initialize page ranks scores to 1
    for url in urls:
        pageRank[url] = 1.0

    for i in range(iters):
        for url in urls:
            summ = 0.0
            for link in inlinks[url]:
                summ += 1.0 * pageRank[link]/rw[link]
            pageRank[url] = (1/len(urls))* (1.0-b)+b*summ
                
    return SortedDict(dict(pageRank))
    
    pass


def get_top_pageranks(inlinks, outlinks, b, n=50, iters=20):
    """
    >>> inlinks = SortedDict({'a': ['c'], 'b': set(['a']), 'c': set(['a', 'b'])})
    >>> outlinks = SortedDict({'a': ['b', 'c'], 'b': set(['c']), 'c': set(['a'])})
    >>> res = get_top_pageranks(inlinks, outlinks, b=.5, n=2, iters=1)
    >>> len(res)
    2
    >>> res[0]  # doctest:+ELLIPSIS
    ('a', 0.6666...
    """
    ###TODO
    #get all the urls from the inlinks
    goturls = SortedList(dict(inlinks).keys())
    #do the compute page rank
    pageRank = compute_pagerank(goturls, inlinks, outlinks, b, iters)
    #sort the pageRank 
    #topNPage = sorted(pageRank.items(),key=operator.itemgetter(1),reverse = True)
    topNPage = sorted(pageRank.items(), key=lambda x: x[1],reverse= True)
    #get only the top N pages
    finalTopNPage = topNPage[:n]
    #return the value
    return finalTopNPage

    pass


def read_names(path):
    """ Do not mofify. Returns a SortedSet of names in the data directory. """
    return SortedSet([os.path.basename(n) for n in glob.glob(path + os.sep + '*')])


def get_links(names, html):
    """
    Return a SortedSet of computer scientist names that are linked from this
    html page. The return set is restricted to those people in the provided
    set of names.  The returned list should contain no duplicates.

    Params:
      names....A SortedSet of computer scientist names, one per filename.
      html.....A string representing one html page.
    Returns:
      A SortedSet of names of linked computer scientists on this html page, restricted to
      elements of the set of provided names.

    >>> get_links({'Gerald_Jay_Sussman'},
    ... '''<a href="/wiki/Gerald_Jay_Sussman">xx</a> and <a href="/wiki/Not_Me">xx</a>''')
    SortedSet(['Gerald_Jay_Sussman'], key=None, load=1000)
    """
    ###TODO
    #remove BeautifulSoap - later


    listofHrefs = []
    listofHrefTexts = []
    FinalSortedSet = SortedSet()
    splice_char = '/'
    #getting all the tags using the BeautifulSoup
    #soup = BeautifulSoup(html, "html.parser") 
    #fectching all the links in anchor tags
    #for link in soup.find_all('a'):
        #listofHrefs.append(link.get('href'))
    for i in range(0,len(listofHrefs)):
        value = listofHrefs[i][6:]
        listofHrefTexts.append(value)
    listofHrefTexts = re.findall(r'href="([^"]*)', html)
    #print(listofHrefTexts)
    for i in listofHrefTexts:
        #print(i)
        value = i[6:]
        listofHrefs.append(value)
    #print(listofHrefs)
    listofHrefs = list(set(listofHrefs))
    #print(len(listofHrefs))
    for href in listofHrefs:
        for name in names:
            #windows OS handling
            if(name == "Guy_L._Steele,_Jr"):
                names.remove(name)
                names.add("Guy_L._Steele,_Jr.")
            if(href == name):
                FinalSortedSet.add(name)
            
    
    return FinalSortedSet
    
    pass

def read_links(path):
    """
    Read the html pages in the data folder. Create and return two SortedDicts:
      inlinks: maps from a name to a SortedSet of names that link to it.
      outlinks: maps from a name to a SortedSet of names that it links to.
    For example:
    inlinks['Ada_Lovelace'] = SortedSet(['Charles_Babbage', 'David_Gelernter'], key=None, load=1000)
    outlinks['Ada_Lovelace'] = SortedSet(['Alan_Turing', 'Charles_Babbage'], key=None, load=1000)

    You should use the read_names and get_links function above.

    Params:
      path...the name of the data directory ('data')
    Returns:
      A (inlinks, outlinks) tuple, as defined above (i.e., two SortedDicts)
    """
    ###TODO
    
    inlinks = SortedDict() #output
    outlinks = SortedDict() #output
    
    SetofNames = SortedSet()
   
    #reading all the folders from the path and creating a set of Computer Scientists names
    for name in read_names(path):
        #windows os handling
        if name == "Guy_L._Steele,_Jr":
            name = "Guy_L._Steele,_Jr."
        SetofNames.add(name)
        inlinks[name] = SortedSet() #creating an empty inlinks of names as sortedSet
      
    #reading their inlinks and outlinks
    for name in SetofNames:
        
        SetOfInLinks = SortedSet()
        
        fp = open( path + "/"+ name,'r',encoding = "utf-8")
        soup = BeautifulSoup(fp.read(),"html.parser")
        linksFound = []
        linksFound = soup.findAll('a', href=re.compile("/wiki/"))
        
        HTML = ""
        for link in linksFound:
            HTML = HTML + str(link)
            HTML = HTML + " and "
         
        #get All the outlinks by calling get_links
        outlinks[name] = get_links(SetofNames,HTML)
        #print(outlinks[name])
        #if any self reference, remove them
        if name in outlinks[name]:
            outlinks[name].remove(name) 
        
  
        for outlink in outlinks[name]:
            SetOfInLinks.add(name)
            #print(SetOfInLinks)
            inlinks[outlink].update(SetOfInLinks)
            #print(inlinks[outlink])

    return (inlinks,outlinks)
    
   
    pass


def print_top_pageranks(topn):
    """ Do not modify. Print a list of name/pagerank tuples. """
    print('Top page ranks:\n%s' % ('\n'.join('%s\t%.5f' % (u, v) for u, v in topn)))


def main():
    """ Do not modify. """
    if not os.path.exists('data'):  # download and unzip data
       from urllib.request import urlretrieve
       import tarfile
       urlretrieve('http://cs.iit.edu/~culotta/cs429/pagerank.tgz', 'pagerank.tgz')
       tar = tarfile.open('pagerank.tgz')
       tar.extractall()
       tar.close()
    print('Before calling read_links')
    inlinks, outlinks = read_links('data')
    #output = read_names('data')
    #print(output)
    print('read %d people with a total of %d inlinks' % (len(inlinks), sum(len(v) for v in inlinks.values())))
    print('read %d people with a total of %d outlinks' % (len(outlinks), sum(len(v) for v in outlinks.values())))
    topn = get_top_pageranks(inlinks, outlinks, b=.8, n=20, iters=10)
    print_top_pageranks(topn)


if __name__ == '__main__':
    main()
