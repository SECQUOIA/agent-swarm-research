"""Verifier (review r1 of minlplib-status): independent re-fetch of MINLPLib
site files, the 69 instance pages and the 69 OSIL files. Sequential, 1 s
delay between requests. Writes to ../dl/. Own code; does not import the
track's code.
"""
import hashlib
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "..", "dl")
UA = "minlp-notes verifier (sequential, 1 req/s)"

PAPER = """lnts50 lnts100 lnts200 lnts400 dtoc5 camshape100 camshape200 camshape400
camshape800 lukvle10 optcdeg2 hvycrash ex6_2_7 ex6_2_5 etamac pricing050 chain50 chain100
chain200 chain400 catmix100 catmix200 catmix400 catmix800 powerflow0030p powerflow0039p
powerflow0039r pindyck eg_int_s eg_disc_s eg_disc2_s kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9
kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8 waterno2_06 waterno2_09 waterno2_12 waterno2_18
waterno2_24 ann_cumene_tanh""".split()
AUDIT = """glider100 topopt-cantilever_60x40_50 methanol50 sssd20-04persp sssd22-08persp
sssd25-04persp sssd25-08persp nuclear14 ghg_3veh nd_netgen-2000-3-4-b-a-ns_7
watercontamination0303 smallinvDAXr1b150-165 smallinvDAXr2b150-165 smallinvDAXr1b200-220
smallinvDAXr2b200-220 eniplac lop97icx spring stockcycle emfl050_3_3 emfl050_5_5 emfl100_3_3
emfl100_5_5 rocket100 rocket200 rocket400""".split()
ALL = PAPER + AUDIT
assert len(PAPER) == 43 and len(set(ALL)) == 69


def get(url, limit=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = r.read(limit) if limit else r.read()
        return r.status, dict(r.headers), data


def main():
    os.makedirs(os.path.join(DL, "site"), exist_ok=True)
    os.makedirs(os.path.join(DL, "inst"), exist_ok=True)
    os.makedirs(os.path.join(DL, "osil"), exist_ok=True)
    man = {}
    jobs = [("site", f"https://www.minlplib.org/{f}", os.path.join(DL, "site", f), None)
            for f in ("instances.html", "minlplib.solu", "bounddates.html", "dates.html")]
    for n in ALL:
        jobs.append(("inst", f"https://www.minlplib.org/{n}.html", os.path.join(DL, "inst", n + ".html"), 400000))
        jobs.append(("osil", f"https://www.minlplib.org/osil/{n}.osil", os.path.join(DL, "osil", n + ".osil"), None))
    for kind, url, path, limit in jobs:
        if os.path.exists(path):
            continue
        try:
            st, hd, data = get(url, limit)
        except Exception as e:  # noqa: BLE001
            man[url] = dict(error=repr(e))
            print("ERR", url, e, flush=True)
            time.sleep(1)
            continue
        if kind == "inst":
            k = data.find(b"<PRE>")
            if k >= 0:
                data = data[:k]
        with open(path, "wb") as f:
            f.write(data)
        man[url] = dict(status=st, last_modified=hd.get("Last-Modified"), bytes=len(data),
                        sha256=hashlib.sha256(data).hexdigest(),
                        fetched=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        print(st, url, len(data), hd.get("Last-Modified"), flush=True)
        time.sleep(1)
    json.dump(man, open(os.path.join(DL, "manifest.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
