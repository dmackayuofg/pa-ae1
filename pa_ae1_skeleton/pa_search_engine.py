# -*- coding: utf-8 -*-

"""
Module: 
pa_search_engine

About:
Implements functions used by a directory search engine

SOME FUNCTIONS OR THEIR SKELETONS HAVE BEEN PROVIDED
HOWEVER, YOU ARE FREE TO MAKE ANY CHANGES YOU WANT IN THIS FILE
AS LONG AS IT REMAINS COMPATIBLE WITH main.py and tester.py
"""

#%% ---------------------------------------------------------------------------
# Required Imports
#------------------------------------------------------------------------------
import string
from timeit import default_timer as timer
import os

#%%----------------------------------------------------------------------------
def dict_to_file(di, fi):
    os.makedirs(os.path.dirname(fi), exist_ok=True)
    with open(fi, "w") as f:
        for key, value in di.items():
            f.write("%s:%s\n" % (key, value))

#%%----------------------------------------------------------------------------
def print_result(result):
    """
    Print result (all docs with non-zero weights)
    """
    print("# Search Results:")
    count = 0
    for val in result: 
        if val[1] > 0: 
            print(val[0])
            count += 1
    print(count, " results returned")

#%%----------------------------------------------------------------------------
def crawl_folder(folder
                ,forward_index
                ,invert_index
                ,term_freq
                ,inv_doc_freq
                ,doc_rank
                ):
    """"
    Crawls a given folder, and runs the indexer on each file
    """
    
    total_docs = 0
    for file in os.scandir(folder):
        if file.is_file():
            total_docs += 1
            index_file(file.name, file.path, forward_index, invert_index, term_freq, doc_rank)

    for word in invert_index.keys():
        inv_doc_freq[word] = len(invert_index[word])/total_docs

#%%----------------------------------------------------------------------------
def sanitize_word(word):
    """
    Removes all non ascii characters from a given word
    """
    
    chars = []
    alphanumeric_chars = set(string.ascii_letters + string.digits)

    for char in word:
        if char in alphanumeric_chars:
            chars.append(char.lower())
    newword = "".join(chars)
    return newword

#%%----------------------------------------------------------------------------
def parse_line(line):
    """    
    Parses a given line, 
    removes whitespaces, splits into list of sanitize words
    Uses sanitize_word()
    
    HINT: Consider using the "strip()" and "split()" function here
    
    """

    list_of_words_unsanitized = line.split()
    list_of_words_clean = []

    for word in list_of_words_unsanitized:
        list_of_words_clean.append(sanitize_word(word))

    return list_of_words_clean

#%%----------------------------------------------------------------------------
def index_file  (filename
                ,filepath
                ,forward_index
                ,invert_index
                ,term_freq
                ,doc_rank
                ):
    """    
    Given a file, indexes it by calculating its:
        forward_index
        term_freq
        doc_rank
        and updates the invert_index (which is calculated across all files)
    """

    start = timer()
    with open(filepath, 'r', encoding="utf-8") as f:
        contents = f.read()
        contents_clean = parse_line(contents)
        forward_index_calc(forward_index, contents_clean, filename)
        inverted_index_calc(invert_index, contents_clean, filename)
        term_frequency_calc(term_freq, contents_clean, filename)
        document_rank_calc(doc_rank, contents_clean, filename)

    end = timer()
    print("Time taken to index file: ", filename, " = ", end-start)

#%%----------------------------------------------------------------------------
def forward_index_calc(forward_index, contents, filename):
    seen = set()
    for word in contents:
        seen.add(word)
    forward_index[filename] = seen

#%%----------------------------------------------------------------------------
def inverted_index_calc(invert_index, contents, filename):
    for word in contents:
        if word not in invert_index:
            invert_index[word] = set()
        invert_index[word].add(filename)

#%%----------------------------------------------------------------------------
def term_frequency_calc(term_freq, contents, filename):
    total_words = len(contents)
    occurences = {}

    for word in contents:
        if word not in occurences:
            occurences[word] = 1
        else:
            occurences[word] += 1

    for word in occurences:
        occurences[word] = occurences[word] / total_words

    term_freq[filename] = occurences

#%%----------------------------------------------------------------------------
def document_rank_calc(doc_rank, contents, filename):
    doc_rank[filename] = 1/len(contents)

#%%----------------------------------------------------------------------------
def search  (search_phrase
             ,forward_index
             ,invert_index
             ,term_freq
             ,inv_doc_freq
             ,doc_rank    
             ,is_ordered=False
             ):
    """    
    For every document, you can take the product of TF and IDF 
    for term of the query, and calculate their cumulative product. 
    Then you multiply this value with that documents document-rank 
    to arrive at a final weight for a given query, for every document. 
    """

    words = parse_line(search_phrase)
    result = []
    
    for filename in forward_index:
        if not is_ordered: # normal entry
            weight = 1
            for word in words:
                word_weight = (term_freq[filename].get(word, 0) * inv_doc_freq.get(word, 0))
                weight *= word_weight
            weight *= doc_rank[filename]
            result.append((weight, filename))

        else: # extra feature
            missing = False
            weight = 0
            for i, word in enumerate(words):
                if word not in term_freq[filename]:
                    missing = True
                    break
                word_weight = (term_freq[filename].get(word, 0) * inv_doc_freq.get(word, 0))
                weight += word_weight * (1 / (i+1))
            if missing:
                result.append((0, filename))
                continue
            weight *= doc_rank[filename]
            result.append((weight, filename))
            weight = 1

    result = sorted(result, reverse=True)
    sorted_result = []
    for v, k in result:
        sorted_result.append((k, v))

    return sorted_result
