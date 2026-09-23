"""Run distinct existing exact boundary diagnostics and retain provenance."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib, json, subprocess, time
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCES = [
 'code/bilevel_dense_box/second_review_checks.py',
 'code/bilevel_dense_box/check_conditioned_hardness_first_review.py',
 'code/bilevel_response/check_conditioned_additive_second.py',
 'code/bilevel_vertex_integrity/check_structure_and_path.py',
 'code/bilevel_parameterized/check_mixed_radix_gap.py',
 'code/parametric_path_lp/exact_shadow_check.py',
 'code/parametric_path_lp/exact_diagonal_follower_check.py',
 'code/parametric_path_lp/check_affine_strip_projection_review.py',
]
def run(source):
    start=time.monotonic()
    proc=subprocess.run(['python',source],cwd=ROOT,text=True,capture_output=True)
    logfile=OUT/(Path(source).stem+'.log')
    logfile.write_text(proc.stdout+proc.stderr)
    return dict(command=['python',source], exit_code=proc.returncode,
                seconds=round(time.monotonic()-start,3), log=logfile.name,
                sha256=hashlib.sha256((ROOT/source).read_bytes()).hexdigest())
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        records=list(pool.map(run,SOURCES))
    (OUT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    for rec in records:
        print(rec['exit_code'],rec['command'][1],rec['seconds'])
    if any(rec['exit_code'] for rec in records): raise SystemExit(1)
