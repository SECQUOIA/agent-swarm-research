"""Check final documents against exact saved integration quantities."""
import csv,json,re
from fractions import Fraction as Q
from pathlib import Path
from markdown_it import MarkdownIt
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
S=BASE/'open-instances-summary.md';A=BASE/'bound-audit/audit-report.md';R=BASE/'publication/READINESS.md'
texts={p:p.read_text() for p in (S,A,R,OUT/'commands.md')}
G=json.loads((OUT/'gap-values.json').read_text())
def gap_cell(text,expected):
    tokens=re.findall(r'\d+(?:\.\d+)?(?:e[+-]?\d+)?%?',text.split('(')[0])
    value=Q(tokens[0].rstrip('%'))
    assert value>=Q(G[expected]['exact_upper']),(expected,text,G[expected])
    assert value==Q(G[expected]['display_value']),(expected,'wrong checked display')
    print('PASS gap cell',expected,text.strip())
s=texts[S]
sections=re.split(r'^## ',s,flags=re.M)
closed=next(x for x in sections if x.startswith('Instances closed'))
rows=[line.split('|') for line in closed.splitlines() if line.startswith('| ')][1:]
expanded=[]
for col in rows:
    name=col[1].strip()
    if name in ('chain50–400','catmix100–800'):
        ns=(50,100,200,400) if name.startswith('chain') else (100,200,400,800)
        expanded.extend(name.split('–')[0].rstrip('0123456789')+str(n) for n in ns)
        values=[Q(x) for x in re.findall(r'\d+(?:\.\d+)?e[+-]?\d+',col[5])]
        if name.startswith('chain'):assert values==[Q('1.01e-14')] and all(values[0]>=Q(G[f'chain{n}']['exact_upper']) for n in ns)
        else:assert all(v>=Q(G[f'catmix{n}']['exact_upper']) for n,v in zip(ns,values)) and len(values)==4
        print('PASS grouped gaps',name)
    else:
        key='pricing050' if name.startswith('pricing') else name;expanded.append(key);gap_cell(col[5],key)
assert len(expanded)==31
kan=next(x for x in sections if x.startswith('Relaxation certified'))
for line in kan.splitlines():
    col=line.split('|')
    if line.startswith('| kan_') and len(col)==4:gap_cell(col[2],col[1].strip())
improved=next(x for x in sections if x.startswith('Instances substantially'))
for line in improved.splitlines():
    if line.startswith('| waterno') or line.startswith('| ann_'):
        col=line.split('|');name=col[1].strip();gap_cell(col[5],'ann' if name.startswith('ann') else name)
        if name=='waterno2_06':
            values=re.findall(r'(\d+\.\d+)%',col[5]);assert [Q(v) for v in values]==[Q(G[k]['display_value']) for k in [name,name+' separator',name+' wave2']]
        if name.startswith('ann'):assert Q(re.findall(r'(\d+)%',col[5])[0])>=Q(G['ann wave3 primal']['exact_upper'])
lit=next(x for x in sections if x.startswith('Prior literature'))
names=[line.split('|')[1].strip() for line in lit.splitlines() if line.startswith('| ')][1:]
campaign=list(csv.DictReader((BASE/'publication/solver-runs/results_table.csv').read_text().splitlines()))
assert len(names)==43 and len(set(names))==43 and set(names)=={x['instance'] for x in campaign}
print('PASS literature covers all 43 instances exactly once; 31 closed')
# Parse actual Markdown tables: every source row must attach to its header.
# Source-width checks also catch excess cells which Markdown would discard.
parser=MarkdownIt('commonmark').enable('table')
def check_tables(text,label):
    lines=text.splitlines();tokens=parser.parse(text)
    covered=set();fenced=set();tables=[]
    for token in tokens:
        if token.type=='fence':fenced.update(range(*token.map))
        if token.type!='table_open':continue
        start,end=token.map;covered.update(range(start,end))
        width=len(re.split(r'(?<!\\)\|',lines[start]))
        for no in range(start,end):
            fields=re.split(r'(?<!\\)\|',lines[no])
            assert fields[0]==fields[-1]=='' and len(fields)==width,(label,no+1,'table width')
        tables.append((start+1,end-2-start,width-2))
    orphan=[i+1 for i,line in enumerate(lines) if line.startswith('|') and i not in covered and i not in fenced]
    assert not orphan,(label,'table rows detached from header',orphan)
    assert all(rows>=1 for _,rows,_ in tables),(label,'empty table')
    return tables
for p in (S,A,R):
    tables=check_tables(texts[p],str(p))
    if p==S:assert any(rows==43 and cols==3 for _,rows,cols in tables)
    print('PASS rendered table header attachment',p.name,tables)
original=(OUT/'review-r1-before'/S.name).read_text()
try:check_tables(original,'original broken literature table')
except AssertionError as exc:
    assert 'table rows detached from header' in str(exc)
    print('PASS negative control: original literature table is rejected')
else:raise AssertionError('broken literature table was accepted')
print('PASS all three documents: Markdown table parsing, row widths and header attachment')
for p,text in texts.items():
    # Recorded commands may contain literal Markdown; only rendered links count.
    for token in parser.parse(text):
        for child in token.children or []:
            if child.type!='link_open':continue
            target=child.attrGet('href')
            if '://' in target or target.startswith('#'):continue
            path=target.split('#')[0];assert (p.parent/path).exists(),(p,'missing link',target)
print('PASS all local Markdown links')
for stale in ('1.67%','0.0693 for n8','(exact value of the certificate)','no\nexactly feasible point was constructed','partly by sampling','1.4e-6 relative'):
    assert stale not in s,stale
for name in ('eg_int_s','eg_disc_s','eg_disc2_s'):
    row=next(x for x in s.splitlines() if x.startswith('| '+name+' |'));assert 'A1/A2' in row
assert 'A1**' in s and 'A2**' in s
assert 'drafted and has NOT been submitted' in s and 'drafted and has NOT been submitted' in texts[A]
assert 'SCIP on ex6_2_5, ex6_2_7 and pindyck' in texts[R]
print('PASS stale current claims absent; assumptions/filing/decisions explicit')
# Confirm the applied-list split without changing protected originals.
records=json.loads((OUT/'replacements.json').read_text());assert len(records)==40 and sum(r['applied_to_original'] for r in records)==33
print('PASS ordered replacement record: 40 validated, 33 owned, 7 protected')
print('ALL DOCUMENT CHECKS PASSED')
