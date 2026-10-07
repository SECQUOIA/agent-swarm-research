# Stage 3, round 1: independent review 1

**Findings: 0 major issues; 0 minor issues.** I found no mathematical or
oracle-model repair required in the frozen Stage 3 section.

I read `sections/06-lp-application.tex` in full, its integration in `main.tex`,
the bibliography additions, `audit/stage3-author.md`, and the complete
`2026-09-04-sparse-lp-newton-access-separation.md` source note. I did not read
peer reviews and did not edit the manuscript. The earlier stages' established
theorems are used here under their stated hypotheses; introduction and final
literature packaging are outside this review's scope.

## LP and Newton system

The construction in `eq:lp-family` has the asserted orthonormal bases, rank,
norms, condition number, and constant row and column degrees. The feasible
affine line is exactly `1 + lambda*q_0`. Orthogonality to the strictly positive
`q_+` forces both signs in `q_0`, so its nonnegative portion is a nontrivial
compact segment. The strictly positive sum `1^T*q_0=cos(theta)/sqrt(3)` proves
the objective is nonconstant.

Proposition `prop:lp-center` uses a consistent dual sign convention. Eliminating
the linearized primal, dual, and complementarity equations gives
`H_t*Delta y=A_t*1`, with the displayed right side and dual direction. The
additional statement that the primal direction is
`-(cos(theta)/sqrt(3))*q_0` follows by subtracting the projection of `1` onto
the row space from `1`, with the stated sign. It is independent of `t`.
Explicitly identifying this fact prevents the dual-state lower bound from
being mistaken for a lower bound on solving the LP itself.

## Full input contracts and hybrid lower bounds

The normal oracle is a full unitary with the prescribed compressed block.
The rectangular oracle is a valid Halmos completion: its two singular-vector
blocks are unitary and its column null vector has eigenvalue `-1`. The public
identity padding cannot reveal the parameter. The right-side oracle is also
fully specified, including the action orthogonal to its prepared state.

The contract explicitly withholds classical information about `t` and hidden
coefficients. In particular, the exact right-side norm would allow the
reconstruction

    t = ((norm(b_t)/a)^2 - 1)/delta,

so its exclusion is necessary and correctly stated. Supplying the normalized
preparation unitary does not silently supply this norm. All calls to that
unitary, its inverse, and controlled versions are counted.

The target endpoint overlap and trace distance in `eq:lp-target` are correct.
The fixed-error condition leaves endpoint outputs separated by more than
`d_rho/2`. The complete endpoint oracle differences have the stated orders:
`O(delta)` for the normal matrix, `O(sqrt(delta))` for the factor, and
`O(delta)` for the right side. The factor bound is valid because
`sqrt(rho*delta)<1/2` under the section's assumptions. The inverse and
controlled-query bounds are preserved, and a coherent selection among query
types also has its norm difference bounded by the largest branch difference.

Purification, bounded-query measurement deferral, and the hybrid argument
therefore apply to the entire state algorithm. Trace-distance contraction
under discarded registers is used in the correct direction. The lower bounds
continue to hold when the algorithm queries the right-side oracle; they are
not bounds for an artificially RHS-free state model.

## Matching state upper bounds

The two amplitude-estimation experiments have probabilities `t^2` and `t`,
respectively. In the normal model, division by `t>=delta` after taking the
square root of the probability estimate gives the displayed error bound at
`M=O(1/delta)`. In the factor model, the direct probability estimate has error
`O(delta)` at `M=O(1/sqrt(delta))`. Clipping cannot increase either parameter
error, and a median of a fixed number of repetitions gives the required
failure probability for fixed output error.

The derivative

    |d arctan(sqrt(delta/t))/dt| = sqrt(delta)/(2*sqrt(t)*(t+delta))

is at most `1/(4*delta)` on the interval. Consequently, successful estimation
gives the asserted state error, and convexity bounds the unconditional mixed
output error including failures. The proof does not condition its output
contract on successful estimation. The algorithm is permitted to measure and
discard the estimate because this is a state task. Its rotations depend on
the estimate and public data, with no uncounted input oracle.

The supplementary pseudoinverse identity and squared support overlap
`(8/9)*(1+delta)` are correct. The proof does not rely on a generic rectangular
solver bound that omits its overlap cost.

## Compiler transfer and factor bypass

The compiler contract in `eq:lp-staircase` is deliberately matrix-only. This
distinction is sufficient and necessary for the particular trigonometric
degree reduction stated in its proof; no unproved compiler lower bound with
extra RHS access is claimed.

Replacing the varying normal-oracle block by the periodic sine/cosine family
leaves a unitary oracle for every real angle and agrees with the supplied
oracle on the principal promised interval. Every converter entry remains a
bounded trigonometric polynomial of the required degree even if gates mix
the public eigenspaces. The designated diagonal entry therefore meets the
scalar hypotheses of the fixed and joint lower bounds. This is stronger and
more precise than merely asserting an invariant-eigenspace reduction for
arbitrary circuits.

The earlier upper constructions apply with singleton high band `c=1`.
The conversion from `K=eta/delta` to logarithms of absolute accuracy is valid
throughout `eta<=delta^(1+beta)`. The equivalence with the condition number
is uniform over the family up to the explicitly allowed `rho` constants.

The zero-query coarse tier is correct: its proposed public contraction has
uniform error exactly `G_0*delta`. The model has public spectral projectors,
so the general model's nonzero constant lower bound does not transfer. The
section clearly explains both this correction and the absence of a
positive-width high spectral interval.

The two-query factor construction is valid on the row output space. The
independent identity

    J_R^* U_A (I-Pi_C) U_A^* J_R = I_R - A_t*A_t^T

directly verifies the block, normalization, and query count. A free dilation
of the public projector supplies an actual coherent circuit. The column null
vector does not add an unintended eigenvalue to the row output. No state
estimation and re-preparation argument is used as a substitute for reusable
coherent compilation.

## Scope and source coverage

The digital-entry formulas recover `t` from one exact value and support the
stated fixed-error bypass at sufficiently high digital precision. The normal
matrix is indeed strictly diagonally dominant. The one-controlled-query LCU
construction encodes `(I-H_t)/2`, so it does not satisfy the unit-normalized
contract by itself.

The section preserves the source note's actual LP realization and both access
comparisons, improves the factor-state upper bound to a sharp fixed-error
order, and repairs the source's unqualified transfer of the coarse compiler
tier. Its final scope statement accurately excludes unconditional sparse-input,
LP-solver, and end-to-end QIPM lower-bound interpretations. Public knowledge
of the primal direction is disclosed rather than obscured.

## References and numerical validation

I directly checked the estimate and success probability in [Brassard–Høyer–
Mosca–Tapp, Theorem
12](https://userpages.cs.umbc.edu/lomonaco/ams/specialpapers/brassard/Brassard.pdf).
They support the upper-bound proof, with `O(M)` preparation/inverse calls.
The cited discussions in [Orsucci–Dunjko, Sections 4.3 and
5.4–5.5](https://elib.dlr.de/145449/1/q-2021-11-08-573.pdf) support the
normalization requirement, the digital diagonally-dominant construction,
and the importance of the support overlap in factor-based methods. These
tools are attributed as prior work. The QSVT citation was checked in Stage 1;
the projector identity here also verifies the claimed implementation without
relying on an implicit left-versus-right convention.

A fresh diagnostic using
`/workspace/local-home/miniconda3/envs/qipm/bin/python` checked 24 endpoint instances
with `rho` in `{1.1,2,10,100}` and `delta` equal to `{1e-2,1e-4,1e-6}/rho`.
Checks included basis orthogonality, normal-matrix factorization, the Newton
equation, primal-direction feasibility and parameter independence, both full
oracle unitarities, the projector-compression formula, and the right-side norm.
The largest residual was `1.373e-15`. All 12 endpoint target-distance checks
and the corresponding three-oracle perturbation inequalities passed. These
are supplemental numerical checks, not proof certificates.
