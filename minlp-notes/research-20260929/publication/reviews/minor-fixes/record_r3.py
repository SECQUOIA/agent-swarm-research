"""Generate scoped inventories and GNU-compatible round-1/round-3 diffs."""
import difflib
import json
from pathlib import Path

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent
B = W / 'before-r3'

def diff(before, after, old_name, new_name):
    lines = difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                 fromfile=old_name, tofile=new_name)
    return ''.join(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n'
                   for line in lines)

f = W / 'report_changes.patch'
snapshot = B / 'publication__reviews__minor-fixes__report_changes.patch'
if not snapshot.exists():
    snapshot.write_bytes(f.read_bytes())
patch = []
for before in sorted((W / 'before').glob('*.txt')):
    track = before.stem.replace('__', '/')
    after = W / 'before-r2' / (before.stem+'__report.md')
    patch.append(diff(before.read_text(), after.read_text(),
                      f'before/{track}/report.md', f'after/{track}/report.md'))
f.write_text(''.join(patch))

new_artifacts = ['edit_r3.py', 'finish_r3.py', 'check_r3.py', 'record_r3.py', 'validate_r3.py',
                 'commands-r3.json', 'response-r3.md', 'check_r3.log',
                 'dtoc5_reference_r3.log', 'protected-r3.json', 'validation_r3.log',
                 'report_changes_r3.patch', 'FILES-r3.json']
f = W / 'FILES.json'
snapshot = B / 'publication__reviews__minor-fixes__FILES.json'
if not snapshot.exists():
    snapshot.write_bytes(f.read_bytes())
changed = [Path(before.name.replace('__', '/')) for before in sorted(B.iterdir())]
created = [Path('publication/reviews/minor-fixes') / name for name in new_artifacts]
snapshots = [before.relative_to(R) for before in sorted(B.iterdir())]
inventory = sorted({path.as_posix() for path in changed+created+snapshots})
(W / 'FILES-r3.json').write_text(json.dumps({'base': 'research-20260929', 'files': inventory}, indent=2)+'\n')
cumulative = json.loads(f.read_text())
for rel in inventory:
    cumulative.append(rel[len('publication/'):] if rel.startswith('publication/') else '../'+rel)
f.write_text(json.dumps(sorted(set(cumulative)), indent=2)+'\n')

patch = []
for before in sorted(B.iterdir()):
    rel = before.name.replace('__', '/')
    after = R / rel
    patch.append(diff(before.read_text(), after.read_text(), 'before-r3/'+rel, rel))
for name in new_artifacts:
    if name in ['report_changes_r3.patch', 'check_r3.log', 'validation_r3.log']:
        # The patch cannot contain itself; the live verification log is inventoried.
        continue
    after = W / name
    if after.exists():
        patch.append(diff('', after.read_text(), '/dev/null', after.relative_to(R).as_posix()))
(W / 'report_changes_r3.patch').write_text(''.join(patch))
print('Regenerated GNU-compatible historical patch, round-3 diff and complete write inventories.')
