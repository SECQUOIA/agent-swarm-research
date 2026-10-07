# Find long sentences (approximate word count, math collapsed) in main-text sections.
import re, sys, pathlib
base = pathlib.Path(__file__).resolve().parents[3] / "sections"
files = ["abstract","intro","related","setting","setting-growthcert","grids","growth","growth-sharp",
         "exact","exact-localized","recourse","recourse-valuefn","recourse-local","recourse-convex",
         "recourse-cuts","recourse-mixed","recourse-balanced","constraints","optsets","limits",
         "computation","conclusion"]
thr = int(sys.argv[1]) if len(sys.argv) > 1 else 55
for f in files:
    lines = (base / f"{f}.tex").read_text().split("\n")
    # join with line tracking
    text = ""; starts = []
    for i, l in enumerate(lines, 1):
        l = re.sub(r"(?<!\\)%.*", "", l)
        starts.append((len(text), i)); text += l + " "
    # collapse math
    t = re.sub(r"\\\[.*?\\\]", " M ", text, flags=re.S)
    t2 = re.sub(r"\$[^$]*\$", " M ", text)
    # sentence split on '. ' followed by capital or end (approximate), using t2 positions
    pos = 0
    for m in re.finditer(r"[^.;]*?\.(\s+(?=[A-Z\\])|$)", t2):
        s = m.group(0)
        words = [w for w in re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", " ", s).split() if re.search(r"[A-Za-z]", w)]
        if len(words) >= thr and "begin{" not in s:
            # locate line of start in original text approx by searching first 30 chars
            print(f"{f}.tex ~{len(words)} words: {s.strip()[:160]}")
