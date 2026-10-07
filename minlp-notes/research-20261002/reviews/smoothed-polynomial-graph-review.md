# Review of the polynomial graph-constraint corollary

Date: 2026-10-02. Disposition: approved within the stated parameterization
model; no blocking issue found. This is an independent actual-file
mathematical review, not external peer review or a novelty assessment.

Reviewed [the completed graph-constraint note](../new-direction/smoothed-polynomial-graph-constraints.md),
its [targeted checker](../new-direction/check_polynomial_graph_constraints.py),
and the relevant interfaces in the
[sparse polynomial box theorem](../new-direction/smoothed-sparse-polynomial.md),
[finite-noise tails](../new-direction/polynomial-finite-noise-tails.md), and
[constructive exact fallback](../new-direction/polynomial-exact-fallback-construction.md).

## 1. Substitution and the expanded decomposition

With degree bounds \(d,e\ge1\) and graph depth \(D\), a dependent
coordinate has degree at most \(E=e^D\) and at most
\(a=\max\{1,k^D\}\) free ancestors. Objective factors have composed
degree at most \(dE\); the auxiliary-noise terms have degree at most
\(E\le dE\). Bounded depth prevents iterated polynomial composition from
creating unbounded degree. Explicit substitution has polynomial bit work
for fixed \(d,e,D\), even when the parent bound \(k\) is part of the input.
Coefficient arithmetic and the number of fixed-degree monomials remain
polynomial in that input.

The ancestor-expanded tree decomposition is valid. For a fixed free
coordinate, take its original occurrence subtree and the occurrence
subtrees of all dependent descendants. Every dependency edge has both
endpoints in an equality bag, so consecutive subtrees on an ancestral
path intersect. Their union is connected. This proves running intersection,
not merely factor-scope containment. Each expanded bag contains at most
\(ap\) free coordinates. Keeping symbolic ancestors despite cancellation
is conservative and preserves the argument.

An objective-only decomposition would not justify this reasoning. The note
correctly requires all equality scopes to be covered. It also correctly
forbids additional restrictions on outputs unless they are redundant:
arbitrary output bounds could cut the free product domain.

## 2. A single noise law before sampling

Conditioning on all auxiliary coefficients leaves the retained free
coefficients independent and uniform on their original grid. The pullback
\(G_\eta\) is then a fixed polynomial on an unchanged product domain.
The common curvature premise applies to every conditioned polynomial.
Consequently both the rounding argument and coordinate semiconcavity
argument retain their hypotheses.

The order of selecting constants avoids a sampling-precision circle. The
section-count constant depends on degree, dimension, and domain formula
size, not polynomial coefficient values or heights. The active-gradient
root count is also uniform in the auxiliary coefficients. The fallback's
algebraic dimensions depend on the composed degree and base input; new
coefficient bits enter only polynomially. Although the referenced fallback
is stated for added linear coefficients, its construction bounds arbitrary
coefficients through their heights, so it applies to the affine family of
composed coefficients here.

Uniform derivative bounds and the base fallback budget can therefore be
chosen first. The displayed thresholds, cutoff, and common power-of-two
grid size then follow before either coefficient vector is drawn.
Conditional fallback probability is at most \(1/(2B)\), and averaging
over the auxiliary draw preserves the expected-work bound. No resampling
or conditioning on successful closure is used.

## 3. Exact output and evaluation

The map \(\Phi(t)=(t,\Psi(t))\) is globally injective because it retains
all free coordinates. Adding its defining equations to the unique free
patch optimizer specifies exactly one feasible ambient point. The reduced
Hessian certificate supplies uniqueness on the patch; a positive ambient
Hessian is unnecessary. The triangular equality Jacobian also justifies
the stated reverse-substitution multiplier and chain-rule interpretation.

The usual output is implicit. Applying a fixed-degree polynomial map to
the free-coordinate evaluator costs polynomial work at requested precision,
with polynomially many extra precision bits for derivative magnitudes.
The fallback output can likewise retain polynomial expressions in its
selected algebraic coordinates. No expansion of all output minimal
polynomials is required. This distinction is necessary and is present in
the note.

## 4. Examples and scope

The connected product graph example has the asserted path decomposition
after substitution. Its pure second derivative receives at most two terms
of size two from adjacent squared products, plus \(2\lambda\).
Neither the targets nor auxiliary bilinear perturbations increase that
bound. Hence \(L'=4+2\lambda\) is valid.

The unanchored linear-map example correctly defeats the unchanged
conditional-noise argument: the event \(c_2=3\sigma\) forces both original
coefficients to their upper endpoints and makes \(c_1\) deterministic.
The event has positive probability under every stated finite grid.
This does not establish hardness for that parallelogram.

The curvature example also checks out. An ambient mixed derivative \(H\)
becomes part of the pullback's pure second derivative \(2H+4\varepsilon\),
although the ambient diagonal bounds are only \(2\varepsilon\).
A uniformly bounded inverse therefore does not justify reusing the ambient
coordinate-curvature parameter.

The result is a global parameterization corollary of the box theorem.
It is an expected polynomial bound at fixed expanded bag size and suitable
numerical width/noise bounds, not an FPT bound in bag size, a theorem for
general coupled constraints, or a guarantee for arbitrary inverse charts.
The note states these limitations clearly.

## 5. Correction and targeted verification

The initial draft did not explicitly require \(d,e\ge1\). I requested
that convention because a degree-zero objective could otherwise make
\(dE\) fail to bound the auxiliary polynomial noise terms. The author
added it. Constant actual factors and maps are still allowed under these
positive upper bounds. No other correction was requested.

The command actually run was

```text
python3 research-20261002/new-direction/check_polynomial_graph_constraints.py
```

It passed 1,125 exact coupled quartic rounding/curvature cases, the
overlapping depth-two decomposition fixture, and the finite-noise and
curvature obstruction fixtures. I read the checker as well as running it.
These finite diagnostics support the identities; the all-input guarantees
come from the proofs and inherited theorem interfaces.

A separate inline `python3` check of the reviewed note passed local-link,
trailing-whitespace, paired-math-delimiter, and sequential-equation-tag
checks, plus 12 exact conditional-noise examples and six pullback-curvature
identities. No project-wide verification, CI inspection, or external
literature search was run.
