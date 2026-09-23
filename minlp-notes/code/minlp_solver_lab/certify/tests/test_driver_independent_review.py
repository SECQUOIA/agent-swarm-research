"""Independent integration check of signed nonlinear and fixed-value semantics."""
import json
from fractions import Fraction as F

from certify.driver import check_certificate, load_instance, prepare_model, write_lp


def test_nonlinear_maximum_fixed_variable_and_constant_transfer(tmp_path):
    instance = tmp_path / "instance.py"
    instance.write_text(
        "import pyomo.environ as pe\n"
        "m=pe.ConcreteModel()\n"
        "m.x=pe.Var(bounds=(0,2))\n"
        "m.y=pe.Var(initialize=2)\n"
        "m.y.fix()\n"
        "m.c=pe.Constraint(expr=m.x**2+2*m.y<=8)\n"
        "m.obj=pe.Objective(expr=-(m.x-m.y)**2+3*m.x+7,sense=pe.maximize)\n"
    )
    exact = prepare_model(load_instance(str(instance)))
    assert exact.box["y"] == [F(2), F(2)]
    lemmas = [
        dict(name="rowcut", row="c_ub", z={"x": "2"}, a={"x": "4"}, b="-8"),
        dict(name="objcut", row="objective_epi", z={"x": "2", "_lbesh_epigraph": "0"},
             a={"x": "-3", "_lbesh_epigraph": "-1"}, b="-7"),
    ]
    (tmp_path / "lemma.json").write_text(json.dumps(dict(sig_digits=12, lemmas=lemmas)))
    cuts = [(entry["name"], {k: F(v) for k, v in entry["a"].items()}, F(entry["b"]))
            for entry in lemmas]
    write_lp(str(tmp_path / "master.lp"), [v.name for v in exact.variables],
             {v.name: "C" for v in exact.variables}, exact.box, exact.rows, cuts,
             exact.obj_coefs, exact.obj_const)
    (tmp_path / "master_complete.vipr").write_text("""VER 1.0
VAR 3
x
y
_lbesh_epigraph
INT 0
OBJ min 1 2 1
CON 6 4
B0 G 0 1 0 1
B1 L 2 1 0 1
B2 G 2 1 1 1
B3 L 2 1 1 1
C0 L 8 1 0 4
C1 L 7 2 0 -3 2 -1
RTP range -13 inf
SOL 0
DER 1
D0 G -13 OBJ { lin 2 1 -3 5 -1 } -1
""")
    report = check_certificate(str(instance), str(tmp_path), verbose=False)
    assert report["ok"], report
    assert report["certified_master_lb"] == "-13"
    assert report["certified_bound_original_sense"] == "13"
    # The same master proof cannot justify a stronger nonlinear row cut.
    lemmas[0]["b"] = "-7"
    (tmp_path / "lemma.json").write_text(json.dumps(dict(sig_digits=12, lemmas=lemmas)))
    rejected = check_certificate(str(instance), str(tmp_path), verbose=False)
    assert not rejected["ok"]
    assert "certified_bound_original_sense" not in rejected
    assert "supporting-point conditions fail" in str(rejected["checks"])
