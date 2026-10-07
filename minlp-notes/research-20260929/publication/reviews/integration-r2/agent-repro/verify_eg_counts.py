"""Integration review r2 (agent-repro): recompute eg_disc2_s all-leaf numbers from stored
logs and NPZ data, and check the EG map entry and the 54 EG command records.

Reads only. Imports numpy and the standard library; no repository module is imported.
Run with:  python3 -I -B verify_eg_counts.py   (from any directory)
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import glob
import hashlib
import json
import os
import re
import sys

import numpy as np

R = (_PUBLIC_REPO + '/research-20260929')
P = R + "/publication"
TRACK = P + "/eg-recheck"
REV = P + "/reviews/eg-recheck-r1"
NCH = {0: 4, 1: 5, 2: 6, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
problems = []


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ---------- A. text logs: cert_p*_c*.log
cert_logs = sorted(glob.glob(TRACK + "/logs/cert_p*_c*.log"))
print("cert logs:", len(cert_logs))
per_part = {}
log_time = {}
for path in cert_logs:
    k, c = map(int, re.search(r"cert_p(\d+)_c(\d+)\.log$", path).groups())
    t = open(path).read()
    proc = int(re.search(r"processed (\d+), pre-closed", t)[1])
    lv = int(re.search(r"certifying (\d+)", t)[1])
    m = re.search(r"certified (\d+)/(\d+); failures (\d+).*?time (\d+)s", t)
    cov = "generated == popped multiset: True" in t and "bad reduced boxes 0" in t
    d = per_part.setdefault(k, dict(chunks=[], proc=set(), certified=0, fail=0, time=0, cov=True))
    d["chunks"].append(c)
    d["proc"].add(proc)
    d["certified"] += int(m[1])
    d["chunk_total"] = d.get("chunk_total", 0) + int(m[2])
    d["fail"] += int(m[3])
    d["time"] += int(m[4])
    d["cov"] &= cov
    log_time[(k, c)] = int(m[4])
tot_l = tot_f = tot_p = tot_t = 0
for k in sorted(per_part):
    d = per_part[k]
    assert sorted(d["chunks"]) == list(range(NCH[k])), (k, d["chunks"])
    assert len(d["proc"]) == 1
    proc = d["proc"].pop()
    print(f"part {k}: chunks {len(d['chunks'])}, processed {proc}, certified {d['certified']}/{d['chunk_total']}, "
          f"failures {d['fail']}, coverage ok {d['cov']}, time {d['time']} s")
    tot_l += d["certified"]; tot_f += d["fail"]; tot_p += proc; tot_t += d["time"]
print(f"TEXT LOGS: parts {len(per_part)}, chunks {len(cert_logs)}, certified leaves {tot_l}, failures {tot_f}, "
      f"processed boxes {tot_p}, sum of logged chunk times {tot_t} s")

# rec logs: processed counts from the tree-recording runs
rec_proc = {}
for k in range(8):
    t = open(f"{TRACK}/logs/rec_disc2_p{k}.log").read()
    rec_proc[k] = int(re.search(r"recorded (\d+) processed", t)[1])
print("recorded processed boxes per part (rec logs):", rec_proc, "sum", sum(rec_proc.values()))

# ---------- B. NPZ data: res/p*_c*.npz and rec/*.npz
n_tot = f_tot = p_tot = 0
t_npz = 0.0
for k in range(8):
    files = sorted(glob.glob(f"{TRACK}/res/p{k}_c*.npz"))
    assert len(files) == NCH[k]
    Z = [np.load(f, allow_pickle=False) for f in files]
    n = int(Z[0]["n_leaves"])
    sel = np.concatenate([z["sel"] for z in Z])
    ok = np.concatenate([z["ok"] for z in Z])
    assert all(int(z["n_leaves"]) == n and int(z["nchunks"]) == NCH[k] for z in Z)
    exact_once = np.array_equal(np.sort(sel), np.arange(n))
    interleave = all(np.array_equal(z["sel"], np.arange(int(z["chunk"]), n, NCH[k])) for z in Z)
    cov = all(bool(z["cov_ok"]) and int(z["nbad_red"]) == 0 and int(z["n_open"]) == 0 and int(z["n_tiny"]) == 0
              for z in Z)
    proc = {int(z["n_proc"]) for z in Z}
    rec = np.load(f"{TRACK}/rec/rec_disc2_p{k}.npz", allow_pickle=False)
    nrec = len(rec["P_lo"])
    lv = np.load(f"{REV}/leaves_p{k}.npz", allow_pickle=False)
    boxes_same = all(np.array_equal(lv[a][z["sel"]], z[a]) for z in Z for a in ("lo", "hi"))
    mg = np.concatenate([z["mg"] for z in Z])
    t_npz += sum(float(z["time"]) for z in Z)
    print(f"npz part {k}: n_leaves {n}, every index exactly once {exact_once}, interleaved {interleave}, "
          f"ok {int(ok.sum())}/{n}, coverage flags {cov}, n_proc {proc}, rec P rows {nrec}, "
          f"reviewer leaves {len(lv['lo'])} boxes identical {boxes_same}, all margins > 0 {bool(np.all(mg > 0))}")
    if not (exact_once and interleave and cov and ok.all() and proc == {nrec} == {rec_proc[k]} and boxes_same):
        problems.append(f"npz part {k} inconsistent")
    n_tot += n; f_tot += int((~ok).sum()); p_tot += nrec
print(f"NPZ: leaves {n_tot}, failures {f_tot}, processed boxes {p_tot}, chunk CPU time {t_npz:.0f} s")

# ---------- C. interval sample union
allsel = {}
for f in sorted(glob.glob(f"{REV}/sample_[ABC]_p*.npz")):
    k = int(re.search(r"_p(\d)\.npz$", f)[1])
    z = np.load(f, allow_pickle=False)
    s = allsel.setdefault(k, set())
    s.update(int(i) for i in z["sel"])
    assert np.all(z["st"] == z["st"]), f
union = sum(len(s) for s in allsel.values())
print("interval sample parts:", sorted(allsel), "distinct per part:", {k: len(s) for k, s in allsel.items()},
      "union", union)
# whether each sample file recorded zero failures
nf = 0
for f in sorted(glob.glob(f"{REV}/sample_[ABC]_p*.npz")):
    z = np.load(f, allow_pickle=False)
    nf += int(np.sum(~np.isfinite(z["minmg"]) & (z["minmg"] < 0))) + int(np.sum(z["minmg"] <= 0))
print("sample leaves with own smallest piece margin <= 0:", nf)
for label in "ABC":
    t = open(f"{REV}/logs/own_sample_{label}.log").read()
    print(f"own_sample_{label}.log: ", re.findall(r"part (\d): (\d+) distinct leaves; certified (\d+)/(\d+)", t))

# ---------- D. expected numbers
exp = dict(leaves=1114361, failures=0, processed=1152830, chunks=38, sample=10404, sample_parts=[0, 2, 3, 4, 5, 6, 7])
got = dict(leaves=tot_l, failures=tot_f, processed=tot_p, chunks=len(cert_logs), sample=union,
           sample_parts=sorted(allsel))
for key in exp:
    print(f"check {key}: expected {exp[key]}, got {got[key]}: {'OK' if exp[key] == got[key] else 'MISMATCH'}")
    if exp[key] != got[key]:
        problems.append(f"{key} mismatch")
assert n_tot == tot_l and p_tot == tot_p == sum(rec_proc.values())

# ---------- E. result-map entry paths
rm = json.load(open(P + "/reproduction/result-map.json"))
row = next(r for r in rm if r["instance"] == "eg_disc2_s")
miss = []
hashbad = []
nref = 0
for key in ("scripts", "saved_inputs", "outputs", "numeric_evidence"):
    for e in row.get(key, []):
        p = R + "/" + e["path"]
        nref += 1
        if not os.path.isfile(p):
            miss.append(p)
        elif "sha256" in e and sha(p) != e["sha256"]:
            hashbad.append(e["path"])
print(f"result-map eg_disc2_s: {nref} path references, missing {len(miss)}, hash mismatches {len(hashbad)}")
for p in miss + hashbad:
    print("   ", p)
problems += [f"missing map path {p}" for p in miss] + [f"map hash mismatch {p}" for p in hashbad]
print("all_leaf_recheck.expected:", json.dumps(row["all_leaf_recheck"]["expected"]))
print("history:", row["all_leaf_recheck"].get("history"))
for key in ("eg_int_s", "eg_disc_s"):
    r2 = next(r for r in rm if r["instance"] == key)
    print(key, "reported_row:", r2["reported_row"])
    for k2 in ("scripts", "saved_inputs", "outputs", "numeric_evidence"):
        for e in r2.get(k2, []):
            if not os.path.isfile(R + "/" + e["path"]):
                problems.append(f"missing {key} map path {e['path']}")

# ---------- F. the 54 EG command records
cmds = [c for c in json.load(open(P + "/reproduction/commands.json")) if c["id"].startswith("eg-recheck/")]
print("EG command records:", len(cmds), "unique ids:", len({c["id"] for c in cmds}))
hist = [c["id"] for c in cmds if "do not repeat" in c.get("execution", "")]
print("marked 'do not repeat':", len(hist))
print("not marked historical:", [(c["id"], c["execution"]) for c in cmds if c["id"] not in hist])
for c in cmds:
    out = R + "/" + c["output"].removeprefix("$R/")
    if not os.path.isfile(out):
        problems.append(f"cmd {c['id']}: output missing {out}")
        continue
    if sha(out) != c["sha256"]:
        problems.append(f"cmd {c['id']}: output hash mismatch")
    for p in c["inputs"] + c["result_files"]:
        q = os.path.expanduser(p) if p.startswith("~/") else R + "/" + p.removeprefix("$R/")
        if not os.path.isfile(q):
            problems.append(f"cmd {c['id']}: missing {p}")
    m = re.match(r"eg-recheck/cert-p(\d)-c(\d)$", c["id"])
    if m:
        k, ch = map(int, m.groups())
        want = (f"python3 recheck_leaves.py rec/rec_disc2_p{k}.npz eg_disc2_s 5.642100574331458 "
                f"{ch} {NCH[k]} res/p{k}_c{ch}.npz")
        if c["command"] != want or c["cwd"] != "$R/publication/eg-recheck":
            problems.append(f"cmd {c['id']}: command/cwd differ: {c['cwd']} {c['command']}")
        if c["output"] != f"$R/publication/eg-recheck/logs/cert_p{k}_c{ch}.log":
            problems.append(f"cmd {c['id']}: output {c['output']}")
        t = open(out).read()
        cm = re.search(r"certified (\d+)/(\d+); failures (\d+)", t)
        if c["expected"].get("certified") != int(cm[1]):
            problems.append(f"cmd {c['id']}: expected certified {c['expected']} vs log {cm[1]}")
        # the log states the saved file path; check it is the recorded result file
        saved = re.search(r"saved (\S+);", t)[1]
        if not saved.endswith(f"publication/eg-recheck/res/p{k}_c{ch}.npz"):
            problems.append(f"cmd {c['id']}: log saved {saved}")
    m = re.match(r"eg-recheck/record-p(\d)$", c["id"])
    if m:
        k = int(m[1])
        t = open(out).read()
        saved = re.search(r"-> (\S+)", t)[1]
        if not saved.endswith(f"publication/eg-recheck/rec/rec_disc2_p{k}.npz"):
            problems.append(f"cmd {c['id']}: log saved {saved}")
ids = sorted(c["id"] for c in cmds)
print("ids:", ids)
timefields = sorted({k for c in cmds for k in c})
print("record fields:", timefields)

print("\nPROBLEMS:", problems if problems else "none")
sys.exit(1 if problems else 0)
