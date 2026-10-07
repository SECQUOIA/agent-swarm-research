"""Convert a GAMS savepoint GDX (variable levels) to a MINLPLib-style .sol file.
Usage: python3 gdx2sol.py <gdx> <out.sol>"""
import re, subprocess, sys
G = 'gdxdump'
txt = subprocess.run([G, sys.argv[1]], capture_output=True, text=True).stdout
with open(sys.argv[2], "w") as f:
    for m in re.finditer(r"Variable (\w+) /L ([-+0-9.Ee]+)", txt):
        f.write(f"{m.group(1)} {m.group(2)}\n")
