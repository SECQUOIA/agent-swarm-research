import gurobipy as gp
# min -(x+y) s.t. x*y <= 1, x in [0,3], y in [0,2]; optimum (3,1/3), f* = -10/3 (sharp: bound x<=3 and curve active)
def run(eps, rounds=15):
    lx,ux,ly,uy=0.0,3.0,0.0,2.0; ws=[]
    U=-10/3+eps
    for k in range(rounds):
        nb=[]
        for var in ('x','y'):
            for s in (1,-1):
                m=gp.Model(); m.Params.OutputFlag=0; m.Params.FeasibilityTol=1e-9; m.Params.OptimalityTol=1e-9
                x=m.addVar(lb=lx,ub=ux); y=m.addVar(lb=ly,ub=uy); w=m.addVar(lb=-1e9)
                m.addConstr(w>=lx*y+ly*x-lx*ly); m.addConstr(w>=ux*y+uy*x-ux*uy)
                m.addConstr(w<=1); m.addConstr(-(x+y)<=U)
                m.setObjective(s*(x if var=='x' else y)); m.optimize()
                if m.Status!=2: return ws
                nb.append(s*m.ObjVal)
        lx,ux,ly,uy=max(lx,nb[0]),min(ux,nb[1]),max(ly,nb[2]),min(uy,nb[3])
        ws.append((ux-lx,uy-ly))
    return ws
for eps in (1e-3,1e-6):
    ws=run(eps); print(eps, [('%.2e'%a,'%.2e'%b) for a,b in ws[:10]])
