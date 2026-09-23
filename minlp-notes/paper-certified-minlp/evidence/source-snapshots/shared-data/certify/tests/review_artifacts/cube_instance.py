import pyomo.environ as pe
m = pe.ConcreteModel()
m.x = pe.Var(bounds=(0, 10), initialize=1.0)
m.y = pe.Var(bounds=(0, 1000), initialize=1.0)
m.c1 = pe.Constraint(expr=m.x**3 - m.y <= 0)
m.obj = pe.Objective(expr=m.y, sense=pe.minimize)
