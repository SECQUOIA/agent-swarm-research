"""Unit test of driver.Driver.admit with patched load average and MemAvailable.
Checks: waits while load1 > 30 or MemAvailable < 8 GB, logs each wait when it
begins or its reason changes, logs the admission after a wait, records the
admission values, and returns None when the driver stops during a wait."""
import os
import shutil
import sys
import threading
from argparse import Namespace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import driver  # noqa: E402

out = HERE / "unit_admit"
shutil.rmtree(out, ignore_errors=True)
args = Namespace(out=str(out), instances=["ex6_2_5"], solvers=["SCIP"], reslim=30, jobs=1, mem_cap_gb=8.0,
                 hard_extra_s=600, min_cpu_ratio=0.9, max_retries=2, max_load=30.0, min_mem_gb=8.0)
driver.ADMIT_POLL_S = 0.01
state = {}
os.getloadavg = lambda: (state["load"], 0.0, 0.0)
driver.meminfo_gb = lambda: (state["mem"], 0.0)


def feed(seq):
    it = iter(seq)

    def tick(timeout=None):
        try:
            state["load"], state["mem"] = next(it)
        except StopIteration:
            pass
        return False
    return tick


d = driver.Driver(args)
d.queue = []

# 1) immediate admission: no log line
state.update(load=5.0, mem=20.0)
r = d.admit("a__X")
assert r["admission_wait_s"] < 1 and r["load1_at_admission"] == 5.0, r
assert not (out / "driver.log").exists()

# 2) load too high, then load and memory, then memory only, then fine
state.update(load=40.0, mem=20.0)
d.stop.wait = feed([(40.0, 20.0), (35.0, 5.0), (35.0, 5.0), (10.0, 5.0), (10.0, 20.0)])
r = d.admit("b__X")
log = (out / "driver.log").read_text().splitlines()
print("\n".join(log))
assert len(log) == 4, log
assert "wait b__X" in log[0] and "load1 40.0 > 30" in log[0] and "MemAvailable" not in log[0]
assert "load1 35.0 > 30" in log[1] and "MemAvailable 5.0 GB < 8 GB" in log[1]
assert "load1" not in log[2] and "MemAvailable 5.0 GB < 8 GB" in log[2]
assert "admit b__X after waiting" in log[3] and "load1 10.0" in log[3]
assert r["load1_at_admission"] == 10.0 and r["mem_available_gb_at_admission"] == 20.0, r

# 3) stop while waiting returns None
d.stop = threading.Event()
state.update(load=99.0, mem=20.0)
threading.Timer(0.2, d.stop.set).start()
assert d.admit("c__X") is None
assert d.waiting is None
print("OK")
