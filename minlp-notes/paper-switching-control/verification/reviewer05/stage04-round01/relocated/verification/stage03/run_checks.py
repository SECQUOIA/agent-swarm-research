"""Run the stage 3 exact verification suite using only bundled files."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
REFERENCE=HERE.parent/'reference'
if __name__=='__main__':
 if not __debug__:raise RuntimeError('Run without -O')
 manifest=json.loads((REFERENCE/'origin-manifest.json').read_text())
 for name,item in manifest.items():
  assert hashlib.sha256((REFERENCE/name).read_bytes()).hexdigest()==item['sha256'],name
 (HERE/'integrity.log').write_text(f'All {len(manifest)} bundled original artifact hashes match.\n')
 for script in [REFERENCE/name for name in ('arbitrary_block_certificate.py','three_switch_heavy_certificate.py','two_switch_global_certificate.py','two_switch_equal_mass_certificate.py','general_reach_research.py','check_seeded_review.py')]+[HERE/'check_new_results.py',HERE/'check_chronological.py']:
  out=subprocess.run([sys.executable,str(script)],cwd=HERE,text=True,capture_output=True)
  (HERE/(script.stem+'.log')).write_text(out.stdout+out.stderr)
  if out.returncode:raise RuntimeError(f'{script.name} failed: see its log')
  print(f'PASS {script.name}',flush=True)
 print('All stage 3 checks passed with bundled local dependencies.')
