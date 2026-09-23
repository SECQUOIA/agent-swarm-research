from pathlib import Path
import json,subprocess
out=Path('paper-network-simplex/verification/reviewer5/stage06-round02')
text=(out/'manuscript.txt').read_text()
start=text.index('PYTHONPATH=code python -m network_simplex_benchmarks.paper_stage06')
command=text[start:].split('\n\n',1)[0]
# Python is a harmless Bash function that prints its argument vector here.
script='python() { printf "ARG:%s\\n" "$@"; printf "END\\n"; }\n'+command+'\n'
r=subprocess.run(['bash','-c',script],capture_output=True,text=True)
expected='ARG:-m\nARG:network_simplex_benchmarks.paper_stage06\nARG:--output\nARG:paper-network-simplex/verification/stage06-benchmarks.json\nEND\nARG:paper-network-simplex/verification/stage06-tables.py\nEND\n'
assert r.returncode==0 and r.stdout==expected,(r.stdout,r.stderr)
print(json.dumps(dict(status='PASS',extracted_command=command,arguments=r.stdout),indent=2))
