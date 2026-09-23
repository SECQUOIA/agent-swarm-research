"""Independent regressions for proof-rule boundaries and assumption discharge."""
import pytest

from certify.vipr import validate_vipr


def replay(tmp_path, derivations, *, integers="INT 1\n0", constraint="b G 1/2 OBJ",
           objective="min", result="range 1 inf", solutions="SOL 0"):
    records = derivations.strip().splitlines()
    content = (f"VER 1.1\nVAR 1\nx\n{integers}\nOBJ {objective}\n1 0 1\n"
               f"CON 1 0\n{constraint}\nRTP {result}\n{solutions}\n"
               f"DER {len(records)}\n" + "\n".join(records) + "\n")
    path = tmp_path / "independent.vipr"
    path.write_text(content)
    return validate_vipr(path)


def test_unsplit_proves_integer_bound_with_one_infeasible_branch(tmp_path):
    result = replay(tmp_path, """
left L 0 OBJ { asm } -1
right G 1 OBJ { asm } -1
contradiction G 1/2 0 { lin 2 0 1 1 -1 } -1
join G 1 OBJ { uns 3 1 2 2 } -1
""")
    assert result["ok"], result


def test_unsplit_cannot_exclude_continuous_points_between_branches(tmp_path):
    result = replay(tmp_path, """
left L 0 OBJ { asm } -1
right G 1 OBJ { asm } -1
contradiction G 1/2 0 { lin 2 0 1 1 -1 } -1
join G 1 OBJ { uns 3 1 2 2 } -1
""", integers="INT 0")
    assert not result["ok"]
    assert "integer disjunction" in result["error"]


def test_unsplit_preserves_cross_branch_dependencies(tmp_path):
    result = replay(tmp_path, """
left L 0 OBJ { asm } -1
right G 1 OBJ { asm } -1
contradiction G 1 0 { lin 2 2 1 1 -1 } -1
join G 1000000 OBJ { uns 3 1 3 2 } -1
""", constraint="b G 0 OBJ", result="range 1000000 inf")
    assert not result["ok"]
    assert "undischarged assumptions" in result["error"]


def test_unsplit_preserves_unrelated_common_assumption(tmp_path):
    result = replay(tmp_path, """
left L 0 OBJ { asm } -1
right G 1 OBJ { asm } -1
unrelated G 1000000 OBJ { asm } -1
join G 1000000 OBJ { uns 3 1 3 2 } -1
""", constraint="b G 0 OBJ", result="range 1000000 inf")
    assert not result["ok"]
    assert "undischarged assumptions" in result["error"]


def test_zero_multiplier_does_not_introduce_assumption_dependency(tmp_path):
    result = replay(tmp_path, """
false_assumption G 1 0 { asm } -1
bound G 1 OBJ { lin 2 0 1 1 0 } -1
""", constraint="b G 1 OBJ")
    assert result["ok"], result


@pytest.mark.parametrize("values", [(1, 5), (5, 1)])
def test_cutoff_uses_best_verified_solution_independently_of_order(tmp_path, values):
    result = replay(tmp_path, """
cutoff L 1 OBJ { sol } -1
bound G 1 OBJ { lin 1 0 1 } -1
""", constraint="b G 1 OBJ", solutions=f"SOL 2\ns1 1 0 {values[0]}\ns2 1 0 {values[1]}")
    assert result["ok"], result


@pytest.mark.parametrize("cutoff,accepted", [("1", True), ("2", True), ("3", False)])
def test_maximization_cutoff_direction_and_best_solution(tmp_path, cutoff, accepted):
    result = replay(tmp_path, f"""
cutoff G {cutoff} OBJ {{ sol }} -1
bound L 2 OBJ {{ lin 1 0 1 }} -1
""", constraint="b L 2 OBJ", objective="max", result="range 1 2",
        solutions="SOL 2\ns1 1 0 2\ns2 1 0 1")
    assert result["ok"] is accepted, result


def test_infeasibility_cannot_depend_on_incumbent_cutoff(tmp_path):
    result = replay(tmp_path, "false G 1 0 { sol } -1", constraint="b G 1 OBJ",
                    result="infeas", solutions="SOL 1\ns1 1 0 1")
    assert not result["ok"]
    assert "infeasibility proof must have empty SOL" in result["error"]


def test_nonintegral_equality_cannot_be_rounded_to_integer_equality(tmp_path):
    result = replay(tmp_path, "bound E 1 OBJ { rnd 1 0 1 } -1", constraint="b E 1/2 OBJ")
    assert not result["ok"]
    assert "rounding equality" in result["error"]


def test_maximization_witness_cannot_supply_an_upper_bound(tmp_path):
    # max x+y over binary [0,1]^2 has optimum 2; witness (0,1) proves no upper bound 1.
    path = tmp_path / "forged_max.vipr"
    path.write_text("""VER 1.0
VAR 2
x y
INT 2
0 1
OBJ max
2 0 1 1 1
CON 4 4
xl G 0 1 0 1
xu L 1 1 0 1
yl G 0 1 1 1
yu L 1 1 1 1
RTP range 1 1
SOL 1
witness 1 1 1
DER 1
forged L 1 OBJ { sol } -1
""")
    result = validate_vipr(path)
    assert not result["ok"]
    assert "incumbent cutoff" in result["error"]


@pytest.mark.parametrize("tail", [
    "weaker G 0 OBJ { lin 1 0 1 } -1",
    "unused_assumption G 1000000 OBJ { asm } -1",
])
def test_closed_proving_row_survives_a_valid_nonproving_tail(tmp_path, tail):
    result = replay(tmp_path, f"proved G 1 OBJ {{ lin 1 0 1 }} -1\n{tail}",
                    constraint="b G 1 OBJ")
    assert result["ok"], result
    assert result["derivations"] == 2


@pytest.mark.parametrize("tail,error", [
    ("bad_arithmetic G 2 OBJ { lin 1 0 1 } -1", "does not dominate"),
    ("bad_cutoff L 0 OBJ { sol } -1", "verified feasible solution"),
    ("bad_global G 1000000 OBJ { asm } -1 global", "global marker"),
    ("bad_reference G 1 OBJ { lin 1 99 1 } -1", "out-of-range"),
])
def test_closed_proving_row_does_not_hide_an_invalid_counted_tail(tmp_path, tail, error):
    result = replay(tmp_path, f"proved G 1 OBJ {{ lin 1 0 1 }} -1\n{tail}",
                    constraint="b G 1 OBJ")
    assert not result["ok"]
    assert error in result["error"], result


def test_infeasibility_proved_before_a_valid_tautological_tail(tmp_path):
    result = replay(tmp_path, """
contradiction G 1 0 { lin 1 0 1 } -1
tautology G 0 0 { lin 0 } -1
""", constraint="inconsistent G 1 0", result="infeas")
    assert result["ok"], result
    assert result["derivations"] == 2
