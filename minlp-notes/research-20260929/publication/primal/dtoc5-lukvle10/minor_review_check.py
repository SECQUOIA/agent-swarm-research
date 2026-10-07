"""Check formatter carry without executing gaps.py's top-level file writes."""
import ast
from fractions import Fraction as Q
from pathlib import Path
p=Path(__file__).resolve().parent
mod=ast.parse((p/'gaps.py').read_text()); fn=next(x for x in mod.body if isinstance(x,ast.FunctionDef) and x.name=='sci_up')
ns={'Fraction':Q}; exec(compile(ast.Module(body=[fn],type_ignores=[]),'gaps.py','exec'),ns)
for q in map(Q,['9.9999','0.000099999','99.999','1.00001','0.99999']):
 s=ns['sci_up'](q); assert Q(s)>=q; print(q,'->',s)
print('PASS: carry and ordinary rounding preserve an upper bound.')

# Re-evaluate only the stored p5 objective, without KKT solves or trajectory propagation.
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
