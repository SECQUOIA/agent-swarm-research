"""End-to-end boundary checks for the nonlinear-to-MILP certificate contract."""
import json
from pathlib import Path
from fractions import Fraction

import pytest

from certify.driver import check_certificate, load_instance, prepare_model, write_lp


def bundle(tmp_path, source, proof=None):
    instance = tmp_path / "instance.py"
    instance.write_text("import pyomo.environ as pe\nm=pe.ConcreteModel()\n" + source)
    exact = prepare_model(load_instance(str(instance)))
    (tmp_path / "lemma.json").write_text(json.dumps({"sig_digits": 12, "lemmas": []}))
    write_lp(str(tmp_path / "master.lp"), [v.name for v in exact.variables],
             {v.name: "I" if v.is_integer() else "C" for v in exact.variables},
             exact.box, exact.rows, [], exact.obj_coefs, exact.obj_const)
    if proof is not None:
        (tmp_path / "master_complete.vipr").write_text(proof)
    return str(instance)


LINEAR_MODEL = "m.x=pe.Var(bounds=(1,None))\nm.obj=pe.Objective(expr=m.x)\n"
LINEAR_PROOF = """VER 1.0
VAR 1
x
INT 0
OBJ min 1 0 1
CON 1 1
B0 G 1 1 0 1
RTP range 1 inf
SOL 0
DER 1
D0 G 1 OBJ { lin 1 0 1 } -1
"""


def test_full_check_replays_proof_without_external_binary(tmp_path):
    instance = bundle(tmp_path, LINEAR_MODEL, LINEAR_PROOF)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = check_certificate(instance, str(tmp_path), verbose=False)
    assert result["ok"] and result["status"] == "verified"
    assert result["certified_bound_original_sense"] == "1"
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


def test_partial_checks_never_report_a_certified_bound(tmp_path):
    instance = bundle(tmp_path, LINEAR_MODEL)
    partial = check_certificate(instance, str(tmp_path), require_vipr=False, verbose=False)
    assert partial["partial_ok"] and not partial["ok"]
    assert partial["status"] == "partial" and "certified_master_lb" not in partial
    complete = check_certificate(instance, str(tmp_path), verbose=False)
    assert not complete["ok"] and complete["status"] == "rejected"


def test_sol_zero_false_bound_rejected_end_to_end(tmp_path):
    forged = Path(__file__).parent / "review_artifacts/bogus2.vipr"
    instance = bundle(tmp_path, LINEAR_MODEL, forged.read_text())
    result = check_certificate(instance, str(tmp_path), verbose=False)
    assert not result["ok"]
    assert "certified_master_lb" not in result
    assert "sol inference" in result["proof"]["error"]


def test_wrong_master_and_duplicate_json_fail_closed(tmp_path):
    instance = bundle(tmp_path, LINEAR_MODEL, LINEAR_PROOF.replace("B0 G 1", "B0 G 2"))
    assert not check_certificate(instance, str(tmp_path), verbose=False)["ok"]
    (tmp_path / "lemma.json").write_text('{"lemmas":[],"lemmas":[],"sig_digits":12}')
    result = check_certificate(instance, str(tmp_path), verbose=False)
    assert not result["ok"] and "duplicate JSON key" in str(result["checks"])


def test_source_names_with_scip_prefix_keep_their_identity(tmp_path):
    instance = bundle(tmp_path, LINEAR_MODEL.replace("m.x", "m.t_x"),
                      LINEAR_PROOF.replace("\nx\n", "\nt_x\n"))
    assert check_certificate(instance, str(tmp_path), verbose=False)["ok"]


def test_maximization_retains_constant_and_flips_bound(tmp_path):
    source = "m.x=pe.Var(bounds=(None,3))\nm.obj=pe.Objective(expr=2*m.x+5,sense=pe.maximize)\n"
    proof = """VER 1.0
VAR 2
x
objconst
INT 0
OBJ min 2 0 -2 1 -5
CON 3 3
B0 L 3 1 0 1
B1 G 1 1 1 1
B2 L 1 1 1 1
RTP range -11 inf
SOL 0
DER 1
D0 G -11 OBJ { lin 2 0 -2 2 -5 } -1
"""
    instance = bundle(tmp_path, source, proof)
    result = check_certificate(instance, str(tmp_path), verbose=False)
    assert result["ok"] and result["sense"] == -1
    assert result["certified_master_lb"] == "-11"
    assert result["certified_bound_original_sense"] == "11"


def test_failed_external_corroboration_cannot_expose_bound(tmp_path, monkeypatch):
    from types import SimpleNamespace
    import subprocess
    instance = bundle(tmp_path, LINEAR_MODEL, LINEAR_PROOF)
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: SimpleNamespace(
        returncode=1, stdout="Successfully verified optimal value range [1, inf)\n"))
    result = check_certificate(instance, str(tmp_path), viprchk="test-checker", verbose=False)
    assert not result["ok"] and "certified_master_lb" not in result


def test_multiple_objectives_rejected(tmp_path):
    instance = tmp_path / "instance.py"
    instance.write_text("import pyomo.environ as pe\nm=pe.ConcreteModel()\n" +
                        LINEAR_MODEL + "m.obj2=pe.Objective(expr=-m.x)\n")
    with pytest.raises(ValueError, match="exactly one"):
        prepare_model(load_instance(str(instance)))
