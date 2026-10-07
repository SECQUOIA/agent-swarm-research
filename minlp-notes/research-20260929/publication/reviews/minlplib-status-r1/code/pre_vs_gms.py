"""Verifier: extract the GAMS listing embedded in an (archived) MINLPLib
instance page (between <PRE> and </PRE>), HTML-unescape it, and compare it
with a .gms file. Prints whether the texts are identical, identical after
whitespace normalisation, and the first differing lines otherwise.

Usage: python3 pre_vs_gms.py PAGE.html FILE.gms
"""
import difflib
import html
import re
import sys


def listing(page):
    t = open(page, encoding="utf-8", errors="replace").read()
    i = t.find("<PRE>")
    j = t.rfind("</PRE>")
    if i < 0 or j < 0:
        return None
    body = t[i + 5:j]
    # strip any html tags inside (links etc.)
    body = re.sub(r"<[^>]+>", "", body)
    return html.unescape(body)


def main(page, gms):
    a = listing(page)
    b = open(gms, encoding="utf-8", errors="replace").read()
    if a is None:
        print("no <PRE> listing")
        return
    na = [l.rstrip() for l in a.strip("\n").split("\n")]
    nb = [l.rstrip() for l in b.strip("\n").split("\n")]
    print(f"listing lines {len(na)}, gms lines {len(nb)}, raw identical: {a.strip(chr(10)) == b.strip(chr(10))}")
    print(f"identical after rstrip of lines: {na == nb}")
    if na != nb:
        d = list(difflib.unified_diff(na, nb, "archived", "current", n=0, lineterm=""))
        print(f"diff lines: {len(d)}")
        for l in d[:40]:
            print(l[:200])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
