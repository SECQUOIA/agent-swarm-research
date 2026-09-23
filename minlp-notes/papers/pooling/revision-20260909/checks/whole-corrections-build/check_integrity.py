"""Compare editorial changes with the source snapshot; run from papers/pooling."""
from collections import Counter
import difflib
from pathlib import Path
import re

base = Path('revision-20260909/checks/whole-corrections-build')
files = [Path('main.tex'), Path('bibliography.bib')]
files += sorted(p for folder in ('sections', 'appendices', 'figures')
                for p in Path(folder).glob('*.tex'))
diff = []
envs = 'theorem|lemma|proposition|corollary|definition|example|remark|proof'


def terminology(s):
    s = re.sub(r'\b[Oo]utput(s?)\b',
               lambda m: ('Product' if m[0][0].isupper() else 'product') + m[1], s)
    return re.sub(r'\ban(\s+products?\b)', r'a\1', s)


def blocks(s):
    return [m[0] for m in re.findall(
        r'(\\begin\{(' + envs + r')\}.*?\\end\{\2\})', s, re.S)]


def math(s):
    return re.findall(
        r'\$(?:[^$\\]|\\.)*\$|\\\[.*?\\\]|'
        r'\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}.*?'
        r'\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?)\}', s, re.S)


counts = Counter()
new_labels = []
for f in files:
    old, new = (base / 'before' / f).read_text(), f.read_text()
    if old != new:
        diff.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                       fromfile='before/' + str(f), tofile='after/' + str(f)))
    if f.suffix != '.tex':
        continue
    a, b = blocks(old), blocks(new)
    assert len(a) == len(b), (f, 'formal environment count')
    for i, (x, y) in enumerate(zip(a, b)):
        assert terminology(x) == terminology(y), (f, i, 'formal content')
    assert math(old) == math(new), (f, 'mathematical fragments changed')
    a = re.findall(r'\\label\{([^}]+)\}', old)
    b = re.findall(r'\\label\{([^}]+)\}', new)
    assert [label for label in b if label in a] == a, (f, 'existing labels')
    new_labels.extend(label for label in b if label not in a)
    counts.update(re.findall(r'\\begin\{(' + envs + r')\}', new))
    assert not re.search(r'\ban\s+products?\b', new), (f, 'article agreement')

assert counts['proof'] == 93
assert sum(v for k, v in counts.items() if k not in ('proof', 'remark')) == 95
assert new_labels == ['s3:refinement-guide']
(base / 'source.diff').write_text(''.join(diff))
log = (
    f'Environment counts: {dict(counts)}\n'
    '95 formal claims (including 3 examples), 2 remarks, 93 proofs retained.\n'
    'All formal statements and proofs unchanged after only physical product terminology '
    'and associated a/an normalization.\n'
    'All inline/display mathematical fragments byte-identical.\n'
    'All existing labels retained in order; only new label: s3:refinement-guide.\n'
    'No article-agreement errors from an output -> a product remain.\n'
)
(base / 'integrity.txt').write_text(log)
print(log)
