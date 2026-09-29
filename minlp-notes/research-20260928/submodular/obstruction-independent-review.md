# Independent adversarial review of the two obstruction notes

Date: 2026-09-28. Reviewer: `near_submod_prior`, independent of the authors
of the reviewed examples. Scope: the saved
[one-edge note](one-edge-obstructions.md), its exact checker, the
[PSD-center note](psd-center-obstruction.md), and both PSD certificates.

No substantive mathematical defect was found in the reviewed statements.
The conclusions are negative boundaries for particular proposed methods,
not complexity classifications or a substantial original main contribution.
The review corrected one ambiguous sentence in the one-edge note: only its
**unperturbed** example is sign-switchable. The perturbed example is not.

## One-positive-edge obstructions

The original four-variable matrix is positive definite by the stated Schur
complement. The perturbed matrix with \(Q_{34}=Q_{43}=-1/10\) is positive
definite by the displayed sum of squares: its positive leaf-square term
forces both leaves to zero at any zero of the sum, after which the other
squares force both endpoints to zero. Its one positive edge has a negative
path between its endpoints, so diagonal sign switching cannot remove the
positive edge while preserving all negative signs.

The conditional support calculations are correct. Fixing both endpoint
indicators leaves a strict violation of the support submodular inequality
for each matrix. This rebuts the proposed reduction in the existing support
coordinates. It does not exclude another lifting, a different support
encoding, or a polynomial optimization method.

For the perturbed example, the endpoint-inactive lower bound is valid:
drop box and nonnegativity restrictions as well as the nonnegative activation
penalties, then use the positive definite three-coordinate quadratic.
Its Schur coefficient is \(2-2/(4-\eta^2)\), yielding

\[
-\frac9{2-2/(4-\eta^2)}=-\frac{3591}{598}
> -\frac{1428}{235}>-\frac{123}{20}.
\]

Thus endpoint-inactive supports cannot defeat either claimed global value.
When both endpoints are present, strict convexity on each support and the
four conditional values prove that exactly the two singleton-leaf continuous
solutions are globally optimal. Both have all coordinates in \([0,2]\).

At ratios \(1/2\) and \(2\), the added square vanishes at one of these
global solutions, so majorization gives equality of the surrogate optimum
with the original optimum. At ratio 1, the respective surrogate values are
\(-6\) and \(-1428/235\). These are strictly greater than
\(-123/20\), which proves failure of quasiconvexity and of single-valley
unimodality. A nonunimodal scalar function may still admit exact polynomial
optimization by a different argument; no contrary implication is justified.

I checked the inherited support-face oracle's implementation and ran the
updated exact checker. Independently, I enumerated all 81 combinations of
inactive, free, and upper-bound coordinates directly on the finite box,
solved each free-coordinate stationarity system in SymPy rational
arithmetic, and checked relevant upper-bound KKT conditions. This independent
calculation did not call the inherited oracle. For both matrices it returned

\[
\min F=-123/20,\qquad
\operatorname*{argmin}_x F=
\{(3/2,3/4,3/4,0),(3/4,3/2,0,3/4)\},
\]

and it reproduced all six reported scalar-envelope values. Since activation
costs are nonnegative, a zero coordinate can always be treated as inactive;
this justifies that finite-box enumeration without separate active-zero
indicator states.

## PSD-center obstruction derived from prior work

The modification of Burer–Natarajan–Willemsen's Example 4 is correct.
I inspected the local primary PDF, pages 14 and 43–44, for the original
matrix and explicit rational witness. The added endpoint terms
\(8x_i(1-x_i)\) are nonnegative on the unit box, and the added center
squares are nonnegative everywhere. The resulting center block has exact
eigenvalues \(1/16\) and \(801/16\), while its two endpoints have zero
diagonal coefficients.

For an independent proof of the true minimum, I optimized the two-dimensional
convex center problem at each binary endpoint choice. With endpoints
\((x_1,x_4)\), the exact results are:

| Endpoints | Center minimizer \((x_2,x_3)\) | Minimum |
| --- | --- | --- |
| \((0,0)\) | \((0,0)\) | \(0\) |
| \((0,1)\) | \((0,224/401)\) | \(72/401\) |
| \((1,0)\) | \((0,0)\) | \(20\) |
| \((1,1)\) | \((392/401,1)\) | \(7137/6416\) |

These values were obtained by exact active-face stationarity and KKT checks.
The objective is separately affine in the two endpoint variables, so some
minimum over the entire box has binary endpoints. The table therefore proves
that the true minimum is zero without relying on the old example's global
nonnegativity proof.

I independently entered the prior paper's explicit \((\mu,X)\) using exact
fractions. All five leading principal minors of the moment matrix are
positive; all full RLT inequalities hold. The old objective value is
\(-109/1024\), the endpoint modifications have zero relaxed value, and
the modified value is exactly

\[
-109/1024+(125/1024+231/512)/16=-1157/16384<0.
\]

This proves the stated full-SDP–RLT gap. The note correctly distinguishes
positive definiteness of the center block from convexity of the whole
quadratic. Its conclusion also correctly leaves the stable-positive theorem
intact, because the two positive-diagonal vertices in the example are
adjacent. No preservation of the gap after adding triangle inequalities is
claimed or established for this modification.

The novelty assessment is appropriate: the main phenomenon and rational
witness are inherited from prior work. The modification is a useful structural
specialization, not a new general SDP-gap theorem.

## Additional rational PSD certificate

I verified the JSON certificate directly, without loading the numerical
discovery file or using the certificate-generating script. The matrix is
symmetric, its moment matrix has five positive leading principal minors,
all full RLT inequalities hold, and the binary-coordinate diagonal equalities
hold. Its exact objective is

\[
-704315984787773/202950000000000000<0.
\]

Independent rational KKT minimization gives the following shifted values:

| Binary leaves | Center minimizer | Minimum |
| --- | --- | --- |
| \((0,0)\) | \((0,1/12)\) | \(0\) |
| \((0,1)\) | \((1/82,38/41)\) | \(0\) |
| \((1,0)\) | \((0,1/12)\) | \(2547/1804\) |
| \((1,1)\) | \((4/11,1)\) | \(0\) |

Negative leaf diagonal coefficients justify binary endpoint minimization
by coordinatewise concavity. Thus this is a valid independent instance of
the same obstruction. It adds no stronger structural conclusion than the
short prior-derived example.

## Significance and verification limits

The one-edge examples remove two attractive shortcuts: indicator branching
alone and a unimodal ratio-envelope search. The PSD examples remove a natural
positive-definite-center extension of the local exactness theorem. These
findings save effort and make future conjectures more precise. They establish
neither exact near-Stieltjes tractability nor hardness, and they do not provide
a stronger useful relaxation or demonstrated solver capability. No flagship
result has emerged from these examples.

Targeted saved commands run in this review:

```text
python research-20260928/submodular/check_one_edge_obstructions.py
python research-20260928/submodular/check_psd_center_obstruction.py
python research-20260928/submodular/check_psd_center_prior_obstruction.py
```

All passed. Three additional `python` heredocs performed the independent
finite-box enumeration, JSON-certificate check, and prior-witness/endpoint
check described above. They used exact SymPy rational arithmetic and passed.
For source inspection I used `pdftotext -f 13 -l 14 -layout` and
`pdftotext -f 43 -l 45 -layout` on the local primary PDF. An initial attempt
to read it with Python `fitz` failed because that module was unavailable;
this did not affect the verification, and `pdftotext` succeeded.

The exact computations establish the displayed finite examples and their
arithmetic. The universal inferences follow from majorization, KKT
sufficiency for the convex fibers, and endpoint reduction. They do not
establish novelty, a general algorithm, or computational hardness. No Lean
proof, project-wide verification, or CI inspection was performed.
