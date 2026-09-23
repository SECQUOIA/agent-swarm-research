from pathlib import Path
import argparse, ast, json
HERE=Path('/home/sgusev/repo/minlp-notes/paper-correlated-measurements/supplement')
tree=ast.parse((HERE/'reproduce.py').read_text())
commands_node=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='commands' for t in n.targets))
commands=eval(compile(ast.Expression(commands_node),'wrapper','eval'),{'root':HERE/'legacy','str':str})
rows=[]
for name,cmd in commands.items():
 path=HERE/'legacy'/cmd[0];mod=ast.parse(path.read_text());parser=argparse.ArgumentParser(prog=cmd[0])
 env={'Path':Path,'HERE':path.parent,'directory':path.parent,'__file__':str(path),'int':int,'float':float,'str':str}
 for node in ast.walk(mod):
  if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='add_argument' and isinstance(node.func.value,ast.Name) and node.func.value.id=='parser':
   args=[eval(compile(ast.Expression(a),'arg','eval'),env) for a in node.args]
   kwargs={a.arg:eval(compile(ast.Expression(a.value),'kw','eval'),env) for a in node.keywords}
   parser.add_argument(*args,**kwargs)
 try:
  result=vars(parser.parse_args(cmd[1:]));status='passes parser'
 except SystemExit as e:result={};status=f'parser exits {e.code}'
 input_files={k:str(v) for k,v in result.items() if k in ('input','source','memory')}
 assert all(Path(v).exists() for v in input_files.values())
 rows.append({'study':name,'status':status,'input_files':input_files})
print(json.dumps(rows,indent=2))
(HERE.parent/'verification/stage05-review5/parser-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
