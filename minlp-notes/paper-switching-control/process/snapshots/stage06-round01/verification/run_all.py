"""Run every portable proof and archived-experiment suite, without network access."""
from pathlib import Path
import subprocess,sys
if not __debug__:
    raise SystemExit('Do not use -O: the exact checkers require assertions.')
ROOT=Path(__file__).resolve().parent.parent
commands=[
 'verification/reference/uniform_certificate.py',
 'verification/reference/one_switch_certificate.py',
 'verification/stage01/check_boundaries.py',
 *[f'verification/stage{i:02d}/run_checks.py' for i in range(2,6)],
 'verification/stage06/check_results.py',
 'verification/stage06/render_results.py --check',
]
for command in commands:
    print(f'Running {command}',flush=True)
    result=subprocess.run([sys.executable,*command.split()],cwd=ROOT,text=True,capture_output=True)
    log=ROOT/'verification'/('complete-'+Path(command.split()[0]).parent.name+'-'+Path(command.split()[0]).stem+'.log')
    log.write_text(result.stdout+result.stderr)
    if result.returncode:
        print(result.stdout+result.stderr)
        raise SystemExit(f'FAILED: {command}; see {log}')
print('PASS: all portable proof, integrity, exact algorithm, and archived experiment suites')
print('Public fine-source reproduction is separate: verification/stage06/experiments.py --fetch')
