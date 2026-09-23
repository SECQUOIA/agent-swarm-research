exec((__import__('pathlib').Path(__file__).parent/'check_fresh.py').read_text().split('# Complete-block fixture.')[0])
counts=0
for row in r['local']:
 L=row['L'];T=rho**(L+1)/(1-rho);N=rho**(L+2)*(1-rho**L)*(1-rho**(L+1))/((1-rho)*(1-rho**2));delta=0 if L==7 else 2*(T+N/2)
 assert delta==Q(row['delta'])
 if delta>=1:assert row['status']=='bound >= 1; no transfer';continue
 atoms=[]
 for S in ss:
  J=prior.copy()
  for t in S:
   h=[i for i in S if t-L<=i<t];beta=R.extract([t],h)*R.extract(h,h).inv() if h else s.zeros(1,0)
   Dt=R[t,t]-(beta*R.extract(h,[t]))[0];ft=F[t,:]-beta*F.extract(h,range(p));J+=ft.T*ft/Dt
  atoms.append(prior+(J-prior)/(1-delta))
 weights=list(map(Q,row['mixture_weights']));assert min(weights)>=0 and sum(weights)==1
 J=sum((w*B for w,B in zip(weights,atoms)),s.zeros(p));W=mat(row['weight_witness']);assert J==mat(row['mixture_information']) and W*J==s.eye(p)
 prices=[s.trace(W*B) for B in atoms];assert max(prices)==Q(row['price_max']);assert num(row['lower'])<=ln(J.det())<=num(row['upper'])-num(max(prices)-p)
 counts+=len(atoms)
print('Independent local transferred hull witnesses passed:',counts)
