"""Run bundled stage 4 exact checks; optional LP audits need SciPy/NumPy."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys

HERE=Path(__file__).resolve().parent
REFERENCE=HERE.parent/'reference'

def main():
    if not __debug__:raise RuntimeError('Run without -O')
    parser=argparse.ArgumentParser()
    parser.add_argument('--with-lp-audits',action='store_true')
    args=parser.parse_args()
    manifest=json.loads((REFERENCE/'origin-manifest.json').read_text())
    for name,item in manifest.items():
        assert hashlib.sha256((REFERENCE/name).read_bytes()).hexdigest()==item['sha256'],name
    commands=[(HERE/'check_finite_formula.py',[]),(HERE/'check_floor_chambers.py',[]),
              (REFERENCE/'small_grid_boundary.py',[]),(REFERENCE/'check_small_grid_review.py',[])]
    if args.with_lp_audits:
        commands += [(REFERENCE/'check_finite_math_review.py',[]),
                     (REFERENCE/'check_finite_grid_review.py',['--skip-milp'])]
    summary={'original_artifacts_verified':len(manifest),'checks':[]}
    for script,options in commands:
        result=subprocess.run([sys.executable,str(script)]+options,cwd=HERE,
                              text=True,capture_output=True)
        (HERE/(script.stem+'.log')).write_text(result.stdout+result.stderr)
        if result.returncode:raise RuntimeError(f'{script.name} failed: see its log')
        summary['checks'].append({'script':script.name,'arguments':options,'output':result.stdout.strip()})
        print(f'PASS {script.name}',flush=True)
    (HERE/'check-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(f'All stage 4 checks passed; {len(manifest)} original artifact hashes match.')

if __name__=='__main__':main()
