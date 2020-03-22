import itertools, math
from easygame import *
from constants import *

def formatuj_cislo(cislo):
    sufixy = [ '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y' ]
    exponent = 0
    while exponent+1 < len(sufixy) and cislo % 1000 == 0:
        cislo //= 1000
        exponent += 1
    return str(cislo) + sufixy[exponent]

def terminate():
    close_window()
    sys.exit()

def square_distance(pt1, pt2):
    return (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2

def total_distance(seq):
    answer = 0
    for x, y in zip( seq[:-1], seq[1:] ):
        answer += math.sqrt( square_distance(x,y) )
    return answer

def optimize_order(seq):
    best = float('inf')
    bestseq = None
    for perm in itertools.permutations(seq):
        curr = total_distance( [WAREHOUSE_POS] + list(perm) + [WAREHOUSE_POS] )
        if curr < best:
            best, bestseq = curr, perm
    return list(bestseq)

def stages_in_menu(state):
    candidates = list( range(1, state.stage+1) )
    candidates = [ ( STAGES[c].cost, c ) for c in candidates ]
    while len(candidates) > 9: candidates.remove( min(candidates) )
    return [ c[1] for c in candidates ]

