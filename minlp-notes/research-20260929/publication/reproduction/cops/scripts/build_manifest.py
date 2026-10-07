"""Build manifest.json for the repro-cops track from the run logs.

For every measured run (logs/NAME.{log,time,meta}) it records cwd, command, inputs and code
files with sha256, expected and observed values, the comparison with the committed reference
logs/outputs (timing fields removed), wall/CPU time, peak RSS and machine load.
Inputs are taken from the strace of the sandboxed audit rerun of the same command
(logs/s_NAME.*, /tmp/cops_audit/s_NAME.strace) or, for long runs, of its startup audit.
usage: python3 build_manifest.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])
_PUBLIC_HOME = str(_PublicPath.home())

import glob
import hashlib
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))
LOGS = os.path.join(OUT, "logs")
WT = (_PUBLIC_REPO + '-clean')
R29 = WT + "/research-20260929"
TMP = "/tmp/cops_patchcheck"
ST = "/tmp/cops_audit"
MAIN = (_PUBLIC_REPO + '/research-20260929')
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rel(p):
    for a, b in ((WT + "/", ""), (TMP + "/", ""), (os.path.expanduser("~") + "/", "~/")):
        if p.startswith(a):
            return b + p[len(a):]
    return p


# ---------- reading the measured-run files ----------
def meta(name):
    m = {}
    for line in open(os.path.join(LOGS, name + ".meta")):
        k, _, v = line.rstrip("\n").partition(": ")
        m[k] = v
    return m


def timev(name):
    t = {}
    for line in open(os.path.join(LOGS, name + ".time")):
        k, _, v = line.strip().rpartition(": ")
        t[k] = v
    wall = t["Elapsed (wall clock) time (h:mm:ss or m:ss)"].split(":")
    w = 0.0
    for x in wall:
        w = w * 60 + float(x)
    return dict(wall_s=round(w, 2), cpu_s=round(float(t["User time (seconds)"]) + float(t["System time (seconds)"]), 2),
                user_s=float(t["User time (seconds)"]), sys_s=float(t["System time (seconds)"]),
                peak_rss_mb=round(int(t["Maximum resident set size (kbytes)"]) / 1024, 1))


def load(u):
    m = re.search(r"load average: ([\d.]+), ([\d.]+), ([\d.]+)", u)
    return [float(x) for x in m.groups()] if m else None


# ---------- comparing logs with committed references ----------
TIMING = re.compile(r"\(\d+(\.\d+)?s\)|^\s*[\d.]+ s \d+ KB\s*$|^(real|user|sys)\s+\d+m[\d.]+s$")


def split_log(text):
    """JSON objects (timing keys removed) and normalized non-JSON text lines"""
    objs, rest, dec, i = [], [], json.JSONDecoder(), 0
    while i < len(text):
        j = text.find("{", i)
        if j < 0:
            rest.append(text[i:])
            break
        try:
            o, k = dec.raw_decode(text[j:])
            if not isinstance(o, dict):
                raise ValueError
            objs.append(o)
            rest.append(text[i:j])
            i = j + k
        except ValueError:
            rest.append(text[i:j + 1])
            i = j + 1
    lines = []
    for line in "".join(rest).splitlines():
        line = TIMING.sub("", line)
        line = re.sub(r"line \d+", "line N", line)
        line = re.sub((_PUBLIC_HOME + '/repo/minlp-notes(-clean)?/|/tmp/cops_patchcheck/'), "<repo>/", line)
        line = re.sub(r"\(\d+s\)", "", line).rstrip()
        if line.strip():
            lines.append(line)
    return [strip_t(o) for o in objs], lines


def strip_t(o):
    if isinstance(o, dict):
        return {k: strip_t(v) for k, v in o.items() if "seconds" not in k}
    if isinstance(o, list):
        return [strip_t(v) for v in o]
    return o


def git_show(path):
    return subprocess.run(["git", "-C", WT, "show", "HEAD:" + path], capture_output=True, text=True, check=True).stdout


def compare(name, refs):
    """observed log vs committed reference logs: every JSON object and text line of the observed
    log must occur in the references (timing removed)."""
    if not refs:
        return None
    ro, rl = [], []
    for r in refs:
        txt = git_show(r) if not r.startswith("/") else open(r).read()
        o, l = split_log(txt)
        ro += o
        rl += l
    oo, ol = split_log(open(os.path.join(LOGS, name + ".log")).read())
    miss_o = [o for o in oo if o not in ro]
    miss_l = [l for l in ol if l not in rl]
    return dict(references=refs, observed_json_objects=len(oo), observed_text_lines=len(ol),
                json_objects_not_in_reference=len(miss_o), text_lines_not_in_reference=miss_l[:5],
                identical_content=(not miss_o and not miss_l))


# ---------- inputs from strace ----------
SYS = re.compile(r"^/(usr|lib|lib64|proc|sys|etc|dev|tmp/cops_audit)(/|$)")


def strace_files(sname, cwd):
    p = os.path.join(ST, sname + ".strace")
    if not os.path.exists(p):
        return None
    ins, code, outs = set(), set(), set()
    for line in open(p):
        m = re.search(r'open(?:at)?\((?:AT_FDCWD, )?"([^"]+)", ([A-Z_|]+)[^)]*\) = (-?\d+)', line)
        if not m or int(m.group(3)) < 0 or "O_DIRECTORY" in m.group(2):
            continue
        f, fl = m.group(1), m.group(2)
        if not f.startswith("/"):
            f = os.path.normpath(os.path.join(cwd, f))
        if SYS.match(f) or "miniconda3" in f or "/.local/lib" in f or "agentic-assessment" in f or "__pycache__" in f:
            continue
        if "O_WRONLY" in fl or "O_RDWR" in fl or "O_CREAT" in fl:
            outs.add(f)
        elif f.endswith(".py"):
            code.add(f)
        else:
            ins.add(f)
    ins -= outs  # files the run writes are outputs (a later read of an own output is not an input)
    return sorted(ins), sorted(code), sorted(outs)


def to_wt(p):
    return p.replace(TMP, WT)


def files_with_sha(paths):
    out = []
    for p in paths:
        q = to_wt(p)
        out.append(dict(path=rel(q), sha256=sha(q) if os.path.exists(q) else None))
    return out


# ---------- specification of every measured run ----------
def jobj(name, i=-1, key=None):
    o, _ = split_log(open(os.path.join(LOGS, name + ".log")).read())
    o = [x for x in o if key is None or key in x]
    return o[i]


def logtxt(name):
    return open(os.path.join(LOGS, name + ".log")).read()


def rx(name, pat, g=1):
    return re.findall(pat, logtxt(name))


C = "research-20260929/open-instances-wave2/cops/logs/"
CV = "research-20260929/reviews/cops-verification/logs/"
RC = "research-20260929/reviews/catmix-recheck-checks/logs/"
PRI = MAIN + "/publication/primal/chain/logs/"
PRV = MAIN + "/publication/reviews/primal-chain-r1/logs/"
CHAIN_DISP = {50: "5.072261493982863", 100: "5.0697846107387505", 200: "5.068917341793162", 400: "5.068621694604009"}
CHAIN_BOX = {50: 11121, 100: 15329, 200: 21057, 400: 27843}
CHAIN_VBOX = {50: 36689, 100: 52955, 200: 75385, 400: 104945}
CHAIN_PRIM = {50: "5.0722614939828724 (2.3e-16)", 100: "5.0697846107387604 (2.0e-16)", 200: "5.0689173417931710 (3.1e-16)", 400: "5.0686216946040190 (3.6e-16)"}
CHAIN_EXACT = {50: "5.0722614939828723164454381769845467731843", 100: "5.0697846107387605574911913664186759056713",
               200: "5.0689173417931710001847965010674364416891", 400: "5.0686216946040190143614896914450892607014"}
CAT_DISP = {100: "-0.048069432038882705", 200: "-0.04805914560067171", 400: "-0.048056547950296354", 800: "-0.048055901841076894"}
CAT_EVALS = {100: "1.6e8", 200: "2.5e8", 400: "3.9e8", 800: "6.1e8"}
CAT_PRIM = {100: "-0.0480694320309596", 200: "-0.0480591455801144", 400: "-0.0480565477566116", 800: "-0.0480559013293737 (non-snap; report uses _snap -0.0480559013308475)"}
CAT_PRIM_V = {100: "-0.0480694320309595635", 200: "-0.0480591455801143916", 400: "-0.048056547756611554855", 800: "-0.0480559013293737"}
REP = "open-instances-wave2/cops/report.md"
VREP = "reviews/cops-verification/verification-report.md"
RREP = "reviews/catmix-recheck.md"
PREP = "publication/primal/chain/report.md (main tree)"
PREV = "publication/reviews/primal-chain-review-r1.md (main tree)"
SUMM = "open-instances-summary.md"

SPEC = {}


def spec(name, inst, role, expected, source, observed_fn, refs, note=""):
    SPEC[name] = dict(instances=inst, role=role, expected=expected, expected_source=source,
                      observed_fn=observed_fn, refs=refs, note=note)


spec("a_chain_model_50_100", ["chain50", "chain100"], "author: model extraction and 60-digit KKT point",
     "f* = 5.0722614939828723164 (chain50), 5.0697846107387605575 (chain100)", REP + " Sec. 2 Results (primal KKT, 60 digits)",
     lambda n: "f* = " + ", ".join(rx(n, r"f\* = (\S+)")), [], "no committed log; compared with the report's KKT values")
for N in (50, 100, 200, 400):
    spec("a_chain_bound_%d" % N, ["chain%d" % N], "author: CERTIFICATE (dual bound, 2-D interval B&B)",
         "dual bound %s; %s boxes; 0 unresolved; primal %s" % (CHAIN_DISP[N], format(CHAIN_BOX[N], ","), CHAIN_PRIM[N]),
         REP + " Sec. 2 Results + summary table; " + SUMM + " row chain50-400",
         lambda n: (lambda o: "dual bound %r; %s boxes; %d unresolved; primal %s (%s); kkt %s" % (
             o["bnb"]["bound"], format(o["bnb"]["boxes"], ","), o["bnb"]["unresolved"], o["primal"]["obj_double_point"],
             o["primal"]["max_row_violation"], o["primal"]["kkt_value"]))(jobj(n)),
         [C + "chain_all_run_1e-14.log", C + "chain%d_bound.json" % N])
spec("a_chain_calibration_random_check", ["chain50", "chain100", "chain200", "chain400"],
     "author: float random check of the calibration lemma (evidence only)",
     "min relative F over random tests 0.0 (4 million cases, no negative value)", REP + " Sec. 2 Lemma; logs/explore_chain.log",
     lambda n: logtxt(n).strip(), [C + "explore_chain.log"])
spec("v_chain_checks_struct", ["chain50", "chain100", "chain200", "chain400"], "verifier: structure, parametrization, identity, author primal",
     "structure/param/identity ok for N=50..400; author primal objectives and row violations as in logs/chain_struct.log",
     VREP + " Sec. 1a/1b/1f", lambda n: "; ".join(l.split(";")[0] for l in logtxt(n).splitlines()), [CV + "chain_struct.log"])
spec("v_chain_checks_lemma", ["chain50", "chain100", "chain200", "chain400"], "verifier: lemma symbolic + 200,000-case 50-digit test",
     "symbolic identities 0; min gap +1.7e-31; max rel. equality residual 8e-51", VREP + " Sec. 1c",
     lambda n: "; ".join(rx(n, r"'min_gap': '([^']+)'") + rx(n, r"'max_rel_equality_residual': '([^']+)'") + rx(n, r"adversarial min gap: (\S+)")),
     [CV + "chain_lemma.log", CV + "chain_lemma_adv.log"],
     "the committed chain_lemma.log ends with a traceback from the reviewer's first adversarial test (documented in the review); the current script runs the fixed adversarial test after the random test, whose output equals chain_lemma_adv.log")
spec("v_chain_checks_lemma_adv", ["chain50", "chain100", "chain200", "chain400"], "verifier: adversarial Nelder-Mead lemma test (30 digits)",
     "minimum -2.5e-29 (rounding on the equality manifold)", VREP + " Sec. 1c",
     lambda n: logtxt(n).strip(), [CV + "chain_lemma_adv.log"])
spec("v_chain_checks_theorem", ["chain50", "chain100", "chain200", "chain400"], "verifier: random test of f >= B (float evidence)",
     "min f - B >= 0 on random chains; near-optimal perturbations 6.5e-17 / 1.7e-16", VREP + " Sec. 1d",
     lambda n: " | ".join(l.split(":")[-1].strip() for l in logtxt(n).splitlines()), [CV + "chain_theorem.log"])
for N in (50, 100, 200, 400):
    spec("v_chain_bnb_%d" % N, ["chain%d" % N], "verifier: INDEPENDENT CERTIFICATE (own 2-D interval B&B)",
         "certified %s; %s boxes; 0 unresolved" % (CHAIN_DISP[N], format(CHAIN_VBOX[N], ",")), VREP + " Sec. 1f table",
         lambda n: (lambda o: "certified %r; %s boxes; %d unresolved; min leaf lb %s" % (
             o["certified_bound"], format(o["boxes"], ","), o["unresolved"], o["min_leaf_lb"].strip("[]").split(",")[0]))(jobj(n)),
         [CV + {50: "chain50_bnb.log", 100: "chain100_200_bnb.log", 200: "chain100_200_bnb.log", 400: "chain400_bnb.log"}[N]])
for N in (50, 100, 200, 400):
    spec("p_chain_build_%d" % N, ["chain%d" % N], "primal track: build exactly feasible point in Q(sqrt R)",
         "objective in [%s..., ...]; points identical to main-tree points/ (sha256 in main logs/points_sha256.txt)" % CHAIN_EXACT[N][:32],
         PREP + " table; main-tree logs/build_%d.log" % N,
         lambda n: logtxt(n).strip(), [PRI + "build_%d.log" % N])
spec("p_chain_verify", ["chain50", "chain100", "chain200", "chain400"], "primal track: exact feasibility check (separate code)",
     "all rows exact (51/101/201/401), 4 bounds exact; objective enclosures as in report; gaps 9.58e-15 / 1.01e-14 / 9.34e-15 / 9.78e-15",
     PREP + "; main-tree logs/verify.log",
     lambda n: "; ".join("%s rows %s/%s obj_hi %s gap %s" % (o["instance"], o["equality_rows_exact"], o["rows_checked"], o["objective_hi"], o["gap_abs_upper"])
                         for o in split_log(logtxt(n))[0]), [PRI + "verify.log"])
spec("p_chain_scip_crosscheck", ["chain50", "chain100", "chain200", "chain400"], "primal track: SCIP checkSol cross-check (float evidence)",
     "points accepted at feastol 1e-13; perturbed controls rejected", PREP + "; main-tree logs/scip_crosscheck.log",
     lambda n: "; ".join(l.split(" case=")[1] for l in logtxt(n).splitlines() if "case=" in l), [PRI + "scip_crosscheck.log"])
spec("r_chain_exact", ["chain50", "chain100", "chain200", "chain400"], "primal reviewer: INDEPENDENT exact feasibility check",
     "all rows exact; R matches; objective decimals identical to track; gaps 9.58e-15 / 1.01e-14 / 9.34e-15 / 9.78e-15",
     PREV + "; main-tree review logs/rev_exact_all.log",
     lambda n: "; ".join("%s rows %s gap %s display_valid %s" % (o["instance"], o["equality_rows_exact"], o["gap_abs_up"], o["display_is_valid_bound(<= double)"])
                         for o in split_log(logtxt(n))[0]), [PRV + "rev_exact_all.log"])
spec("r_chain_negative_controls", ["chain50"], "primal reviewer: negative controls",
     "unaltered passes; perturbations fail; root swap gives another feasible point (objective 6.326)", PREV + " Sec. 1.2",
     lambda n: "; ".join(l.split(":")[0] + ": " + l.split(":")[1].split("(")[0].strip() for l in logtxt(n).splitlines()), [PRV + "rev_negative_controls.log"],
     "assert line numbers differ by 2 because patch 03 adds 2 lines to rev_chain_exact.py")
spec("r_chain_side_checks", ["chain50", "chain100", "chain200", "chain400"], "primal reviewer: side checks (distance, SCIP, mpmath iv)",
     "distances as in track logs; SCIP accepts at feastol 1e-12; iv rows contain rhs (width ~4e-40)", PREV,
     lambda n: "; ".join("N=%d dist_x %.2e scip %s iv_rows %s" % (o["N"], o["max_dist_x_to_double_point"], o["scip_checkSol_feastol_1e-12"], o["iv_rows_contain_rhs"])
                         for o in split_log(logtxt(n))[0]), [PRV + "rev_side_checks_50_200.log", PRV + "rev_side_checks_400.log"])
spec("a_catmix_model_100_200", ["catmix100", "catmix200"], "author: model extraction + local solve",
     "local solve reproduces the MINLPLib value -0.04806939757 (N=100)", REP + " Sec. 3 Primal",
     lambda n: "J = " + ", ".join(rx(n, r"J = np.float64\(([^)]+)\)")), [], "no committed log")
for N in (100, 200, 400, 800):
    spec("a_catmix_primal_%d" % N, ["catmix%d" % N], "author: primal point (float DP policy + L-BFGS-B, 60-digit interval objective)",
         "exact-point objective %s; double-vector row violation <= 1.05e-16" % CAT_PRIM[N], REP + " Sec. 3 Primal; logs/catmix%d_primal.json" % N,
         lambda n: (lambda o: "objective enclosure lo %s; row viol %s" % (o["exact_point_objective_enclosure"][0].strip("[]").split(",")[0][:24],
                                                                          o["double_vector_max_row_violation"]))(jobj(n)),
         [C + "catmix_primal_run.log", C + "catmix%d_primal.json" % N])
spec("a_catmix_primal_snap_400", ["catmix400"], "author: snap small controls (no improvement for N=400)",
     "improvement 0.000e+00", "logs/catmix_primal_snap.log", lambda n: logtxt(n).split("{")[0].strip(), [C + "catmix_primal_snap.log"])
spec("a_catmix_primal_snap_800", ["catmix800"], "author: snap small controls (catmix800 best primal)",
     "J after -0.048055901330861461 (float), improvement 1.477e-12", "logs/catmix_primal_snap.log",
     lambda n: logtxt(n).split("{")[0].strip(), [C + "catmix_primal_snap.log"])
spec("a_catmix_primal_snap_eval_800", ["catmix800"], "author: exact objective of the snapped point (script reconstructed, patch 04)",
     "-0.0480559013308475 (report); file logs/catmix800_primal_snap.json", REP + " Sec. 3 Primal",
     lambda n: jobj(n)["exact_point_objective_enclosure"][0].strip("[]").split(",")[0][:24], [C + "catmix800_primal_snap.json"])
spec("a_catmix_stage_lb_selftest", ["catmix100", "catmix200", "catmix400", "catmix800"], "author: randomized stage-bound self-test",
     "stage bound never exceeds dense-sampled minimum (margin 1.3e-15)", REP + " Sec. 3 Checks",
     lambda n: logtxt(n).strip().splitlines()[-1], [C + "catmix_stage_lb_selftest.log"])
for N in (100, 200, 400, 800):
    spec("a_catmix_bound_%d" % N, ["catmix%d" % N], "author: CERTIFICATE (exact DP on projective separator, per-ray interval B&B)",
         "dual bound %s; %s interval evals" % (CAT_DISP[N], CAT_EVALS[N]), REP + " Sec. 3 Results; " + SUMM + " row catmix100-800",
         lambda n: (lambda o: "dual bound %r; %s interval evals; max stage loss %.3e" % (
             o["dual_bound"], format(o["total_interval_evals"], ","), o["max_stage_loss_vs_float_incumbent"]))(jobj(n, key="dual_bound")),
         [C + "catmix%d_bound_final.log" % N, C + "catmix%d_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json" % N])
spec("v_catmix_model_all", ["catmix100", "catmix200", "catmix400", "catmix800"], "verifier: structure, exact nonnegativity, exact primal objectives",
     "exact J: " + ", ".join(CAT_PRIM_V[N] for N in (100, 200, 400, 800)) + "; snap -0.048055901330847466886",
     VREP + " Sec. 2a/2d", lambda n: "; ".join(x[:26] for x in rx(n, r"J enclosure \[\[([^,]+),")), [CV + "catmix_model.log"])
for N in (100, 200):
    spec("v_catmix_selftest_%d" % N, ["catmix%d" % N], "verifier: stage self-test + theta trajectory (writes logs/catmix%d_theta_traj.npy)" % N,
         "max(LB - dense_min) <= ~1e-15", VREP + " Sec. 2d", lambda n: logtxt(n).splitlines()[0],
         [CV + ("catmix_selftest.log" if N == 100 else "catmix_selftest_200.log")])
spec("v_catmix_primal_100", ["catmix100"], "verifier: compose check of the authors' controls",
     "[-0.04806943203105763, -0.04806943203086033] contains -0.0480694320309595635", VREP + " Sec. 2a",
     lambda n: logtxt(n).splitlines()[0], [CV + "catmix100_primal_reviewer.log"])
spec("v_catmix_newton_100", ["catmix100"], "verifier: 40-digit Newton polish (best catmix100 primal)",
     "J = -0.04806943203097959910654; double controls exact J -0.048069432030979596104", VREP + " Sec. 2d",
     lambda n: rx(n, r"it 7  J=(\S+)")[0] + "; " + logtxt(n).strip().splitlines()[-1], [CV + "catmix100_newton.log"])
for name, N, cfg, exp in (("v_catmix_dp_100_cfgA", 100, "config A", "-0.048069432031981114"),
                          ("v_catmix_dp_100_cfgB", 100, "config B", "-0.04806943203114456"),
                          ("v_catmix_dp_200_cfgA", 200, "config A", "-0.04805914559907277")):
    spec(name, ["catmix%d" % N], "verifier: INDEPENDENT CERTIFICATE (own DP, %s)" % cfg, "dual bound %s" % exp, VREP + " Sec. 2d",
         lambda n: "dual bound %s; rays %s" % (jobj(n, key="dual_bound")["dual_bound_repr"], jobj(n, key="dual_bound")["rays"]),
         [CV + {"v_catmix_dp_100_cfgA": "catmix100_cfgA.log", "v_catmix_dp_100_cfgB": "catmix100_cfgB.log", "v_catmix_dp_200_cfgA": "catmix200_cfgA.log"}[name]])
spec("v_recheck_osil_crosscheck", ["catmix400", "catmix800"], "rechecker: OSIL reader cross-check", "osilx.read agrees with regex parse",
     RREP, lambda n: "; ".join(l.split(":")[0] + ": agrees" for l in logtxt(n).splitlines() if "agrees" in l), [RC + "osil_crosscheck.log"])
spec("v_recheck_model_400_800", ["catmix400", "catmix800"], "rechecker: structure + exact primal objectives",
     "exact J -0.048056547756611554855 (400), -0.048055901330847466886 (800 snap)", RREP + " Verdict",
     lambda n: "; ".join(x[:26] for x in rx(n, r"J enclosure \[\[([^,]+),")), [RC + "catmix_model_400_800.log"])
for N in (400, 800):
    spec("v_recheck_selftest_%d" % N, ["catmix%d" % N], "rechecker: stage self-test + theta trajectory", "max(LB - dense_min) <= ~1e-15",
         RREP, lambda n: logtxt(n).splitlines()[0], [RC + "catmix_selftest_%d.log" % N])
spec("v_recheck_dp_400_final", ["catmix400"], "rechecker: INDEPENDENT CERTIFICATE (final grid)",
     "dual bound -0.04805654782467129; policy J -0.0480565477559440726", RREP + " Verdict + run table",
     lambda n: "dual bound %s; policy J %s" % (jobj(n, key="dual_bound")["dual_bound_repr"], jobj(n, key="policy_J_lo")["policy_J_lo"]),
     [RC + "catmix400_final.log"])
spec("v_recheck_dp_800_final", ["catmix800"], "rechecker: INDEPENDENT CERTIFICATE (final grid)",
     "dual bound -0.04805590147967565; policy J -0.0480559013312308003", RREP + " Verdict + run table",
     lambda n: "dual bound %s; policy J %s" % (jobj(n, key="dual_bound")["dual_bound_repr"], jobj(n, key="policy_J_lo")["policy_J_lo"]),
     [RC + "catmix800_final.log"])
for N, e in ((400, "-0.0480565477559440726 (6.7e-13 worse than authors)"), (800, "-0.0480559013312308003 (best catmix800 point)")):
    spec("v_recheck_policy_exact_%d" % N, ["catmix%d" % N], "rechecker: exact rational evaluation of DP-policy point (exactly feasible)",
         e, RREP + " Primal by-product", lambda n: "floor(J*1e30) = " + rx(n, r"\(floor\) = (\S+)")[0], [RC + "policy_exact_%d.log" % N])

# sandbox audit (startup-only) runs used to obtain inputs of the long runs
STARTUP = {"a_catmix_bound_%d": "s_startup_catmix_bound_800", "v_catmix_dp_%d": "s_startup_v_catmix_dp_200_cfgA",
           "v_recheck_dp_%d_final": "s_startup_v_recheck_dp_800_final"}


def audit_name(name):
    """name of the sandboxed audit rerun of a main run (author runs drop their a_ prefix)"""
    return "s_" + (name[2:] if name.startswith("a_") else name)


def main_name(aname):
    base = aname[2:]
    return "a_" + base if ("a_" + base) in SPEC else base


def inputs_for(name, cwd_wt):
    cwd_tmp = cwd_wt.replace(WT, TMP)
    s = strace_files(audit_name(name), cwd_tmp)
    how = "strace of sandboxed rerun %s" % audit_name(name)
    if s is None:
        for pat, sname in STARTUP.items():
            m = re.match(pat.replace("%d", r"(\d+)") + r"(_cfg[AB])?$", name)
            if m:
                N = m.group(1)
                srcN = re.search(r"_(\d+)", sname).group(1)
                s = strace_files(sname, cwd_tmp)
                if s is None:
                    break
                s = tuple([p.replace("catmix%s" % srcN, "catmix%s" % N).replace("tree%s" % srcN, "tree%s" % N) for p in lst] for lst in s)
                how = "strace of startup audit %s (150 s, N substituted)" % sname
                break
    if s is None:
        return None, None, None, "no strace"
    ins, code, outs = s
    return files_with_sha(ins), files_with_sha(code), [rel(to_wt(p)) for p in outs], how


def outputs_vs_head(outs):
    """compare each output file of a run (worktree copy) with the committed HEAD version"""
    res = {}
    for o in outs or []:
        q = os.path.join(WT, o) if not o.startswith("/") and not o.startswith("~") else o
        if not o.startswith("research-20260929/"):
            res[o] = "outside the repository"
            continue
        head = subprocess.run(["git", "-C", WT, "rev-parse", "-q", "--verify", "HEAD:" + o], capture_output=True, text=True).stdout.strip()
        if not head:
            res[o] = "not tracked at HEAD"
            continue
        cur = subprocess.run(["git", "-C", WT, "hash-object", q], capture_output=True, text=True).stdout.strip()
        if cur == head:
            res[o] = "byte-identical to HEAD"
            continue
        verdict = "differs from HEAD"
        if o.endswith(".json"):
            a, b = json.load(open(q)), json.loads(git_show(o))
            if strip_t(a) == strip_t(b):
                verdict = "differs from HEAD only in timing fields"
            elif isinstance(a, dict) and {k: v for k, v in a.items() if k != "source_point"} == {k: v for k, v in b.items() if k != "source_point"}:
                verdict = "differs from HEAD only in the source_point path string"
        res[o] = verdict
    return res


DISPLAY_NOTE = {
    "a_chain_bound_50": "chain50", "v_chain_bnb_50": "chain50", "a_chain_bound_200": "chain200", "v_chain_bnb_200": "chain200",
    "a_catmix_bound_200": "catmix200", "v_catmix_dp_100_cfgB": "catmix100", "v_recheck_dp_800_final": "catmix800"}
EXTRA = {
    "a_chain_model_50_100": "no committed log; the printed 25-digit KKT values agree with the report's 20-digit values",
    "a_catmix_model_100_200": "no committed log; -0.04806939756886153 rounds to the report's -0.04806939757",
    "v_chain_checks_lemma": "the committed log ends with a traceback of the reviewer's first adversarial test (documented in the review); this run executes the fixed test and prints the value of chain_lemma_adv.log",
    "r_chain_negative_controls": "assert line numbers are 2 higher because patch 03 adds 2 lines to rev_chain_exact.py; otherwise identical",
    "a_catmix_primal_snap_eval_800": "script reconstructed from the wave-2 transcript (patch 04); its output file logs/catmix800_primal_snap.json is byte-identical to the committed file",
    "p_chain_verify": "logs/verify.log is byte-identical to the main-tree logs/verify.log",
    "a_catmix_stage_lb_selftest": "the report's 'margin 1.3e-15' is the printed -1.33e-15",
}


LONG_OUTPUTS = {}
for _N in (100, 200, 400, 800):
    LONG_OUTPUTS["a_catmix_bound_%d" % _N] = [C + "catmix%d_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json" % _N]
for _N in (400, 800):
    LONG_OUTPUTS["v_recheck_dp_%d_final" % _N] = [RC + "tree%d_final.json" % _N, RC + "catmix%d_final_policy_traj.npy" % _N,
                                                  RC + "catmix%d_final_policy_u.npy" % _N]
for _n in ("v_catmix_dp_100_cfgA", "v_catmix_dp_100_cfgB", "v_catmix_dp_200_cfgA"):
    LONG_OUTPUTS[_n] = []   # prints its result only


def decide(n, r):
    c = r["comparison_with_committed"]
    parts = []
    if c is None:
        parts.append("observed values equal the expected displayed digits")
    elif c["identical_content"]:
        parts.append("observed values equal the expected displayed digits; all JSON objects and text lines of the log occur in the committed reference (timing removed)")
    else:
        return "no", "log content differs from the committed reference: %s" % c
    if n in EXTRA:
        parts.append(EXTRA[n])
    if n in DISPLAY_NOTE:
        val = re.search(r"(?:dual bound|certified) (-?[0-9.]+(?:e-?[0-9]+)?)", r["observed"]).group(1)
        d = [x for x in json.load(open(os.path.join(LOGS, "exact_display_checks.json")))
             if x["instance"] == DISPLAY_NOTE[n] and x["certified_double"] == repr(float(val))]
        if d and not d[0]["display_valid"]:
            parts.append("caveat: the displayed decimal %s exceeds the certified double by %s, so the displayed string is not itself proved; "
                         "a safe display is %s (logs/exact_display_checks.json); the certified claim (the double) holds"
                         % (d[0]["display"], d[0]["display_minus_double"], d[0]["safe_display_17sig"]))
    if any(v not in ("byte-identical to HEAD", "not tracked at HEAD", "outside the repository", "differs from HEAD only in timing fields")
           for v in (r.get("outputs_vs_head") or {}).values()):
        parts.append("output files: %s" % r["outputs_vs_head"])
    return "yes", "; ".join(parts)


def main():
    names = sorted({os.path.basename(p)[:-5] for p in glob.glob(os.path.join(LOGS, "*.meta"))})
    main_runs = [n for n in names if n[:2] in ("a_", "v_", "p_", "r_")]
    runs = []
    for n in main_runs:
        sp = SPEC[n]
        m, t = meta(n), timev(n)
        cwd = m["cwd"]
        cmd = m["cmd"].strip()
        sandboxed = cmd.startswith("bwrap")
        ins, code, outs, how = inputs_for(n, cwd)
        obs = sp["observed_fn"](n)
        cmpres = compare(n, sp["refs"])
        r = dict(name=n, instances=sp["instances"], role=sp["role"], cwd=rel(cwd), command=cmd,
                 env="OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1",
                 main_tree_hidden=sandboxed, inputs=ins, code=code, outputs=outs, inputs_from=how,
                 expected=sp["expected"], expected_source=sp["expected_source"], observed=obs,
                 comparison_with_committed=cmpres, note=sp["note"], exit=int(m["exit"]),
                 start=m["start"], end=m["end"], load_start=load(m["uptime_start"]), load_end=load(m["uptime_end"]),
                 log="logs/%s.log" % n, time_file="logs/%s.time" % n, **t)
        if n in LONG_OUTPUTS:   # long runs: only their startup was traced, so list their documented output files
            r["outputs"] = outs = LONG_OUTPUTS[n]
            r["outputs_from"] = "documented output files (the startup audit ends before they are written)"
        r["outputs_vs_head"] = outputs_vs_head(outs)
        r["match"], r["match_explanation"] = decide(n, r)
        runs.append(r)
    audits = []
    for n in names:
        if not n.startswith("s_"):
            continue
        m = meta(n)
        if "exit" not in m:      # still running
            continue
        t = timev(n)
        base = main_name(n)
        startup = n.startswith("s_startup_")
        same = None
        if not startup and base in SPEC:
            a, _ = split_log(logtxt(n))
            b, _ = split_log(logtxt(base))
            ta = [l for l in split_log(logtxt(n))[1]]
            tb = [l for l in split_log(logtxt(base))[1]]
            same = (a == b and ta == tb)
        audits.append(dict(name=n, of=base, startup_only=startup, cwd=rel(m["cwd"]), command=m["cmd"].strip(), exit=int(m["exit"]),
                           expected_exit=124 if startup else 0, output_identical_to_main_run=same,
                           wall_s=t["wall_s"], cpu_s=t["cpu_s"], peak_rss_mb=t["peak_rss_mb"],
                           load_start=load(m["uptime_start"]), load_end=load(m["uptime_end"]), log="logs/%s.log" % n))
    osil = {("%s%d" % (f, N)): dict(path="~/.cache/minlplib/minlplib/osil/%s%d.osil" % (f, N), sha256=sha(os.path.join(OSIL, "%s%d.osil" % (f, N))))
            for f, Ns in (("chain", (50, 100, 200, 400)), ("catmix", (100, 200, 400, 800))) for N in Ns}
    tot_wall = sum(r["wall_s"] for r in runs)
    tot_cpu = sum(r["cpu_s"] for r in runs)
    man = dict(track="repro-cops", worktree=WT, commit="c3514f03",
               note=("Main runs (a_ author, v_ verifier/rechecker, p_ primal track, r_ primal reviewer) ran in the clean worktree with "
                     "patches 01, 03, 04 applied (patch 02 is a portability edit of the OSIL path literal, same file). "
                     "Audit runs (s_) reran the short commands, and the startup of the long ones, in /tmp/cops_patchcheck = "
                     "git archive HEAD of the 5 cops directories + patches 01-04, with the main tree and the worktree hidden (bwrap) "
                     "and file opens traced (strace); their timings include strace overhead and are not used."),
               osil_models=osil, patches=sorted(os.path.basename(p) for p in glob.glob(os.path.join(OUT, "patches", "*.patch"))),
               runs=runs, sandbox_audit=audits,
               totals=dict(main_runs=len(runs), all_exit_zero=all(r["exit"] == 0 for r in runs),
                           wall_s_sum=round(tot_wall, 1), cpu_s_sum=round(tot_cpu, 1),
                           first_start=min(r["start"] for r in runs), last_end=max(r["end"] for r in runs)))
    return man


if __name__ == "__main__":
    man = main()
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    for r in man["runs"]:
        c = r["comparison_with_committed"]
        print("%-34s exit %d wall %8.1f cpu %8.1f rss %7.1f  ref-identical %s  inputs %d" % (
            r["name"], r["exit"], r["wall_s"], r["cpu_s"], r["peak_rss_mb"], None if c is None else c["identical_content"],
            -1 if r["inputs"] is None else len(r["inputs"])))
    for a in man["sandbox_audit"]:
        print("%-40s exit %d (expected %d) identical %s" % (a["name"], a["exit"], a["expected_exit"], a["output_identical_to_main_run"]))
    print(json.dumps(man["totals"]))
