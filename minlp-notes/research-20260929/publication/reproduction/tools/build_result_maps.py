"""Map the saved summary and audit rows to existing scripts, inputs and outputs."""
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

from finish_paths import RESEARCH, OUT
from eg_evidence import TRACK, EXPECTED, evidence_paths, update_command_index


def record(path):
    p = Path(path).expanduser() if path.startswith("~/") else RESEARCH / path
    assert p.is_file(), path
    return dict(path=path, sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def primary(name):
    oi = "open-instances"
    v = "reviews/open-instances-verification"
    small = "reviews/wave2-small-verification"
    if name.startswith("lnts"):
        return v, "python3 v_lnts.py 50 100 200 400", [f"{oi}/logs/lnts_{name}_primal.txt"], [f"{v}/logs/lnts_verify.json"]
    if name == "dtoc5":
        return v, "python3 v_dtoc5.py", [f"{oi}/logs/dtoc5_y.npy"], [f"{v}/logs/dtoc5_verify.json"]
    if name.startswith("camshape"):
        return v, "python3 v_camshape.py 100 200 400 800", [], [f"{v}/logs/camshape_verify.json"]
    if name == "lukvle10":
        return v, "python3 v_lukvle10_prep.py; python3 v_lukvle10_bnb.py 1", [f"{oi}/minlplib_sol/lukvle10.p5.sol"], [f"{v}/logs/lukvle10_bnb.json", f"{v}/logs/lukvle10_prep.json"]
    if name == "optcdeg2":
        p = "reviews/bangbang-verification"
        return p, "python3 v_model.py; python3 v_states.py; python3 v_primal.py; python3 v_qcal_exact.py", ["theory-bangbang/logs/optcdeg2_qcal_data.npz"], [f"{p}/logs/qcal_exact.json", f"{p}/logs/primal_check.json"]
    if name.startswith("chain"):
        p = "open-instances-wave2/cops"
        return p, f"python3 chain_model.py {name[5:]}; python3 chain_bound.py 1e-14 {name[5:]}", [], [f"{p}/logs/{name}_bound.json", f"{p}/logs/{name}_primal.txt"]
    if name.startswith("catmix"):
        n = name[6:]
        if n in ("100", "200"):
            p = "reviews/cops-verification"
            args = "100 16 0.0697 0.0715 20 300 25" if n == "100" else "200 15 0.0695 0.0717 19 200 24"
            return p, f"python3 v_catmix_selftest.py {n}; python3 v_catmix_dp.py {args}", [f"{p}/logs/{name}_theta_traj.npy"], [f"{p}/logs/{name}_cfg{'B' if n == '100' else 'A'}.log"]
        p = "reviews/catmix-recheck-checks"
        return p, "See README.md: exact recheck_dp.py command, followed by policy_exact.py", [f"{p}/logs/{name}_theta_traj.npy", f"{p}/logs/{name}_final_policy_u.npy"], [f"{p}/logs/tree{n}_final.json", f"{p}/logs/{name}_final.log"]
    if name == "hvycrash":
        return small, "python3 v_hvycrash.py", [], [f"{small}/logs/hvycrash.json"]
    if name in ("ex6_2_7", "ex6_2_5"):
        tau = "6e-15" if name.endswith("7") else "1e-17"
        return small, f"python3 gibbs_bound.py {name} 0=logs/{name}_bb_type0_tau{tau}.json", [f"{small}/logs/{name}_kkt.json", f"{small}/logs/{name}_bb_type0_tau{tau}.json"], [f"{small}/logs/{name}_bound.json"]
    if name in ("etamac", "pricing050"):
        return small, f"python3 v_{name}.py", [], [f"{small}/logs/{name}.json"]
    if name == "pindyck":
        p = "reviews/pindyck-review-checks"
        return p, "python3 final_bound.py", [f"{p}/ranges.pkl", f"{p}/author_data.pkl", f"{p}/logs/primal_enclosure.txt"], [f"{p}/logs/final_bound.log"]
    if name.startswith("eg_"):
        p = "open-instances-wave3/eg/retry"
        tags = ["int9_final"] if name == "eg_int_s" else ["disc9_p0", "disc9_p1"] if name == "eg_disc_s" else [f"disc2_9_p{k}" for k in range(8)]
        return p, "python3 summary.py; see README.md for generation and verify_primal.py", [f"{p}/logs/{tag}.npz" for tag in tags], [f"{p}/logs/{tag}.log" for tag in tags] + [f"{p}/sol/{name}.retry.sol"]
    if name.startswith("kan_"):
        p = "open-instances-wave3/kan"
        return p, f"python3 run_kan.py {name} 1e-10 7200; python3 kan_summary.py", [str(next((RESEARCH / "open-instances-wave3/sol").glob(name + ".p*.sol")).relative_to(RESEARCH))], [f"open-instances-wave3/logs/{name}.result.json", "reviews/wave3-verification/logs/kan_infeas_cert.log"]
    if name == "powerflow0030p":
        p = "reviews/wave3-verification/powerflow"
        return p, f"python3 run_root.py {name}", [f"open-instances-wave3/logs/{name}.sdpcert.json", f"open-instances-wave3/sol/{name}.p1.sol"], ["publication/reproduction/network/logs/pf.verifier_root_stored.powerflow0030p.log"]
    if name.startswith("powerflow"):
        p = "open-instances-wave3/powerflow/ext"
        return p, f"python3 verify_exact.py {name} bb3t", [f"{p}/logs/{name}.bb3t.json", f"open-instances-wave3/sol/{name}.p1.sol"], [f"{p}/logs/{name}.bb3t.log"]
    if name.startswith("waterno2"):
        tt = name[-2:]
        p = "reviews/waterno2-verification"
        ins = [f"open-instances-wave2/waterno2/logs/mult_{tt}_w1_impl.json"]
        outs = [f"open-instances-wave2/waterno2/logs/cert_{tt}_w1_impl.json"]
        if tt == "06":
            ins += ["open-instances-wave2/waterno2/sepbranch/logs/cert3.pkl", "open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz"]
            outs += ["open-instances-wave2/waterno2/sepbranch/logs/cert3_verify.json", "open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json"]
        else:
            ins += [f"open-instances-wave2/waterno2/logs/primal_{tt}_w2.json"]
        outs += [f"{p}/logs/vsum.log", "reviews/waterno2-recheck/logs/vsum2.log"]
        return p, f"python3 vsum.py {int(tt)}; see README.md for the two T=6 extensions", ins, outs
    if name == "ann_cumene_tanh":
        p = "reviews/ann-extension-review-checks"
        return p, "See README.md and commands.json: replay.py, leaves.py, verify_boxes.py", ["open-instances-wave3/ann/ext_logs/open1800_v1.npz", "open-instances-wave3/ann/ext_logs/open_run2.npz", "open-instances-wave3/ann/ext_logs/ann_tm_v1_snapshot.py", "open-instances-wave3/ann/ext_logs/ann_tm_run2_snapshot.py"], ["open-instances-wave3/ann/ext_logs/run_v1_1800.log", "open-instances-wave3/ann/ext_logs/run2_resume_5400.log"]
    raise ValueError(name)


def expanded(label):
    if label == "chain50–400":
        return [f"chain{n}" for n in [50, 100, 200, 400]]
    if label == "catmix100–800":
        return [f"catmix{n}" for n in [100, 200, 400, 800]]
    if label.startswith("kan_r3"):
        return [f"kan_r{r}_h1_n{n}" for r, ns in [(3, [4, 5, 9]), (5, [3, 5, 8])] for n in ns]
    return [label.replace(" (max)", "")]


def numeric_evidence(name, outputs):
    """Map certificate/primal numbers at their saved precision, before display rounding."""
    evidence = []

    def add(path, value, quantity):
        evidence.append(dict(path=path, value=str(value), quantity=quantity))

    def load(path):
        return json.loads((RESEARCH / path).read_text())

    first = outputs[0]
    if name.startswith("lnts"):
        d = next(d for d in load(first) if d["name"] == name)
        add(first, d["cert_1e-12"]["bound"], "lower bound")
        add(first, d["own_primal"]["obj"], "tolerance-feasible primal")
    elif name.startswith("camshape"):
        d = next(d for d in load(first) if d["n"] == int(name[8:]))
        add(first, d["bound"], "exact optimum enclosure display")
    elif name == "dtoc5":
        d = load(first)
        add(first, re.search(r"[0-9.]+", d["dual_bound"][0])[0], "lower enclosure endpoint")
        add(first, d["own_primal"]["obj"], "tolerance-feasible primal")
    elif name == "lukvle10":
        add(first, load(first)["dual_bound"], "lower bound display before outward rounding")
        add(outputs[1], load(outputs[1])["p5"]["obj"], "listed primal")
    elif name == "optcdeg2":
        add(first, load(first)["bound_str"], "scaled exact bound (divide by 10**20)")
        add(outputs[1], load(outputs[1])["rigorous_primal"]["J_point"], "rigorously feasible primal display")
    elif name.startswith("chain"):
        d = load(first)
        add(first, d["bnb"]["bound"], "binary64 lower bound representation")
        add(first, d["primal"]["obj_double_point"], "tolerance-feasible primal")
    elif name.startswith("catmix"):
        log = next(path for path in outputs if path.endswith(".log"))
        text = (RESEARCH / log).read_text()
        add(log, re.search(r'"dual_bound": (-?[0-9.e+-]+)', text)[1], "binary64 lower bound representation")
        if '"policy_J_hi"' in text:
            add(log, re.search(r'"policy_J_hi": "([^"]+)"', text)[1], "exact policy objective display")
    elif name == "hvycrash":
        add(first, load(first)["own_point_decimal60"]["objective"], "exact objective")
    elif name.startswith("ex6_"):
        d = load(first)
        add(first, d["dual_bound"], "lower bound")
        add(first, d["own_primal_objective_enclosure"][1], "primal enclosure endpoint")
    elif name == "etamac":
        add(first, load(first)["bound"]["dual_bound"], "lower bound before outward display")
    elif name == "pricing050":
        d = load(first)
        add(first, d["certificate"]["upper_bound"], "upper bound (maximization)")
        add(first, d["own_primal"]["objective_exact"], "exact primal display")
    elif name == "pindyck":
        add(first, "-1170.4862854360886163932", "safe lower bound")
        add(first, "-1170.486285436088562087577425069289", "primal enclosure endpoint")
    elif name.startswith("eg_"):
        if name == "eg_disc_s":
            # The minimum over all parts binds the full-domain lower bound.
            logs = [path for path in outputs if path.endswith(".log")]
            first = min(logs, key=lambda path: Fraction(float(re.search(
                r'certified lower bound np.float64\(([^)]+)\)',
                (RESEARCH / path).read_text())[1])))
        text = (RESEARCH / first).read_text()
        add(first, re.search(r'certified lower bound np.float64\(([^)]+)\)', text)[1], "lower bound")
        sol = next(path for path in outputs if path.endswith(".retry.sol"))
        add(sol, re.search(r'objvar\s+(\S+)', (RESEARCH / sol).read_text())[1], "exactly feasible primal display")
    elif name.startswith("kan_"):
        d = load(first)
        add(first, d["dual_bound"], "network relaxation R lower bound")
        add(first, d["primal_obj"], "network relaxation R primal")
    elif name == "powerflow0030p":
        add(first, "576.8934122988004698491596317863177375044", "stored certificate lower enclosure endpoint display")
        add(first, "576.89341347037138687", "listed primal")
    elif name.startswith("powerflow"):
        text = (RESEARCH / first).read_text()
        add(first, re.search(r'FINAL .*?certified LB ([0-9.]+)', text)[1], "lower bound before outward display")
        add(first, re.search(r'UB ([0-9.]+)', text)[1], "primal upper bound")
    elif name.startswith("waterno2"):
        if name.endswith("06"):
            path = "open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json"
            add(path, load(path)["bound_rounded_down"], "cell-slopes lower bound")
        else:
            path = "reviews/waterno2-verification/logs/vsum.log"
            text = (RESEARCH / path).read_text()
            value = re.search(r'T=' + str(int(name[-2:])) + r':.*?sum = ([0-9.]+)', text)[1]
            add(path, value, "full horizon lower bound")
            add("reviews/waterno2-recheck/logs/vsum2.log", value, "independent full horizon lower bound")
    elif name.startswith("ann_"):
        add(outputs[-1], "-3386.5402291369187", "lower bound before outward display")
        add(outputs[-1], "-3379.982394046125", "network primal")
    assert evidence, name
    return evidence


def all_numbers(value, path):
    """Retain every numeric leaf in each saved audit record, including margins."""
    evidence = []
    if isinstance(value, dict):
        for child in value.values():
            evidence.extend(all_numbers(child, path))
    elif isinstance(value, list):
        for child in value:
            evidence.extend(all_numbers(child, path))
    elif type(value) in (int, float) or isinstance(value, str) and re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", value):
        evidence.append(dict(path=path, value=str(value), quantity="saved audit numeric field"))
    return evidence


def main():
    summary = []
    listed = {p["name"]: p for p in json.loads((RESEARCH / "bound-audit/pages.json").read_text())}
    result_table = False
    for line in (RESEARCH / "open-instances-summary.md").read_text().splitlines():
        if not line.startswith("| "):
            continue
        cells = [p.strip() for p in line.strip("|").split("|")]
        if cells[0] in ("instance", "instances"):
            result_table = "best listed dual" in cells
            continue
        if not result_table:
            continue
        for name in expanded(cells[0]):
            cwd, cmd, inputs, outputs = primary(name)
            scripts = []
            for part in cmd.split(";"):
                words = part.strip().split()
                if words[:1] == ["python3"]:
                    scripts.append(record(cwd + "/" + words[1]))
            if name.startswith("catmix") and name[6:] in ("400", "800"):
                scripts += [record(cwd + "/recheck_dp.py"), record(cwd + "/policy_exact.py")]
            if name.startswith("ann_"):
                scripts += [record(cwd + "/replay.py"), record(cwd + "/leaves.py"), record(cwd + "/verify_boxes.py")]
            if name.startswith("eg_"):
                scripts += [record(cwd + "/egbb.py"), record(cwd + "/verify_primal.py")]
            if name == "eg_disc2_s":
                extra_scripts, extra_inputs, extra_outputs = evidence_paths()
                scripts += [record(p) for p in extra_scripts]
                inputs += extra_inputs
                outputs += extra_outputs
            summary.append(dict(instance=name, reported_row=cells, cwd="$R/" + cwd,
                                command=cmd, scripts=scripts,
                                listed_snapshot=listed[name],
                                osil="~/.cache/minlplib/minlplib/osil/" + name + ".osil",
                                saved_inputs=[record(p) for p in inputs], outputs=[record(p) for p in outputs],
                                numeric_evidence=numeric_evidence(name, outputs)))
            if name == "eg_disc2_s":
                summary[-1]["all_leaf_recheck"] = dict(
                    cwd="$R/" + TRACK, command="python3 summarize.py",
                    command_index_prefix="eg-recheck/", expected=EXPECTED,
                    history="The earlier retry review sampled 110,676 of 979,044 leaves outside part 1.")
                for value, quantity in [("1114361", "all-leaf count"), ("0", "all-leaf failures")]:
                    summary[-1]["numeric_evidence"].append(dict(
                        path=TRACK + "/logs/summarize.log", value=value, quantity=quantity))
    assert len(summary) == 43
    assert len({row["instance"] for row in summary}) == 43
    update_command_index()
    (OUT / "result-map.json").write_text(json.dumps(summary, indent=2) + "\n")
    result = json.loads((RESEARCH / "bound-audit/results.json").read_text())
    pairs = json.loads((RESEARCH / "bound-audit/summary.json").read_text())["pairs"]
    screened = json.loads((RESEARCH / "bound-audit/screen.json").read_text())["pairs"]
    audit = []
    lines = ["# All screened audit instances\n", "Paths below are relative to `$R/bound-audit`. Commands run there.\n",
             "The saved `summary.json` contains all exact pair enclosures and classifications;\n",
             "`audit-map.json` retains them without shortening their digits. See README.md for\n",
             "special certificates, software versions, runtime sources and historical limits.\n\n",
             "| instance | screened points | final classes | commands | saved point outputs |\n",
             "|---|---|---|---|---|\n"]
    for name in sorted({p["name"] for p in screened}):
        tags = sorted({name + "." + p["point"] for p in screened if p["name"] == name})
        ins, outs, commands = [], [], []
        for tag in tags:
            ins.append(record("bound-audit/sol/" + tag + ".sol"))
            commands += ["python3 audit_eval.py " + tag, "python3 verify_one.py " + tag]
            for d in ["eval", "verify"]:
                path = "bound-audit/logs/" + d + "/" + tag + ".json"
                if (RESEARCH / path).exists():
                    outs.append(record(path))
        own_pairs = [p for p in pairs if p["name"] == name]
        own_results = [p for p in result if p["name"] == name]
        classes = sorted({p["cls"] for p in own_pairs})
        special = []
        for pattern in [f"cert_*_{name}.json", f"cert_*_{name}.*.json"]:
            special.extend(str(p.relative_to(RESEARCH)) for p in (RESEARCH / "bound-audit/logs").glob(pattern))
        audit.append(dict(instance=name, commands=commands, scripts=[record("bound-audit/audit_eval.py"), record("bound-audit/verify_one.py")],
                          inputs=ins, point_outputs=outs, special_certificates=[record(p) for p in sorted(set(special))],
                          classified_pairs=own_pairs, result_rows=own_results,
                          outputs=[record("bound-audit/summary.json"), record("bound-audit/results.json")],
                          numeric_evidence=all_numbers(own_pairs, "bound-audit/summary.json")
                          + all_numbers(own_results, "bound-audit/results.json")))
        point_names = ", ".join(t[len(name) + 1:] for t in tags)
        lines.append(f"| {name} | {point_names} | {', '.join(classes)} | `python3 audit_eval.py {name}.pK`; `python3 verify_one.py {name}.pK` for listed K | `logs/eval/{name}.pK.json`; existing `logs/verify/{name}.pK.json`; special certificates in `audit-map.json` |\n")
    assert len(audit) == 46
    (OUT / "audit-map.json").write_text(json.dumps(audit, indent=2) + "\n")
    (OUT / "audit-instances.md").write_text("".join(lines))
    print(f"Mapped {len(summary)} summary instances and {len(audit)} audit instances.")


if __name__ == "__main__":
    main()
