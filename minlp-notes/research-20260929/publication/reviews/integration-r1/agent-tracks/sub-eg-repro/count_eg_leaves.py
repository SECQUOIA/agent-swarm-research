"""Sum per-chunk certification totals from eg-recheck cert_p*_c*.log (read-only)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import glob, re, os, sys
from collections import defaultdict
LOGS = (_PUBLIC_REPO + '/research-20260929/publication/eg-recheck/logs')
hdr = re.compile(r"processed (\d+), pre-closed (\d+), open (\d+), tiny (\d+); recorded LB (\S+)")
lv = re.compile(r"leaves: closed boxes (\d+), pre-closed (\d+), slabs (\d+), tiny (\d+), open (\d+); certifying (\d+)")
res = re.compile(r"independent certification vs theta\* = (\S+): certified (\d+)/(\d+); failures (\d+) .*?time (\d+)s")
parts = defaultdict(dict)
files = sorted(glob.glob(os.path.join(LOGS, "cert_p*_c*.log")))
print("chunk logs:", len(files))
tot_cert = tot_n = tot_fail = tot_time = 0
for f in files:
    k, c = map(int, re.search(r"cert_p(\d+)_c(\d+)\.log", f).groups())
    txt = open(f).read()
    h = hdr.search(txt); l = lv.search(txt); r = res.findall(txt)
    assert h and l and len(r) == 1, f
    th, cert, n, fail, t = r[0]
    assert th == "5.642100574331458", (f, th)
    p = parts[k]
    proc = int(h.group(1)); closed, slabs = int(l.group(1)), int(l.group(3))
    for key, v in (("processed", proc), ("closed", closed), ("slabs", slabs),
                   ("preclosed", int(h.group(2)) + int(l.group(2))), ("open", int(h.group(3)) + int(l.group(5))),
                   ("tiny", int(h.group(4)) + int(l.group(4)))):
        p.setdefault(key, v); assert p[key] == v, (f, key)
    p.setdefault("chunks", []).append(c)
    p["cert"] = p.get("cert", 0) + int(cert); p["n"] = p.get("n", 0) + int(n)
    p["fail"] = p.get("fail", 0) + int(fail); p["time"] = p.get("time", 0) + int(t)
P = L = 0
for k in sorted(parts):
    p = parts[k]; leaves = p["closed"] + p["slabs"]
    print(f"part {k}: chunks {sorted(p['chunks'])} processed {p['processed']} closed {p['closed']} slabs {p['slabs']} "
          f"leaves {leaves} certified {p['cert']}/{p['n']} fail {p['fail']} cpu {p['time']}s "
          f"preclosed/open/tiny {p['preclosed']}/{p['open']}/{p['tiny']} "
          f"processed==2*closed-1: {p['processed'] == 2*p['closed']-1}")
    assert p["n"] == leaves
    P += p["processed"]; L += leaves
    tot_cert += p["cert"]; tot_n += p["n"]; tot_fail += p["fail"]; tot_time += p["time"]
print(f"TOTAL processed {P} leaves {L} certified {tot_cert}/{tot_n} failures {tot_fail} cpu {tot_time}s")
print("leaves parts 0,2-7:", L - (parts[1]['closed'] + parts[1]['slabs']))
