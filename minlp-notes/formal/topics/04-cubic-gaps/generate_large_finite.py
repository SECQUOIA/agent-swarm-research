#!/usr/bin/env python3
"""Emit the exhaustive Lean count certificate for the 192-variable example.

This generator supplies no trusted arithmetic answers. Each emitted proposition
is checked by Lean's kernel decision procedure.
"""
from pathlib import Path
import argparse

HEADER = '''import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Fintype.Fin
import Mathlib.Tactic.FinCases

namespace CubicGap

/-- Integer count polynomial for the 192-variable cubic example. -/
def largeValue (a b c : ℕ) : ℤ :=
  2 * (c.choose 3 : ℤ) + 3 * (b : ℤ) * (c.choose 2 : ℤ) +
    120 * (b.choose 2 : ℤ) + 105 * (a : ℤ) * c +
    70 * (a : ℤ) * b + 63 * (a.choose 2 : ℤ)

'''

def generate():
    parts = [HEADER]
    for c in range(65):
        parts.append(f'''set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- This finite certificate checks all 65² count pairs at this fixed third count.
theorem large_minorant_c{c} : ∀ a b : Fin 65,
    105 * largeValue a b {c} ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * {c} - 51743768 := by
  simp only [largeValue, Nat.choose_two_right]
  decide +kernel

''')
    parts.append('''/-- The proposed affine function minorizes the cubic count polynomial at every
vertex count triple in the 192-variable example. -/
theorem large_minorant (a b c : Fin 65) :
    105 * largeValue a b c ≥
      871710 * (a : ℤ) + 900446 * (b : ℤ) + 899046 * (c : ℤ) - 51743768 := by
  fin_cases c
''')
    for c in range(65):
        parts.append(f'  · exact large_minorant_c{c} a b\n')
    parts.append('\nend CubicGap\n')
    return ''.join(parts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = generate()
    if args.check:
        target = Path(__file__).resolve().parents[2] / 'Formal/CubicGap/LargeFinite.lean'
        if target.read_text() != expected:
            raise SystemExit(f'FAIL: generated certificate differs from {target}')
        print('PASS: CubicGap/LargeFinite.lean matches its generator')
    elif args.output is not None:
        args.output.write_text(expected)
    else:
        parser.error('use --output PATH or --check')
