"""Compare copied /tmp replay and paper data using exact rational arithmetic."""
import ast
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path('/tmp/kan-guard')
HERE = ROOT/'checks'
NAMES = ['kan_r3_h1_n4','kan_r3_h1_n5','kan_r3_h1_n9',
         'kan_r5_h1_n3','kan_r5_h1_n5','kan_r5_h1_n8']

def normalized(path):
    tree=ast.parse(path.read_text())
    tree.body=tree.body[1:]  # descriptive module docstring
    tree.body=[n for n in tree.body if not
        (isinstance(n,ast.FunctionDef) and n.name in ('minquad','_minquad_exact')) and not
        (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MINQUAD_STATS' for t in n.targets))]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='dict':
            node.keywords=[k for k in node.keywords if k.arg!='minquad_stats']
    return ast.dump(tree,include_attributes=False)
assert normalized(HERE/'original_kan_bnb_rigexp.py') == normalized(HERE/'kan_bnb_rigexp.py')
print('PASS unchanged AST outside minquad, its counters/fallback, result counter field, and module description')
paper=json.loads((ROOT/'archive/numbers.json').read_text())
printed_lines=(ROOT/'archive/tab-kan.tex').read_text().splitlines()
manifest=json.loads((HERE/'replay-manifest.json').read_text())
assert hashlib.sha256((HERE/'kan_bnb_rigexp.py').read_bytes()).hexdigest()==manifest['source_hashes']['checks/kan_bnb_rigexp.py']
assert hashlib.sha256((HERE/'original_kan_bnb_rigexp.py').read_bytes()).hexdigest()=='82ca1dbd5def9b4bb2b701650e6961b53833f0074383dce20e509d7a86b29b33'
rows=[]
for name in NAMES:
    replay_path=HERE/'logs'/(name+'.bnb.json')
    if not replay_path.exists():
        if '--partial' in sys.argv: continue
        raise RuntimeError('Missing replay: '+name)
    new=json.loads(replay_path.read_text())
    old=json.loads((ROOT/'archive'/(name+'.bnb.json')).read_text())
    log=(ROOT/'archive'/(name+'.rigexp.log')).read_text()
    log_result=json.loads(log[log.index('{'):])
    assert log_result==old
    assert paper['kan'][name]['L']==paper['instances'][name]['L']
    metadata=paper['kan'][name]
    paper_exact=F(metadata['L']['exact'])
    paper_display=F(metadata['L']['display'])
    printed_line=next(line for line in printed_lines if '\\inst{'+name+'}' in line and '&' in line)
    assert F(printed_line.split('&')[3].strip().strip('$'))==paper_display
    assert paper_display<=paper_exact
    assert metadata['size']['osil_sha256']==hashlib.sha256((ROOT/'osil'/(name+'.osil')).read_bytes()).hexdigest()
    assert new['done'] and new['open']==0
    stats=new['minquad_stats']
    assert stats['guard_calls']==stats['fallback_calls']
    assert stats['guard_entries']==stats['fallback_entries']
    changed={key:dict(old=old[key],new=new[key]) for key in old if key!='time' and old[key]!=new[key]}
    delta=F(new['lower_bound'])-F(old['lower_bound'])
    margin=F(new['lower_bound'])-paper_exact
    display_margin=F(new['lower_bound'])-paper_display
    row=dict(instance=name,L_ver=repr(new['lower_bound']),L_ver_hex=new['lower_bound'].hex(),
        previous_L_ver=repr(old['lower_bound']),previous_L_ver_hex=old['lower_bound'].hex(),
        previous_delta_exact=str(delta),changed_archive_fields=changed,
        processed=new['processed'],open=new['open'],done=new['done'],
        calls=stats['calls'],entries=stats['entries'],guard_calls=stats['guard_calls'],
        guard_entries=stats['guard_entries'],fallback_calls=stats['fallback_calls'],
        fallback_entries=stats['fallback_entries'],guard_reasons=stats['reasons'],
        reported_L_display=metadata['L']['display'],reported_L_exact=str(paper_exact),
        margin_above_reported_exact=str(margin),margin_above_reported_display=str(display_margin),
        confirms_exact_reported_L=margin>=0,confirms_displayed_L=display_margin>=0,
        elapsed_seconds=new['time'])
    print(name,'L_ver',row['L_ver'],'nodes',row['processed'],'calls',row['calls'],
          'entries',row['entries'],'guards',row['guard_entries'],'fallbacks',row['fallback_entries'],
          'old delta',str(delta),'above exact paper L',format(float(margin),'.12g'))
    if margin<0 or display_margin<0:
        print('WARNING: REPLAY LOWER BOUND IS BELOW A REPORTED PAPER LOWER BOUND:',name)
    rows.append(row)
if '--partial' not in sys.argv:
    out=dict(rows=rows,all_six_complete=len(rows)==6,
             all_reported_bounds_confirmed=all(r['confirms_exact_reported_L'] and r['confirms_displayed_L'] for r in rows))
    (HERE/'comparison.json').write_text(json.dumps(out,indent=2)+'\n')
    assert out['all_six_complete']
