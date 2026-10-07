# Final mathematical review: certificates, cutoffs, and residuals

Date: 2026-10-05. **No unresolved mathematical findings in the assigned
scope.** The completed `sections/certificates.tex`, `sections/cutoff.tex`,
and `sections/residual.tex` resolve the first-round findings. I also
checked the nonemptiness premise in `prop:fixed-limit` and the agreement
between `prop:round-check` and the certified closure algorithm. Only this
report was written; no manuscript file was edited by the reviewer.

## First-round findings: final status

- **Finite pools and lifted feasibility: resolved.** Both the current-round
  screen and the completed-round test use finite pools. The latter now
  checks complete lifted points on the rebuilt box. A screen bounds one
  frozen round; protection requires feasibility on the proposed inner box
  itself. Projected monotonicity suffices for protection and objective-value
  ceilings; reuse of an auxiliary vector requires lifted monotonicity.
  `ex:lambda` now supplies objective `v=s` and includes degenerate boxes.
- **Fixed-box completeness and order premises: resolved.** The equivalence
  between fixed boxes and pools of at most `2n` witnesses uses compact
  attainment. Rational witnesses are guaranteed for a prescribed rational
  box, rational cutoff, rational polytope, and rational affine objective.
  This gives completeness of checking a prescribed box; it does not promise
  discovery of a useful box or a rational iteration limit. Adding common
  lifted rows preserves order under the explicitly stated lifted-monotone
  premise (`certificates.tex:497`). Discovery costs and merging ceilings
  no longer assert unsupported impossibility or strict improvement.
- **Cutoff thresholds and frontiers: resolved.** The whole-pool threshold
  remains sufficient; the face threshold is sharp for retaining a subpool
  on the same box. The full-relaxation threshold uses compact face minima,
  with `+infinity` for absent faces. Below it the next round may find an
  empty cutoff set, rather than necessarily move an endpoint. Mixing
  cannot lower the same-box face threshold. Frontier and response results
  require a nonempty pool and optimize its convex hull only; filtering
  after new rows does not recover the old convex hull intersected with
  those rows. Repeated values, cutoff equality, an empty candidate set,
  and screening intervals at the smallest pool value are covered.
- **Invariant regions, active regimes, and incumbent scope: resolved.** An
  incumbent supplies a protected singleton only when it lies in the current
  box (`residual.tex:48` and `268`). A global incumbent outside a node
  supplies no invariant order interval there. The matrix comparison must
  hold on a verified invariant region, including every active regime the
  trajectory can enter. Changing the cutoff requires verified data for
  the new map; a current basis or observed ratio alone is insufficient.
- **Residual arithmetic and examples: resolved.** The after-round ceiling
  is `Me <= e - dbar` at the exact Jacobi image, even when `dbar` is an upper
  residual. Complete exact sequential movement supplies an upper Jacobi
  residual; selective, interrupted, and outward-rounded movement need not.
  The least-majorant argument handles zero residual, singular `I-M`, and
  inactive noncontracting directions; the inverse formula is restricted
  to `rho(M)<1`, and exact rational solves require rational data. The
  inactive example is defined on all subboxes. Heron's error identity
  proves convergence and quadratic convergence, with the already fixed
  starting case covered. The finite-history construction handles `N=1`
  and distinguishes an exact observed residual from a uniform comparison.
- **Integration: resolved.** The three sections use the shared
  `eq:closed-family`, `prop:fixed-limit`, and `lem:sequential` statements.
  References to the deleted local limit theorem and its `(L1),(L2)`
  premises are absent. The evaluated policy is explicitly limited to
  current-round screening; it does not implement the stronger certificates.

## Additional second-round finding: resolved

The previous version of `prop:round-check` used a projected pool and tested
projected feasibility, but `ex:round-check` demonstrated failure of an old
auxiliary lift. In that example both projected endpoints remain feasible
on the new box; only the stored lift `(1/2,0)` fails. Thus the example did
not prove the stated projected-test failure and the test differed from
the algorithm's row check.

The root corrected `certificates.tex:556` to require a finite complete
lifted pool `widehat W` in `R_U(B)`, with projected pool
`W=pi_x(widehat W)`, and to test `widehat W` in `R_U(B')`. I reread the
final statement and proof. Part (a) gives the correct finite witness pool;
part (b) follows from identical input and output boxes; and the rejected
auxiliary vertex proves part (c). No objection remains.

## Supporting results and limits of the guarantees

`foundations.tex:286` now explicitly assumes every Jacobi iterate is
nonempty. Nested compact boxes then have a nonempty limit. Fixedness of
that limit additionally requires `eq:closed-family`; compactness of each
individual relaxation is insufficient. The cutoff restart proposition
(`cutoff.tex:286`) assumes `U' >= f*`, ensuring nonempty restart iterates,
and uses closedness at the new cutoff. Relaxation-sound earlier steps
retain the new greatest fixed box, giving the stated sandwich and equal
limits. These premises are consistent.

`algorithms.tex:157`, especially part (c), matches the corrected lifted
test. A committed round starting at a fixed box detects it. Arrival at a
fixed box can miss the check because of the returned auxiliary coordinates;
the next committed round succeeds. The bound of at most `m+1` rounds
explicitly requires sufficient budget and successful proposal checks.
It does not promise successful numerical proposals or finite termination
of an asymptotically converging iteration. Singleton pools and singleton
limits remain valid certificates.

The cutoff fixed-point shift compares existing ordered fixed points and
retains the stronger `rho(M)<1` premise. The sensitivity estimate in the
cutoff variable is needed only at the old fixed point, whereas the ordered
matrix comparison must apply to both points. The trajectory theorem
requires an invariant region and a finite supersolution instead, and
makes the separate qualification for fixedness of its limit. These two
results are not conflated.

## Verification performed

This pass used manual proof review and targeted source reads with `sed`
and `nl`, including `certificates.tex:520--632`,
`foundations.tex:276--328`, `algorithms.tex:152--224`,
`cutoff.tex:207--244,272--314`, and `residual.tex:1--378`.
The following targeted commands were also run from the paper directory:

```sh
rg -n 'finite|same row|lifted nesting|rational|tau|empty|incumbent|threshold|pool|fixed-limit' sections/certificates.tex sections/cutoff.tex
rg -n 'L1|L2|limit-protected|thm:residual-tail|eq:order-lipschitz' sections/certificates.tex sections/cutoff.tex sections/residual.tex
sha256sum sections/certificates.tex sections/cutoff.tex sections/residual.tex
```

The stale-reference search returned no matches (exit status 1, as expected).
The numerical examples are unchanged from the exact rational checks
recorded in `review-certificates-r1.md`; those checks were not repeated.
No solver run, experiment, literature search, LaTeX build, project-wide
verification, or CI inspection was performed in this pass. Checks listed
in `author-certificates.md` are the author's results, not this review's.

Reviewed snapshot SHA-256 values:

```text
274823fd974086f63d074d65037559dec7e80230a27a61914282a0da88baa562  certificates.tex
042b81c0555789198cfa1294f400318f55af90556b0dd8e970ba7478a046377d  cutoff.tex
49703b1836c1e96d53c845c7e9f20466c553fd81149586fd770e44705b1d1d60  residual.tex
```
