import gurobipy as gp
def obbt_iter(a, U, box, rounds=40):
    (lx,ux),(ly,uy)=box; ws=[]
    for k in range(rounds):
        nb=[]
        for var in ('x','y'):
            for sense in (1,-1):
                m=gp.Model(); m.Params.OutputFlag=0
                x=m.addVar(lb=lx,ub=ux); y=m.addVar(lb=ly,ub=uy); w=m.addVar(lb=-gp.GRB.INFINITY)
                s = 1 if a>0 else -1  # for a>0 need under-estimators of xy; for a<0 over-estimators
                if a>0:
                    m.addConstr(w>=lx*y+ly*x-lx*ly); m.addConstr(w>=ux*y+uy*x-ux*uy)
                else:
                    m.addConstr(w<=ux*y+ly*x-ux*ly); m.addConstr(w<=lx*y+uy*x-lx*uy)
                m.addConstr(x*x+y*y+a*w<=U)
                m.setObjective(sense*(x if var=='x' else y)); m.optimize()
                if m.Status!=2:
                    print("status", m.Status); return ws
                nb.append(sense*m.ObjVal)
        lx,ux,ly,uy=max(lx,nb[0]),min(ux,nb[1]),max(ly,nb[2]),min(uy,nb[3])
        ws.append(max(ux-lx,uy-ly))
    return ws
# f = x^2 + y^2 + a*x*y, minimizer 0 (|a|<2), f*=0; start box [-1,1.3]x[-1.2,1]
for a in (0.5,1.0,1.5,1.9,-1.0):
    ws=obbt_iter(a,1e-6,((-1,1.3),(-1.2,1)))
    print(a, len(ws), ['%.2e'%w for w in ws[:12]], 'ratios', [round(ws[i+1]/ws[i],3) for i in range(min(len(ws)-1,12))])
