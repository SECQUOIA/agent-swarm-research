"""Finite-state search for two factor colors avoiding all odd Berge cycles.

This stronger property is sufficient for a balanced factor partition. The
search uses exact two-terminal series/parallel composition, preserving simple
bipartite graphs. It is experimental proof discovery, not a verified theorem.
"""

import argparse
import itertools


def xor_masks(a, b, toggle):
    return sum(1 << value for value in {i ^ j ^ toggle for i in range(2)
               if a & (1 << i) for j in range(2) if b & (1 << j)})


def series(first, second):
    left, middle, direct_a, states_a = first
    middle_b, right, direct_b, states_b = second
    if middle != middle_b:
        return None
    states = set()
    for a, b in itertools.product(states_a, states_b):
        if a[1] != b[0]:
            continue
        paths = [xor_masks(a[c + 2], b[c + 2], middle) for c in range(2)]
        states.add((a[0], b[1], *paths))
    return left, right, False, frozenset(states)


def parallel(first, second):
    left, right, direct_a, states_a = first
    left_b, right_b, direct_b, states_b = second
    if (left, right) != (left_b, right_b) or (direct_a and direct_b):
        return None
    states = set()
    for a, b in itertools.product(states_a, states_b):
        if a[:2] != b[:2]:
            continue
        if any(xor_masks(a[c + 2], b[c + 2], left ^ right) & 2 for c in range(2)):
            continue
        states.add((a[0], a[1], a[2] | b[2], a[3] | b[3]))
    return left, right, direct_a or direct_b, frozenset(states)


def reverse(kind):
    left, right, direct, states = kind
    return right, left, direct, frozenset((s[1], s[0], s[2], s[3]) for s in states)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=10)
    args = parser.parse_args()
    base = (0, 1, True, frozenset({(-1, 0, 2, 0), (-1, 1, 0, 2)}))
    witnesses = {base: "VF", reverse(base): "FV"}
    for iteration in range(args.rounds):
        old = list(witnesses)
        new = {}
        for a, b in itertools.product(old, old):
            for operation, symbol in [(series, "S"), (parallel, "P")]:
                result = operation(a, b)
                if result is None or result in witnesses or result in new:
                    continue
                expression = f"{symbol}({witnesses[a]},{witnesses[b]})"
                if not result[-1]:
                    print("COUNTEREXAMPLE", expression, flush=True)
                    return
                new[result] = expression
        witnesses.update(new)
        print("round", iteration + 1, "types", len(witnesses), "new", len(new), flush=True)
        if not new:
            for kind, expression in witnesses.items():
                print(kind, expression)
            return


if __name__ == "__main__":
    main()
