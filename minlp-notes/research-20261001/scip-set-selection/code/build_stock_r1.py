"""Relink stock SCIP using the benchmark objects, without changing that build."""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

from pathlib import Path
import hashlib
import shlex
import subprocess
import tarfile

BUILD = Path((_PUBLIC_HOME + '/build-scip/selection/build-lapack'))
WORK = Path((_PUBLIC_HOME + '/build-scip/selection/revision-r1-stock'))
ARCHIVE = Path((_PUBLIC_HOME + '/build-scip/scipoptsuite-10.0.3.tgz'))
WORK.mkdir(exist_ok=True)
with tarfile.open(ARCHIVE) as archive:
    source = archive.extractfile('scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c').read()
(WORK / 'nlhdlr_quadratic.c').write_bytes(source)
target = BUILD / 'scip/src/CMakeFiles/scip.dir'
flags = dict(line.split(' = ', 1) for line in (target / 'flags.make').read_text().splitlines() if ' = ' in line)
args = shlex.split(flags['C_DEFINES'] + ' ' + flags['C_INCLUDES'] + ' ' + flags['C_FLAGS'])
compiler = (_PUBLIC_HOME + '/miniconda3/envs/scipbuild/bin/gcc')
subprocess.run([compiler, *args, '-c', str(WORK / 'nlhdlr_quadratic.c'), '-o', str(WORK / 'quadratic-stock.o')], check=True)
subprocess.run([compiler, *args, '-c', (_PUBLIC_HOME + '/build-scip/selection/scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c'), '-o', str(WORK / 'quadratic-patched-check.o')], check=True)
assert (WORK / 'quadratic-patched-check.o').read_bytes() == (target / 'scip/nlhdlr_quadratic.c.o').read_bytes()
print('Recompiled patched object is byte-identical to the benchmark object.', flush=True)
command = shlex.split((target / 'link.txt').read_text())
command[command.index('CMakeFiles/scip.dir/scip/nlhdlr_quadratic.c.o')] = str(WORK / 'quadratic-stock.o')
command[command.index('-o') + 1] = str(WORK / 'scip-stock')
(WORK / 'link-argv.txt').write_text(shlex.join(command) + '\n')
subprocess.run(command, cwd=BUILD / 'scip/src', check=True)
for path in (ARCHIVE, WORK / 'nlhdlr_quadratic.c', WORK / 'scip-stock'):
    print(hashlib.sha256(path.read_bytes()).hexdigest(), path)
subprocess.run(['ldd', str(WORK / 'scip-stock')], check=True)
