"""Run the official SCIP Opt Suite binaries (install/<version>/...) on a model
for a list of random seed shifts and classify each claim against the exact
witness value (WRONG if 'optimal' and dual bound > witness value + 1e-4).

usage: python3 run_binary.py MODEL.cip WITNESS_VALUE VERSIONS SEEDS [param=value,...]
VERSIONS: comma list among 10.0.2,10.0.3,10.1.0 (or 'dbgsol' for the local
build with the debug-solution mechanism, 'master' for the local build of SCIP master); SEEDS: comma list or a-b range.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.join(HERE, "install", "extralib", "usr", "lib", "x86_64-linux-gnu")


def binary(ver):
    if ver == "dbgsol":
        return os.path.join(HERE, "build", "dbgsol-10.0.2", "bin", "scip"), os.environ.get("LD_LIBRARY_PATH", "")
    if ver == "master":  # local Release build of SCIP master (11.0.0-dev) with SoPlex master (build/build_master.sh)
        return os.path.join(HERE, "build", "scip-master", "bin", "scip"), os.path.join(HERE, "conda-env", "lib")
    d = os.path.join(HERE, "install", ver, f"scipoptsuite-{ver}")
    return os.path.join(d, "bin", "scip"), os.path.join(d, "lib64") + ":" + EXTRA


def run(ver, model, params, timelimit=600):
    exe, ld = binary(ver)
    fd, setf = tempfile.mkstemp(suffix=".set")
    with os.fdopen(fd, "w") as f:
        f.write(f"limits/time = {timelimit}\n")
        for k, v in params.items():
            f.write(f"{k} = {v}\n")
    env = dict(os.environ, LD_LIBRARY_PATH=ld, OMP_NUM_THREADS="1")
    p = subprocess.run([exe, "-s", setf, "-c", f"read {model}", "-c", "optimize", "-c", "quit"],
                       capture_output=True, text=True, env=env, timeout=timelimit + 120)
    os.unlink(setf)
    out = p.stdout
    st = re.search(r"SCIP Status\s*:\s*(.*)", out)
    pb = re.search(r"Primal Bound\s*:\s*([-+0-9.eE]+|[+-]?infinity)", out)
    db = re.search(r"Dual Bound\s*:\s*([-+0-9.eE]+|[+-]?infinity)", out)
    nd = re.search(r"Solving Nodes\s*:\s*(\d+)", out)
    ver_line = re.search(r"SCIP version [^\n]*", out)
    return dict(status=st.group(1).strip() if st else f"exit{p.returncode}",
                primal=float(pb.group(1)) if pb else None, dual=float(db.group(1)) if db else None,
                nodes=int(nd.group(1)) if nd else None, version=ver_line.group(0) if ver_line else "?",
                out=out, rc=p.returncode)


def seeds_of(s):
    if "-" in s:
        a, b = s.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in s.split(",")]


def main():
    model, wval = sys.argv[1], float(sys.argv[2])
    vers, seeds = sys.argv[3].split(","), seeds_of(sys.argv[4])
    extra = {}
    if len(sys.argv) > 5 and sys.argv[5]:
        for kv in sys.argv[5].split(","):
            k, v = kv.split("=")
            extra[k] = v
    for ver in vers:
        nwrong = 0
        for s in seeds:
            prm = dict(extra)
            prm["randomization/randomseedshift"] = s
            r = run(ver, model, prm)
            wrong = r["status"].startswith("problem is solved [optimal") and r["dual"] is not None and r["dual"] > wval + 1e-4
            nwrong += wrong
            print(f"{ver} seed {s:3d} {r['status'][:40]:40s} dual {r['dual']} primal {r['primal']} nodes {r['nodes']} "
                  f"{'WRONG' if wrong else 'ok'}", flush=True)
        print(f"# {ver} ({r['version']}) {os.path.basename(model)} extra={extra}: wrong in {nwrong} of {len(seeds)} seeds",
              flush=True)


if __name__ == "__main__":
    main()
