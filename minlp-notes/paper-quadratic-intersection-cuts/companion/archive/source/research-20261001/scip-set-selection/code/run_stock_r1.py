"""Checkpointed stock rerun: same commands as run_bench.py; eight workers at most.

Usage: python3 code/run_stock_r1.py [WALL_TIMEOUT_SECONDS]
Each solver is wrapped in GNU timeout (default 720 s, kill after 10 s). Completed
logs are atomically renamed, so interruption cannot leave a false checkpoint.
SIGINT/SIGTERM kill process groups, including timeout and its solver child.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
import threading
import time

from run_bench import command

BASE = Path(__file__).resolve().parent.parent
BINARY = (_PUBLIC_HOME + '/build-scip/selection/revision-r1-stock/scip-stock')
OUT = BASE / 'logs/full_stock'
ACTIVE = set()
LOCK = threading.Lock()
STOP = threading.Event()
WALL_TIMEOUT = int(sys.argv[1]) if len(sys.argv) > 1 else 720


def shutdown(signum, frame):
    STOP.set()
    with LOCK:
        for pid in ACTIVE:
            try:
                os.killpg(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def load_record(event, **extra):
    return dict(event=event, utc=datetime.now(timezone.utc).isoformat(),
                load=os.getloadavg(), **extra)


def run(inst, seed):
    path = OUT / f'{inst}.scip.s{seed}.log'
    if path.exists():
        txt = path.read_text()
        if re_complete(txt):
            return load_record('skip', instance=inst, seed=seed)
        attempts = OUT / 'attempts'
        attempts.mkdir(exist_ok=True)
        path.replace(attempts / f'{path.stem}.{time.time_ns()}.log')
    if STOP.is_set():
        return load_record('cancelled', instance=inst, seed=seed)
    temporary = path.with_suffix('.partial')
    started = time.monotonic()
    with temporary.open('w') as log:
        with LOCK:
            if STOP.is_set():
                return load_record('cancelled', instance=inst, seed=seed)
            process = subprocess.Popen(['timeout', '--signal=TERM', '--kill-after=10s', f'{WALL_TIMEOUT}s',
                                        BINARY, '-c', command(inst, 'scip', seed, 'full', 300)],
                                       stdout=log, stderr=subprocess.STDOUT,
                                       env=dict(os.environ, OMP_NUM_THREADS='1'), start_new_session=True)
            ACTIVE.add(process.pid)
        try:
            rc = process.wait()
        finally:
            with LOCK:
                ACTIVE.discard(process.pid)
        log.write(f'\n@@ wallclock {time.monotonic() - started:.2f} returncode {rc}\n')
    if not STOP.is_set():
        temporary.replace(path)
    return load_record('done', instance=inst, seed=seed, returncode=rc,
                       wall=time.monotonic() - started)


def re_complete(text):
    return ('returncode 0' in text and 'SCIP Status' in text
            and 'Solution           :' in text and 'Solving Time (sec)' in text)


def main():
    OUT.mkdir(exist_ok=True)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    instances = (BASE / 'logs/testset_full.txt').read_text().split()
    assert len(instances) == len(set(instances)) == 60
    with (OUT / 'driver.jsonl').open('a', buffering=1) as checkpoint:
        checkpoint.write(json.dumps(load_record('start', workers=8, binary=BINARY,
                                                cpu_limit=300, clocktype=1, wall_timeout=WALL_TIMEOUT)) + '\n')
        with ThreadPoolExecutor(max_workers=8) as executor:
            pending = {executor.submit(run, i, s) for i in instances for s in (1, 2)}
            while pending:
                completed = {f for f in pending if f.done()}
                for future in completed:
                    record = future.result()
                    checkpoint.write(json.dumps(record) + '\n')
                    print(json.dumps(record), flush=True)
                pending -= completed
                if pending:
                    checkpoint.write(json.dumps(load_record('load', pending=len(pending))) + '\n')
                    STOP.wait(30) if not STOP.is_set() else time.sleep(0.1)
        assert not ACTIVE
        checkpoint.write(json.dumps(load_record('finish', stopped=STOP.is_set())) + '\n')
    if STOP.is_set():
        raise SystemExit(1)


if __name__ == '__main__':
    main()
