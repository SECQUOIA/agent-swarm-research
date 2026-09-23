"""Verify an extracted supplement and its recorded measurement inputs."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

files = json.loads((root / 'SHA256.json').read_text())
for name, expected in files.items():
    assert digest(root / name) == expected, ('archive file differs', name)
provenance = json.loads((root / 'measurement-provenance.json').read_text())
record = json.loads((root / provenance['record_path']).read_text())
assert digest(root / provenance['record_path']) == provenance['record_sha256']
assert set(record['input_hashes']) == set(provenance['input_mapping'])
for name, entry in provenance['input_mapping'].items():
    assert record['input_hashes'][name] == entry['measured_sha256'], name
    assert digest(root / entry['measured_path']) == entry['measured_sha256'], name
    assert digest(root / name) == entry['current_sha256'], name
solver = root / 'paper-structured-bilevel/code/compressed_solver.py'
measured = root / provenance['input_mapping'][str(solver.relative_to(root))]['measured_path']
line = b'    constraints = tuple(constraints)\n'
assert solver.read_bytes().count(line) == 1
assert solver.read_bytes().replace(line, b'', 1) == measured.read_bytes()
print(f'PASS: {len(files)} exported files and {len(provenance["input_mapping"])} measured inputs; iterator change isolated')
