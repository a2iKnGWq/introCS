from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    loca = a.split('\n')
    locb = b.split('\n')
    return out(loca, locb)


def sentences(a, b):
    """Return sentences in both a and b"""

    loca = sent_tokenize(a)
    locb = sent_tokenize(b)
    return out(loca, locb)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    loca = helper(a, n)
    locb = helper(b, n)
    return out(loca, locb)

def helper(a, n):
    absloc = []
    for i in range(len(a)-n+1):
        absloc.append(a[i:(i+n)])   #a[i:n + i]
    return absloc


def out(loca, locb):
    locz = []
    for i in loca:
        for j in locb:
            if i == j:
                if i not in locz:
                    locz.append(i)    
    return locz