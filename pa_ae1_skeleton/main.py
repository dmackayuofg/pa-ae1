# -*- coding: utf-8 -*-
"""
Practical Algorithms.
University of Glasgow.

Assessed Exercise 1

This is main file that runs the search engine.

***************************************
*** This file SHOULD NOT BE CHANGED ***
***************************************
"""

import pa_search_engine as pa 
from timeit import default_timer as timer

#%%----------------------------------------------------------------------------
# main
# 
#------------------------------------------------------------------------------
            
if __name__ == "__main__":
    forward_index = {}
    invert_index = {}
    term_freq = {}
    inv_doc_freq = {}
    doc_rank = {}
    
    target_dir = "search_dir"
    
    print("Crawling initiated")
    start = timer()
    pa.crawl_folder(target_dir, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)
    end = timer()
    print("Crawling concluded in ", end-start, " seconds")                            
    
    print("Writing indices to files")
    pa.dict_to_file(forward_index, "output_files/forward_index.txt")
    pa.dict_to_file(invert_index, "output_files/invert_index.txt")
    pa.dict_to_file(term_freq, "output_files/term_freq.txt")
    pa.dict_to_file(inv_doc_freq, "output_files/inv_doc_freq.txt")
    pa.dict_to_file(doc_rank, "output_files/doc_rank.txt")
    
    
    print("Search engine ready for queries, target directory = ", target_dir)
    while(True):
        search_phrase = input("Enter your search term: ")
        if(search_phrase == ""):
            break
        start = timer()
        result = pa.search(search_phrase, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)
        end = timer()

        pa.print_result(result)
        
        print("# Search took ", end-start, " seconds")
        
    
