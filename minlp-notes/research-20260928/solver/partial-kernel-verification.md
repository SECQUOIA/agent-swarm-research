# Targeted verification of partial kernel rounding

Date: 2026-09-28. Main statement:
[partial-kernel-rounding.md](partial-kernel-rounding.md).

The following targeted command was run successfully:

```text
python research-20260928/solver/check_partial_kernel.py
```

Its output was:

```text
PASS: {'conditional_matrix_checks': 51, 'objective_identity_checks': 3, 'zero_density_checks': 2, 'counterexample_checks': 4}
```

The script uses exact SymPy rational arithmetic. For kernel parameters
`m=2,3,4`, it constructs a one-dimensional shared matrix moment functional
with four supported shared states and a private two-dimensional triangular
polytope. The private moment matrices deliberately include moments that
cannot come from a measure on that polytope: one has `E(y_1²)=1` and
`E(y_1)=1/2`, contradicting `0<=y_1<=1`. Thus the construction tests
conditional-mean recovery without assuming private representing measures.

At 17 rational target coordinates for each kernel, the script checks all
principal minors of the conditional matrix, membership of the recovered
mean in the triangle, inherited second-moment bounds, and the Jensen
inequality for a polynomial positive-definite private quadratic block. It
also exactly integrates the smoothed polynomial matrix objective under
arcsine measure and compares it with the damped Chebyshev-moment formula
and the theorem's coefficient error bound. Two exact zero-density cases
exercise the kernel's vanishing behavior.

The negative tests show that affine private inequalities alone permit
arbitrarily large private second moments. They also verify the explicit
nonconvex counterexample in the main note, in which a feasible degree-two
private moment matrix has objective `-4` for a problem with true minimum
`-1` and no shared coordinates.

These checks verify finite examples and algebraic identities. They do not
prove the general interval-positivity representation, all-order degree
bounds, general matrix moment inequalities, junction-tree gluing, or the
main theorem. The paper proof and independent adversarial reviews address
those parts. No Lean formalization was performed. No project-wide checks
were run and no CI status or logs were inspected.
