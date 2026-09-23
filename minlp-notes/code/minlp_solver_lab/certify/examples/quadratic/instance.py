import pyomo.environ as pe
m = pe.ConcreteModel()
m.x = pe.Var(domain=pe.Binary)
m.y = pe.Var(bounds=(0, 2))
m.c = pe.Constraint(expr=(m.x - 0.5)**2 <= m.y)
m.obj = pe.Objective(expr=m.y)
