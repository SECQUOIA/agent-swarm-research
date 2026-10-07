"""Build manifest.json for the clean reproduction of the "small" family.

For every step run by tools/run_step.sh (logs/<id>.meta, .out, .time) this collects: cwd,
command, exit code, wall time, CPU time (user + system), peak RSS, load at start and end, the
sha256 of the inputs (current content, and the committed content when the file is tracked and
was rewritten), the expected values with their source, the observed values, and the comparison
of each output with the committed log (raw, and after removing timing fields).

    python3 build_manifest.py            (run from anywhere; writes ../manifest.json)
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import glob
import hashlib
import io
import json
import os
import pickle
import re
import subprocess
from fractions import Fraction

import numpy as np

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LOGS = os.path.join(OUT, "logs")
WT = (_PUBLIC_REPO + '-clean')
R29 = WT + "/research-20260929"
S = "open-instances-wave2/small"
V = "reviews/wave2-small-verification"
PR = "reviews/pindyck-review-checks"
ER = "open-instances-wave3/eg/retry"
RV = "reviews/eg-retry-review-checks"
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
SUMMARY = "research-20260929/open-instances-summary.md"
NOTE_SMALL = "research-20260929/open-instances-wave2/small/report.md"
NOTE_PIND = "research-20260929/open-instances-wave2/small/pindyck-extension.md"
REV_SMALL = "research-20260929/reviews/wave2-small-verification/verification-report.md"
REV_PIND = "research-20260929/reviews/pindyck-review.md"
NOTE_EG = "research-20260929/open-instances-wave3/eg/retry.md"
REV_EG = "research-20260929/reviews/eg-retry-review.md"


def osil(name):
    return os.path.join(OSIL, name + ".osil")


# ----------------------------------------------------------------------------------------------
# step specifications
#   inputs: paths relative to research-20260929 (or absolute)
#   expect: (quantity, expected string, source, how)  how = ("re", regex on .out)
#           or ("json", file, [keys]) or ("re_file", file, regex); compare: "exact" | "lower_display"
#           | "upper_display"  (display: the expected string is an outward-rounded display of a
#           bound; it must lie on the safe side of the observed value)
#   refs: (observed, reference) pairs: observed = "OUT" (the step's stdout/stderr) or a file
#           path; reference = a committed file (compared with git HEAD); kind = text|json|pickle|npz
# ----------------------------------------------------------------------------------------------
def E(q, exp, src, how, cmp="exact"):
    return dict(quantity=q, expected=exp, source=src, how=how, compare=cmp)


STEPS = [
    dict(id="A01_small_ev_points", inst=["hvycrash", "ex6_2_7", "ex6_2_5", "etamac", "pricing050", "pindyck"],
         role="primal check of the MINLPLib points (50 digits)",
         inputs=[f"{S}/ev.py", "reviews/open-instances-verification/osilx.py"] + [osil(n) for n in
                 ["hvycrash", "ex6_2_7", "ex6_2_5", "etamac", "pricing050", "pindyck"]] +
                [f"{S}/sol/{t}.sol" for t in ["hvycrash.p1", "hvycrash.p2", "hvycrash.p3", "ex6_2_7.p1", "ex6_2_5.p1",
                                              "etamac.p1", "pricing050.p1", "pindyck.p1"]],
         expect=[E("hvycrash.p3 objective", "-0.218499999999997", NOTE_SMALL + " s3", ("re", r"hvycrash\.p3: obj (\S+)")),
                 E("etamac.p1 objective", "-15.294675643462758375", NOTE_SMALL + " s5 (-15.2946756434628)", ("re", r"etamac\.p1: obj (\S+)")),
                 E("pricing050.p1 objective", "-1813.829078449835321", NOTE_SMALL + " s6", ("re", r"pricing050\.p1: obj (\S+)"))],
         refs=[("OUT", f"{S}/logs/ev_points_small.log", "text")]),
    dict(id="A02_hvycrash_cert", inst=["hvycrash"], role="certificate (author): exact identity and feasible point",
         inputs=[f"{S}/hvycrash.py", f"{S}/ev.py", osil("hvycrash")] + [f"{S}/sol/hvycrash.p{k}.sol" for k in (1, 2, 3)],
         expect=[E("objective on the feasible set (exact)", "-437/2000 = -0.2185", SUMMARY, ("re", r"= (-437/2000 = -0\.2185) exactly")),
                 E("constructed point objective", "-0.2185", SUMMARY, ("re", r"constructed point \(60 digits\): obj (\S+)")),
                 E("constructed point max row violation", "3.89e-62", NOTE_SMALL + " s3", ("re", r"max row viol (\S+) max bound"))],
         refs=[("OUT", f"{S}/logs/hvycrash.log", "text"), (f"{S}/logs/hvycrash.log", f"{S}/logs/hvycrash.log", "text"),
               (f"{S}/logs/hvycrash_point.txt", f"{S}/logs/hvycrash_point.txt", "text")]),
    dict(id="A03_gibbs_model", inst=["ex6_2_7", "ex6_2_5"], role="structure check (author)",
         inputs=[f"{S}/gibbs_model.py", osil("ex6_2_7"), osil("ex6_2_5")],
         expect=[E("ex6_2_7 R_p", "1/20000000000000", NOTE_SMALL + " s4.1 (5e-14)", ("re", r"ex6_2_7 .*R_p = \[\['0', '0', '([^']+)'\]")),
                 E("ex6_2_5 R_p", "0", NOTE_SMALL + " s4.1", ("re", r"ex6_2_5 .*R_p = \[\['([^']+)', '0', '0'\]"))],
         refs=[]),
    dict(id="A04_ex6_2_7_cert", inst=["ex6_2_7"], role="certificate (author)",
         inputs=[f"{S}/gibbs.py", f"{S}/gibbs_model.py", f"{S}/ia.py", f"{S}/ev.py", osil("ex6_2_7")],
         expect=[E("dual bound", "-0.16084761549352554", NOTE_SMALL + " s1, s4.3", ("re", r"RIGOROUS DUAL BOUND: (\S+)")),
                 E("primal value", "-0.16084761546360086", NOTE_SMALL + " s4.3", ("re", r"primal: (\S+);")),
                 E("primal max row violation", "6.68e-52", NOTE_SMALL + " (6.7e-52)", ("re", r"primal point: obj \S+, max row viol (\S+),"))],
         refs=[("OUT", f"{S}/logs/ex6_2_7_run.out", "text"), (f"{S}/logs/ex6_2_7_gibbs.log", f"{S}/logs/ex6_2_7_gibbs.log", "text"),
               (f"{S}/logs/ex6_2_7_gibbs.json", f"{S}/logs/ex6_2_7_gibbs.json", "json"),
               (f"{S}/logs/ex6_2_7_primal.txt", f"{S}/logs/ex6_2_7_primal.txt", "text")]),
    dict(id="A05_ex6_2_5_cert", inst=["ex6_2_5"], role="certificate (author)",
         inputs=[f"{S}/gibbs.py", f"{S}/gibbs_model.py", f"{S}/ia.py", f"{S}/ev.py", osil("ex6_2_5")],
         expect=[E("dual bound", "-70.752077836333563", NOTE_SMALL + " s1, s4.3", ("re", r"RIGOROUS DUAL BOUND: (\S+)")),
                 E("primal value", "-70.752077833447706", NOTE_SMALL + " s4.3", ("re", r"primal: (\S+);")),
                 E("primal max row violation", "8.6e-50", NOTE_SMALL, ("re", r"primal point: obj \S+, max row viol (\S+),"))],
         refs=[("OUT", f"{S}/logs/ex6_2_5_run.out", "text"), (f"{S}/logs/ex6_2_5_gibbs.log", f"{S}/logs/ex6_2_5_gibbs.log", "text"),
               (f"{S}/logs/ex6_2_5_gibbs.json", f"{S}/logs/ex6_2_5_gibbs.json", "json"),
               (f"{S}/logs/ex6_2_5_primal.txt", f"{S}/logs/ex6_2_5_primal.txt", "text")]),
    dict(id="A06_etamac_cert", inst=["etamac"], role="certificate (author)",
         inputs=[f"{S}/etamac.py", f"{S}/ia.py", f"{S}/ev.py", osil("etamac"), f"{S}/sol/etamac.p1.sol"],
         expect=[E("dual bound", "-15.294675643368096", NOTE_SMALL + " s1, s5.3", ("re", r"RIGOROUS DUAL BOUND \(etamac\): (\S+)")),
                 E("primal value (row violation 6e-14)", "-15.2946756433680896", NOTE_SMALL + " s5.3", ("re", r"primal \(KKT point, 17 digits\): obj (\S+),"))],
         refs=[("OUT", f"{S}/logs/etamac_run.out", "text"), (f"{S}/logs/etamac.log", f"{S}/logs/etamac.log", "text"),
               (f"{S}/logs/etamac_primal.txt", f"{S}/logs/etamac_primal.txt", "text")]),
    dict(id="A07_pricing050_model", inst=["pricing050"], role="structure check (author)",
         inputs=[f"{S}/pricing050_model.py", osil("pricing050")], expect=[], refs=[]),
    dict(id="A08_pricing050_cert", inst=["pricing050"], role="certificate (author; maximization, upper bound)",
         inputs=[f"{S}/pricing050.py", f"{S}/pricing050_model.py", f"{S}/ev.py", osil("pricing050"), f"{S}/sol/pricing050.p1.sol"],
         expect=[E("upper bound (max form)", "-1813.8290784519704", NOTE_SMALL + " s1, s6", ("re", r"RIGOROUS UPPER BOUND \(max form, pricing050\): (\S+)")),
                 E("primal value (exactly feasible)", "-1813.8290784519731", NOTE_SMALL + " s6", ("re", r"primal \(max form\) (\S+);"))],
         refs=[("OUT", f"{S}/logs/pricing050.log", "text"), (f"{S}/logs/pricing050.log", f"{S}/logs/pricing050.log", "text"),
               (f"{S}/logs/pricing050_primal.txt", f"{S}/logs/pricing050_primal.txt", "text")]),
    dict(id="A09_pindyck_primal", inst=["pindyck"], role="primal point p* (author) and local concavity (superseded part)",
         inputs=[f"{S}/pindyck.py", f"{S}/ia.py", f"{S}/ev.py", osil("pindyck"), f"{S}/sol/pindyck.p1.sol"],
         expect=[E("J(p*) (50 digits)", "1170.4862854360885621", NOTE_SMALL + " s7", ("re", r"J\(p\*\) \(50 digits\) = (\S+)")),
                 E("primal max row violation", "8.3e-28", NOTE_SMALL + " s7", ("re", r"primal point: obj \S+, max row viol (\S+),"))],
         refs=[("OUT", f"{S}/logs/pindyck.log", "text"), (f"{S}/logs/pindyck.log", f"{S}/logs/pindyck.log", "text"),
               (f"{S}/logs/pindyck_primal.txt", f"{S}/logs/pindyck_primal.txt", "text")]),
    dict(id="A10_pindyck_cert", inst=["pindyck"], role="certificate (author)",
         inputs=[f"{S}/pindyck_global.py", f"{S}/tm1.py", f"{S}/ia.py", f"{S}/ev.py", osil("pindyck"), f"{S}/logs/pindyck_primal.txt"],
         expect=[E("dual bound (min form)", "-1170.4862854360886163932", SUMMARY + "; " + NOTE_PIND,
                   ("re", r"every feasible point has objective >= (\S+)")),
                 E("objective at p* (upper end)", "-1170.486285436088562087577", NOTE_PIND, ("re", r"objective -J\(p\*\) <= (\S+);")),
                 E("leaf boxes", "9", NOTE_PIND, ("re", r"on all of Theta \((\d+) boxes"))],
         refs=[("OUT", f"{S}/logs/pindyck_global.log", "text"), (f"{S}/logs/pindyck_global.log", f"{S}/logs/pindyck_global.log", "text")]),
    dict(id="A11_v_hvycrash", inst=["hvycrash"], role="independent verification",
         inputs=[f"{V}/v_hvycrash.py", f"{V}/common.py", osil("hvycrash")] + [f"{V}/sol/hvycrash.p{k}.sol" for k in (1, 2, 3)],
         expect=[E("own feasible point objective", "-0.2185", REV_SMALL + " s2", ("re", r"\{'objective': '(\S+)', 'max_row_violation'")),
                 E("own point max row violation", "3.121e-60", REV_SMALL + " (3.1e-60)", ("re", r"'max_row_violation': '(\S+)'\}"))],
         refs=[("OUT", f"{V}/logs/hvycrash.log", "text"), (f"{V}/logs/hvycrash.json", f"{V}/logs/hvycrash.json", "json"),
               (f"{V}/logs/hvycrash_own_point.txt", f"{V}/logs/hvycrash_own_point.txt", "text")]),
    dict(id="A12_v_gibbs_sym", inst=["ex6_2_7", "ex6_2_5"], role="independent verification (structure, scaling identity)",
         inputs=[f"{V}/gibbs_sym.py", f"{V}/common.py", osil("ex6_2_7"), osil("ex6_2_5")], expect=[],
         refs=[("OUT", f"{V}/logs/gibbs_sym.log", "text")]),
    dict(id="A13_v_gibbs_kkt", inst=["ex6_2_7", "ex6_2_5"], role="independent verification (multipliers)",
         inputs=[f"{V}/gibbs_kkt.py", f"{V}/gibbs_sym.py", osil("ex6_2_7"), osil("ex6_2_5")], expect=[],
         refs=[("OUT", f"{V}/logs/gibbs_kkt.log", "text"), (f"{V}/logs/ex6_2_7_kkt.json", f"{V}/logs/ex6_2_7_kkt.json", "json"),
               (f"{V}/logs/ex6_2_5_kkt.json", f"{V}/logs/ex6_2_5_kkt.json", "json")]),
    dict(id="A14_v_gibbs_bb_ex6_2_7", inst=["ex6_2_7"], role="independent verification (tangent-plane B&B, tau 6e-15)",
         inputs=[f"{V}/gibbs_bb.py", f"{V}/ivgen.py", f"{V}/gibbs_sym.py", f"{V}/logs/ex6_2_7_kkt.json", osil("ex6_2_7")],
         expect=[E("B&B ok", "true", REV_SMALL + " s3", ("json", f"{V}/logs/ex6_2_7_bb_type0_tau6e-15.json", ["ok"])),
                 E("boxes", "42111", REV_SMALL + " s3", ("json", f"{V}/logs/ex6_2_7_bb_type0_tau6e-15.json", ["nbox"]))],
         refs=[(f"{V}/logs/ex6_2_7_bb_type0_tau6e-15.json", f"{V}/logs/ex6_2_7_bb_type0_tau6e-15.json", "json")]),
    dict(id="A15_v_gibbs_bb_ex6_2_5", inst=["ex6_2_5"], role="independent verification (tangent-plane B&B, tau 1e-17)",
         inputs=[f"{V}/gibbs_bb.py", f"{V}/ivgen.py", f"{V}/gibbs_sym.py", f"{V}/logs/ex6_2_5_kkt.json", osil("ex6_2_5")],
         expect=[E("B&B ok", "true", REV_SMALL + " s3", ("json", f"{V}/logs/ex6_2_5_bb_type0_tau1e-17.json", ["ok"])),
                 E("boxes", "131111", REV_SMALL + " s3", ("json", f"{V}/logs/ex6_2_5_bb_type0_tau1e-17.json", ["nbox"]))],
         refs=[(f"{V}/logs/ex6_2_5_bb_type0_tau1e-17.json", f"{V}/logs/ex6_2_5_bb_type0_tau1e-17.json", "json")]),
    dict(id="A16_v_gibbs_bound_ex6_2_7", inst=["ex6_2_7"], role="independent verification (bound assembly, own primal)",
         inputs=[f"{V}/gibbs_bound.py", f"{V}/common.py", f"{V}/logs/ex6_2_7_bb_type0_tau6e-15.json", f"{V}/logs/ex6_2_7_kkt.json",
                 osil("ex6_2_7"), f"{V}/sol/ex6_2_7.p1.sol"],
         expect=[E("dual bound (20 digits, as printed)", "-0.16084761546364904344", REV_SMALL + " s3 (-0.16084761546364904)",
                   ("json", f"{V}/logs/ex6_2_7_bound.json", ["dual_bound"])),
                 E("summary display of the dual bound", "-0.16084761546364905", SUMMARY,
                   ("json", f"{V}/logs/ex6_2_7_bound.json", ["dual_bound"]), "lower_display"),
                 E("own exact primal objective", "-0.16084761546360086152", REV_SMALL + "; " + SUMMARY + " (-0.16084761546360086)",
                   ("json", f"{V}/logs/ex6_2_7_bound.json", ["own_primal_objective_enclosure", 1])),
                 E("gap", "4.8182e-14", SUMMARY + " (4.8e-14)", ("json", f"{V}/logs/ex6_2_7_bound.json", ["gap_upper_primal_minus_bound"]))],
         refs=[("OUT", f"{V}/logs/ex6_2_7_bound.log", "text"), (f"{V}/logs/ex6_2_7_bound.json", f"{V}/logs/ex6_2_7_bound.json", "json")]),
    dict(id="A17_v_gibbs_bound_ex6_2_5", inst=["ex6_2_5"], role="independent verification (bound assembly, own primal)",
         inputs=[f"{V}/gibbs_bound.py", f"{V}/common.py", f"{V}/logs/ex6_2_5_bb_type0_tau1e-17.json", f"{V}/logs/ex6_2_5_kkt.json",
                 osil("ex6_2_5"), f"{V}/sol/ex6_2_5.p1.sol"],
         expect=[E("dual bound (20 digits, as printed)", "-70.75207783344770758", REV_SMALL + " s3",
                   ("json", f"{V}/logs/ex6_2_5_bound.json", ["dual_bound"])),
                 E("summary display of the dual bound", "-70.75207783344770759", SUMMARY,
                   ("json", f"{V}/logs/ex6_2_5_bound.json", ["dual_bound"]), "lower_display"),
                 E("own exact primal objective", "-70.75207783344770558", REV_SMALL + "; " + SUMMARY + " (-70.752077833447706)",
                   ("json", f"{V}/logs/ex6_2_5_bound.json", ["own_primal_objective_enclosure", 1])),
                 E("gap", "2.0e-15", SUMMARY, ("json", f"{V}/logs/ex6_2_5_bound.json", ["gap_upper_primal_minus_bound"]))],
         refs=[("OUT", f"{V}/logs/ex6_2_5_bound.log", "text"), (f"{V}/logs/ex6_2_5_bound.json", f"{V}/logs/ex6_2_5_bound.json", "json")]),
    dict(id="A18_v_gibbs_sanity", inst=["ex6_2_7", "ex6_2_5"], role="supporting check (not part of the proof)",
         inputs=[f"{V}/gibbs_sanity.py", f"{V}/logs/ex6_2_7_kkt.json", f"{V}/logs/ex6_2_5_kkt.json"], expect=[],
         refs=[("OUT", [f"{V}/logs/ex6_2_7_sanity.log", f"{V}/logs/ex6_2_5_sanity.log"], "text")]),
    dict(id="A19_v_etamac", inst=["etamac"], role="independent verification (bound and exactly feasible primal)",
         inputs=[f"{V}/v_etamac.py", f"{V}/common.py", f"{V}/ivgen.py", osil("etamac"), f"{V}/sol/etamac.p1.sol"],
         expect=[E("dual bound (20 digits, as printed)", "-15.294675643368092168", REV_SMALL + " s4 (-15.294675643368092)",
                   ("json", f"{V}/logs/etamac.json", ["bound", "dual_bound"])),
                 E("summary display of the dual bound", "-15.294675643368093", SUMMARY,
                   ("json", f"{V}/logs/etamac.json", ["bound", "dual_bound"]), "lower_display"),
                 E("gap to own exactly feasible point", "2.577e-15", SUMMARY + " (2.6e-15)", ("json", f"{V}/logs/etamac.json", ["gap"]))],
         refs=[("OUT", f"{V}/logs/etamac.log", "text"), (f"{V}/logs/etamac.json", f"{V}/logs/etamac.json", "json")]),
    dict(id="A20_v_pricing050", inst=["pricing050"], role="independent verification (upper bound and exact primal)",
         inputs=[f"{V}/v_pricing050.py", f"{V}/common.py", osil("pricing050"), f"{V}/sol/pricing050.p1.sol"],
         expect=[E("upper bound (20 digits, as printed)", "-1813.8290784519730577", REV_SMALL + " s5; " + SUMMARY,
                   ("json", f"{V}/logs/pricing050.json", ["certificate", "upper_bound"])),
                 E("own exact primal objective (20 digits)", "-1813.8290784519730578", REV_SMALL + " s5",
                   ("json", f"{V}/logs/pricing050.json", ["own_primal", "objective_20"])),
                 E("gap", "1.041e-17", SUMMARY + " (1.0e-17)", ("json", f"{V}/logs/pricing050.json", ["gap"]))],
         refs=[("OUT", f"{V}/logs/pricing050.log", "text"), (f"{V}/logs/pricing050.json", f"{V}/logs/pricing050.json", "json")]),
    dict(id="A21_pr_primal_check", inst=["pindyck"], role="independent verification (primal, J and grad J enclosure)",
         inputs=[f"{PR}/primal_check.py", f"{PR}/own_model.py", f"{PR}/own_osil.py", osil("pindyck"), f"{S}/logs/pindyck_primal.txt"],
         expect=[],
         refs=[(f"{PR}/logs/primal_check.txt", f"{PR}/logs/primal_check.txt", "text"),
               (f"{PR}/logs/primal_enclosure.txt", f"{PR}/logs/primal_enclosure.txt", "text")]),
    dict(id="A22_pr_author_data", inst=["pindyck"], role="independent verification (extract the author's certificate data)",
         inputs=[f"{PR}/author_data.py", f"{S}/pindyck_global.py", f"{S}/tm1.py", f"{S}/ia.py", osil("pindyck")],
         expect=[E("author leaves", "9", REV_PIND, ("re", r"leaves: (\d+) splits"))],
         refs=[(f"{PR}/author_data.pkl", f"{PR}/author_data.pkl", "pickle")]),
    dict(id="A23_pr_own_ranges", inst=["pindyck"], role="independent verification (own G' and Theta')",
         inputs=[f"{PR}/own_ranges.py", f"{PR}/own_model.py", f"{PR}/own_osil.py", osil("pindyck"), f"{S}/logs/pindyck_primal.txt"],
         expect=[], refs=[(f"{PR}/logs/own_ranges.log", f"{PR}/logs/own_ranges.log", "text"), (f"{PR}/ranges.pkl", f"{PR}/ranges.pkl", "pickle")]),
    dict(id="A24_pr_own_ranges_authorG", inst=["pindyck"], role="independent verification (ranges over the author's G)",
         inputs=[f"{PR}/own_ranges.py", f"{PR}/author_data.pkl", osil("pindyck"), f"{S}/logs/pindyck_primal.txt"],
         expect=[], refs=[(f"{PR}/logs/own_ranges_authorG.log", f"{PR}/logs/own_ranges_authorG.log", "text"),
                          (f"{PR}/ranges_authorG.pkl", f"{PR}/ranges_authorG.pkl", "pickle")]),
    dict(id="A25_pr_own_concavity", inst=["pindyck"], role="independent verification (own concavity B&B)",
         inputs=[f"{PR}/own_concavity.py", f"{PR}/own_psi.py", f"{PR}/ranges.pkl", f"{PR}/ranges_authorG.pkl", f"{PR}/author_data.pkl"],
         expect=[], refs=[(f"{PR}/logs/own_concavity.log", f"{PR}/logs/own_concavity.log", "text"), ("OUT", f"{PR}/logs/own_concavity.out", "text"),
                          (f"{PR}/leaves.pkl", f"{PR}/leaves.pkl", "pickle")]),
    dict(id="A26_pr_verify_own_leaves", inst=["pindyck"], role="independent verification (own leaves, coverage, exact test)",
         inputs=[f"{PR}/verify_own_leaves.py", f"{PR}/own_psi.py", f"{PR}/leaves.pkl"],
         expect=[E("all own leaves pass", "True", REV_PIND, ("re", r"ALL LEAVES PASS: (\w+)"))],
         refs=[(f"{PR}/logs/verify_own_leaves.log", f"{PR}/logs/verify_own_leaves.log", "text")]),
    dict(id="A27_pr_author_leaves_check", inst=["pindyck"], role="independent verification (author's 9 leaves with own code)",
         inputs=[f"{PR}/author_leaves_check.py", f"{PR}/own_psi.py", f"{PR}/author_data.pkl"], expect=[],
         refs=[(f"{PR}/logs/author_leaves_check.log", f"{PR}/logs/author_leaves_check.log", "text")]),
    dict(id="A28_pr_final_bound", inst=["pindyck"], role="independent verification (final bound, exact rationals)",
         inputs=[f"{PR}/final_bound.py", f"{PR}/ranges.pkl", f"{PR}/author_data.pkl", f"{PR}/logs/primal_enclosure.txt",
                 f"{S}/logs/pindyck_primal.txt"],
         expect=[E("own bound (G')", "-1170.4862854360886163931058729", REV_PIND + " s6", ("re", r"\[own G'\] every feasible point has objective >= -UB = (\S+)")),
                 E("claimed bound <= own bound", "True", REV_PIND, ("re", r"<= own bound -UB: (\w+)"))],
         refs=[(f"{PR}/logs/final_bound.log", f"{PR}/logs/final_bound.log", "text")]),
    dict(id="A29_pr_hess_check", inst=["pindyck"], role="supporting check (not part of the proof)",
         inputs=[f"{PR}/hess_check.py", f"{PR}/ranges.pkl", f"{PR}/author_data.pkl", f"{S}/logs/pindyck_primal.txt"], expect=[],
         refs=[(f"{PR}/logs/hess_check.log", f"{PR}/logs/hess_check.log", "text")]),
    dict(id="A30_pr_af_soundness", inst=["pindyck"], role="supporting check (not part of the proof)",
         inputs=[f"{PR}/af_soundness.py", f"{PR}/ranges.pkl", f"{PR}/author_data.pkl", f"{PR}/ranges_authorG.pkl"], expect=[],
         refs=[(f"{PR}/logs/af_soundness.log", f"{PR}/logs/af_soundness.log", "text")]),
]

EGIN = [f"{ER}/egbb.py", f"{ER}/egfast.py", f"{ER}/egtm.py", f"{ER}/egdata.py", f"{ER}/explore.py",
        "open-instances-wave3/eg/eg_model.py", "open-instances-wave3/kan/kan_iv.py", f"{S}/ia.py", f"{S}/ev.py",
        "reviews/open-instances-verification/osilx.py"]
for sid, name, log, val, boxes, extra in [
        ("A31_eg_int_cert", "eg_int_s", "int9_final.log", "6.4531031529331155", "56189", []),
        ("A32_eg_disc_cert_p0", "eg_disc_s", "disc9_p0.log", "5.7605396106949955", "62779", []),
        ("A33_eg_disc_cert_p1", "eg_disc_s", "disc9_p1.log", "5.760539610694994", "55973", []),
        ("A34_eg_disc2_cert_p1", "eg_disc2_s", "disc2_9_p1.log", "5.642100574331458", "134607", [])]:
    STEPS.append(dict(id=sid, inst=[name], role="certificate (author; run " + ("C" if "int" in sid else "E" if "disc_" in sid else "G part 1") + ")",
                      inputs=EGIN + [osil(name), f"open-instances-wave3/sol/{name}.p1.sol"],
                      expect=[E("certified lower bound", val, NOTE_EG + " s5", ("re", r"certified lower bound np\.float64\(([^)]+)\)")),
                              E("processed boxes", boxes, NOTE_EG + " s5", ("re", r"B&B: done=True processed (\d+) "))],
                      refs=[("OUT", f"{ER}/logs/{log}", "eglines"), ("OUT", f"{ER}/logs/{log}", "text")]))
for sid, name, npz, val in [("A35_eg_int_primal", "eg_int_s", "int9_final.npz", "6.4531031593842274088"),
                            ("A36_eg_disc_primal", "eg_disc_s", "disc9_p1.npz", "5.7605396164535106058"),
                            ("A37_eg_disc2_primal", "eg_disc2_s", "disc2_9_p1.npz", "5.6421005799711067563")]:
    STEPS.append(dict(id=sid, inst=[name], role="primal check (author; writes retry/sol/<name>.retry.sol, 50-digit OSIL check)",
                      inputs=[f"{ER}/verify_primal.py", f"{S}/ev.py", f"{ER}/logs/{npz}", osil(name)],
                      expect=[E("objective of the exactly feasible point", val[:18], SUMMARY + " / " + NOTE_EG,
                                ("re", r"objective (\d\.\d{16})")),
                              E("max row violation", "0.0", NOTE_EG, ("re", r"max row violation (\S+) "))],
                      refs=[(f"{ER}/sol/{name}.retry.sol", f"{ER}/sol/{name}.retry.sol", "text")]))
STEPS.append(dict(id="A38_rv_check_primal", inst=["eg_int_s", "eg_disc_s", "eg_disc2_s"], role="independent verification (primal points at 60 digits from the GAMS text)",
                  inputs=[f"{RV}/check_primal.py", f"{RV}/gms_model.py"] + [f"{RV}/data/{n}.gms" for n in ("eg_int_s", "eg_disc_s", "eg_disc2_s")] +
                         [f"{ER}/sol/{n}.retry.sol" for n in ("eg_int_s", "eg_disc_s", "eg_disc2_s")] +
                         [f"open-instances-wave3/sol/{n}.p1.sol" for n in ("eg_int_s", "eg_disc_s", "eg_disc2_s")],
                  expect=[], refs=[("OUT", f"{RV}/logs/check_primal.log", "text")]))
RVIN = [f"{RV}/indep_cert.py", f"{RV}/gms_model.py", f"{RV}/verify_tree.py"]
STEPS.append(dict(id="B01_rv_check_decode", inst=["eg_int_s", "eg_disc_s", "eg_disc2_s"], role="independent verification (decoding vs GAMS text)",
                  inputs=[f"{RV}/check_decode.py", f"{RV}/gms_model.py"] + [f"{RV}/data/{n}.gms" for n in ("eg_int_s", "eg_disc_s", "eg_disc2_s")] +
                         [osil(n) for n in ("eg_int_s", "eg_disc_s", "eg_disc2_s")],
                  expect=[], refs=[("OUT", f"{RV}/logs/check_decode.log", "text")]))
for sid, name, log, val, boxes in [("B02_rv_rec_int", "eg_int_s", "rec_int.log", "6.4531031529331155", "56189"),
                                   ("B04_rv_rec_disc_p0", "eg_disc_s", "rec_disc_p0.log", "5.7605396106949955", "62779"),
                                   ("B06_rv_rec_disc_p1", "eg_disc_s", "rec_disc_p1.log", "5.760539610694994", "55973"),
                                   ("B08_rv_rec_disc2_p1", "eg_disc2_s", "rec_disc2_p1.log", "5.642100574331458", "134607")]:
    alog = {"rec_int.log": "int9_final.log", "rec_disc_p0.log": "disc9_p0.log", "rec_disc_p1.log": "disc9_p1.log",
            "rec_disc2_p1.log": "disc2_9_p1.log"}[log]
    STEPS.append(dict(id=sid, inst=[name], role="independent verification (tree recording: replays the author's B&B with recording)",
                      inputs=[f"{RV}/record_run.py"] + EGIN + [osil(name), f"open-instances-wave3/sol/{name}.p1.sol"],
                      expect=[E("certified lower bound", val, NOTE_EG, ("re", r"certified lower bound np\.float64\(([^)]+)\)")),
                              E("processed boxes", boxes, REV_EG + " s5", ("re", r"B&B: done=True processed (\d+) "))],
                      refs=[("OUT", f"{RV}/logs/{log}", "text"), ("OUT", f"{ER}/logs/{alog}", "eglines")]))
for sid, name, rec, th, n in [("B03_rv_verify_int", "eg_int_s", "rec_int", "6.4531031529331155", "33385"),
                              ("B05_rv_verify_disc_p0", "eg_disc_s", "rec_disc_p0", "5.760539610694994", "46223"),
                              ("B07_rv_verify_disc_p1", "eg_disc_s", "rec_disc_p1", "5.760539610694994", "40573"),
                              ("B09_rv_verify_disc2_p1", "eg_disc2_s", "rec_disc2_p1", "5.642100574331458", "135317")]:
    vlog = rec.replace("rec_", "verify_") + ".log"
    STEPS.append(dict(id=sid, inst=[name], role="independent verification (coverage and independent re-certification of every leaf)",
                      inputs=RVIN + [f"{RV}/logs/{rec}.npz"] + [f"{RV}/data/{name}.gms"],
                      expect=[E("leaves certified", f"{n}/{n}", REV_EG + " s5", ("re", r"certified (\d+/\d+); failures")),
                              E("failures", "0", REV_EG + " s5", ("re", r"; failures (\d+) "))],
                      refs=[("OUT", f"{RV}/logs/{vlog}", "text")]))
STEPS.append(dict(id="D01_display_check", inst=["ex6_2_7", "ex6_2_5", "etamac", "pricing050"],
                  role="added check (this track): summary display strings against the exact interval end points",
                  inputs=[os.path.join(OUT, "tools", "display_check.py"), f"{V}/gibbs_bound.py", f"{V}/v_etamac.py", f"{V}/v_pricing050.py"],
                  expect=[], refs=[]))

# ----------------------------------------------------------------------------------------------
TIMING = [re.compile(r"\b\d+(\.\d+)?\s?s\b"), re.compile(r"\b\d+(\.\d+)?\s?min\b")]


def norm_text(lines):
    out = []
    for ln in lines:
        if re.match(r"^(real|user|sys)\s", ln):
            continue
        for pat in TIMING:
            ln = pat.sub("<T>", ln)
        out.append(ln.rstrip())
    while out and out[-1] == "":
        out.pop()
    return out


def head_bytes(rel):
    p = "research-20260929/" + rel
    r = subprocess.run(["git", "-C", WT, "show", "HEAD:" + p], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def path_of(rel):
    return rel if os.path.isabs(rel) else os.path.join(R29, rel)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def drop_keys(d, keys=("sec", "time")):
    if isinstance(d, dict):
        return {k: drop_keys(v, keys) for k, v in d.items() if k not in keys}
    if isinstance(d, list):
        return [drop_keys(v, keys) for v in d]
    return d


def deep_eq(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(deep_eq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(deep_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        a, b = np.asarray(a), np.asarray(b)
        return a.shape == b.shape and a.dtype == b.dtype and bool(np.array_equal(a, b, equal_nan=a.dtype.kind == "f"))
    try:
        r = a == b
        return bool(r) if not isinstance(r, np.ndarray) else bool(r.all())
    except Exception:
        return repr(a) == repr(b)


def compare(step, obs, ref, kind):
    refs = ref if isinstance(ref, list) else [ref]
    rb = b"".join((head_bytes(r) or b"") for r in refs)
    if obs == "OUT":
        ob = open(os.path.join(LOGS, step + ".out"), "rb").read()
        oname = f"logs/{step}.out"
    else:
        p = path_of(obs)
        if not os.path.exists(p):
            return dict(observed=obs, reference=ref, exists=False)
        ob = open(p, "rb").read()
        oname = obs
    res = dict(observed=oname, reference=ref, kind=kind, identical_bytes=ob == rb,
               sha256_observed=sha(ob), sha256_reference=sha(rb))
    if kind in ("text", "eglines"):
        a = norm_text(rb.decode(errors="replace").splitlines())
        b = norm_text(ob.decode(errors="replace").splitlines())
        if kind == "eglines":     # progress, final and certified-bound lines only (as publication/eg-recheck/compare_logs.py)
            keep = ("  it ", "B&B:", "  certified lower bound", "== ", "part ")
            a = [x for x in a if x.startswith(keep)]
            b = [x for x in b if x.startswith(keep)]
            res["lines_compared"] = len(a)
        res["identical_apart_from_timings"] = a == b
        if a != b:
            diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
            res["lines_reference"], res["lines_observed"] = len(a), len(b)
            res["n_differing_lines"] = len(diffs) + abs(len(a) - len(b))
            res["first_differences"] = [dict(line=i + 1, reference=x[:300], observed=y[:300]) for i, x, y in diffs[:4]]
    elif kind == "json":
        try:
            a, b = json.loads(rb), json.loads(ob)
            res["identical_apart_from_timings"] = drop_keys(a) == drop_keys(b)
            if not res["identical_apart_from_timings"]:
                res["differing_keys"] = sorted(k for k in set(a) | set(b) if drop_keys(a.get(k)) != drop_keys(b.get(k)))[:20]
        except Exception as e:
            res["error"] = repr(e)
    elif kind == "pickle":
        try:
            a, b = pickle.load(io.BytesIO(rb)), pickle.load(io.BytesIO(ob))
            res["identical_content"] = deep_eq(a, b)
        except Exception as e:
            res["error"] = repr(e)
    return res


def get_json(rel, keys):
    d = json.load(open(path_of(rel)))
    for k in keys:
        d = d[k]
    return d


def observe(step, how):
    if how[0] == "re":
        txt = open(os.path.join(LOGS, step + ".out"), errors="replace").read()
        m = re.search(how[1], txt)
        return m.group(1) if m else None
    if how[0] == "json":
        v = get_json(how[1], how[2])
        return json.dumps(v) if isinstance(v, bool) else str(v)
    raise ValueError(how)


def check(e, obs):
    if obs is None:
        return False, "value not found in the output"
    exp = e["expected"]
    if e["compare"] == "exact":
        return obs == exp, "exact string match" if obs == exp else f"differs: expected {exp}, observed {obs}"
    x, d = Fraction(obs), Fraction(exp.replace("−", "-"))
    if e["compare"] == "lower_display":
        ok = d <= x
        return ok, f"display {exp} {'<=' if ok else '>'} printed value {obs} (difference {float(d - x):.2e}); see D01 for the exact end point"
    ok = d >= x
    return ok, f"display {exp} {'>=' if ok else '<'} printed value {obs} (difference {float(d - x):.2e}); see D01"


def parse_meta(step):
    m = {}
    for line in open(os.path.join(LOGS, step + ".meta")):
        k, _, v = line.partition(": ")
        m[k.strip()] = v.strip()
    return m


def parse_time(step):
    t = {}
    p = os.path.join(LOGS, step + ".time")
    if not os.path.exists(p):
        return t
    for line in open(p):
        k, _, v = line.strip().partition(": ")
        t[k] = v
    wall = t.get("Elapsed (wall clock) time (h:mm:ss or m:ss)", "0:0")
    parts = [float(x) for x in wall.split(":")]
    ws = parts[-1] + 60 * parts[-2] + (3600 * parts[-3] if len(parts) > 2 else 0)
    return dict(wall_s=round(ws, 2), cpu_s=round(float(t.get("User time (seconds)", 0)) + float(t.get("System time (seconds)", 0)), 2),
                peak_rss_mb=round(int(t.get("Maximum resident set size (kbytes)", 0)) / 1024, 1),
                exit_status_time=t.get("Exit status"))


def input_info(rel):
    p = path_of(rel)
    d = dict(path=p if os.path.isabs(rel) else "research-20260929/" + rel)
    if os.path.exists(p):
        d["sha256"] = sha(open(p, "rb").read())
    else:
        d["sha256"] = None
        d["missing"] = True
    if not os.path.isabs(rel):
        hb = head_bytes(rel)
        if hb is None:
            d["tracked"] = False
        else:
            d["tracked"] = True
            if d["sha256"] != sha(hb):
                d["sha256_committed"] = sha(hb)
                d["note"] = "differs from the committed file (patched for the clean checkout, or regenerated by an earlier step)"
    return d


def main():
    steps_out = []
    for st in STEPS:
        sid = st["id"]
        if not os.path.exists(os.path.join(LOGS, sid + ".meta")):
            steps_out.append(dict(id=sid, status="not run"))
            continue
        meta, tm = parse_meta(sid), parse_time(sid)
        exps = []
        for e in st["expect"]:
            try:
                obs = observe(sid, e["how"])
            except Exception as ex:
                obs = None
                e = dict(e, error=repr(ex))
            ok, why = check(e, obs)
            exps.append(dict(quantity=e["quantity"], expected=e["expected"], source=e["source"], observed=obs, match=ok, explanation=why))
        cmps = [compare(sid, o, r, k) for o, r, k in st["refs"]]
        steps_out.append(dict(
            id=sid, instances=st["inst"], role=st["role"], cwd=meta.get("cwd"), command=meta.get("cmd"),
            guard_mode=meta.get("guard_mode"), exit_code=int(meta.get("rc", "-1").split()[0]),
            start=meta.get("start"), end=meta.get("end"),
            load_start=meta.get("loadavg_start"), load_end=meta.get("loadavg_end"),
            uptime_start=meta.get("uptime_start"), uptime_end=meta.get("uptime_end"),
            **tm, guard_main_tree_accesses=os.path.exists(os.path.join(LOGS, sid + ".guard")),
            inputs=[input_info(i) for i in st["inputs"]], expected_values=exps, log_comparisons=cmps,
            stdout_log=f"logs/{sid}.out"))
    diag = []
    for p in sorted(glob.glob(os.path.join(LOGS, "pre_*.meta")) + glob.glob(os.path.join(LOGS, "post_*.meta"))):
        sid = os.path.basename(p)[:-5]
        meta = parse_meta(sid)
        g = os.path.join(LOGS, sid + ".guard")
        diag.append(dict(id=sid, cwd=meta.get("cwd"), command=meta.get("cmd"), exit_code=int(meta.get("rc", "-1").split()[0]),
                         guard_log=open(g).read().strip().splitlines() if os.path.exists(g) else [],
                         last_output_line=(open(os.path.join(LOGS, sid + ".out")).read().strip().splitlines() or [""])[-1]))
    man = dict(
        track="repro-small", worktree=WT,
        commit=subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        environment=dict(python=subprocess.run(["python3", "--version"], capture_output=True, text=True).stdout.strip(),
                         note="mpmath 1.3.0, numpy 2.5.1, scipy 1.18.0, sympy 1.14.0, highspy 1.15.1; OMP/OPENBLAS/MKL threads 1; "
                              "PYTHONDONTWRITEBYTECODE=1; clean-checkout guard (guard/usercustomize.py) in strict mode"),
        osil_cache=OSIL, steps=steps_out, diagnosis_runs=diag)
    tot = [s for s in steps_out if "wall_s" in s]
    man["totals"] = dict(steps_run=len(tot), wall_s_sum=round(sum(s["wall_s"] for s in tot), 1),
                         cpu_s_sum=round(sum(s["cpu_s"] for s in tot), 1),
                         all_exit_zero=all(s["exit_code"] == 0 for s in tot),
                         all_expected_match=all(e["match"] for s in tot for e in s["expected_values"]))
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    for s in steps_out:
        if "wall_s" not in s:
            print(f"{s['id']}: {s.get('status')}")
            continue
        em = "".join("Y" if e["match"] else "N" for e in s["expected_values"])
        cm = []
        for c in s["log_comparisons"]:
            v = c.get("identical_apart_from_timings", c.get("identical_content", c.get("exists")))
            cm.append("Y" if v else "N")
        print(f"{s['id']:30s} rc={s['exit_code']} wall={s['wall_s']:8.1f} cpu={s['cpu_s']:8.1f} rss={s['peak_rss_mb']:7.1f}MB "
              f"exp={em or '-':6s} logs={''.join(cm) or '-':6s} guard={'HIT' if s['guard_main_tree_accesses'] else 'ok'}")
    print("totals:", man["totals"])


if __name__ == "__main__":
    main()
