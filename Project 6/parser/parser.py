import nltk
import sys
from nltk.tokenize import word_tokenize
nltk.download('punkt')
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NPV | NPV Adv
NPV -> PNP | PNP AV | PNP AV PNP | NPV NPV | NPV Conj NPV | NPV Conj V NP
AV -> V | Adv V | Adv V Adv | V Adv
PNP -> P NP | PNP PNP| NP
NP -> Det AN | AN | AN | NP NP
AN -> N | AA N
AA -> Adj | AA AA
"""

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
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Return all lowercased tokens with alphabetical chars
    return [word.lower() for word in word_tokenize(sentence) if word.isalpha()]



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Function to check a branch's type and check for nested NPs
    def check_branch(branch):
        if branch.label() == 'NP':
            np_subtrees = list(branch.subtrees(lambda t: t.label() == 'NP' and t != branch))
            if len(np_subtrees) == 0:
                return True
        return False
    
    # Return the result of this run on all
    return [branch for branch in tree.subtrees() if check_branch(branch)]

if __name__ == "__main__":
    main()
