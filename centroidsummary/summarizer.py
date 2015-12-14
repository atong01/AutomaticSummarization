from nltk.tokenize import sent_tokenize,word_tokenize
import os
from collections import Counter

"""
Recursively inspects a directory tree, finding all "*.txt" files that are
children of that directory.
Note:
    since this is a recursive search it may take a very long time/timeout if
    files are symlinked
Args:
    path (str): path to dataset directory, should be a directory containing
                hashed .txt and .xml files containing wiki articles
    ext (str):  extension of files to find
Yields:
    all txt files that are children to the specified path, with the absolute
    and relative paths
"""
def recursiveFinder(path, ext):
    for dir in os.listdir(path):
        abs_path = os.path.join(path, dir)
        if os.path.isdir(abs_path):
            for i, dir in recursiveFinder(abs_path, ext):
                yield i, dir
        elif abs_path.endswith(ext):
            yield abs_path, os.path.splitext(dir)[0]

"""
preprocess a wiki article given a body into sentances
"""
def preprocess(body):
    sents = sent_tokenize(body)
    return [word_tokenize(sent) for sent in sents]

def get_text(filepath):
    with open(filepath) as f:
        text = f.read()
    return text

class Document(object):
    def __init__(self, title, text):
        self.title = title
        self.text = self._parse_text(text)
        self.isValid = (not self.text is None)
        self.bag = self._init_bag()

    def _parse_text(self, text):
        try:
            if type(text) == list:
                return text
            elif type(text) == str:
                return preprocess(text)
        except UnicodeDecodeError:
            return None
    def _init_bag(self):
        d = Counter()
        if not self.isValid:
            return None
        for sentance in self.text:
            for word in sentance:
                d[word] += 1
        return d

"""
A Document Set represents a set of documents each with a title and body

Note:
    while initializing a Document set, it ignores any article with a
    UnicodeDecodeError, therefore may produce significantly fewer documents
    in the set than in the specified path
"""
class DocumentSet(object):
    def __init__(self, path, num = None):
        if num is None:
            self.file_list = [i for i in recursiveFinder(path, "txt")]
        else:
            self.file_list = [i for i in recursiveFinder(path, "txt")][:num]
        self.doc_dict  = self._hash_docs()

    def _hash_docs(self):
        d = {}
        for full, title in self.file_list:
            text = get_text(full)
            d[title] = Document(title, text)
        return d

    def compute_df(self):
        d = Counter()
        for title, doc in self.doc_dict.iteritems():
            if doc.isValid:
                d += doc.bag
        return d


def time_plot():
    def wrapper(func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)
        return wrapped
    import timeit
    import time
    f = open("times.txt", "a")
    for i in range(200, 2000, 100):
        t0 = time.time()
        dd = DocumentSet("../data", num = i)
        t1 = time.time() - t0
        print >>f, "%d,%f" %(i, t1)

def main():
#    file_list = [i for i in recursiveFinder("../data", "txt")]
#    text = get_text("sample.txt")
#    sents = preprocess(text)
#    dd = DocumentSet("sample")
    
    print len([i for i in recursiveFinder("../data", "txt")])
#    dd.compute_df()
#    dd = DocumentSet("../data")

if __name__ == "__main__":
#    main()
    time_plot()
#    dd = DocumentSet("../data")
