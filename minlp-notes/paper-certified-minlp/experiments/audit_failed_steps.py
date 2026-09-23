#!/usr/bin/env python3
"""Recompute the twelve first-failed lin steps independently with Fraction.

Uses the shared row parser, but not the kernel's linear-combination arithmetic.
With --extract reads bounded proof prefixes and writes small exact witnesses.
Without --extract checks those portable witnesses without any large proof file.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys


def plain(row):
    return {'sense':row.sense,'rhs':str(row.rhs),'coefficients':{str(k):str(v) for k,v in row.coefficients.items()}}


def extract(lab,evidence,out):
    sys.path.insert(0,str(lab))
    from certify.vipr import _header,_records,_Tokens,_row
    records=json.loads(evidence.read_text())['results']
    out.mkdir(parents=True,exist_ok=True)
    for record in records:
        name=record['instance'];target=record['derivation'];path=lab/'results/cert'/name/'master_complete.vipr'
        with path.open(encoding='ascii') as f:
            h=_header(f);m=len(h['rows'])
            for offset,fields,_ in _records(f,h['derivations']):
                if m+offset==target:
                    b=fields.index('{');assert fields[b+1]=='lin'
                    n=int(fields[b+2]);pairs=[(int(fields[b+3+2*i]),Q(fields[b+4+2*i])) for i in range(n)]
                    break
            else:raise AssertionError(name)
        needed={i for i,_ in pairs};sources={}
        with path.open(encoding='ascii') as f:
            h=_header(f)
            for idx,row in h['rows'].items():
                if idx in needed:sources[idx]=plain(row)
            for offset,fields,_ in _records(f,h['derivations']):
                idx=m+offset
                if idx in needed or idx==target:
                    row=_row(_Tokens(fields),h['n'],h['objective'])
                    if idx==target:claimed=plain(row);break
                    sources[idx]=plain(row)
        artifact={'instance':name,'proof_sha256_from_frozen_replay':record['proof_sha256_from_replay'],
                  'target_index':target,'claimed':claimed,
                  'sources':[{'index':i,'multiplier':str(q),**sources[i]} for i,q in pairs],
                  'recorded_combined_rhs':record['combined_rhs'],
                  'recorded_residual':record['combined_minus_claimed_rhs'],
                  'scope':'Direct justification of one recorded lin step; no assertion that preceding source rows are valid.'}
        (out/f'{name}.json').write_text(json.dumps(artifact,indent=2)+'\n')
    verify(out)


def verify(out):
    checks=[]
    for path in sorted(out.glob('*.json')):
        r=json.loads(path.read_text());total={};rhs=Q(0);senses=set()
        for source in r['sources']:
            q=Q(source['multiplier']);rhs+=q*Q(source['rhs'])
            if q and source['sense']:senses.add(source['sense']*(1 if q>0 else -1))
            for variable,value in source['coefficients'].items():total[variable]=total.get(variable,Q(0))+q*Q(value)
        total={k:v for k,v in total.items() if v}
        claimed={k:Q(v) for k,v in r['claimed']['coefficients'].items() if Q(v)}
        residual=rhs-Q(r['claimed']['rhs'])
        assert rhs==Q(r['recorded_combined_rhs']) and residual==Q(r['recorded_residual'])
        if len(senses)>1:kind='incompatible_inequality_directions'
        else:
            assert total==claimed and r['claimed']['sense']==-1 and residual>0
            kind='overstrong_upper_rhs'
        checks.append({'instance':r['instance'],'failure':kind,'exact_residual':str(residual)})
    assert len(checks)==12
    assert sum(r['failure']=='overstrong_upper_rhs' for r in checks)==11
    print(json.dumps({'checked_steps':12,'results':checks},indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--extract',action='store_true')
    ap.add_argument('--lab',type=Path);ap.add_argument('--evidence',type=Path);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    if a.extract:extract(a.lab.resolve(),a.evidence.resolve(),a.out.resolve())
    else:verify(a.out.resolve())
