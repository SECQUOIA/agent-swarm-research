import re, difflib
old = open('process/w5/sections-before-w5/limits.tex').read() + open('process/w5/sections-before-w5/optsets.tex').read()
new = open('sections/appendix-lbproduct.tex').read() + open('sections/appendix-proximal.tex').read()
def proofs(t):
    return re.findall(r'\\begin\{proof\}(.*?)\\end\{proof\}', t, re.S)
op = proofs(old); npf = proofs(new)
def norm(s): return ' '.join(s.split())
for o in op:
    on = norm(o)
    best = max(npf, key=lambda n: difflib.SequenceMatcher(None, on[:300], norm(n)[:300]).ratio())
    r = difflib.SequenceMatcher(None, on, norm(best)).ratio()
    if r < 0.999:
        print("=== ratio %.3f" % r, on[:80])
        if r > 0.6:
            sm = difflib.SequenceMatcher(None, on.split(), norm(best).split())
            for tag,i1,i2,j1,j2 in sm.get_opcodes():
                if tag!='equal':
                    print("  ", tag, ' '.join(on.split()[i1:i2])[:200], '-->', ' '.join(norm(best).split()[j1:j2])[:200])
