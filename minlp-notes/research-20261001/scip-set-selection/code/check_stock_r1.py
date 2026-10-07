"""Check relink identity on off full solves, cut-on roots and tln7's tree."""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

from pathlib import Path
import json
import os
import re
import subprocess
import time

from parse_logs import parse
from run_bench import command, BINARY

BASE = Path(__file__).resolve().parent.parent
STOCK = (_PUBLIC_HOME + '/build-scip/selection/revision-r1-stock/scip-stock')
OUT = BASE / 'logs/stock_checks_r1'


def run(inst, setting, seed, mode, binary, label, nodes=None):
    directory = OUT / label
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f'{inst}.{setting}.s{seed}.log'
    cmd = command(inst, setting, seed, mode, 300)
    if nodes:
        cmd = 'set limits nodes %d ' % nodes + cmd
    start = time.monotonic()
    with path.open('w') as f:
        p = subprocess.run(['timeout', '--kill-after=10s', '720s', binary, '-c', cmd],
                           stdout=f, stderr=subprocess.STDOUT, env=dict(os.environ, OMP_NUM_THREADS='1'))
        f.write(f'\n@@ wallclock {time.monotonic()-start:.2f} returncode {p.returncode}\n')
    return path


def signature(path):
    r = parse(str(path))
    keys = ('status', 'nodes', 'primal', 'dual', 'firstlp', 'rootdual', 'gencuts', 'addcuts', 'returncode', 'error')
    result = {k: r.get(k) for k in keys}
    txt = path.read_text()
    for row in ('primal LP', 'dual LP'):
        match = re.findall(r'\n  ' + row + r'\s*:\s*\S+\s+(\d+)\s+(\d+)', txt)
        result[row] = match[-1] if match else None
    return result


def main():
    results = []
    for i in ('nvs17', 'st_glmp_fp2', 'ex5_4_2'):
        stock = run(i, 'off', 1, 'full', STOCK, 'stock-off')
        archived = BASE / f'logs/full/{i}.off.s1.log'
        same = signature(stock) == signature(archived)
        if i == 'ex5_4_2':
            for path in (stock, archived):
                assert '(node 3643) unresolved numerical troubles in LP 3040' in path.read_text()
        print('stock off vs archived patched off', i, same, signature(stock), flush=True)
        assert same
        results.append(dict(kind='off-full', instance=i, same=same, signature=signature(stock)))
    for i in ('blend029', 'ex8_3_2', 'kall_circlespolygons_c1p11', 'st_e31', 'tln7'):
        stock = run(i, 'scip', 0, 'root', STOCK, 'stock-root')
        patched = run(i, 'scip', 0, 'root', BINARY, 'patched-root')
        same = signature(stock) == signature(patched)
        print('stock vs patched cut-on root', i, same, signature(stock), flush=True)
        assert same
        results.append(dict(kind='cut-on-root', instance=i, same=same, signature=signature(stock)))
    stock = run('tln7', 'scip', 0, 'full', STOCK, 'stock-tree', nodes=2000)
    patched = run('tln7', 'scip', 0, 'full', BINARY, 'patched-tree', nodes=2000)
    for label, path in (('stock', stock), ('patched', patched)):
        print('tln7 2000 nodes', label, signature(path), flush=True)
        results.append(dict(kind='tree', binary=label, signature=signature(path)))
    assert signature(stock) != signature(patched)
    (OUT / 'summary.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
