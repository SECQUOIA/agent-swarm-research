"""R9 writing lens: sentence-length and word-count checks on the manuscript source.

Read-only. Strips LaTeX roughly (math -> X, commands removed), splits main-text
paragraphs into sentences, and reports:
  * abstract word count (math counted as one word each),
  * per-file sentence counts, mean length, and sentences above a threshold,
  * the longest sentences overall with file:line.
Usage: python R9_writing_sentences.py [threshold]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEC = ROOT / "sections"
MAIN = [
    "00-abstract", "01-introduction", "01b-results", "02-setting",
    "03-composition", "04-quadratic", "05-original", "06-certification",
    "07-implementation", "08a-setup", "08b-validity", "08c-minlplib",
    "08d-funnel", "08e-path", "08f-star", "08g-summary", "09-conclusions",
]
THRESH = int(sys.argv[1]) if len(sys.argv) > 1 else 45


def strip_env(text, env):
    return re.sub(r"\\begin\{%s\*?\}.*?\\end\{%s\*?\}" % (env, env), " ", text, flags=re.S)


def clean(tex):
    t = re.sub(r"(?<!\\)%.*", "", tex)
    for env in ("table", "figure", "tabular", "equation", "align", "proof"):
        t = strip_env(t, env)
    t = re.sub(r"\\\[.*?\\\]", " X ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " X ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", "X", t)
    t = re.sub(r"\\(cite[pt]?|citep|citet|ref|eqref|label)\*?(\[[^\]]*\])*\{[^}]*\}", "R", t)
    t = re.sub(r"\\(emph|code|textbf|textit|paragraph|subsection|section)\*?\{([^}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = t.replace("~", " ").replace("{", "").replace("}", "")
    return t


def sentences_with_lines(path):
    raw = path.read_text()
    lines = raw.splitlines()
    # map character offset -> line number on the raw text, then clean per paragraph
    out = []
    para, start = [], None
    for i, line in enumerate(lines + [""], 1):
        if line.strip() == "":
            if para:
                text = clean("\n".join(para))
                text = re.sub(r"\s+", " ", text).strip()
                # split on sentence end followed by space and capital/digit
                parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text)
                for s in parts:
                    w = len(s.split())
                    if w:
                        out.append((start, w, s))
                para, start = [], None
        else:
            if start is None:
                start = i
            para.append(line)
    return out


def main():
    abstract = clean((SEC / "00-abstract.tex").read_text())
    abstract = re.sub(r"\s+", " ", abstract).strip()
    print(f"abstract words (math = 1 word): {len(abstract.split())}")
    allsent = []
    print(f"\n{'file':22s} {'sent':>5s} {'mean':>6s} {'>'+str(THRESH):>5s}")
    for name in MAIN:
        p = SEC / f"{name}.tex"
        ss = sentences_with_lines(p)
        long_ = [s for s in ss if s[1] > THRESH]
        mean = sum(s[1] for s in ss) / max(1, len(ss))
        print(f"{name:22s} {len(ss):5d} {mean:6.1f} {len(long_):5d}")
        allsent += [(name, *s) for s in ss]
    allsent.sort(key=lambda r: -r[2])
    print(f"\nlongest sentences (paragraph start line):")
    for name, line, w, s in allsent[:25]:
        print(f"  {name}.tex:{line} [{w} words] {s[:150]}...")


if __name__ == "__main__":
    main()
