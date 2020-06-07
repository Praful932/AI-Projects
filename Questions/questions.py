import nltk
import sys
import os
import string
import math
import re
from heapq import nlargest

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = dict()
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        with open(file_path, encoding='utf-8') as f:
            data[file_name] = "".join(f.readlines())

    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    words = [word for word in nltk.word_tokenize(document) if word not in nltk.corpus.stopwords.words("english")
             and re.match("[a-z]", word)]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idf = dict()
    total_docs = len(documents.keys())
    for document in documents.keys():
        s = set(documents[document])
        for word in s:
            try:
                word_idf[word] += 1
            except KeyError:
                word_idf[word] = 1

    for word in word_idf:
        word_idf[word] = math.log(total_docs/word_idf[word])

    return word_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    topfiles = dict()
    for file_name in files.keys():
            for word in query:
                if word in file_name:
                    try:
                        topfiles[file_name] += idfs[word] * file_name.count(word)
                    except KeyError:
                        topfiles[file_name] = idfs[word] * file_name.count(word)

    return nlargest(n, topfiles, key=topfiles.get)
        


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topsentences = dict()
    for s in sentences:
        word_count = 0
        topsentences[s] = dict()
        for word in query:
            if word in sentences[s]:
                word_count += 1
                try:
                    topsentences[s]['idfs'] += idfs[word]
                except KeyError:
                    topsentences[s]['idfs'] = idfs[word]

        # If sentence contains 0 matching words from query
        if not word_count:
            topsentences[s]['idfs'] = 0
        topsentences[s]['qtd'] = word_count/len(sentences[s])

    matches = nlargest(n, topsentences.items(), key = lambda x:(x[1]['idfs'],x[1]['qtd']))
    final_sentences = []

    for m in matches:
        final_sentences.append(m[0])

    return final_sentences



if __name__ == "__main__":
    main()
