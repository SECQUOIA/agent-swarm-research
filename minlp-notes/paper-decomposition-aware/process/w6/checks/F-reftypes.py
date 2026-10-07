"""F-consistency: check that the word before each \ref matches the environment type of the label (from cleveref data in main.aux)."""
import re, glob, os
aux = open('/tmp/dpaper/out/main.aux').read()
typ = {}
for m in re.finditer(r'\\newlabel\{([^}]*)@cref\}\{\{\[([^\]]*)\]', aux):
    typ[m.group(1)] = m.group(2)
words = {'Theorem':'theorem','Theorems':'theorem','Thm.':'theorem','Thms.':'theorem','Lemma':'lemma','Lemmas':'lemma',
 'Proposition':'proposition','Propositions':'proposition','Corollary':'corollary','Cor.':'corollary','Example':'example',
 'Remark':'remark','Definition':'definition','Algorithm':'algorithm','Section':'section|subsection|subsubsection|paragraph',
 'Sections':'section|subsection|subsubsection|paragraph','Appendix':'appendix|subappendix|section|subsection','Appendices':'appendix|subappendix|subsection',
 'Table':'table','Figure':'figure'}
bad = []
for f in sorted(glob.glob('sections/*.tex')):
    txt = open(f).read()
    for m in re.finditer(r'(\w+\.?)~\\ref\{([^}]*)\}', txt):
        w, lab = m.group(1), m.group(2)
        if w not in words: continue
        t = typ.get(lab)
        if t is None: bad.append((f, w, lab, 'NOLABEL')); continue
        if not re.fullmatch(words[w], t): bad.append((f, txt[:m.start()].count('\n')+1, w, lab, t))
for b in bad: print(b)
print('checked; mismatches:', len(bad))
