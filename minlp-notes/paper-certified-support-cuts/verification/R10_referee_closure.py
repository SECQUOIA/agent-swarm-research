"""Round-3 referee-closure checks (targeted, read-only).

Reproduces the facts used in evidence/review3-referee.md:
  1. page layout of the compiled PDF (main text, references, appendices) from
     development/draft-round3/main.txt, and the number of cited references;
  2. abstract length (math counted as one word);
  3. campaign-5 cut counts per part and the replay status of every part
     (replay-part*.log / replay.json), i.e. whether the manuscript's
     "274,489 records, all passed replay" is backed by finished replays;
  4. Part 5C-b: callbacks, cut-cap hits and root-bound differences between the
     caps 32n and 64n;
  5. campaign-5 host load (start and end readings).
No solver is run. Usage: python R10_referee_closure.py
"""
import collections
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)
V5 = os.path.join(PAPER, "experiments", "v5", "runs")


def page_layout():
    pages = open(os.path.join(PAPER, "development", "draft-round3", "main.txt")).read().split("\f")
    marks = {}
    for i, p in enumerate(pages, 1):
        for line in p.splitlines():
            s = line.strip()
            if re.match(r"^References$", s) and "refs" not in marks:
                marks["refs"] = i
            if re.match(r"^A\s+Proof details", s) and "app" not in marks:
                marks["app"] = i
    print(f"pages {len(pages) - (1 if not pages[-1].strip() else 0)}; references start p. {marks.get('refs')}; "
          f"appendices start p. {marks.get('app')}")
    cited = set()
    for f in glob.glob(os.path.join(PAPER, "sections", "*.tex")) + glob.glob(os.path.join(PAPER, "figures", "*.tex")):
        for m in re.finditer(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}", open(f).read()):
            cited.update(k.strip() for k in m.group(1).split(","))
    bib = set(re.findall(r"^@\w+\{([^,]+),", open(os.path.join(PAPER, "references.bib")).read(), re.M))
    print(f"cited references {len(cited)}; bib entries {len(bib)}; uncited {sorted(bib - cited)}")


def abstract_words():
    t = open(os.path.join(PAPER, "sections", "00-abstract.tex")).read()
    t = t.replace("\\begin{abstract}", "").replace("\\end{abstract}", "")
    t = re.sub(r"\$[^$]*\$", "M", t)
    print(f"abstract words {len(t.split())}")


def campaign5_replay():
    total = 0
    for part in ["partS5", "partC5a", "partC5b", "partS5-rerun-spike"]:
        cuts = 0
        n = 0
        for line in open(os.path.join(V5, part, "records.jsonl")):
            r = json.loads(line)
            n += 1
            c = r.get("cuts") or 0
            cuts += c if isinstance(c, int) else len(c)
        rj = os.path.join(V5, part, "replay.json")
        log = os.path.join(V5, f"replay-{part}.log")
        status = "no replay.json"
        if os.path.exists(rj):
            d = json.load(open(rj))
            status = f"replay.json passed={d.get('passed')} replayed={d.get('replayed_cuts')}"
        elif os.path.exists(log):
            status = f"log {os.path.getsize(log)} bytes, no replay.json"
        print(f"{part}: records {n}, cuts {cuts}; {status}")
        if part != "partS5-rerun-spike":
            total += cuts
    print(f"campaign 5 cuts (protocol parts) {total}; campaigns 3-5 total {7498 + 30998 + 104771 + total}")


def c5b_caps():
    recs = [json.loads(l) for l in open(os.path.join(V5, "partC5b", "records.jsonl"))]
    calls = [r["separation"]["calls"] for r in recs]
    print(f"5C-b callbacks {min(calls)}-{max(calls)}")
    root = collections.defaultdict(dict)
    for r in recs:
        n = int(re.search(r"_n(\d+)_", r["name"]).group(1))
        cap = int(r["mode"].split("cap")[1])
        if r["separation"]["cuts"] >= cap * n:
            print(f"  cap reached: {r['name']} {r['mode']} cuts {r['separation']['cuts']}")
        root[r["name"]][r["mode"]] = r["root_dual"] if r["root_dual"] is not None else r["dual"]
    for p in ("frozen", "rowdir"):
        d = max(abs(v[p + "-cap32"] - v[p + "-cap64"]) for v in root.values())
        print(f"  max |root(cap32) - root(cap64)| {p}: {d:.3g}")


def c5_load():
    for part in ["partS5", "partC5a", "partC5b"]:
        L = []
        for line in open(os.path.join(V5, part, "records.jsonl")):
            r = json.loads(line)
            for k in ("load_start", "load_end"):
                x = r.get(k)
                if isinstance(x, (list, tuple)):
                    x = x[0]  # one-minute load average
                if x is not None:
                    L.append(float(x))
        L.sort()
        print(f"load {part}: min {L[0]:.2f} median {L[len(L) // 2]:.2f} max {L[-1]:.2f}; "
              f"readings > 20: {sum(x > 20 for x in L)}")


if __name__ == "__main__":
    page_layout()
    abstract_words()
    campaign5_replay()
    c5b_caps()
    c5_load()
