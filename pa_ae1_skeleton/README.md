*The PA Directory Search Engine*

Practical Algorithms 2025-26, University of Glasgow
Assessed Exercise 1

Submitted by: Drew Mackay, 2652958M
(If applicable,) project was done in partnership with: 

# A: Complexity Analysis
Present the following complexity analysis in this report:

+ Big-O complexity of the indexing operation.
+ Big-O complexity of a search operation (given that indexing has been done already).
+ Big-O complexity of a search operation if it were implemented in a brute force fashion (that is, no indexing performed, all search queries go through the entire text of all files every time).

You should be very clear about what you mean by n when presenting your Big-O complexity analysis.

_Note_: You don’t have to do a line-by-line code-analysis like we do in certain other problems. Instead, present your analysis as a text description that walks through the relevant operations, comments on their complexity with rationale, and then presents the overall complexity.

## Your Answer

### Indexing Operation

The indexing operation is executed by calling the `index_file` method on each file, so we must discuss everything this method contains.

`index_file` begins by opening and reading the file, which is an O(n) operation, where n is the length of the characters in the file.

Then the `parse_line` method is called on the data, which first splits the contents into a list of words using the `.split()` method, which is an O(n) operation where n is the characters in the file.
We then loop over each word and call the `sanitize_word` method.
In `sanitize_word`, we loop over each character in the word, check if the char is in the set, and then append the char to the string. These are both O(1) operations so overall it is O(m) because of the loop, where m is the characters in the word.
This makes the entire method of `parse_line` O(n) time, where n is the characters in the file.

Now that we have our dataset ready, we move to building the individual indexing dictionaries.
First, in `forward_index_calc`, we loop over every word in the file, and add them to a set (which checks duplicates in O(1) time). Due to the loop, this is O(n) time overall, where n is the words in the list.

Next, in `inverted_index_calc`, we loop over every word in the file, and check if the word is in the dictionary. If not we add it and make a new set for its key. If so, we add the current filename to the set for the current word if it's not already there (the membership check is done during the sets `.add()` method). All of these are O(1) operations, so due to the loop, this is O(n) time overall, where n is the words in the list.

Then, in `term_frequency_calc`, we loop over each word, check membership and append. Then we loop over the keys in the dictionary once do a calculation. The first loop is O(n) where n is the words in the list. The second loop is O(m) where m is unique words in the loop. Worst case this is also O(n). Overall this method is O(n).

Finally in `document_rank_calc`, we have a simple O(1) operation.

The aforementioned `index_file` method is thus O(n), where n is the characters in the file.

`index_file` is called by `crawl_folder`, which involves looping over each file of interest and indexing it. If we consider this he highest level of the indexing operation, then the indexing operation takes O(n) time, where n is the total number of characters **in all the files** (could also be described as O(nk), where k is number of files and n is the characters per file, if that wasn't clear).

### Search Operation

The search operation is executed by calling the `search` method on the user's search phrase.

We first call `parse_line` on the search phrase, which we have established is O(n) where n is the characters in the phrase.

Then we loop over every file in the directory, and then loop over every word in the search phrase. For each word we perform some dictionary lookups and assignments, all O(1) operations. For each each file we then perform some more O(1) operations. This makes this whole loop take O(nk) time, where n is the number of words in the phrase and k is the number of files.

Now that we have our weights, we need to sort the files by the weights.
We call Python's `sorted` method, which according to the [Python documentation](https://docs.python.org/3.10/howto/sorting.html) uses the [Timsort sorting algorithm](https://en.wikipedia.org/wiki/Timsort) which has O(nlog(n)) time.
Then we have to flip the order of the tuples. We loop over each file again, taking O(n) time.

The overall time complexity of the searching operation is O(nlog(n)) time, where n is the number of files. The operation with the largest time complexity is the sorting of the results.

### Bruteforce Search Operation

The steps involved in a bruteforce approach, where we haven't done the indexing beforehand, are:

1. Read each file. This is an O(n) operation where n is the total characters across all files.
2. Split and sanitize each word. This is an O(n) operation where n is the total characters across all files.
3. Create the term frequency dictionary for each file. This is an O(w) operation where w is the number of words across all files.
4. Calculate the inverse document frequency by going through every files term frequency dictionary. This is an O(pk) operation where p is the words in the search phrase, and k is the number of files.
5. Calculate the weight for each document, using the term frequency and the inverse document frequency dictionaries, and document rank. This calculation is O(1) time, for each word in the search phrase, for each file. So it is a O(pk) operation.
6. Then we sort by the weights. As established before, this is a O(klog(k)) operation when using Python's `.sorted()` method

The most significant operations are first three steps, as number of characters/words will greatly exceed the number of words in a query or the number of files. With words being proportional to characters, we can say that overall this approach has O(n) time, where n is the number of characters across all files.

This is much larger than the searching for the precalculated index, which has O(nlog(n)) where n is the number of files.

# B: Choice of Data Structures

Explain and justify your choice of data structures.

## Your Answer

Going 1 by 1 of each function that I wrote, first there is `sanitize_word`. I choose to use a set to hold the correct characters, instead of a list. A set uses hashing to check membership, which has an average case of O(1), and a worst case of O(n). Lists must always loop through the entire list to check membership, so they always take O(n) time. I consulted [this page from the Python documentation](https://wiki.python.org/moin/TimeComplexity) to make my decision. 
I then choose to create a characters list inside of the loop and then create the string after, instead of a string inside of the loop. This is because strings are immutable, so the string would be copied and new one would be created everytime, which is an O(n) operation. List append is O(1).

In `parse_line`, I choose to use a list to hold the words. I considered using a tuple, but tuples are immutable and I need to append to the collection. I also considered using an array as they have O(1) appending like lists and would have less space complexity as I am sure I only need strings, but arrays cannot hold strings.

In `forward_index_calc`, I choose to use a set to hold the seen words, as they have on average O(1) membership checking, and on average O(1) appending. A list has O(n) membership checking and O(1) appending. Note that the `.add()` method does a membership check before appending.

In `inverted_index_calc`, I again choose to use a set for the same reasons.

In `term_frequency_calc`, I use a dictionary to hold the occurences. The only other data structure I could think of being usable would be a list of tuples holding the word and then the occurences, but membership checking is O(1) for dictionaries which is much better than O(n) for lists.

In `search`, `result` was originally declared as a dictionary in the skeleton code, however I think that using a list is more practical. I initially found when I implemented it using a dictionary that since `print_result` expects `search` to return a list of tuples, that it would make sense to implement it as that from the start, instead of converting the dictionary to a list of tuples after calculating the weights. They have identical time complexity, but having a list from the start means we don't need to create the extra dictionary, so we have slightly less memory usage.

# C: Discuss extra features, if any:
If you implemented any extra feature on top of the requirements noted in this hanadout, briefly describe them here.

## Your Answer

I have added a new option for querying. Adding the `--ordered`, or `-o` flag when running `main.py` will 
make it so that the order of the words in your search query implies the importance of each word, descending. 
For example:
```bash
>>> python main.py -o
Enter your search term: anna pierre
# Search Results:
anna_karenina.txt
war_and_peace.txt
Enter your search term: pierre anna
# Search Results:
war_and_peace.txt
anna_karenina.txt
```
War and Peace, and Anna Karenina, both mention the words pierre and anna, but pierre occurs much more than anna  in War and Peace, and vice versa for Anna Karenina.

I have had to minorly change `main.py` to allow for this, however it doesn't interfere with `tester.py`. Result should be identical if the `-o` flag is not included.

Since the original algorithm is entirely multiplicative, simply adding a scalar to each word based on it's index wouldn't work since the order doesn't matter. Instead I had to somewhat intrusively change the algorithm to be summative instead.