"""Exact replay of the complete VIPR subset used by this certificate pipeline.

This module checks proof arithmetic itself; an upstream ``viprchk`` success is
not a substitute.  A checked assumption-free row may establish the requested
relation before the last derivation, but every suffix row and EOF are checked.
We accept VER 1.0/1.1 with complete lin/rnd/asm/uns/sol
reasons, integer/fraction numeric tokens, and one derivation per line.  A single
terminal ``global`` marker asserts that the row has no assumptions.  Labels
and CON's bound count are metadata: references always identify rows by index.

``sol`` retains every feasible point at least as good as a checked incumbent.
It requires a feasible solution and rejects the upstream ``best - 1`` integer
cutoff extension.  No inference therefore requires existence of an optimizer.

A first streaming pass validates references and computes actual last uses in
compact integer arrays.  Replay releases rows at those uses, including for
files whose lifetime annotations are all -1.  Memory is proportional to the
number of rows (8 bytes per row after scanning), live sparse constraints, and
the longest input line, rather than the proof's byte size.  Lifetime annotations
are checked, never trusted to replace a missing row.  This is executable exact
checking, not a formally verified parser or proof kernel.
"""
from array import array
from dataclasses import dataclass, field
from functools import lru_cache
from fractions import Fraction
import re

from flint import fmpq


class ViprError(ValueError):
    """Malformed, unsupported, or mathematically invalid proof."""


_INT = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
_SENSE = {"L": -1, "E": 0, "G": 1}


def _integer(token, minimum=0):
    if not _INT.fullmatch(token):
        raise ViprError(f"invalid integer token: {token[:60]}")
    value = int(token)
    if value < minimum or value > 2**63 - 1:
        raise ViprError(f"integer outside supported range: {token[:60]}")
    return value


@lru_cache(maxsize=4096)
def _rational(token):
    if not _RATIONAL.fullmatch(token):
        raise ViprError(f"expected integer or fraction, got {token[:60]}")
    return fmpq(token)


class _Tokens:
    def __init__(self, tokens):
        self.tokens = iter(tokens)

    def next(self):
        try:
            return next(self.tokens)
        except StopIteration:
            raise ViprError("unexpected end of record/file") from None

    def expect(self, expected):
        got = self.next()
        if got != expected:
            raise ViprError(f"expected {expected}, got {got[:60]}")

    def end(self):
        if next(self.tokens, None) is not None:
            raise ViprError("extra tokens after record/file")


class _HeaderTokens(_Tokens):
    def __init__(self, file):
        self.file = file
        super().__init__(())

    def next(self):
        while True:
            token = next(self.tokens, None)
            if token is not None:
                return token
            line = self.file.readline()
            if not line:
                raise ViprError("unexpected end of file")
            if line.lstrip().startswith("%"):
                continue
            self.tokens = iter(line.split())


@dataclass(slots=True)
class _Row:
    sense: int
    rhs: object
    coefficients: dict
    assumptions: frozenset = field(default_factory=frozenset)
    assumption: bool = False
    label: str = ""

    def falsehood(self):
        return not self.coefficients and (
            (self.sense <= 0 and self.rhs < 0)
            or (self.sense >= 0 and self.rhs > 0)
        )

    def dominates(self, target):
        if self.falsehood():
            return True
        if self.coefficients != target.coefficients:
            return False
        return (
            target.sense > 0 and self.sense >= 0 and self.rhs >= target.rhs
            or target.sense < 0 and self.sense <= 0 and self.rhs <= target.rhs
            or target.sense == self.sense == 0 and self.rhs == target.rhs
        )

    def satisfied(self, values):
        lhs = sum((a * values.get(i, 0) for i, a in self.coefficients.items()), fmpq(0))
        if self.sense < 0:
            return lhs <= self.rhs
        if self.sense > 0:
            return lhs >= self.rhs
        return lhs == self.rhs


def _vector(tokens, n, objective=None):
    size = tokens.next()
    if size == "OBJ":
        if objective is None:
            raise ViprError("OBJ abbreviation is only allowed in constraints")
        return objective
    count = _integer(size)
    if count > n:
        raise ViprError("too many vector entries")
    result = {}
    seen = set()
    for _ in range(count):
        index = _integer(tokens.next())
        if index >= n or index in seen:
            raise ViprError("out-of-range or duplicate vector index")
        seen.add(index)
        value = _rational(tokens.next())
        if value:
            result[index] = value
    return result


def _row(tokens, n, objective):
    label = tokens.next()  # Inference references use row indices, never labels.
    sense = tokens.next()
    if sense not in _SENSE:
        raise ViprError("invalid constraint sense")
    rhs = _rational(tokens.next())
    return _Row(_SENSE[sense], rhs, _vector(tokens, n, objective), label=label)


def _problem(tokens):
    tokens.expect("VER")
    if tokens.next() not in ("1.0", "1.1"):
        raise ViprError("unsupported VIPR version")
    tokens.expect("VAR")
    n = _integer(tokens.next())
    names = [tokens.next() for _ in range(n)]
    if len(set(names)) != n:
        raise ViprError("duplicate variable names")
    tokens.expect("INT")
    count = _integer(tokens.next())
    if count > n:
        raise ViprError("too many integer variables")
    integers = set()
    for _ in range(count):
        index = _integer(tokens.next())
        if index >= n or index in integers:
            raise ViprError("out-of-range or duplicate integer variable index")
        integers.add(index)
    tokens.expect("OBJ")
    sense = tokens.next()
    if sense not in ("min", "max"):
        raise ViprError("invalid objective sense")
    objective = _vector(tokens, n)
    tokens.expect("CON")
    count = _integer(tokens.next())
    bounds = _integer(tokens.next())
    if bounds > count:
        raise ViprError("bound count exceeds constraint count")
    rows = {i: _row(tokens, n, objective) for i in range(count)}
    return n, names, integers, sense, objective, rows


def parse_problem(path):
    """Parse the master section with the exact same grammar as full replay.

    Return the legacy matcher tuple, with standard-library Fraction values.
    Malformed inputs raise ViprError; this function alone does not check a proof.
    """
    with open(path, encoding="ascii") as file:
        _, names, integers, sense, objective, rows = _problem(_HeaderTokens(file))
    def rational(q):
        return Fraction(int(q.numerator), int(q.denominator))
    def vector(coefs):
        return {i: rational(q) for i, q in coefs.items()}
    return (names, integers, sense, vector(objective),
            [(row.label, {1: "G", 0: "E", -1: "L"}[row.sense],
              rational(row.rhs), vector(row.coefficients)) for row in rows.values()])


def _header(file):
    tokens = _HeaderTokens(file)
    n, _, integers, sense, objective, rows = _problem(tokens)
    tokens.expect("RTP")
    relation = tokens.next()
    lower = upper = None
    if relation == "range":
        value = tokens.next()
        lower = None if value == "-inf" else _rational(value)
        value = tokens.next()
        upper = None if value == "inf" else _rational(value)
        if lower is not None and upper is not None and lower > upper:
            raise ViprError("reversed RTP range")
    elif relation != "infeas":
        raise ViprError("invalid RTP relation")
    tokens.expect("SOL")
    solutions = _integer(tokens.next())
    if relation == "infeas" and solutions:
        raise ViprError("infeasibility proof must have empty SOL")
    best = None
    for _ in range(solutions):
        tokens.next()
        values = _vector(tokens, n)
        if any(values.get(i, fmpq(0)).denominator != 1 for i in integers):
            raise ViprError("nonintegral solution")
        if any(not row.satisfied(values) for row in rows.values()):
            raise ViprError("infeasible SOL witness")
        value = sum((a * values.get(i, 0) for i, a in objective.items()), fmpq(0))
        best = value if best is None else min(best, value) if sense == "min" else max(best, value)
    primal = upper if sense == "min" else lower
    if relation == "range" and primal is not None:
        if best is None or (best > primal if sense == "min" else best < primal):
            raise ViprError("SOL does not establish the primal RTP bound")
    tokens.expect("DER")
    derivations = _integer(tokens.next())
    tokens.end()  # DER records must start on the next line.
    return dict(n=n, integers=integers, sense=sense, objective=objective,
                rows=rows, relation=relation, lower=lower, upper=upper,
                solutions=solutions, best=best, derivations=derivations)


def _records(file, count):
    index = 0
    for line in file:
        if not line.strip() or line.lstrip().startswith("%"):
            continue
        if index >= count:
            raise ViprError("trailing data after declared derivations")
        fields = line.split()
        global_claim = fields[-1] == "global"
        if global_claim:
            fields.pop()
        yield index, fields, global_claim
        index += 1
    if index != count:
        raise ViprError("truncated DER section")


def _scan(file, m, count):
    """Compute lifetimes without loading sparse rows or parsing large rationals."""
    last = array("q", [-1]) * m
    declared = array("q", [-1]) * m
    for offset, fields, _ in _records(file, count):
        index = m + offset
        try:
            brace = fields.index("{")
            if brace < 4 or fields[-2] != "}":
                raise ViprError("malformed derivation record")
            reason = fields[brace + 1]
            if reason in ("asm", "sol"):
                if len(fields) != brace + 4:
                    raise ViprError("unexpected inference arguments")
                refs = []
            elif reason in ("lin", "rnd"):
                size = _integer(fields[brace + 2])
                if len(fields) != brace + 5 + 2 * size:
                    raise ViprError("incomplete or malformed linear combination")
                refs = [_integer(fields[j]) for j in range(brace + 3, len(fields) - 2, 2)]
                if len(set(refs)) != len(refs):
                    raise ViprError("duplicate inference reference")
            elif reason == "uns":
                if len(fields) != brace + 8:
                    raise ViprError("malformed unsplit")
                refs = [_integer(value) for value in fields[brace + 2:-2]]
            else:
                raise ViprError(f"unsupported inference: {reason}")
            for ref in refs:
                if ref >= index:
                    raise ViprError("forward or out-of-range inference reference")
                if declared[ref] >= 0 and index > declared[ref]:
                    raise ViprError("reference after declared last use")
                last[ref] = index
            expiry = _integer(fields[-1], -1)
            if expiry >= m + count:
                raise ViprError("last-use annotation outside proof")
            declared.append(expiry)
            last.append(-1)
        except (IndexError, ValueError) as error:
            raise ViprError(f"derivation {index}: {error}") from None
    return last


def _integral_form(row, integers):
    return all(i in integers and a.denominator == 1 for i, a in row.coefficients.items())


def _derive(tokens, row, index, live, header):
    tokens.expect("{")
    reason = tokens.next()
    refs = []
    if reason == "asm":
        row.assumptions = frozenset((index,))
        row.assumption = True
    elif reason == "sol":
        best = header["best"]
        if best is None:
            raise ViprError("sol inference requires a verified feasible solution")
        cutoff = _Row(-1 if header["sense"] == "min" else 1, best, header["objective"])
        if not cutoff.dominates(row):
            raise ViprError("sol inference stronger than verified incumbent cutoff (integer cutoff extension unsupported)")
    elif reason in ("lin", "rnd"):
        count = _integer(tokens.next())
        combined = _Row(0, fmpq(0), {})
        assumptions = set()
        for _ in range(count):
            ref = _integer(tokens.next())
            refs.append(ref)
            coefficient = _rational(tokens.next())
            source = live[ref]
            if not coefficient:
                continue
            sense = source.sense * (1 if coefficient > 0 else -1)
            if sense and combined.sense and sense != combined.sense:
                raise ViprError("unsuitable linear combination")
            if sense:
                combined.sense = sense
            combined.rhs += coefficient * source.rhs
            for variable, value in source.coefficients.items():
                combined.coefficients[variable] = combined.coefficients.get(variable, fmpq(0)) + coefficient * value
            assumptions.update(source.assumptions)
        combined.coefficients = {i: a for i, a in combined.coefficients.items() if a}
        if reason == "rnd":
            if not _integral_form(combined, header["integers"]):
                raise ViprError("rounding requires integer variables with integer coefficients")
            if combined.sense == 0:
                raise ViprError("rounding equality is unsupported")
            combined.rhs = fmpq(combined.rhs.floor() if combined.sense < 0 else combined.rhs.ceil())
        if not combined.dominates(row):
            raise ViprError("linear combination does not dominate claimed row")
        row.assumptions = frozenset(assumptions)
    elif reason == "uns":
        refs = [_integer(tokens.next()) for _ in range(4)]
        c1, a1, c2, a2 = (live[i] for i in refs)
        if not a1.assumption or not a2.assumption:
            raise ViprError("unsplit branch references must name assumptions")
        if not c1.dominates(row) or not c2.dominates(row):
            raise ViprError("unsplit branch does not dominate claimed row")
        low, high = (a1, a2) if a1.sense < 0 else (a2, a1)
        if not (low.sense == -1 and high.sense == 1
                and low.coefficients == high.coefficients
                and low.rhs.denominator == 1 and high.rhs == low.rhs + 1
                and _integral_form(low, header["integers"])):
            raise ViprError("unsplit assumptions do not form an integer disjunction")
        row.assumptions = (c1.assumptions - {refs[1]}) | (c2.assumptions - {refs[3]})
    else:
        raise ViprError("unsupported inference")
    tokens.expect("}")
    _integer(tokens.next(), -1)
    tokens.end()
    return refs, reason


def validate_vipr(path):
    """Return JSON-safe exact proof results; invalid inputs return ``ok=False``.

    The caller must separately establish that this VIPR problem is exactly the
    reconstructed master.  No accepted result here establishes nonlinear
    feasibility of a SOL witness.  File contents must remain stable during
    validation and subsequent problem matching/external checking.
    """
    try:
        with open(path, encoding="ascii") as file:
            header = _header(file)
            start = file.tell()
            live = header.pop("rows")
            m = len(live)
            last = _scan(file, m, header["derivations"])
            file.seek(start)
            live = {i: row for i, row in live.items() if last[i] >= 0}
            peak = len(live)
            dual = header["lower"] if header["sense"] == "min" else header["upper"]
            target = None
            if header["relation"] == "infeas":
                target = _Row(1, fmpq(1), {})
            elif dual is not None:
                target = _Row(1 if header["sense"] == "min" else -1, dual, header["objective"])
            proving_derivation = None
            reasons = {}
            for offset, fields, global_claim in _records(file, header["derivations"]):
                index = m + offset
                try:
                    tokens = _Tokens(fields)
                    row = _row(tokens, header["n"], header["objective"])
                    refs, reason = _derive(tokens, row, index, live, header)
                    if global_claim and row.assumptions:
                        raise ViprError("global marker on a row with undischarged assumptions")
                    reasons[reason] = reasons.get(reason, 0) + 1
                    for ref in set(refs):
                        if last[ref] == index:
                            del live[ref]
                    if last[index] >= 0:
                        live[index] = row
                    peak = max(peak, len(live))
                    if (proving_derivation is None and target is not None
                            and not row.assumptions and row.dominates(target)):
                        proving_derivation = index
                except (ValueError, KeyError) as error:
                    raise ViprError(f"derivation {index}: {error}") from None
            if target is not None and proving_derivation is None:
                raise ViprError("no assumption-free derivation proves RTP (missing proof or undischarged assumptions)")
            return dict(ok=True, relation=header["relation"], sense=header["sense"],
                        lower_bound=None if header["lower"] is None else str(header["lower"]),
                        upper_bound=None if header["upper"] is None else str(header["upper"]),
                        solutions=header["solutions"], derivations=header["derivations"],
                        inferences=reasons, peak_live_rows=peak,
                        proving_derivation=proving_derivation)
    except (OSError, UnicodeError, ValueError, ZeroDivisionError, OverflowError) as error:
        return dict(ok=False, error=str(error))


def check_vipr_output(returncode, stdout, validation):
    """Require successful exit and an exact, complete matching range message.

    The external checker remains an additional check, never the proof authority.
    Both parentheses and square brackets are checked against finite endpoints.
    """
    if not validation.get("ok"):
        return False, "independent VIPR replay failed"
    if returncode != 0:
        return False, f"viprchk exited with status {returncode}"
    if re.search(r"^(?:Verification failed\.|Failed\b|Error\b)", stdout, re.MULTILINE):
        return False, "viprchk output contains a failure diagnostic"
    if validation["relation"] != "range":
        return False, "only finite lower-bound range reports are supported here"
    pattern = re.compile(r"^Successfully verified optimal value range ([\[(])([^,\s]+), ([^\s\])]+)([\])])\.$", re.MULTILINE)
    matches = list(pattern.finditer(stdout))
    if len(matches) != 1:
        return False, "missing or ambiguous complete viprchk success message"
    match = matches[0]
    expected = [validation["lower_bound"], validation["upper_bound"]]
    for i, token in enumerate((match[2], match[3])):
        if expected[i] is None:
            if token != ("-inf" if i == 0 else "inf"):
                return False, "viprchk range differs from exact RTP"
        else:
            try:
                if _rational(token) != _rational(expected[i]):
                    return False, "viprchk range differs from exact RTP"
            except ViprError:
                return False, "malformed viprchk endpoint"
    if match[1] != ("(" if expected[0] is None else "[") or match[4] != (")" if expected[1] is None else "]"):
        return False, "viprchk range brackets do not match endpoints"
    return True, ""
