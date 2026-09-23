"""Adversarial proof-kernel regressions, independent of an external checker."""
from fractions import Fraction

import pytest

from certify.vipr import check_vipr_output, parse_problem, validate_vipr


def proof(*, variables="VAR 1\nx", integers="INT 0", objective="OBJ min\n1 0 1",
          constraints="CON 1 1\nb G 1 1 0 1", rtp="RTP range 1 inf",
          solutions="SOL 0", derivations="DER 1\nd G 1 OBJ { lin 1 0 1 } -1"):
    return f"VER 1.0\n{variables}\n{integers}\n{objective}\n{constraints}\n{rtp}\n{solutions}\n{derivations}\n"


def check(tmp_path, text):
    path = tmp_path / "proof.vipr"
    path.write_text(text)
    return validate_vipr(path)


def test_exact_bound_and_shared_problem_parser(tmp_path):
    text = proof(constraints="CON 1 1\nb G 100000000000000000001/3 1 0 1",
                 rtp="RTP range 100000000000000000001/3 inf",
                 derivations="DER 1\nd G 100000000000000000001/3 OBJ { lin 1 0 1 } -1")
    result = check(tmp_path, text)
    assert result["ok"], result
    assert result["lower_bound"] == "100000000000000000001/3"
    names, integers, sense, objective, rows = parse_problem(tmp_path / "proof.vipr")
    assert (names, integers, sense, objective) == (["x"], set(), "min", {0: Fraction(1)})
    assert rows[0][2] == Fraction(100000000000000000001, 3)


def test_sol_zero_false_bound_regression(tmp_path):
    text = proof(rtp="RTP range 1000000 inf", derivations="""DER 3
cutoff L 0 OBJ { sol } -1
false G 1 0 { lin 2 0 1 1 -1 } -1
bad G 1000000 OBJ { lin 1 2 1 } -1""")
    result = check(tmp_path, text)
    assert not result["ok"]
    assert "requires a verified feasible solution" in result["error"]


@pytest.mark.parametrize("changes, error", [
    ({"variables": "VAR 2\nx x"}, "duplicate variable"),
    ({"integers": "INT 1\n1"}, "integer variable index"),
    ({"variables": "VAR 2\nx y", "integers": "INT 2\n0 0"}, "integer variable index"),
    ({"variables": "VAR 2\nx y", "objective": "OBJ min\n2 0 1 0 1"}, "duplicate vector index"),
    ({"constraints": "CON 1 1\nb G 1 1 1 1"}, "vector index"),
    ({"variables": "VAR 2\nx y", "constraints": "CON 1 1\nb G 1 2 0 0 0 1"}, "duplicate vector index"),
    ({"constraints": "CON 1 2\nb G 1 1 0 1"}, "bound count"),
    ({"objective": "OBJ min\nOBJ"}, "abbreviation"),
    ({"objective": "OBJ min\n-1"}, "integer outside"),
    ({"constraints": "CON 1 1\nb Q 1 1 0 1"}, "constraint sense"),
    ({"rtp": "RTP range 2 1"}, "reversed RTP"),
    ({"rtp": "RTP range 1.0 inf"}, "integer or fraction"),
    ({"rtp": "RTP range 1/0 inf"}, "integer or fraction"),
    ({"derivations": "DER 1\nd G 1 OBJ { lin 1 1 1 } -1"}, "forward"),
    ({"derivations": "DER 1\nd G 1 OBJ { lin 1 99 0 } -1"}, "forward"),
    ({"derivations": "DER 1\nd G 1 OBJ { lin 2 0 1 0 1 } -1"}, "duplicate inference"),
    ({"derivations": "DER 1\nd G 1 OBJ { lin weak 0 } -1"}, "invalid integer"),
    ({"derivations": "DER 2\nd G 1 OBJ { lin 1 0 1 } -1"}, "truncated"),
    ({"derivations": "DER 1\nd G 1 OBJ { lin 1 0 1 } -1 extra"}, "malformed"),
    ({"derivations": "DER 1\nd G 1 OBJ { asm } -1"}, "undischarged"),
    ({"derivations": "DER 0"}, "missing proof"),
    ({"derivations": "DER 1\nd G 2 OBJ { lin 1 0 1 } -1"}, "does not dominate"),
    ({"derivations": "DER 1\nd G 0 OBJ { lin 1 0 1 } -1"}, "no assumption-free derivation proves RTP"),
    ({"derivations": "DER 2\nd G 1 OBJ { lin 1 0 1 } 0\ne G 1 OBJ { lin 1 1 1 } -1"}, "after declared last use"),
    ({"derivations": "DER 1\nd G 1 OBJ { lin 1 0 1 } 2"}, "annotation outside"),
])
def test_malformed_and_invalid_proofs_fail_closed(tmp_path, changes, error):
    result = check(tmp_path, proof(**changes))
    assert not result["ok"], result
    assert error in result["error"], result


def test_trailing_data_is_checked_after_successful_prefix(tmp_path):
    result = check(tmp_path, proof() + "malicious trailing data\n")
    assert not result["ok"]
    assert "trailing data" in result["error"]


@pytest.mark.parametrize("integers, coefficient, expected", [
    ("INT 0", "1", False),
    ("INT 1\n0", "1/2", False),
    ("INT 1\n0", "1", True),
])
def test_rounding_requires_integer_linear_form(tmp_path, integers, coefficient, expected):
    result = check(tmp_path, proof(integers=integers,
        objective=f"OBJ min\n1 0 {coefficient}",
        constraints=f"CON 1 1\nb G 1/2 1 0 {coefficient}",
        derivations="DER 1\nd G 1 OBJ { rnd 1 0 1 } -1"))
    assert result["ok"] is expected, result


def test_integer_rounding_floor_negative_rhs(tmp_path):
    result = check(tmp_path, proof(integers="INT 1\n0", objective="OBJ max\n1 0 1",
        constraints="CON 1 1\nb L -1/2 1 0 1", rtp="RTP range -inf -1",
        derivations="DER 1\nd L -1 OBJ { rnd 1 0 1 } -1"))
    assert result["ok"], result


@pytest.mark.parametrize("solutions,error", [
    ("SOL 1\ns 1 0 0", "infeasible SOL"),
    ("SOL 1\ns 1 0 3/2", "nonintegral solution"),
    ("SOL 0", "primal RTP bound"),
    ("SOL 1\ns OBJ", "abbreviation"),
])
def test_solution_validation(tmp_path, solutions, error):
    result = check(tmp_path, proof(integers="INT 1\n0", rtp="RTP range 1 1", solutions=solutions))
    assert not result["ok"]
    assert error in result["error"]


def test_solution_cutoff_is_safe_and_integer_extension_rejected(tmp_path):
    for cutoff in ("0", "1"):
        result = check(tmp_path, proof(integers="INT 1\n0", solutions="SOL 1\ns 1 0 1",
            derivations=f"DER 2\nc L {cutoff} OBJ {{ sol }} -1\nd G 1 OBJ {{ lin 1 0 1 }} -1"))
        assert result["ok"] is (cutoff == "1"), result


def test_unsplit_integer_disjunction(tmp_path):
    result = check(tmp_path, proof(integers="INT 1\n0", constraints="CON 1 1\nb G 0 1 0 1",
        rtp="RTP range 0 inf", derivations="""DER 5
left L 0 1 0 1 { asm } -1
right G 1 1 0 1 { asm } -1
leftbound G 0 OBJ { lin 1 0 1 } -1
rightbound G 0 OBJ { lin 1 2 1 } -1
join G 0 OBJ { uns 3 1 4 2 } -1"""))
    assert result["ok"], result


@pytest.mark.parametrize("left,right,branch_ref", [
    ("1/2", "3/2", "1"),  # A gap between halves need not cover the integer 1.
    ("0", "1", "0"),      # A model row is not a branching assumption.
    ("0", "2", "1"),      # Nonexhaustive disjunction.
])
def test_invalid_unsplit(tmp_path, left, right, branch_ref):
    result = check(tmp_path, proof(integers="INT 1\n0", constraints="CON 1 1\nb G 0 1 0 1",
        rtp="RTP range 0 inf", derivations=f"""DER 5
left L {left} 1 0 1 {{ asm }} -1
right G {right} 1 0 1 {{ asm }} -1
leftbound G 0 OBJ {{ lin 1 0 1 }} -1
rightbound G 0 OBJ {{ lin 1 2 1 }} -1
join G 0 OBJ {{ uns 3 {branch_ref} 4 2 }} -1"""))
    assert not result["ok"], result


def test_wrong_sign_combination(tmp_path):
    result = check(tmp_path, proof(constraints="CON 2 2\na G 1 1 0 1\nb G 2 1 0 1",
        derivations="DER 1\nd G 1 OBJ { lin 2 0 1 1 -1 } -1"))
    assert not result["ok"]
    assert "unsuitable" in result["error"]


def test_streaming_releases_rows_even_with_unlimited_lifetime_annotations(tmp_path):
    count = 1000
    rows = [f"d{i} G 1 OBJ {{ lin 1 {i} 1 }} -1" for i in range(count)]
    result = check(tmp_path, proof(derivations=f"DER {count}\n" + "\n".join(rows)))
    assert result["ok"], result
    assert result["derivations"] == count
    assert result["peak_live_rows"] == 1


def test_external_success_requires_exact_complete_verdict_and_zero_exit(tmp_path):
    validation = check(tmp_path, proof())
    success = "Successfully verified optimal value range [1, inf).\n"
    assert check_vipr_output(0, success, validation) == (True, "")
    for code, output in [(1, success), (0, "Successfully verified."),
                         (0, success + success), (0, success.replace("[1,", "[2,")),
                         (0, success.replace("inf)", "inf]")),
                         (0, "prefix " + success)]:
        assert not check_vipr_output(code, output, validation)[0]


def test_global_metadata_preserves_an_assumption_free_derivation(tmp_path):
    result = check(tmp_path, proof(derivations="DER 1\nd G 1 OBJ { lin 1 0 1 } -1 global"))
    assert result["ok"], result
    assert result["lower_bound"] == "1"


def test_forged_global_metadata_cannot_discard_assumptions(tmp_path):
    result = check(tmp_path, proof(derivations="""DER 3
branch G 1000000 OBJ { asm } -1
forged G 1000000 OBJ { lin 1 1 1 } -1 global
otherwise_valid G 1 OBJ { lin 1 0 1 } -1"""))
    assert not result["ok"], result
    assert "global marker on a row with undischarged assumptions" in result["error"]


@pytest.mark.parametrize("suffix", ["global global", "global ignored", "ignored global"])
def test_global_metadata_does_not_allow_other_trailing_material(tmp_path, suffix):
    result = check(tmp_path, proof(derivations=f"DER 1\nd G 1 OBJ {{ lin 1 0 1 }} -1 {suffix}"))
    assert not result["ok"], result
