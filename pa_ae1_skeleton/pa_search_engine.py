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

    # with invert_index calculated, we can calculate the inv_doc_freq of each unique word
    # where inv_doc_freq = number of documents with the word / total number of documents
    for word in invert_index.keys():
        inv_doc_freq[word] = len(invert_index[word])/total_docs
        
#%%----------------------------------------------------------------------------
def sanitize_word(word):
    """
    Removes all non ascii characters from a given word
    """    
    newword = ""

    alphanumeric_chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m", # list of the alphanumerics
               "n","o","p","q","r","s","t","u","v","w","x","y","z",
               "A","B","C","D","E","F","G","H","I","J","K","L","M",
               "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
               "0","1","2","3","4","5","6","7","8","9"]
    
    printable_ascii_chars = [] # list of all ascii from 32-127. unsure which is the better to use
    for i in range(32,127):
        printable_ascii_chars.append(chr(i)) 

    for char in word:
        if char in printable_ascii_chars:
            newword += char.lower() # i think this is an appropriate time to lowercase everything, 
                                    # although it isnt implied in the given docstring

    return(newword)

#%%----------------------------------------------------------------------------
def parse_line(line):
    """    
    Parses a given line, 
    removes whitespaces, splits into list of sanitize words
    Uses sanitize_word()
    
    HINT: Consider using the "strip()" and "split()" function here
    
    """    

    line = line.split() # .split() performs the job of .strip() aswell, so i dont think its needed

    list_of_words = []
    for word in line:
        list_of_words.append(sanitize_word(word))

    return(list_of_words)

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

    # the dicts passed in are mutable ! so i dont need to return them. simply populating 
    # them in here or wherever is good enough

    # current filename and filepath is all we have, no actual data is in memory right now.
    # the loop is in crawl_folder, so we dont need to loop and only deal with current filename

    # steps:
    # 1. read the file
    # 2. do any data structure setup for the following functions if required
    # 3. write functions and run on file for:
    #       forward index
    #       inverted index (update not overwrite)
    #       term freq 
    #       NOT inv_doc_freq, its done in crawl_folder
    #       doc rank

    start = timer()
    with open(filepath, 'r', encoding="utf-8") as f:
        # assignment says:
        """
        While you are reading in the files to create the indices though, you will have to be
        careful about cleaning up the text to remove special characters and white spaces, and also
        deal with case sensitivity (recall, the search engine is meant to be case insensitive).
        """
        # i guess i can reuse parse_line, even though i wrote it with the intention of it being used
        # on the users CLI query.

        contents = f.read() # this includes the header, could start at body? examples say its fine
        contents_clean = parse_line(contents)
        forward_index_calc(forward_index, contents_clean, filename)
        inverted_index_calc(invert_index, contents_clean, filename)
        term_frequency_calc(term_freq, contents, filename)
        document_rank_calc(doc_rank, contents, filename)
    
    end = timer()
    print("Time taken to index file: ", filename, " = ", end-start)

#%%----------------------------------------------------------------------------
def forward_index_calc(forward_index, contents, filename):
    # this is just getting all unique words in the text
    # need to create list of all words with no dupes (use a set?)
    # then add a new dict entry to forward_index with key=filename, value=the set of words
    
    # i can cheat this by converting contents to a set
    # but i dont think i can analyse the complexity so i will do it faithfully
    seen_words = []
    for word in contents:
        if word not in seen_words:
            seen_words.append(word)

    forward_index[filename] = seen_words

#%%----------------------------------------------------------------------------
def inverted_index_calc(invert_index, contents, filename):
    # need to go thru each word in contents. if the word is not yet a key, add it with value of a
    # list with 1 entry of the current filename. if the word is a key, set the value to the existing list + the current filename.
    for word in contents:
        if word not in invert_index:
            invert_index[word] = [filename]
        else:
            if filename not in invert_index[word]: # if the word has already come up in the file, we shouldnt add the filename to the list cuz its there already
                invert_index[word].append(filename)

#%%----------------------------------------------------------------------------
def term_frequency_calc(term_freq, contents, filename):
    # the dict will have keys of the filename, and the value is another dict
    # the dict has keys of each word in the dict, and a value of the tf value

    total_words = len(contents)
    occurences = {}

    for word in contents:
        if word not in occurences:
            occurences[word] = 1
        else:
            occurences[word] += 1

    # now need to build a new dict thats just the occurences dict but each value 
    # is divided by total words, doing this inplace would have lower space complexity
    # probably even though its less readable since the variable name is kinda wrong

    for word in occurences:
        occurences[word] = occurences[word] / total_words

    term_freq[filename] = occurences

#%%----------------------------------------------------------------------------
def document_rank_calc(doc_rank, contents, filename):
    doc_rank[filename] = 1/len(contents) # i think its just as simple as this

#%%----------------------------------------------------------------------------
def search  (search_phrase
             ,forward_index
             ,invert_index
             ,term_freq
             ,inv_doc_freq
             ,doc_rank    
             ):
    """    
    For every document, you can take the product of TF and IDF 
    for term of the query, and calculate their cumulative product. 
    Then you multiply this value with that documents document-rank 
    to arrive at a final weight for a given query, for every document. 
    """
    
    words = parse_line(search_phrase)
    result = {}

    <YOUR-CODE-HERE>           

    return(sorted_result)
