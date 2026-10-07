# Check that the proofs moved by the recourse group in W7 are word for word,
# except the documented pointer change in the proof of thm:cv (iii).
import re
base = 'process/w7/sections-before-w7/'
cur = 'sections/'
def blocks(text):
    return re.findall(r'\\begin\{proof\}(?:\[[^\]]*\])?\n(.*?)\\end\{proof\}', text, re.S)
norm = lambda s: ' '.join(s.split())
old_cv = open(base + 'recourse-convex.tex').read()
old_cuts = open(base + 'recourse-cuts.tex').read()
nb = [norm(b) for b in blocks(open(cur + 'appendix-recourse-convex.tex').read())
      + blocks(open(cur + 'appendix-recourse-cuts.tex').read())]
for b in blocks(old_cuts)[3:6]:
    print('cut proof verbatim in Appendix D:', norm(b) in nb)
cvp = [b for b in blocks(old_cv) if '(i) A segment' in b][0]
cvn = norm(cvp).replace(
    'denominator bound; Appendix~\\ref{app:recourse-convex} gives the procedure and its analysis.',
    'denominator bound. The proof below gives the procedure and its analysis.')
print('thm:cv proof verbatim in Appendix C (modulo pointer):', cvn in nb)
for f, n in [('recourse-convex.tex', 1), ('recourse-cuts.tex', 3)]:
    s = open(cur + f).read()
    print(f, 'pointer sentences:', s.count('The proof is in Appendix~\\ref{app:cv-proof}.') + s.count('The proof is in Appendix~\\ref{app:cr-proofs}.'), 'expected', n)
