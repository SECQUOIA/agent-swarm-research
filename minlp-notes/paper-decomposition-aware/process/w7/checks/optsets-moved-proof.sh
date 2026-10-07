#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../../.." && pwd)"
# Check that the proof of thm:cells moved word for word from optsets.tex to appendix-proximal.tex.
cd "${_PUBLIC_REPO}"/paper-decomposition-aware
sed -n '148,186p' process/w7/sections-before-w7/optsets.tex | sed '1d;$d' > /tmp/optsets-old-proof.txt
awk '/Proof of Theorem~\\ref\{thm:cells\}/{f=1;next} f&&/\\end\{proof\}/{exit} f' sections/appendix-proximal.tex > /tmp/optsets-new-proof.txt
diff /tmp/optsets-old-proof.txt /tmp/optsets-new-proof.txt && echo "moved proof identical ($(wc -l < /tmp/optsets-new-proof.txt) lines)"
