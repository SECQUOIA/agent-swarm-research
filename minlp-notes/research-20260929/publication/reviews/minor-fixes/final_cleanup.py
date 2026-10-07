"""Finish minor-review wording and strengthen only the new small checks."""
from pathlib import Path
p=Path(__file__).resolve().parents[2]
def replace(file,a,b):
 s=file.read_text();assert a in s,(file,a);file.write_text(s.replace(a,b))
c=p/'primal/chain/report.md'
replace(c,'**Independence:** the same agent wrote the build and check scripts in the same session, although they share no code. Under the project\'s wording this is "checked by separate code", not "verified". An independent reviewer should rerun or rewrite the check; the generator definition is short enough to recheck in a few dozen lines.','**Independence:** the original author wrote both scripts, which share no code. Independent review r1 subsequently verified the exact-feasibility and objective claims; its checks are recorded in `../../reviews/primal-chain-review-r1.md`.')
s=c.read_text();start=s.index('## Open issues (from the agent\'s structured return)');end=s.index('## Response to review',start)
s=s[:start]+'''## Remaining limitations

The dual bounds L were taken from wave 2 and the independent COPS review; this track did not recheck them. The point is exact but not rational: its coordinates lie in Q(√R), with R up to 14,507 digits. A fully rational construction was not attempted. The integration note above identifies the older dual-display corrections; the main summary's compact range is valid.

'''+s[end:];s=s.replace('- **Dual-bound displays.** Show chain50 and chain200 as 5.0722614939828627 and 5.0689173417931616.','- **Dual-bound displays.** Correct the older reports named above to 5.0722614939828627 and 5.0689173417931616; keep the main summary\'s valid compact range.');c.write_text(s)
for t in ['audit-ir','primal/powerflow']:
 replace(p/t/'report.md','Status: partial.','Status: complete; minor-review fixes applied 2026-10-03.')
replace(p/'primal/chain/minor_review_check.py',"'deviation' in line.lower()","'deviation' in line.lower() or 'max|du|' in line")
replace(p/'literature/network/checks/minor_review_check.py','waterno2_(06|09|12|18|24)','waterno2[_ ](06|09|12|18|24)')
f=p/'scip-bug/minor_review_check.py'
a='# master reruns selected every wrong seed, plus the correct p4 seed 5; raw summaries checked.\nmaster_groups=[(x,n) for x,n in groups if x.startswith(\'master_vbr_b_\')];assert sum(n for _,n in master_groups)==20'
b='''# Match every b seed to its raw default master record.
master_wrong=master_n=0
for model in ['p4','p5','pair2236','pumps_default']:
 b_lines=(p/f'logs/master_vbr_b_{model}.log').read_text().splitlines()
 default_lines=(p/f'logs/master_{model}.log').read_text().splitlines()
 selected={int(re.search(r'seed\\s+(\\d+)',x)[1]) for x in b_lines if x.startswith('master seed')}
 defaults={int(re.search(r'seed\\s+(\\d+)',x)[1]):x.endswith('WRONG') for x in default_lines if x.startswith('master seed')}
 assert selected<=defaults.keys()
 master_n+=len(selected);master_wrong+=sum(defaults[k] for k in selected)
 print('matched master',model,'wrong',sum(defaults[k] for k in selected),'of',len(selected))
assert (master_wrong,master_n)==(19,20)'''
replace(f,a,b)
f=p/'primal/dtoc5-lukvle10/minor_review_check.py'
with f.open('a') as out:out.write('''\n# Re-evaluate only the stored p5 objective, without KKT solves or trajectory propagation.
import mpmath as mp
mp.mp.dps=80
sol=p.parents[2]/'open-instances/minlplib_sol/lukvle10.p5.sol'
v={nm:mp.mpf(value) for nm,value in (line.split() for line in sol.read_text().splitlines())}
x=[v[f'x{i}'] for i in range(1,1001)]
f=mp.fsum((x[2*i]**2)**(x[2*i+1]**2+1)+(x[2*i+1]**2)**(x[2*i]**2+1) for i in range(500))
exact=mp.mpf('352.2380254064956226308712710293664647979978')
print('p5 coordinate objective',mp.nstr(f,40),'difference',mp.nstr(f-exact,12),'objvar',mp.nstr(v['objvar'],30))
assert mp.mpf('5.1e-13')<f-exact<mp.mpf('5.2e-13')
print('PASS: p5 coordinate objective and objvar are distinct from the displayed objective.')
''')
