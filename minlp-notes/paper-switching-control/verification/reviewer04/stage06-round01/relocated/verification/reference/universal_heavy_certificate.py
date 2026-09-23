"""Exact checks of integral rounding followed by first-repeat prefix uncrossing."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from random import Random
from adjacent_pair_flow import rounded, verify_counterexamples


def allocation(row,t):
    k = min(int(t),len(row))
    return sum(row[:k],F(0)) + (row[k]*(t-k) if k<len(row) else 0)


def deadline(row,r):
    cumulative = F(0)
    for j in range(r):
        if cumulative+row[j] > 1:
            return j+(1-cumulative)/row[j]
        cumulative += row[j]
    return F(r)


def verify_word(a,word):
    counts = [0]*len(a)
    for j,q in enumerate(word):
        counts[q] += 1
        for i,row in enumerate(a):
            assert abs(counts[i]-sum(row[:j+1],F(0))) <= 1


def uncross(a,word):
    if any(word[j] == word[j+1] for j in range(len(word)-1)):
        return word,'already_adjacent'
    seen = set()
    for position,q in enumerate(word):
        if q in seen:
            r = position+1
            break
        seen.add(q)
    else:
        raise AssertionError('Repeated mode required')
    old = Counter(word[:r])
    assert old[q] == 2 and all(v == 1 for i,v in old.items() if i != q)
    dq = deadline(a[q],r)
    ceiling = -(-dq.numerator//dq.denominator)
    j = min(r-2,max(0,ceiling-2))
    selected = sorted((i for i in old if i != q),key=lambda i:deadline(a[i],r))
    new = list(word)
    new[j] = new[j+1] = q
    slots = list(range(j))+list(range(j+2,r))
    for i,t in zip(selected,slots):
        new[t] = i
    assert Counter(new[:r]) == old
    assert new[r:] == word[r:]
    verify_word(a,new)
    return new,'uncrossed'


def construct(a):
    heavy = [i for i,row in enumerate(a) if sum(row,F(0)) > 1]
    assert heavy
    word = rounded(a,heavy[-1],repeat=True)
    assert word is not None
    verify_word(a,word)
    new,branch = uncross(a,word)
    assert sum(new[j] != new[j+1] for j in range(len(new)-1)) <= len(new)-2
    return branch


def verify():
    rng = Random(999432)
    counts = Counter()
    for M in range(3,16):
        for trial in range(100):
            n = rng.randint(3,15)
            columns = []
            for _ in range(M):
                weights = [rng.randrange(8) for _ in range(n)]
                weights[0] += 15
                if trial%2:
                    weights[1] += 15
                columns.append([F(w,sum(weights)) for w in weights])
            a = [list(row) for row in zip(*columns)]
            if max(sum(row,F(0)) for row in a) > 1:
                counts[construct(a)] += 1
    for M in range(3,8):
        for word in product(range(3),repeat=M):
            if any(word[j] == word[j+1] for j in range(M-1)):
                continue
            if max(Counter(word).values()) <= 1:
                continue
            a = [[F(int(i==q)) for q in word] for i in range(3)]
            counts[construct(a)] += 1
    verify_counterexamples()
    print(f'Universal heavy-mode construction: {sum(counts.values())} exact profiles passed; {dict(counts)}.')


if __name__ == '__main__':
    verify()
