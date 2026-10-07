"""Check that eg-audit runs the code it claims to run.

1. Unchanged copies are byte-identical to their originals in research-20260929/ (md5 printed):
   cert/indep_cert.py, cert/gms_model.py, cert/data/*.gms and every file under record/.
2. cert/indep_cert_audit.py: undoing the audit wrappers mechanically
   (self._aexp(E, "site") -> np.exp(E); self._apow(X, k, "site"[, False]) -> X ** k) and dropping
   the other lines marked '# AUDIT' gives back the original indep_cert.py, line for line (blank
   lines ignored).  So the only changes are the checks; every value the certifier uses is the one
   the original computes.
3. cert/margin_cert_audit.py and cert/recheck_audit.py: every added or changed line carries the
   marker AUDIT or is a comment or blank; the replaced original lines are printed for review.
"""
import difflib
import glob
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, ".."))
R = os.environ.get("EG_AUDIT_R") or os.path.normpath(os.path.join(A, "..", "..", "..", "research-20260929"))
REV = os.path.join(R, "reviews", "eg-retry-review-checks")
REC = os.path.join(R, "publication", "eg-recheck")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def unwrap(line):
    """undo self._aexp(...) and self._apow(...) in one line (balanced parentheses)."""
    for name in ("self._aexp(", "self._apow("):
        while name in line:
            i = line.index(name)
            j, depth, args, cur = i + len(name), 1, [], ""
            while depth:
                ch = line[j]
                if ch in "([":
                    depth += 1
                elif ch in ")]":
                    depth -= 1
                if depth == 1 and ch == ",":
                    args.append(cur.strip()); cur = ""
                elif depth:
                    cur += ch
                j += 1
            args.append(cur.strip())
            new = f"np.exp({args[0]})" if name == "self._aexp(" else f"{args[0]} ** {args[1]}"
            line = line[:i] + new + line[j:]
    return line


def main():
    bad = 0
    print("== 1. unchanged copies")
    pairs = [(os.path.join(A, "cert", f), os.path.join(REV, f)) for f in ("indep_cert.py", "gms_model.py")]
    pairs += [(p, os.path.join(REV, "data", os.path.basename(p))) for p in sorted(glob.glob(os.path.join(A, "cert", "data", "*.gms")))]
    for p in sorted(glob.glob(os.path.join(A, "record", "research-20260929", "**", "*"), recursive=True)):
        if os.path.isfile(p):
            pairs.append((p, os.path.join(R, os.path.relpath(p, os.path.join(A, "record", "research-20260929")))))
    for a, b in pairs:
        same = open(a, "rb").read() == open(b, "rb").read()
        bad += not same
        print(f"  {'identical' if same else 'DIFFERENT'}  {md5(a)}  {os.path.relpath(a, A)}  <-  {os.path.relpath(b, R)}")
    print("== 2. indep_cert_audit.py with the audit undone == indep_cert.py")
    orig = [x.rstrip() for x in open(os.path.join(REV, "indep_cert.py")) if x.strip()]
    back = []
    for x in open(os.path.join(A, "cert", "indep_cert_audit.py")):
        if "# AUDIT" in x:
            if "self._aexp(" not in x and "self._apow(" not in x:
                continue
            x = unwrap(x.split("  # AUDIT")[0])
        if x.strip():
            back.append(x.rstrip())
    same = back == orig
    bad += not same
    print(f"  identical after undoing the audit: {same} ({len(orig)} non-blank lines)")
    if not same:
        print("\n".join(difflib.unified_diff(orig, back, "indep_cert.py", "undone", lineterm="", n=0)))
    print("== 3. marked changes of the other two copies")
    for new, old in (("margin_cert_audit.py", os.path.join(REC, "margin_cert.py")),
                     ("recheck_audit.py", os.path.join(REC, "recheck_leaves.py"))):
        a = open(old).read().splitlines()
        b = open(os.path.join(A, "cert", new)).read().splitlines()
        d = list(difflib.unified_diff(a, b, lineterm="", n=0))
        added = [x[1:] for x in d if x.startswith("+") and not x.startswith("+++")]
        removed = [x[1:] for x in d if x.startswith("-") and not x.startswith("---")]
        unmarked = [x for x in added if "AUDIT" not in x and x.strip() and not x.strip().startswith("#")]
        bad += len(unmarked)
        print(f"  {new}: {len(added)} added/changed lines, unmarked {len(unmarked)}; replaced original lines:")
        for x in removed:
            print(f"    - {x.strip()}")
        for x in unmarked:
            print(f"    UNMARKED + {x}")
    print("ALL COPY CHECKS PASSED" if not bad else f"COPY CHECKS FAILED ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
