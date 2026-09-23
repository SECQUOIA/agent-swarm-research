#!/usr/bin/env python3
"""Extract and examine the three new external-OK/internal-rejected steps."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import sys


def main():
    a=argparse.ArgumentParser();a.add_argument('--lab',type=Path,required=True);a.add_argument('--campaign',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args()
    sys.path.insert(0,str(args.lab.resolve()))
    from certify.vipr import _header,_records,_row,_Tokens
    args.out.mkdir(parents=True,exist_ok=True)
    def plain(row):return{'label':row.label,'sense':row.sense,'rhs':str(row.rhs),'coefficients':{str(k):str(v)for k,v in row.coefficients.items()}}
    summaries=[]
    for name,target in [('smallinvDAXr1b200-220',4082),('smallinvDAXr3b100-110',1639),('smallinvDAXr4b200-220',26121)]:
        path=args.campaign/'replay-artifacts'/name/'master_complete.vipr'
        with path.open()as f:
            h=_header(f);m=len(h['rows'])
            for off,tokens,_ in _records(f,h['derivations']):
                if m+off==target:
                    pos=tokens.index('{');reason=tokens[pos+1]
                    if reason=='uns':refs=[int(s)for s in tokens[pos+2:pos+6]];multipliers=None
                    else:
                        assert reason=='lin';n=int(tokens[pos+2]);refs=[int(tokens[pos+3+2*i])for i in range(n)];multipliers=[tokens[pos+4+2*i]for i in range(n)]
                    target_tokens=tokens;break
            else:raise AssertionError(name)
        found={}
        with path.open()as f:
            h=_header(f)
            found={k:{**plain(v),'justification':'input'}for k,v in h['rows'].items()if k in refs}
            for off,tokens,_ in _records(f,h['derivations']):
                idx=m+off
                if idx in refs or idx==target:
                    found[idx]={**plain(_row(_Tokens(tokens),h['n'],h['objective'])),'justification':' '.join(tokens[tokens.index('{'):])}
                if idx==target:break
        report={'instance':name,'target_index':target,'reason':reason,'integer_indices':sorted(h['integers']),
                'target':found[target],'antecedents':[{'index':i,**found[i]}for i in refs],'multipliers':multipliers,
                'scope':'Local supplied inference only; no claim that all preceding rows are valid.'}
        if reason=='lin':
            directions=[];coeff={};rhs=Q(0)
            for ref,q in zip(refs,map(Q,multipliers)):
                row=found[ref];direction=row['sense']*(1 if q>0 else -1)if q else 0
                if direction:directions.append(direction)
                rhs+=q*Q(row['rhs'])
                for k,v in row['coefficients'].items():coeff[k]=coeff.get(k,Q(0))+q*Q(v)
            report['multiplied_senses']=directions;report['combined_rhs']=str(rhs)
            report['combined_coefficients']={k:str(v)for k,v in coeff.items()if v}
            report['source_tautologies']=[r['index']for r in report['antecedents']if not r['coefficients']and(r['sense']<0 and Q(r['rhs'])>=0 or r['sense']>0 and Q(r['rhs'])<=0 or r['sense']==0 and Q(r['rhs'])==0)]
            report['summary']={'multiplied_senses':sorted(set(directions)),'source_tautologies':report['source_tautologies'],'antecedents':len(refs)}
        else:
            a,b=found[refs[1]],found[refs[3]];low,high=(a,b)if a['sense']<0 else(b,a)
            report['summary']={'low':low,'high':high,'same_coefficients':low['coefficients']==high['coefficients'],'rhs_difference':str(Q(high['rhs'])-Q(low['rhs'])),'all_form_variables_integer':all(int(i)in h['integers']for i in low['coefficients'])}
        (args.out/f'{name}.json').write_text(json.dumps(report,indent=2)+'\n')
        summaries.append({'instance':name,**report['summary']})
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
