"""Run the existing audit display checker in a disposable copy only."""
import json,os,re,shutil,subprocess,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='minlp-integration-audit-') as tmp:
    tmp=Path(tmp);(tmp/'logs').mkdir()
    for name in ('check_display.py','results.json','audit-report.md'):shutil.copy2(BASE/'bound-audit'/name,tmp/name)
    for p in (BASE/'bound-audit/logs').glob('cert_socp_*.json'):shutil.copy2(p,tmp/'logs'/p.name)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    argv=['python3','-B',str(tmp/'check_display.py')]
    r=subprocess.run(argv,capture_output=True,text=True,env=env,check=True)
    print(r.stdout,end='')
    assert 'ok 84, failed 8, skipped 1' in r.stdout
    print('PASS: expected eight historical quotations, no new display failure')
    (OUT/'audit-display-command.json').write_text(json.dumps({'argv':argv,'cwd':str(tmp),'exit':r.returncode,'expected':'ok 84, failed 8, skipped 1','disposable_copy_removed':True},indent=2)+'\n')
