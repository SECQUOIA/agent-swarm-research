# Completed research at the requested stopping point

Date: 2026-10-02. The user requested completion of the current ideas and
extensions, followed by a stop. This record distinguishes completed
theorems from the remaining open questions. Research is paused; no new
direction is authorized by this closeout.

## Strongest completed point-output results

For fixed degree, the [globally convex polynomial theorem](new-direction/globally-convex-polynomial-point-oracle.md)
gives deterministic polynomial-bit approximation of a fixed minimum-norm
optimizer on a bounded rational polytope. The objective must be convex on
all of Euclidean space, with convexity promised or its verification charged.
No strong-convexity modulus or unique optimum is required. Its constructive
error bound is

```
dist(x,argmin_P f) <= Gamma (f(x)-min_P f)^(1/D),
log Gamma = poly_D(I).
```

Global convexity, polynomial interpolation and rational gradient samples
identify an affine slice containing precisely the optimal set. A rational
Hoffman bound makes the distance constant effective. Ordinary convex value
optimization then needs only polynomially many accuracy bits to return a
feasible rational point within `2^-q` of the fixed optimizer. Two independent
actual-file reviews and a separate root derivation passed.

The [cubic polytope theorem](new-direction/convex-cubic-polytope-point-oracle.md)
requires convexity only on the supplied polytope. Affinity of the cubic
Hessian gives a different proof and a polynomial-bit fourth-root error
constant. It also gives a deterministic minimum-norm optimizer Cauchy
oracle. This weaker convexity premise matters: a globally convex cubic
is already quadratic, whereas a genuine cubic can be convex on a bounded
domain. Both results permit lower-dimensional rational polytopes.

These point guarantees strengthen certified objective-gap output.
They do not decide exact active constraints or provide small expanded
algebraic coordinates. The reviewed quartic point reductions concern
convexity on a bounded box; they do not satisfy the higher-degree theorem's
global convexity premise. Their PosSLP and Square Root Sum implications
remain conditional complexity statements.

## Consequences for structured nonconvex optimization

| Supplied structure | Completed capability |
| --- | --- |
| Arbitrary fixed-degree polynomial with a nonconvex coordinate core and convex residuals on a product box | One finite core-noise law supports certified values and a fixed optimal core at every precision, in expected `f_D(k)(1+L/sigma)^k poly_D(I+q)` work. Residual point distance is not promised. |
| Bounded rational polytope and `F+alpha||v||^2/2` convex on it | The coupled value/core theorem gives the corresponding guarantee with `alpha` in place of `L`. These parameters need not be comparable. |
| The preceding coupled model, with total degree at most three | The [cubic completion](new-direction/cubic-core-full-point-oracle.md) gives a fixed full optimizer Cauchy name at the inherited expected cost, including unperturbed residual coordinates. |
| Fixed degree and a core quadratic convexifier valid on all of Euclidean space | [Global completion](new-direction/globally-convex-polynomial-point-oracle.md#7-bounded-transfer-to-the-already-current-core-completion-interface) gives the same full-point capability beyond cubics. |
| Convex objective on the polytope, with selected coordinates perturbed | The [convex-coordinate theorem](new-direction/joint-convex-core-point-oracle.md) gives ordinary expected `poly_D(I+q)` selected-coordinate approximation. |
| Rational quadratic objective in the supported core models | [Rational reconstruction](new-direction/qp-core-cauchy-reconstruction.md) recovers an exact rational optimizer and value. |

The full-point completions select the minimum-norm optimizer in the fiber
of the lexicographically first optimal core. A convex surrogate on the
original feasible polytope avoids assuming continuity of moving optimal
fibers. Its error bound uses known rational rows despite the exact core's
possibly irrational coordinates. Short rational core approximations suffice
for an effective regularized completion. The search retains its original
convexification parameter.

An [explicit affine-power representation](new-direction/affine-power-core-point-oracle.md)
provides a directly verifiable higher-degree class: a PSD quadratic plus
positive rational multiples of even powers of rational affine forms,
with an affine term. Its direct proof preserves explicit constants and
serves as a concrete instance of the global-convexifier result.

For a solver, these results could supply certified high-precision primal
solutions for structured continuous subproblems and low-dimensional
nonconvex corrections. The theory does not establish competitive runtime.
Practical value still requires implementable certificates, moderate search
parameters, effective convex subproblem solvers, and computational evaluation.
The smoothed results solve the sampled objective. They do not automatically
solve the original objective; on a unit core box the established objective
regret bound is `k sigma` plus the requested optimization error.

## Prior work and limits

The [global-convex source audit](prior-art/globally-convex-polynomial-point-prior.md)
compares Li's constrained qualitative error bound with the computable
polynomial-bit constant and fixed-selector conclusion here. The
[cubic audit](prior-art/convex-cubic-point-oracle-prior.md) also distinguishes
classical exact convex QP, weak convex value optimization, and hard convexity
recognition. Kannan--Rademacher's convex program with a low-dimensional
polynomial perturbation is a central antecedent for the nonconvex core
work; the [coupled audit](prior-art/coupled-polytope-core-value-oracle-prior.md)
states its range-relative approximation and accuracy-dependent grid cost.
These comparisons do not establish publication priority. Yang's 2009
error-bound paper remains abstract-only in the local knowledge base; no
theorem-level conclusion is attributed to its unavailable full text.

The [residual-convex cubic closing note](new-direction/residual-convex-cubic-boundary.md)
preserves a useful incomplete extension. Residual Hessian kernels are fixed
on relative core faces, and the relevant minors have degree at most two.
Supplied face/minor margins give effective fiber bounds. A uniform margin
certificate and a full smoothed point algorithm were not proved. Examples
disprove a uniform fiber error constant and naive minimum-norm completion
at approximate cores; they do not prove computational hardness.

## Verification and stopping status

Important results received independent adversarial actual-file reviews,
followed by root's separate proof checks. Exact arithmetic diagnostics
exercise interpolation, invariance, error bounds, feasible repair, finite
noise certificates and completion budgets. They are finite correctness
fixtures, not general solver implementations or runtime benchmarks.
The [research record](PROGRESS.md) lists the exact commands and their scopes.
No Lean verification, project-wide local verification or CI inspection is
claimed. Current work is documented, including the unresolved extension,
and stops at the user's request.

The earlier stop missed an October 1 background BP certificate search.
On October 2 the user explicitly requested its termination. PID 244853 was
stopped and its exit confirmed; its log was retained, but no final certificate
or checkpoint exists. The [experiment closeout](../research-20261001/orbit-closure/CLOSEOUT.md)
records the remaining issues and work. No replacement run was started.
