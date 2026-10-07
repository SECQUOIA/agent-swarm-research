# Word counts for the current abstract and the proposed replacement (math counted as one word per $...$).
import re, pathlib
base = pathlib.Path(__file__).resolve().parents[3]
def count(tex):
    tex = re.sub(r"\\begin\{abstract\}|\\end\{abstract\}", " ", tex)
    tex = re.sub(r"\$[^$]*\$", " M ", tex)
    tex = re.sub(r"\\[a-zA-Z]+", " ", tex)
    return len([w for w in tex.split() if re.search(r"[A-Za-z0-9]", w)])
cur = (base / "sections/abstract.tex").read_text()
new = open(base / "process/w4/checks/cwriting_abstract_proposed.tex").read()
print("current abstract words:", count(cur))
print("proposed abstract words:", count(new))
