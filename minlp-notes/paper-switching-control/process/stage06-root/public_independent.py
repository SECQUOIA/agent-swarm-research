"""Root's independent integer-arithmetic audit; not the paper implementation."""
from fractions import Fraction as Q
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

SOURCE = Path('/tmp/cia-paper-root-public.csv')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == '1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883'
lines = [line.split() for line in SOURCE.read_text().splitlines()[1:]]
assert len(lines) == 12001
prefix = [(0, 0, 0)]
max_normalization = Q(0)
max_quantization = Q(0)
for j, line in enumerate(lines[:-1]):
    assert Q(line[0]) == Q(j, 1000)
    values = list(map(Q, line[3:]))
    rates = [x / sum(values) for x in values]
    max_normalization = max(max_normalization, *(abs(a-b) for a,b in zip(values, rates)))
    ideal = [x * 1000000 for x in rates]
    apportioned = [x.numerator // x.denominator for x in ideal]
    ranking = sorted(range(3), key=lambda i: (-(ideal[i]-apportioned[i]), i))
    for i in ranking[:1000000-sum(apportioned)]:
        apportioned[i] += 1
    max_quantization = max(max_quantization, *(abs(x-Q(y,1000000)) for x,y in zip(rates,apportioned)))
    assert sum(apportioned) == 1000000
    prefix.append(tuple(a+b for a,b in zip(prefix[-1], apportioned)))
assert max_quantization < Q(1,1000000)
assert max_normalization < Q(4959, 10**10)
assert Q(lines[-1][0]) == 12


def evaluate(word, ends):
    counts = [0,0,0]
    previous = 0
    error = 0
    for mode, end in zip(word, ends):
        counts[mode] += (end-previous)*1000000
        error = max(error, *(abs(a-b) for a,b in zip(prefix[end], counts)))
        previous = end
    return error


out = {'normalization_rate_bound': str(max_normalization),
       'quantization_rate_bound': str(max_quantization),
       'terminal_masses': [str(Q(x,10**9)) for x in prefix[-1]], 'coarse': []}
best = (min(evaluate((i,), (12000,)) for i in range(3)), None)
for boundary in range(1,12000):
    for p,q in product(range(3), repeat=2):
        if p == q:
            continue
        error = evaluate((p,q), (boundary,12000))
        if error < best[0]:
            best = (error, {'word':[p,q], 'switches':[str(Q(boundary,1000))]})
out['fine_one_switch'] = {'error':str(Q(best[0],10**9)), **best[1]}
for M in (12,24,48):
    boundaries = tuple(range(12000//M,12000,12000//M))
    best = (10**20, None)
    for s in range(4):
        for ends in combinations(boundaries,s):
            for word in product(range(3), repeat=s+1):
                if any(a == b for a,b in zip(word,word[1:])):
                    continue
                error = evaluate(word, ends+(12000,))
                if error < best[0]:
                    best = (error, {'word':word, 'switches':[str(Q(t,1000)) for t in ends]})
        out['coarse'].append({'cells':M,'budget':s,'error':str(Q(best[0],10**9)),**best[1]})
print(json.dumps(out, indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
