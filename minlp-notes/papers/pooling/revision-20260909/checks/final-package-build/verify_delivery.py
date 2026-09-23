"""Verify the source-only delivery build; run from any working directory."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

base = Path(__file__).resolve().parent
paper = base.parents[2]
source = base / 'pooling-latex-source'
archive = paper / 'pooling-latex-source.zip'
manifest = json.loads((base / 'source-manifest.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == {'pooling-latex-source/' + n for n in manifest}
    for name, digest in manifest.items():
        shared = paper / ('submission-README.md' if name == 'README.md' else name)
        assert sha(shared) == sha(source / name) == digest
        assert hashlib.sha256(z.read('pooling-latex-source/' + name)).hexdigest() == digest

log = (source / 'main.log').read_text()
blg = (source / 'main.blg').read_text()
checks = {
    'latex_warnings': len(re.findall(r'Warning', log)),
    'bibtex_warnings': len(re.findall(r'Warning', blg)),
    'overfull_boxes': len(re.findall(r'Overfull', log)),
    'underfull_boxes': len(re.findall(r'Underfull', log)),
    'undefined_references_or_citations': len(re.findall(r'(?:Reference|Citation).*undefined', log)),
    'multiply_defined_labels': len(re.findall(r'multiply defined', log)),
    'latex_errors': len(re.findall(r'^!', log, re.M)),
}
assert all(v == 0 for v in checks.values()), checks
tex = '\n'.join((source / n).read_text() for n in manifest if n.endswith('.tex'))
labels = re.findall(r'\\label\{([^}]+)\}', tex)
assert len(labels) == len(set(labels)) == 273
references = [k.strip() for group in re.findall(r'\\(?:[cC]ref|eqref|ref)\*?\{([^}]+)\}', tex) for k in group.split(',')]
assert not set(references) - set(labels)
aux = (source / 'main.aux').read_text()
cited = {k.strip() for group in re.findall(r'\\citation\{([^}]+)\}', aux) for k in group.split(',')}
bibitems = set(re.findall(r'\\bibitem(?:\[.*?\])?\{([^}]+)\}', (source / 'main.bbl').read_text(), re.S))
assert len(cited) == 39 and cited == bibitems
environments = Counter(re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|example|remark|proof)\}', tex))
assert environments['proof'] == 93
assert sum(v for k, v in environments.items() if k not in ('proof', 'remark')) == 95
pdf = source / 'main.pdf'
assert pdf.read_bytes().startswith(b'%PDF-')
info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
assert pages == 105
old = paper / 'revision-20260909/checks/whole-corrections-build/source/main.pdf'
text_new = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'])
text_reviewed = subprocess.check_output(['pdftotext', '-layout', str(old), '-'])
assert text_new == text_reviewed
(base / 'main-layout.txt').write_bytes(text_new)
shutil.copy2(pdf, paper / 'main.pdf')
assert sha(pdf) == sha(paper / 'main.pdf')
result = dict(checks, pages=pages, source_files=len(manifest), labels=len(labels),
              reference_uses=len(references), distinct_citations=len(cited),
              environments=dict(environments),
              extracted_text_matches_reviewed_correction_pdf=True,
              source_archive_sha256=sha(archive), pdf_sha256=sha(pdf),
              source_manifest=manifest)
(base / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'source_manifest'}, indent=2))
