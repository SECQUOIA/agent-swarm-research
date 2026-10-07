"""W5 exact verifier: targeted checks of the renamed symbols and the small
arithmetic claims touched in this round.

1. Labels of the four exact files equal those of the pre-W5 snapshot.
2. No leftover old notation: minimizer s, H_{JJ}/nabla_J of REC, e_k, A_*,
   q_*, 'optimizer', the bracketed h* terms.
3. Exact arithmetic: lem:snap constants (3/2 n tau = 3/(8R), 1/R = 4 n tau > 2 tau),
   phase accounting of thm:boundary(b) with index k, the cover claim for h*.
"""
import os, re, itertools, random
from fractions import Fraction as Fr

root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
files = ['exact', 'exact-localized', 'appendix-localized', 'appendix-boundary']
lab = re.compile(r'\\label\{([^}]*)\}')
for f in files:
    new = open(os.path.join(root, 'sections', f + '.tex')).read()
    old = open(os.path.join(root, 'process', 'w5', 'sections-before-w5', f + '.tex')).read()
    assert lab.findall(new) == lab.findall(old), f
    bad = [r's\\in\\mathcal S', r'\\mathcal P\(s\)', r'H_\{JJ\}', r'\\nabla_JF',
           r'e_k', r'A_\*', r'q_\*', r'optimizer', r'\]\\\\?,?\s*\\\\?\[', r'\\R\^J\b']
    for b in bad:
        m = re.search(b, new)
        assert m is None, (f, b, new[max(0, m.start() - 60):m.end() + 60])
print('labels unchanged, no leftover old notation')

# lem:snap constants
for n in range(1, 30):
    for R in [1, 2, 7, 64, 1000]:
        tau = Fr(1, 4 * n * R)
        assert Fr(3, 2) * n * tau == Fr(3, 8 * R) < Fr(1, R)
        assert Fr(1, R) == 4 * n * tau > 2 * tau

# phase accounting: sum_{mu=2}^k 2^{k-mu} < 2^{k-1}; trial mu* gets >= M* in
# phase k* = mu* + ceil(log2 M*); total over phases <= 2^{k*} <= 2*2^{mu*}*M*
for mu in range(2, 12):
    for M in range(1, 300):
        ks = mu + (M - 1).bit_length()          # ceil(log2 M) for M >= 1
        assert 2 ** (ks - mu) >= M
        assert all(sum(2 ** (k - m) for m in range(2, k + 1)) < 2 ** (k - 1)
                   for k in range(2, ks + 1))
        total = sum(sum(2 ** (k - m) for m in range(2, k + 1)) for k in range(2, ks + 1))
        assert total <= 2 ** ks <= 2 * 2 ** mu * M

# h*: I_Z cap P and I_C cup (I_Z minus P) cover [n] for every split
random.seed(1)
for _ in range(2000):
    n = random.randint(1, 8)
    IZ = {i for i in range(n) if random.random() < 0.5}
    P = {i for i in range(n) if random.random() < 0.5}
    IC = set(range(n)) - IZ
    assert (IZ & P) | IC | (IZ - P) == set(range(n))
    assert (IZ & P) or (IC | (IZ - P))
print('PASS')
