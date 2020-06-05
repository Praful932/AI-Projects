import nltk
import sys
import re
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP | S Conj VP
NP -> N P N | Det Adj N | Det N | N P S | Det N Adv | Adj N PP | N PP | N
VP -> V Det N | V Det NP | V P NP | V NP | V P N | V Adv VP | V P NP | V Det VP | AdjP N PP | Adv VP | V Adv | V
PP -> P N | P NP | P Det NP 
AdjP -> Adj | Adj AdjP
"""
# N P NP
# NP = Palm of my hand
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        # print(tree,type(tree))
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    words = [word for word in nltk.word_tokenize(sentence) if re.match("[a-z]", word)]
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    npchunks = []
    for branch in tree.subtrees():
        if branch.label()=='NP' and check(branch):
            # print(branch)
            npchunks.append(branch)
    return npchunks

def check(branch):
    for subbranch in branch:
        print(subbranch, branch)
        if isinstance(subbranch, str):
            return
        elif subbranch.label() == 'NP':
            return False
        else:
            check(subbranch)
    return True
        

if __name__ == "__main__":
    main()
