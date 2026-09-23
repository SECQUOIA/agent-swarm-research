# Exact finite checks of scalar quadratic block messages

Date: 2026-09-22. Status: targeted computational verification of the candidate
construction in [the next-frontier note](research-20260922-next-frontier.md).
These checks support its deterministic elimination identities on nine small
instances. They do not verify the general theorem, the density argument, an
expected running-time bound, or novelty.

The checker is
[check_smoothed_block_dp.py](../code/research_20260922/check_smoothed_block_dp.py).
It uses Python `Fraction` for every support QP and SymPy 1.14.0 for exact sets
defined by univariate quadratic inequalities. It uses no floating-point
sampling, Monte Carlo, or optimization solver. No new dependency was installed.

## Instances and assumptions

The objective is

```
x^T Q x + c^T x + sum_i lambda_i z_i,
x_i(1-z_i)=0, z_i in {0,1}.
```

Every diagonal entry of `Q` is one. Every nonzero off-diagonal entry is
`(-1)^(i+j)/32`. The absolute row sums of off-diagonal entries are at most
`1/4`, and `|c_i|<=1`. Thus the data satisfy the candidate's assumptions with

```
d=D=C=1, rho=1/4, M=C/[2d(1-rho)]=2/3, I=[-2/3,2/3].
```

All support matrices are rational and strictly diagonally dominant. The checker
also asserts positivity of every unpivoted elimination pivot, including those
arising in block Schur complements.

The three graphs are a chain of two triangles on five vertices, three triangles
sharing a central vertex on seven vertices, and a four-cycle on four vertices.
The first two are block graphs with blocks of size three. The four-cycle is a
single biconnected block of size four but is **not** a block graph in the usual
clique-block definition. That case checks the algebra for a possible extension;
it is outside the narrower graph class currently stated in the candidate.

Each graph uses three deterministic penalty choices:

- `lambda_i=c_i^2/4`, which creates exact activation ties in isolated terms;
- those values plus alternating perturbations `+/-1/10^8`;
- a negative penalty `lambda_1=-1/100`, together with a small positive shift at
  the last vertex.

Negative penalties are allowed by the candidate's stated perturbation model;
it imposes no nonnegativity condition on the final perturbed penalties. The
checker does not truncate or replace them.

## What is checked

For each vertex, the procedure constructs active support quadratics, including
the vertex's own diagonal term, linear term, and indicator penalty. Child
block messages exclude those parent terms. The procedure combines child
formulas only where their active regions have a common interval, then retains
each resulting **full polynomial**, not a polynomial restricted to that region.

For a block, it enumerates retained active alternatives and one inactive atom
per child vertex. It performs unconstrained rational Schur elimination of the
active block variables. Every resulting quadratic is compared coefficient by
coefficient with a direct elimination of its complete support in the original
matrix. This check applies to every generated candidate, including candidates
later removed from the envelope.

The direct conditional value for a support is obtained from its principal
matrix `H`, linear term `c`, and coupling vector `r` to the boundary variable:

```
q(t)=own(t)+sum(internal penalties)
     - (1/4)c^T H^-1 c - t r^T H^-1 c - t^2 r^T H^-1 r.
```

The conditional minimizer is affine in `t`. For every enumerated conditional
support, the checker verifies that all its free coordinates lie in `I` at
both endpoints of `I`. Affineness then proves the same bound throughout `I`
for those enumerated supports. At both endpoints, it also checks
`|q'(t)|<=8/3`, the candidate's bound
`C+2DM(1+rho)` for these data.

Every message is independently compared with the enumeration of **all** its
internal supports. For each retained DP quadratic `q`, the checker computes
the exact set

```
I intersect intersection_(all brute support quadratics p) {t:q(t)<=p(t)}.
```

It asserts that the union of these sets is all of `I`. Each retained candidate
is already verified to be a feasible full support. Consequently this coverage
identity establishes equality of the two envelopes everywhere on `I`, including
irrational crossings and isolated ties. It is stronger than comparing values
on a finite grid. The quadratic inequality routine has explicit checks for
constant, linear, repeated-root, no-root, and two-root cases.

At each vertex, the inactive atom is computed as
`min_q q(0)-lambda_u`. Its value and stored descendant support are checked
against direct brute-force enumeration with that vertex inactive. In particular,
the subtraction is checked when `lambda_u` is negative.

At the root, the active quadratic minima and inactive atom are compared with
complete support enumeration of the original unconstrained problem. The active
quadratic minimizers are also checked to lie in `I`.

## Results and limits

Targeted command actually run:

```
python code/research_20260922/check_smoothed_block_dp.py
```

Final output:

```
PASS {'instances': 9, 'messages': 66, 'support_qps': 892,
      'endpoint_bounds': 3580, 'derivative_bounds': 864, 'atoms': 48,
      'candidates': 100, 'outside_active_region': 32}
```

The support-QP count includes repeated support solves used for separate
certificates; it is not a count of distinct supports. The endpoint and derivative
counts are exact scalar assertions. In 32 candidate evaluations, a child's
conditional minimizer lay outside the region where its retained quadratic is
active on the child's envelope. Those candidate polynomials still agreed with
direct full-support elimination. This exercises the intended use of retained
full quadratics beyond their active regions.

The checker deliberately uses brute-force support enumeration and pairwise
quadratic inequality intersections. At vertices it finds simultaneous active
combinations by exact interval intersections. It does **not** implement the
proposed efficient envelope merge and therefore provides no evidence for its
running-time bound. All penalties are deterministic rational numbers, so these
checks provide no evidence for a probability or density claim. There was no
Lean verification, project-wide verification, or CI inspection.
