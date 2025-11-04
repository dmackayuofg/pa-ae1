# -*- coding: utf-8 -*-
"""
Practical Algorithms.
University of Glasgow.

Assessed Exercise 1

This is automatic tester that will be used to test your solution.

You should run it yourself to satisfy yourself that your code
runs correctly.

****************************************
**** This file SHOULD NOT BE CHANGED ***
****************************************

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
    
    print("Crawling initated")
    start = timer()
    pa.crawl_folder(target_dir, forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)
    end = timer()
    print("Crawling concluded in ", end-start, " seconds")                            
    

    test_cases = []
    test_cases.append(
                        ("the",
                        ["first_simple.txt"
                        ,"third.txt"
                        ,"first.txt"
                        ,"second.txt"
                        ,"divine_comedy.txt"
                        ,"room_with_a_view.txt"
                        ,"sherlock.txt"
                        ,"oliver_twist.txt"
                        ,"moby_dick.txt"
                        ,"little_women.txt"
                        ,"anna_karenina.txt"
                        ,"war_and_peace.txt"
                        ,"shakespeare.txt"
                        ]
                        )
                    )
                    
    test_cases.append(
                        ("anna",
                        ["anna_karenina.txt"
                        ,"war_and_peace.txt"
                        ,"shakespeare.txt"
                        ]
                        )
                    )


    test_cases.append(
                        ("here comes the sun",
                        ["divine_comedy.txt"
                        ,"room_with_a_view.txt"
                        ,"moby_dick.txt"
                        ,"shakespeare.txt"
                        ,"oliver_twist.txt"
                        ,"little_women.txt"
                        ,"sherlock.txt"
                        ,"anna_karenina.txt"
                        ,"war_and_peace.txt"
                        ]
                        )
                    ) 


    test_cases.append(
                        ("anna oliver",
                        ["shakespeare.txt"
                        ]
                        )
                    ) 

    test_cases.append(
                        ("practical algorithmss",
                        []
                        )
                    )     
    
    #run tests
    for test in test_cases:
        print("\nTEST INIT: query = ", test[0])
        #run test query
        result = pa.search(test[0], forward_index, invert_index, term_freq, inv_doc_freq, doc_rank)
        
        #collect all doc names from result (result returns tuples with docs and weights)
        res_list = []
        for res in result:
            #result list contains all files; pick those with non-zero weights
            if(res[1] > 0) : res_list.append(res[0])
        
        #first check if returned size correct
        assert len(res_list) == len(test[1]), "TEST FAIL: Number of files returned by search is incorrect" 
        
        #now check correct items returned, in sequence
        for i in range(len(res_list)):
            print("Expected in result at position ", i, " : ", test[1][i], ", Found: ", res_list[i])
            assert test[1][i] == res_list[i], "TEST FAIL: Incorrect document or incorrect sequence in search result"
        
        print("TEST PASSED\n")
