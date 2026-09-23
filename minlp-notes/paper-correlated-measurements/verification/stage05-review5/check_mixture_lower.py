from pathlib import Path
import json
import sympy as s
root=Path('/home/sgusev/repo/minlp-notes/paper-correlated-measurements')
d=json.loads((root/'supplement/results/fresh-all.json').read_text())['nested']
F=s.Matrix(d['model']['F']);J0=s.Matrix(d['model']['prior']);rho=s.Rational(3,5)
K=s.Matrix(8,8,lambda i,j:rho**abs(i-j));R=K+s.eye(8);rows=[]
for row in d['nested']:
 A=row['anchors'];q=len(A);KA=K.extract(A,A);H=K.extract(range(8),A)*KA.inv() if q else s.zeros(8,0)
 D=R-H*KA*H.T;Z=F.row_join(H);base=s.diag(J0,KA.inv()) if q else J0
 M=base.copy()
 for S,w in zip(d['schedules'],row['mixture_weights']):
  ZS=Z.extract(S,range(2+q));M+=s.Rational(w)*ZS.T*D.extract(S,S).inv()*ZS
 G=s.Matrix(row['nuisance_witness']) if q else s.zeros(0,2)
 J=M[:2,:2]-M[:2,2:]*M[2:,2:].inv()*M[2:,:2] if q else M
 assert not q or M[2:,2:]*G+M[2:,:2]==s.zeros(q,2)
 assert J==s.Matrix(row['mixture_information'])
 assert s.Matrix(row['weight_witness'])*J==s.eye(2)
 rows.append({'anchors':A,'saved_G_is_exact_minimizer':True,'saved_J_is_exact_schur':True})
(root/'verification/stage05-review5/mixture-lower-check.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
