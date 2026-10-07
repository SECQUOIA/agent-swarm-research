"""Verify response completeness and render the three owned Markdown files."""
import json
import re
from fractions import Fraction as Q
from html.parser import HTMLParser
from pathlib import Path

from markdown_it import MarkdownIt

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
parser = MarkdownIt('commonmark').enable('table')
class TableRows(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables=[]; self.in_body=False
    def handle_starttag(self,tag,attrs):
        if tag=='table':self.tables.append({'heads':0,'body_rows':0})
        elif tag=='thead':self.tables[-1]['heads']+=1
        elif tag=='tbody':self.in_body=True
        elif tag=='tr' and self.in_body:self.tables[-1]['body_rows']+=1
    def handle_endtag(self,tag):
        if tag=='tbody':self.in_body=False

summaries = {}
for rel in ('open-instances-summary.md','bound-audit/audit-report.md','publication/READINESS.md'):
    p=BASE/rel; text=p.read_text(); rendered=parser.render(text)
    h=TableRows();h.feed(rendered)
    assert all(t['heads']==1 and t['body_rows']>=1 for t in h.tables),rel
    assert len(h.tables)==(5 if p.name=='open-instances-summary.md' else 10 if p.name=='audit-report.md' else 4)
    if p.name=='open-instances-summary.md':
        assert h.tables[-1]['body_rows']==43
        # Numeric table rows were not changed by this wording-only response.
        old=(OUT/'review-r1-before'/p.name).read_text()
        numeric=lambda t:[line for line in t.split('## Prior literature')[0].splitlines() if line.startswith('|')]
        assert numeric(old)==numeric(text)
    (OUT/(p.stem+'-rendered-r1.html')).write_text('<!doctype html>\n<meta charset="utf-8">\n'+rendered)
    summaries[rel]=h.tables
    print('PASS rendered HTML tables:',rel,h.tables)
r=(BASE/'publication/READINESS.md').read_text()
response=r.split('## Response to integration review r1')[1].split('## Final gap check')[0]
items=[int(re.match(r'\| (\d+)',line)[1]) for line in response.splitlines() if re.match(r'\| \d+',line)]
assert items==list(range(1,16)),items
assert 'Excluded from this implementation as instructed' in response and 'Excluded as instructed' in response
assert 'An independent review of this final integration has not been performed' not in r
print('PASS all 15 issues accounted for; 2 and 15 excluded; actual review verdict recorded')
env=json.loads((OUT/'environment-r1.json').read_text())
assert Q('47.035')<Q(env['mem_total_gib_exact'])<Q('47.045')
timings=json.loads((OUT/'runtime-evidence-r1.json').read_text())
assert timings['index_count']==443
table=r.split('| family / recorded operation | wall seconds, in listed order |')[1].split('\n\n')[0]
for entry in timings['entries']:
    value=Q(entry['wall_s'])
    shown=[Q(v) for line in table.splitlines() if line.startswith('| ') for v in re.findall(r'\d+(?:\.\d+)?',line.split('|')[2])]
    assert value in shown,entry['id']
print('PASS all selected timing values appear exactly in readiness; memory rounds correctly')
(OUT/'rendered-tables-r1.json').write_text(json.dumps(summaries,indent=2)+'\n')
