"""Regenerate explicit Lean switching-chamber witnesses.

This program selects words with a Python dynamic program. It is not trusted:
every output word is checked by Lean's kernel against the stated prefix and
switch bounds. Run from any directory; --output permits a comparison build.
"""

import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "formal/Formal/SwitchingControl/Certificates.lean"
CHECKER = ROOT / "paper-switching-control/verification/stage04/check_floor_chambers.py"
MARKER = "-- BEGIN GENERATED CERTIFICATES"

spec = importlib.util.spec_from_file_location("floor_checker", CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def ordered_transitions(sigma):
    """Use the argument order of Lean's covered_one and covered_two lemmas."""
    if sigma == 1:
        return [(1, (1, 0, 0)), (1, (0, 1, 0)), (1, (0, 0, 1)), (2, (0, 0, 0))]
    return [
        (1, (0, 1, 1)), (1, (1, 0, 1)), (1, (1, 1, 0)),
        (2, (1, 0, 0)), (2, (0, 1, 0)), (2, (0, 0, 1)),
    ]


class Node:
    """A chamber prefix, with a cheapest word for each final node and mode."""

    def __init__(self, sigma, paths, remaining):
        self.sigma = sigma
        self.remaining = remaining
        self.children = []
        if remaining == 0:
            self.word = min(paths.values(), key=checker.switches)
            return
        for next_sigma, delta in ordered_transitions(sigma):
            next_paths = {}
            for start, finish, letter in checker.edges(sigma, next_sigma, delta):
                for (node, _last_letter), word in paths.items():
                    if node != start:
                        continue
                    candidate = word + (letter,)
                    key = finish, letter
                    if key not in next_paths or checker.switches(candidate) < checker.switches(next_paths[key]):
                        next_paths[key] = candidate
            self.children.append(Node(next_sigma, next_paths, remaining - 1))


def proof(node, budget, allow_exception, indent=2):
    """Emit a proof tree ending in explicit words and kernel decision proofs."""
    pad = " " * indent
    if node.remaining == 0:
        if checker.switches(node.word) > budget:
            if not allow_exception:
                raise ValueError("A chamber has no word within the requested budget")
            return pad + "apply covered_leaf\n" + pad + "exact Or.inr (by decide +kernel)\n"
        prefix = "Or.inl " if allow_exception else ""
        word = "[" + ",".join(map(str, node.word)) + "]"
        return pad + "apply covered_leaf\n" + pad + "exact " + prefix + "⟨" + word + ", by decide +kernel⟩\n"
    constructor = "one" if node.sigma == 1 else "two"
    result = pad + "apply covered_" + constructor + "\n"
    for child in node.children:
        result += pad + "· " + proof(child, budget, allow_exception, indent + 2).lstrip()
    return result


def generate():
    result = "import Formal.SwitchingControl.Finite\n\nnamespace SwitchingControl.Finite\n\n"
    result += (
        MARKER + "\n"
        "-- The words below are witnesses. Each prefix count and switch bound is checked by the kernel.\n"
    )
    for cells, budget, name in [(5, 2, "five"), (6, 3, "six"), (7, 3, "seven")]:
        root = Node(1, {(i, i): (i,) for i in range(3)}, cells - 1)
        if cells == 7:
            predicate = f"(fun h => Solvable {budget} h ∨ h ∈ exceptional)"
            conclusion = f"Solvable {budget} h ∨ h ∈ exceptional"
        else:
            predicate = f"(Solvable {budget})"
            conclusion = f"Solvable {budget} h"
        result += "set_option maxRecDepth 100000 in\nset_option maxHeartbeats 0 in\n-- Exhaustive kernel checks for all chamber witnesses exceed the default heartbeat budget.\n"
        result += f"theorem {name}_cover : ∀ h ∈ histories {cells}, {conclusion} := by\n"
        result += f"  change Covered {predicate} {cells - 1} false [zero]\n"
        result += proof(root, budget, cells == 7)
    return result + "\nend SwitchingControl.Finite\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=SOURCE)
    args = parser.parse_args()
    args.output.write_text(generate())
