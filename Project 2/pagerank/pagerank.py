import os
import random
import re
import sys
from collections import defaultdict

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    final = distributedPages(corpus,1-damping_factor)
    connected_pages = connectedPages(corpus, page)
    for p in connectedPages(corpus, page):
        final[p] += damping_factor / len(connected_pages)
    return final
    
def connectedPages(corpus, page):
    # Obtain all connected pages to provided page
    return corpus[page] if page in corpus else []

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize page counts
    page_counts = defaultdict(int)
    
    # Choose initial page
    current_page = random.choice(list(corpus.keys()))
    
    # Perform random walk and update page counts
    for _ in range(n):
        page_counts[current_page] += 1/n
        current_page = weighted_choice(transition_model(corpus, current_page, damping_factor))
    return dict(page_counts)

def weighted_choice(d):
    # Extract keys and weights from the dictionary
    keys = list(d.keys())
    weights = list(d.values())
    
    # Choose a key based on weights
    chosen_key = random.choices(keys, weights=weights, k=1)[0]
    return chosen_key

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = distributedPages(corpus)
    deviation = True
    
    # Loop until stabilized
    while deviation:
        oldPages = pages.copy()
        deviation = False
        for page in oldPages:
            pages[page] = calculatePR(corpus, page, oldPages, damping_factor)
            if abs(pages[page]-oldPages[page]) >= 0.001:
                deviation = True
    return pages
        
    
def distributedPages(corpus, totalWeight=1):
    # Evenly distributes a provided weight across pages
    pages = {}
    num_pages = len(corpus)
    for page in corpus:
        pages[page] = totalWeight / num_pages
    return pages

def calculatePR(corpus, page, old_pagerank, damping_factor):
    """
    Calculate the PageRank for a single page within the corpus.
    
    Includes handling for dangling nodes
    """
    num_pages = len(corpus)
    dangling_rank = sum(old_pagerank[p] for p in corpus if len(corpus[p]) == 0) / num_pages
    
    incoming_links = [p for p in corpus if page in corpus[p]]
    rank_from_incoming_links = sum(old_pagerank[p] / len(corpus[p]) for p in incoming_links)
    
    new_pagerank = ((1 - damping_factor) / num_pages) + damping_factor * (dangling_rank + rank_from_incoming_links)
    
    return new_pagerank

if __name__ == "__main__":
    main()
