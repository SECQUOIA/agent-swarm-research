"""Compare module-level path constants of each patch-owned Python script
before (HEAD) and after (working tree), evaluating with __file__ set to the
script's real location. Expressions referencing anything but os/str/path
helpers are skipped."""
import ast, json, os, subprocess, sys
REPO = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
own = json.load(open(f'{REPO}/research-20260929/publication/reproduction/logs/owned-scientific-paths.json'))
HOME = os.path.expanduser('~')

def consts(src, path):
    # No builtins: module-level expressions such as open(..., 'w') must not run.
    # (An earlier version without this guard truncated four pindyck review logs;
    # they were restored from HEAD, whose hashes equal the package manifest.)
    env = {'__builtins__': {}, '__file__': path, 'os': os, '_os': os, '_repro_os': os, 'Path': __import__('pathlib').Path,
           'pathlib': __import__('pathlib'), 'str': str}
    out = {}
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.Import):
            continue
        if isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) for t in node.targets):
            try:
                v = eval(compile(ast.Expression(node.value), path, 'eval'), env)
            except Exception:
                continue
            for t in node.targets:
                env[t.id] = v
                if isinstance(v, (str, os.PathLike)):
                    out[t.id] = os.path.normpath(str(v))
    return out

bad = 0; checked = 0
for p in own:
    if not p.endswith('.py'):
        continue
    full = f'{REPO}/{p}'
    try:
        old = subprocess.run(['git', 'show', f'HEAD:{p}'], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        continue
    new = open(full).read()
    co, cn = consts(old, full), consts(new, full)
    if co is None or cn is None:
        print('PARSE-FAIL', p); bad += 1; continue
    for k, v in co.items():
        if k in cn:
            checked += 1
            if cn[k] != v:
                print('DIFF', p, k, v, '->', cn[k]); bad += 1
        elif '/' in v:
            print('MISSING-IN-NEW', p, k, v)
    for k, v in cn.items():
        if k not in co and k.startswith('_') and ('ROOT' in k or 'RESEARCH' in k or 'REPO' in k):
            exp = {'_RESEARCH': f'{REPO}/research-20260929', '_REPO': REPO, '_REPRO_ROOT': REPO}.get(k)
            if exp and v != exp:
                print('ROOTVAR', p, k, v, 'expected', exp); bad += 1
print('checked', checked, 'problems', bad)
