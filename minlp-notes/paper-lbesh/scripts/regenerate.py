#!/usr/bin/env python3
"""Regenerate paper tables, CSV data and PDF figures from compact frozen records.

Only matplotlib is required beyond the standard library (use --no-figures to
regenerate tables without it). No repository imports, solvers, or network calls.
"""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean, median

P = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--no-figures', action='store_true')
args = parser.parse_args()
load = lambda name: json.loads((P/'data'/name).read_text())
provenance = load('provenance.json')
for name, sha in provenance['data_sha256'].items():
    assert hashlib.sha256((P/'data'/name).read_bytes()).hexdigest() == sha, name
R = load('records.json')
assert len(R) == 1464
assert len({(r['run'],r['instance'],r['method']) for r in R}) == 1464
expected = {'main_generated_v1':663,'repeat_heldout_v1_r2':132,'repeat_heldout_v1_r3':132,'quadratic_conic_v1':9,'legacy_external_v1':351,'ablations_pilot_v1':144,'gurobi_trig_sensitivity_v1':9,'legacy_initialization_v1':24}
assert Counter(r['run'] for r in R) == expected
assert not any(r['inconsistent_bound'] or r['contradictions'] for r in R)
M = 'main_generated_v1'
configs = [('hull','single'),('hull','multi'),('bigm','single'),('bigm','multi')]
methods = [f'lbesh-{o}-{f}-{t}' for f,t in configs for o in ('esh','ecp')]
labels = {m:f'{o.upper()} {"hull" if f=="hull" else "big-M"} {t}' for (f,t) in configs for o in ('esh','ecp') for m in [f'lbesh-{o}-{f}-{t}']}
labels.update({'gdpopt-loa':'GDPopt LOA','gams-shot-bigm':'SHOT big-M','gams-shot-hull-convex':r'SHOT $\eps$-hull (convex)','gams-gurobi-bigm':'Gurobi big-M','gams-scip-bigm':'SCIP big-M','conic-hull-gurobi':'Exact conic hull'})
base = methods + ['gdpopt-loa','gams-shot-bigm','gams-shot-hull-convex','gams-gurobi-bigm','gams-scip-bigm']
def select(run=M, method=None, split=None, **kw):
    return [r for r in R if r['run']==run and (method is None or r['method']==method) and (split is None or r['split']==split) and all(r[k]==v for k,v in kw.items())]
def sgm(rows):
    return math.expm1(mean(math.log1p(r['wall_time']) for r in rows))
def par(rows):
    return mean(min(150,r['wall_time']) if r['solved'] else 1500 for r in rows)
def pair(a,b,run=M,split='held_out',names=None,**kw):
    aa={r['instance']:r for r in select(run,a,split,**kw) if r['solved']}
    bb={r['instance']:r for r in select(run,b,split,**kw) if r['solved']}
    common=sorted(aa.keys() & bb.keys() & (set(names) if names is not None else aa.keys()))
    return [aa[n] for n in common],[bb[n] for n in common]
def pname(f,t): return ('Hull' if f=='hull' else 'Big-M')+' '+t
ledger={}
def table(name,columns,headers,rows):
    s='\\begin{tabular}{'+columns+'}\n\\toprule\n'+' & '.join(headers)+r' \\'+'\n\\midrule\n'
    s+='\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n'
    (P/'tables'/f'{name}.tex').write_text(s)
    ledger[name]={'headers':headers,'rows':rows}
rows=[]
for m in base:
    a,b,c=select(method=m,split='held_out'),select(method=m,split='pilot'),select(method=m)
    assert (len(a),len(b),len(c))==(33,18,51)
    rows.append([labels[m],sum(r['solved'] for r in a),sum(r['solved'] for r in b),sum(r['solved'] for r in c),f'{par(a):.2f}'])
table('primary','lrrrr',['Method','Held out /33','Pilot /18','All /51','Held-out PAR10'],rows)
rows=[];pairdata={}
for f,t in configs:
    a,b=pair(f'lbesh-esh-{f}-{t}',f'lbesh-ecp-{f}-{t}')
    pairdata[f,t]=(a,b)
    rows.append([pname(f,t),len(a),f'{sgm(a):.3f}',f'{sgm(b):.3f}',f'{sgm(a)/sgm(b):.3f}',sum(x['wall_time']<y['wall_time'] for x,y in zip(a,b))])
table('pairs','lrrrrr',['Pair','Common','ESH (s)','ECP (s)','Ratio','ESH faster'],rows)
rows=[]
for f,t in configs:
    a,b=pairdata[f,t]
    rows.append([pname(f,t)+f'; {len(a)}']+[f'{mean(x[k] for x in a):.{d}f} / {mean(x[k] for x in b):.{d}f}' for k,d in [('cuts',1),('lp_iters',1),('nlp_solves',2),('nodes',1),('time_cuts',4)]])
table('work','lrrrrr',['Pair; common','Cuts','LP iter.','NLP solves','Nodes','Row separation (s)'],rows)
rows=[]
for f,t in configs:
    a,b=pairdata[f,t]
    rows.append([pname(f,t)]+[f'{median(x[k] for x in a):.1f} / {median(x[k] for x in b):.1f}' for k in ['cuts','lp_iters','nlp_solves','nodes']]+[f'{median(x["time_master"] for x in a):.3f} / {median(x["time_master"] for x in b):.3f}'])
table('work_medians','lrrrrr',['Pair','Cuts','LP iter.','NLP solves','Nodes','Master time (s)'],rows)
rows=[]
for key,groups in [('family',['exp','log','logsumexp','quadratic','reciprocal','trig']),('size',['small','medium','large'])]:
    for g in groups:
        row=[g]
        for f,t in configs:
            a,b=pair(f'lbesh-esh-{f}-{t}',f'lbesh-ecp-{f}-{t}',**{key:g})
            row.append(f'{sgm(a)/sgm(b):.3f} ({len(a)})')
        rows.append(row)
table('family_size','lrrrr',['Stratum','Hull single','Hull multi','Big-M single','Big-M multi'],rows)
rows=[]
for title,first,second in [('Hull / big-M, single','hull-single','bigm-single'),('Hull / big-M, multi','hull-multi','bigm-multi'),('Single / multi, hull','hull-single','hull-multi'),('Single / multi, big-M','bigm-single','bigm-multi')]:
    row=[title]
    for o in ['esh','ecp']:
        a,b=pair(f'lbesh-{o}-{first}',f'lbesh-{o}-{second}')
        row.append(f'{sgm(a)/sgm(b):.3f} ({len(a)})')
    rows.append(row)
table('structure','lrr',['Contrast','ESH ratio (common)','ECP ratio (common)'],rows)
runs=[M,'repeat_heldout_v1_r2','repeat_heldout_v1_r3']
rows=[]
for f in ['hull','bigm']:
    pairs=[pair(f'lbesh-esh-{f}-single',f'lbesh-ecp-{f}-single',run) for run in runs]
    names=set.intersection(*[set(r['instance'] for r in a) for a,b in pairs])
    row=[pname(f,'single')+f'; {len(names)}']
    for run in runs:
        a,b=pair(f'lbesh-esh-{f}-single',f'lbesh-ecp-{f}-single',run,names=names)
        row.append(f'{sgm(a):.3f} / {sgm(b):.3f}; {sgm(a)/sgm(b):.3f}')
    rows.append(row)
table('repetitions','lrrr',['Pair; fixed common','Run 1: ESH/ECP; ratio','Run 2','Run 3'],rows)
rows=[]
for f in ['hull','bigm']:
    for o in ['esh','ecp']:
        m=f'lbesh-{o}-{f}-single'; groups=[select(run,m,'held_out') for run in runs]
        cat={n:{r['category'] for g in groups for r in g if r['instance']==n} for n in [r['instance'] for r in groups[0]]}
        assert all(len(v)==1 for v in cat.values())
        rows.append([labels[m],'/'.join(str(sum(r['solved'] for r in g)) for g in groups),'/'.join(f'{par(g):.3f}' for g in groups)])
table('repeat_outcomes','lrr',['Method','Solved: runs 1/2/3','PAR10: runs 1/2/3'],rows)
rows=[]
for m in ['conic-hull-gurobi']+methods:
    run='quadratic_conic_v1' if m=='conic-hull-gurobi' else M
    a,b=select(run,m,'held_out',family='quadratic'),select(run,m,family='quadratic')
    assert all(r['solved'] for r in b) and len(a)==6 and len(b)==9
    rows.append([labels[m],f'{sgm(a):.3f}',f'{sgm(b):.3f}'])
table('quadratic','lrr',['Method','Held out (6)','All quadratic (9)'],rows)
scope=load('legacy_scope.json');norm=set(scope['nonsmooth_norm_objectives']);smooth=set(scope['without_norm_objectives'])
rows=[]
for m in methods+['gdpopt-loa','gams-shot-bigm','gams-gurobi-bigm','gams-scip-bigm','conic-hull-gurobi']:
    a=select('legacy_external_v1',m)
    rows.append([labels[m],sum(r['solved'] for r in a),sum(r['solved'] and r['instance'] in smooth for r in a),sum(r['solved'] and r['instance'] in norm for r in a),sum(r['category']=='error' for r in a)])
table('legacy','lrrrr',['Method','All /27','No norm /21','Norm /6','Errors'],rows)
rows=[]
for f,t in configs:
    a,b=pair(f'lbesh-esh-{f}-{t}',f'lbesh-ecp-{f}-{t}','legacy_external_v1',split=None,names=smooth)
    rows.append([pname(f,t),len(a),f'{sgm(a):.3f}',f'{sgm(b):.3f}',f'{sgm(a)/sgm(b):.3f}'])
table('legacy_pairs','lrrrr',['Pair','Common /21','ESH (s)','ECP (s)','Ratio'],rows)
rows=[]
for f in ['hull','bigm']:
    for o in ['esh','ecp']:
        m=f'lbesh-{o}-{f}-single';d=select(M,m,'pilot');n=select('ablations_pilot_v1',m+'-nonlp');u=select('ablations_pilot_v1',m+'-usercuts')
        ud={r['instance']:r for r in u}; common=[r for r in d if r['solved'] and ud[r['instance']]['solved']];uv=[ud[r['instance']] for r in common]
        rows.append([labels[m].replace(' single',''),sum(r['solved'] for r in d),sum(r['solved'] for r in n),sum(r['solved'] for r in u),f'{sgm(uv)/sgm(common):.3f}',int(sum(r['user_cuts'] for r in u)),sum(r['user_cuts']>0 for r in u)])
table('ablations','lrrrrrr',['Method','Default','No int. NLP','User cuts','Time ratio','Cuts','Cases'],rows)
rows=[]
for f,t in configs:
    a={r['instance']:r for r in select(method=f'lbesh-esh-{f}-{t}')};b={r['instance']:r for r in select(method=f'lbesh-ecp-{f}-{t}')}
    for n in sorted(a):
        if a[n]['solved']!=b[n]['solved']:
            assert a[n]['solved'];rows.append([n.removeprefix('lbesh.'),a[n]['split'].replace('_',' '),pname(f,t),f'{a[n]["wall_time"]:.2f}',f'{b[n]["wall_time"]:.2f}'])
assert len(rows)==5
table('discordant','llrrr',['Instance suffix','Split','Pair','ESH (s)','ECP (s)'],rows)
rows=[]
for r in sorted(select('gurobi_trig_sensitivity_v1'),key=lambda r:({'small':0,'medium':1,'large':2}[r['size']],r['instance'])):
    b=next(x for x in select(method='gams-gurobi-bigm') if x['instance']==r['instance'])
    codes={'numerical_solve':'S','invalid_witness':'I','feasible_open_gap':'F'}
    rows.append([r['instance'].removeprefix('lbesh.trig.'),codes[b['category']],codes[r['category']],f'{b["wall_time"]:.3f}',f'{r["wall_time"]:.3f}'])
table('trig_followup','lrrrr',['Size.seed','Original','Tightened','Original (s)','Tightened (s)'],rows)
rows=[]
for m in ['gams-gurobi-bigm-initialized','gams-scip-bigm-initialized','gams-shot-bigm-initialized']:
    a=select('legacy_initialization_v1',m)
    rows.append([labels[m.removesuffix('-initialized')],len(a),sum(r['feasible'] for r in a),sum(r['solved'] for r in a),sum(r['category']=='feasible_open_gap' for r in a),sum(r['invalid_witness'] for r in a)])
table('initialization','lrrrrr',['Method','Runs','Valid','Solved','Open/missing gap','Invalid'],rows)
roots=load('cone_roots.json');rows=[]
for o in ['esh','ecp']:
    rr=[r for r in roots if r['run']==M and r['method']==f'lbesh-{o}-hull-single' and r['cone_status']=='optimal']
    vals=[(r['cone_dual_estimate']-r['lp_bound'])/max(1,abs(r['cone_primal_objective'])) for r in rr]
    assert len(vals)==40 and min(vals)>0
    rows.append([o.upper(),f'{min(vals):.2e}',f'{median(vals):.2e}',f'{max(vals):.2e}',sum(abs(v)<=1e-4 for v in vals)])
table('roots','lrrrr',['Separator','Minimum','Median','Maximum',r'$|\Delta|\le10^{-4}$ /40'],rows)
O=load('oracle.json');rows=[]
for scale in [None,1,2,4,8,16,32]:
    a=next(r for r in O['scalar'] if r['scale']==scale and r['policy']=='ecp'); b=next(r for r in O['scalar'] if r['scale']==scale and r['policy']=='esh')
    assert b['cuts']==1 and b['function_calls']==37 and b['gradient_calls']==1
    rows.append(['Base' if scale is None else str(scale),a['cuts'],a['function_calls'],a['gradient_calls'],b['cuts'],b['function_calls'],b['gradient_calls']])
table('oracle','lrrrrrr',['Scale','ECP cuts','Values','Gradients','ESH cuts','Values','Gradients'],rows)
# Per-record CSV is the full individual-outcome supplement (all methods/batches).
with (P/'data'/'records.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(R[0]));w.writeheader()
    for r in sorted(R,key=lambda x:(x['run'],x['instance'],x['method'])):
        w.writerow({k:json.dumps(v,separators=(',',':')) if isinstance(v,(list,dict)) else v for k,v in r.items()})
(P/'data'/'table_values.json').write_text(json.dumps(ledger,indent=2)+'\n')
if not args.no_figures:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(9,3.1),layout='constrained')
    aa=[sgm(a)/sgm(b) for a,b in pairdata.values()]; names=[pname(f,t) for f,t in configs]
    for ax,values,title,xlabel in [(axes[0],aa,'Matched wall time','ESH / ECP shifted mean'),(axes[1],[mean(r['time_cuts'] for r in a)/mean(r['time_cuts'] for r in b) for a,b in pairdata.values()],'Recorded row-separation time','ESH / ECP arithmetic mean')]:
        ax.barh(names,values,color='#275D85');ax.axvline(1,color='black',linewidth=.8,linestyle='--');ax.invert_yaxis();ax.set_title(title);ax.set_xlabel(xlabel)
        for i,v in enumerate(values):ax.text(v+.02,i,f'{v:.3f}',va='center',fontsize=8,bbox={'facecolor':'white','edgecolor':'none','pad':1})
        ax.set_xlim(0,max(values)*1.18)
    axes[0].set_ylabel('Held out; common solved: 32, 30, 31, 29')
    fig.savefig(P/'figures'/'cost_tradeoff.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9,3.1),layout='constrained')
    scales=[None,1,2,4,8,16,32];xx=list(range(len(scales)))
    for o,color,marker in [('ecp','#275D85','o'),('esh','#B85C22','s')]:
        rr=[next(r for r in O['scalar'] if r['scale']==s and r['policy']==o) for s in scales]
        for ax,key in zip(axes,['cuts','function_calls']):ax.plot(xx,[r[key] for r in rr],label=o.upper(),color=color,marker=marker)
    for ax,label in zip(axes,['Cuts to geometric tolerance','Total function evaluations']):ax.set_xticks(xx,['Base','1','2','4','8','16','32']);ax.set_xlabel('Equivalent-row scale a');ax.set_ylabel(label);ax.legend(frameon=False)
    fig.savefig(P/'figures'/'oracle_cost.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
print(f'Regenerated {len(ledger)} tables, full {len(R)}-record CSV'+(' and 2 PDF figures.' if not args.no_figures else '.'))
