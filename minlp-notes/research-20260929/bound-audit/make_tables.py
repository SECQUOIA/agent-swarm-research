"""Markdown tables for audit-report.md from results.json (grouped by instance and point).

Proven enclosures and bounds are rounded outward (lower ends down, upper ends up) from
the exact decimal strings in results.json. Point values, violations and margins are
rounded to nearest; they are sizes, not bounds.

Usage: python3 make_tables.py > logs/tables.md
"""
import json
import os
from collections import OrderedDict
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
SHORT = {"(i) proven invalid": "(i)", "(i-r) invalid as listed, within rounding of shown digits": "(i-r)",
         "(iii) undecided": "(iii)", "(ii) tolerance effect (proven)": "(ii) proven",
         "(ii) tolerance effect": "(ii) repair", "(ii) tolerance effect (numerical)": "(ii) num."}


def g(x, n=10):
    if x is None or x == "":
        return ""
    try:
        return f"{float(x):.{n}g}"
    except (TypeError, ValueError):
        return str(x)


def directed(x, n, up):
    """x (exact decimal string) rounded to n significant digits, up or down"""
    d = Decimal(x)
    if d == 0:
        return "0"
    q = Decimal(1).scaleb(d.adjusted() - n + 1)
    return str(d.quantize(q, rounding=ROUND_CEILING if up else ROUND_FLOOR))


def main():
    rows = json.load(open(os.path.join(HERE, "results.json")))
    groups = OrderedDict()
    for r in rows:
        c = SHORT.get(r["cls"], r["cls"])
        if c == "(i)":
            c = "(i) gross" if r["i_group"] == "gross" else "(i) tolerance-scale"
        k = (r["name"], r["point"], c)
        groups.setdefault(k, []).append(r)
    print("| instance | S | point (section) | f(point) | viol. | solvers: listed dual | class | exact point / bound | note |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (name, pt, cls), rs in groups.items():
        r0 = rs[0]
        duals = "; ".join(f"{r['solver']} {r['d_listed']}" for r in rs)
        if r0.get("obj_lo"):
            ex = f"[{directed(r0['obj_lo'], 13, False)}, {directed(r0['obj_hi'], 13, True)}]"
        elif r0.get("rigorous_opt_lower") is not None:
            ex = f"opt >= {directed(r0['rigorous_opt_lower'], 13, False)}"
        elif r0.get("polished_obj") is not None:
            ex = f"~{g(r0['polished_obj'], 11)} (not verified)"
        else:
            ex = ""
        note = r0.get("note", "")
        if cls in ("(i) gross", "(i) tolerance-scale", "(i-r)"):
            ms = ", ".join(f"{r['solver']} {r['margin_proved']:.3g} ({r['rel_margin']:.2g} of \\|d\\|)" for r in rs)
            note = f"margin {ms}; slack {rs[0]['d_slack']:.1g}"
        elif cls == "(iii)":
            me = min(r.get("margin_eval", 0) for r in rs)
            Me = max(r.get("margin_eval", 0) for r in rs)
            sl = rs[0]["d_slack"]
            tag = "at most (i-r)" if Me <= sl else "(i) if an exact point exists near it"
            note = f"{note[:60]}; margin at the listed point {me:.2g}..{Me:.2g} vs slack {sl:.1g}: {tag}"
        elif cls == "(ii) repair":
            note = "exact repair not beyond the dual"
        elif cls == "(ii) proven":
            note = "dual <= rigorous lower bound on the optimum"
            if r0.get("repaired_obj"):
                note += f"; point repaired to {g(r0['repaired_obj'], 11)}"
        print(f"| {name} | {'yes' if r0['solved'] else ''} | {pt} ({r0['section']}) | {g(r0.get('obj_eval'), 11)} | "
              f"{g(r0.get('viol_eval'), 2)} | {duals} | {cls} | {ex} | {note[:170]} |")


if __name__ == "__main__":
    main()
