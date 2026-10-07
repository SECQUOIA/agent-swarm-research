"""Bind saved native-model metadata to a separately supplied original model.

No saved expression string is parsed or evaluated. Logical domain requirements
are reconstructed from original raw trees after replaying the original affine
bound proof. The reviewed domain walker and native builder are shared trusted
primitives; this is not a second implementation of SCIP or a presolve proof.
"""
from fractions import Fraction
import math

import sympy as sp

from solver.bounds import replay_bounds
from solver.model import build_model, expression, source_domains


def _plain(value):
    """Normalize only JSON's list/tuple distinction; never interpret strings."""
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    return value


def _bound(text):
    if text == "inf":
        return math.inf
    if text == "-inf":
        return -math.inf
    return Fraction(text)


def replay_model_metadata(original, metadata):
    """Return whether metadata binds to the independently decoded original.

    ``original`` uses the ``Instance`` attribute contract. The call reconstructs
    a native model, without solving it, to check the complete deterministic
    metadata and native variable naming. The guard equations are additionally
    derived here from the source-domain projection identities, so their saved
    equations, sides, and witness bounds are not taken as premises.
    """
    rebuilt = None
    try:
        if not isinstance(metadata, dict):
            return False
        if metadata["schema"] != "source-model-v2":
            return False
        if metadata["binding_boundary"] != "submitted PySCIPOpt expression DAG":
            return False
        certificate = metadata["bound_certificate"]
        if not replay_bounds(original, certificate):
            return False
        if certificate["result"]["infeasible"]:
            return False
        bounds = tuple(zip(map(_bound, certificate["result"]["lower"]),
                           map(_bound, certificate["result"]["upper"])))
        if len(bounds) != len(original.var_lb):
            return False
        symbols = tuple(sp.Symbol(f"x{i}", real=True) for i in range(len(bounds)))
        requirements = []
        for index, row in enumerate(original.rows):
            requirements.extend(source_domains(row["nl"], bounds, symbols,
                                               original, row_index=index))
        if metadata["domain_requirements"] != len(requirements):
            return False
        if metadata["proved_domain_requirements"] != sum(r["proved"] for r in requirements):
            return False
        if metadata["source_variables"] != [f"v{i}" for i in range(len(bounds))]:
            return False

        # This reconstruction binds full original rows and native names too.
        # It does not trust a model embedded in the saved metadata.
        rebuilt = build_model(original)
        infinity = float(rebuilt.model.infinity())
        expected_guards, seen = [], set()
        for requirement in requirements:
            if requirement["proved"]:
                continue
            argument = expression(requirement["argument"], symbols)
            kind = requirement["kind"]
            key = kind, sp.srepr(argument)
            if key in seen:
                continue
            seen.add(key)
            index = len(expected_guards)
            witness = None if kind == "nonnegative" else f"source_domain_witness_{index}"
            equation = argument if witness is None else argument*sp.Symbol(witness, real=True)
            expected_guards.append({
                "kind": kind, "row": requirement["row"], "path": list(requirement["path"]),
                "witness": witness, "argument": sp.srepr(argument),
                "constraint": f"source_domain_{index}",
                "submitted_expression": sp.srepr(equation),
                "submitted_lhs": 0.0 if witness is None else 1.0,
                "submitted_rhs": None if witness is None else 1.0,
                "stored_lhs": 0.0 if witness is None else 1.0,
                "stored_rhs": infinity if witness is None else 1.0,
                "witness_bounds": (None if witness is None else
                                   [0.0 if kind == "positive" else -infinity, infinity]),
                "scip_infinity": infinity,
            })
        if _plain(metadata["domain_guards"]) != expected_guards:
            return False
        return _plain(metadata) == _plain(rebuilt.metadata)
    except (AttributeError, IndexError, KeyError, OverflowError, RecursionError,
            TypeError, ValueError, ZeroDivisionError, NotImplementedError):
        return False
    finally:
        if rebuilt is not None:
            rebuilt.model.freeProb()
