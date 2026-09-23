"""Execute the declared supplementary study sequentially after the main batch.

This is orchestration only; the frozen benchmark owns all solver behavior.
Run from the lab directory with the same solver PATH as the main study.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    out = root / "results/lbesh_development"
    plan = json.loads((out / "supplementary_plan_v1.json").read_text())
    primary = out / "main_generated_v1.jsonl"
    deadline = time.monotonic() + 10800
    while True:
        lines = primary.read_text().splitlines()
        if len(lines) == 663:
            try:
                rows = [json.loads(line) for line in lines]
            except json.JSONDecodeError:
                # The final large JSON record may still be being appended.
                if time.monotonic() > deadline:
                    raise
                time.sleep(1)
                continue
            if len({(r['instance'], r['method']) for r in rows}) != 663:
                raise RuntimeError("Primary batch has duplicate jobs")
            break
        if len(lines) > 663 or time.monotonic() > deadline:
            raise RuntimeError("Primary batch did not complete as declared")
        time.sleep(10)
    env = dict(os.environ)
    env.update({k: "1" for k in (
        "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS")})
    expected = json.loads(Path(str(primary) + ".runs/schedule.json").read_text())['metadata']['source_sha256']
    for job in plan['jobs']:
        for name, digest in expected.items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
                raise RuntimeError(f"Frozen runtime source changed: {name}")
        print(f"Starting {job['name']}", flush=True)
        with (out / (job['name'] + '.queue.log')).open('x') as log:
            subprocess.run(job['command'], env=env, stdout=log,
                           stderr=subprocess.STDOUT, check=True)
        print(f"Completed {job['name']}", flush=True)
    (out / 'supplementary_queue_complete.json').write_text(json.dumps({
        'jobs': [j['name'] for j in plan['jobs']],
        'completed_unix_time': time.time(),
        'plan_sha256': hashlib.sha256((out / 'supplementary_plan_v1.json').read_bytes()).hexdigest(),
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
