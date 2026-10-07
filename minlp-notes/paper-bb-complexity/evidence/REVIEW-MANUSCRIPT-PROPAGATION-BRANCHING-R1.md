# Final mathematical review: propagation and branching

Reviewed 2026-10-05 after the author's final stable-source notice. This review
covers `sections/propagation.tex`, `sections/branching.tex`,
`appendices/propagation-proofs.tex`, and `appendices/branching-proofs.tex`.
The repeated coordinate-ambiguity result added during the review is included
in the final disposition below.

## Disposition

**Accepted within the stated mathematical scope. No unresolved mathematical
error or missing proof remains in these four files at the recorded hashes.**
Every selected nonstandard claim has a proof in reachable manuscript TeX.
The results distinguish expression-graph exactness, event counts, search
nodes, and propagation rounds. The branching comparisons fix the oracle and
incumbent, and distinguish rectangular partitions from guillotine trees.
The manuscript does not claim general higher-dimensional competitiveness,
a representation dichotomy, or schedule-independent HC4 round bounds.

This is a mathematical and source-dependency disposition. It does not verify
bibliographic identities, novelty against literature, the other chapters,
or a final standalone LaTeX build. Those are separate integration checks.

## Reviewed source snapshot

SHA-256 hashes from the finished TeX files:

| File | SHA-256 |
|---|---|
| `sections/propagation.tex` | `1125781a1465c9a5f2f490bab596a73c9c9c1eb1bc3da780815b4b9c058f029d` |
| `sections/branching.tex` | `a746e77d893c12c0ae9ea31bd10c220e0ce23e63fa107ecee10cbde2d1c7e39d` |
| `appendices/propagation-proofs.tex` | `5c8d4254c6d78f33c43aadb07ecaea1d434f49ba15a79d32c0cf8586049645ca` |
| `appendices/branching-proofs.tex` | `413818bddd4560ee9525e3297a8629496b44a9a00d58e641b489e27655743b70` |

After the mathematical review, the author wrapped the interval cells and
header in the eleven-node table in braces to prevent LaTeX from parsing a
row's leading `[` as optional spacing. I reread those six cells and refreshed
the appendix hash above. Their intervals, minima, and all mathematical text
are unchanged. A later root typesetting edit placed `H_B` and
`f_i=H_i-y^2-epsilon` on separate alignment rows and explicitly stated
`i in {A,B}`. I inspected the changed display: both maxima and both objective
definitions are unchanged. The refreshed hash includes this edit, and the
accepted disposition remains valid. The narrow follow-up ran only
`sed -n '85,98p' appendices/branching-proofs.tex`,
`sha256sum appendices/branching-proofs.tex`, and a read of this record's hash
table. No unchanged proof review or executable source checks were repeated.

On 2026-10-06, I checked a narrow attribution correction against the
Schichl–Markót–Neumaier comparison in `evidence/LITERATURE.md`. That ledger
states that their validated exclusion regions identify critical points and
do not themselves impose an objective cutoff. The revised opening now
attributes natural interval extensions and validated exclusion regions to
that source, then describes objective-cutoff propagation as this section's
subject. It no longer attributes objective-cutoff propagation to that paper.
The wording agrees with the supplied ledger. The mathematical disposition
remains accepted; the section hash above includes the prose-only edit.
This follow-up ran `rg -n -i -C 5 'schichl|exclusion region|critical.point'
evidence/LITERATURE.md`, `sed -n '1,20p' sections/propagation.tex`,
`sha256sum sections/propagation.tex`, and a read of this record's opening and
hash table. No unchanged proofs or tests were repeated, and no browsing,
literature research, or shared knowledge-base access was performed.

The review used `BRIEF.md`, `AUTHORING-CONVENTIONS.md`,
`ARCHITECTURE-DECISION.md`, `ISSUES.md`, the full `AUDIT-BRANCHING.md`,
the propagation part of `AUDIT-SPATIAL.md`, and
`REVIEW-SHARP-INDUCTION-R1.md`. Relevant original propagation, competitive
branching, and separable-coordinate proofs were also read. Source audits
were treated as evidence; the manuscript proofs were checked independently.

## Propagation findings

| Claim and manuscript proof | Independent finding |
|---|---|
| `prop:fixed-point`; `app:propagation-fixed-point` | Correct. Continuous operations on compact forward domains make each elementary graph closed. Exact revises are monotone, deflationary, and continuous on decreasing compact boxes. The hull of consistent boxes is the greatest consistent box. Explicit fairness requires every exact revise and cutoff infinitely often; partial fairness requires both forward and backward revises. Empty limits are reached at finite iterates by compactness. |
| `prop:pi-box`, `prop:pi-point`, `prop:bound-chain` | Correct. Cutoff thresholds are attained closed upper sets. Thus propagation removal and emptiness use strict inequalities; weak relaxation pruning is a different comparison. A point evaluation supplies the singleton witness and the upper bound by its objective value. |
| `prop:flat-formula`; proof in the section | Correct with distinct root-child coordinates and nonzero collected coefficients. Signed endpoint support gives the necessary bound. The constructed unary intervals and independent root supports give sufficiency. Endpoint maxima, rather than full range maxima, are essential. Compact subbox endpoints give attainment. |
| Three-square representation example | Correct after adding the missing lower argument. Same-side intervals give nonnegative `Phi`; intervals crossing zero give `Phi >= -max_U x^2 >= -1`. The symmetric root interval attains `-1`. Repeated direct root references are explicitly excluded or collected. |
| `prop:one-sided`; proof in the section | Correct as a sufficient condition. The grouped excess identity is exact; choosing the sole positive-excess coordinate proves the lower bound. Equality for lifted coordinates requires the explicit attainable-product condition `z(C)=B_z`. No necessity or representation dichotomy is asserted. |
| `prop:local-exactness`; proof in the section | Correct with the now explicit `w_0>0`, unconstrained model, fixed optimal incumbent, Lipschitz objective, and quadratic relaxation-error bound. A positive fixed mesh certifies boxes in the exactness neighborhood or outside it; the integer width potential bounds the tree. This is an ideal fixed-point node result, not a round or runtime result. |
| `prop:witness`; proof in the section | Correct for arbitrary continuous DAGs below a sum of distinct child coordinates. Exact expression ranges support every nonroot elementary constraint. Single use is needed only for the additional forward-range identity. |
| `prop:cnd-transfer`; `app:propagation-transfer` | Correct. The Taylor witness gives linear loss on coordinate segments. Strict removal bounds every nearest-face distance, and hence yields the quadratic-gap point certificate. The inheritance proof uses the minimum cutoff over the entire inherited chain. Discarded owners exclude retained boundaries; their closed test boxes supply the event certificates. Covering and arcsine estimates apply to certified owners. The logarithmic consequence now explicitly requires a neighborhood of the minimizer inside `N`. |
| `prop:nd1`; `app:propagation-face-loss` | Correct under the explicit positive radius and growth assumptions. Aggregate loss confines removed points to one face layer. The small-gradient comparison gives the factors `8/3` and `5/4`. The residual integral in `n-1` coordinates is uniformly finite for `n>=2` with `gamma>0`. A connected embedded arc with all tangent coordinates bounded away from zero has controlled slab length. No unsupported general positive-dimensional ND1 conclusion is asserted. |
| `prop:slow-rounds`, `prop:fast-rounds`; `app:propagation-rounds` | Both complete schedule-specific proofs check. The expanded quadratic uses old forward term ranges in its backward root projections, followed by the power revise. Its endpoint recurrences preserve a nonempty box through the threshold range and give the arctangent coefficient `pi/8`. The lifted endpoint example uses `u>=0`, `0<U_0<1/2`, and the doubly exponential upper contraction. Neither proof is extended to all schedules or representations. |

The CND and ND1 lower bounds count terminal and removed-piece events.
Conversion to search nodes requires a bounded number of phases per node.
The chapter keeps this qualification explicit and does not hide unbounded
round work in a node count. Original-constraint revises, stronger whole-DAG
contractors, and auxiliary-variable operations are outside these witnesses.
The representation `f_*+|f-f_*|` is restricted to the unconstrained domain
where `f>=f_*`, and is identified as encoding the optimal value.

## Branching findings

| Claim and manuscript proof | Independent finding |
|---|---|
| `branching:four-competitive`; proof in the section | Correct for every continuous objective and uniform positive `alpha`, without convexity. Endpoint positivity makes every invalid-node minimizer interior. The crossing cancellation forces the larger nested node to cross the opposite certificate endpoint. The three crossing classes and unique certificate-breakpoint splits give `4N-5`. The finite-prefix bound proves termination. The valid-root case is stated separately. Arbitrary minimizer ties, including history-dependent ties, are valid for this 1D theorem. |
| `branching:ratio-range`; `app:branching-small-certificates` | The complete two-piece proof is correct, including the nonpositive-bracket case. The eleven-node construction has five unique invalid minima and six valid leaves. The simple three-piece certificate at `2/5,3/5` has minima `209/160000,0,209/160000`. The two incompatible breakpoint requirements, including outside-test-knot cases, prove an optimum of three intervals. The known ratio range is `[11/5,4]`; strict pointwise bounds are not used to claim a strict supremum. |
| `branching:germ-obstruction`; `app:branching-information` | Correct. The explicit maxima of lines agree near the unique root minimizer and endpoints, while surviving tight-chord tests force two distinct unique optimal cuts. Deterministic and randomized quantifiers have the correct order. Symmetric positive compactly supported smoothing preserves the affine tests, convexity, endpoint minima, and common root data. Each smoothed function is nonanalytic because its smoothed `H` is affine on an endpoint neighborhood and nonaffine near the smoothed V. The analytic-germ limitation is explicit. |
| `branching:dimension-obstruction`; `app:branching-dimension` | Correct. The explicit rigid/nonrigid family has the stated root and endpoint margins, global optimum zero, and a three-node optimal tree. All corner boxes with a free rigid label have identical permitted local data and are strictly invalid. Re-cuts contribute one corner child; free-coordinate cuts contribute two. Contracting finite re-cut chains supplies at least `2^d` branching nodes, and the label sum is `2^(n+1)-n-2`. The deterministic root-label sharpening and randomized distribution-of-local-rules averaging are valid. Locality and coordinate-wise minimizer selection are explicit. This is exponential dimension dependence at fixed tolerance, not accuracy growth at fixed dimension. |
| `branching:persistent-clamp`; proof in the section | Correct. The continuous fixed-point equation for the relative split has an interior solution except for the pure minimizer rule. Its alternating kink positions and geometric widths give the explicit logarithmic chain count. The bad kink is fixed for this family. |
| `branching:recentring`; `app:branching-safety` | Correct. The first `J` safe cuts cannot reach a sufficiently near-bound kink and remain invalid under the explicit tolerance inequality. Varying the kink with tolerance gives the uniform worst-case obstruction. Recentering stays safe for `theta<=1/3`; its three distance regimes give exactly `J+1` zero-tolerance hitting splits and at most `2J+3` nodes at positive tolerance. Hitting optimality is not promoted to optimality among finite-tolerance certificates. |
| Separable brackets; `branching:multi-separation`, `app:branching-multi` | Correct. Slices use the whole tolerance and products allocate it. For multisection, all `2^D` z-intervals have identical validity for a fixed x history. The left pieces of the right-spine histories stay unsplit in x and are invalid through depth `2k`. The strict x estimate handles equality in the floor-defined tolerance threshold. The count is `Omega(epsilon^-1/2 log(1/epsilon))`, versus an explicit guillotine `O(epsilon^-1/2)` certificate. Two- and four-child nodes are counted as processed boxes. |
| `branching:sharp-induction`; `branching:phase-lemma`, `app:branching-sharp` | Correct under the fixed coordinate-wise selection and fixed separable oracle. Sharp halves collapse to zero relaxation value and zero selected gap. The phase forest has at most `kappa` terminal split intervals, each chain has at most `2kappa(kappa+1)+1` nodes, and finite-prefix counting establishes termination. Frontier refinement proves `sum_j N_Aj <= N+H-1`, closing the induction recurrence. The slice converts the final leaf estimate to the stated rectangular-certificate node bound. The arbitrary coordinate may have no zero on a restricted interval; the 1D proof needs only nonnegativity plus a positive budget. Every fixed coordinate-wise selection is allowed only under the all-sharp-minimizers version of the assumptions. The explicit sharp family and its slopes demonstrate that the hypotheses are nonempty. |

The selected claims require no general sum of phase costs for arbitrary
separable objectives. The manuscript leaves that problem open. The constants
in the sharp-coordinate recurrence depend only on the number of unsplit
sharp coordinates; the node bound is converted from a leaf count using
`T=2L-1`, rather than asserting the same leaf factor for node ratios.

## Corrections resolved during this review

Concrete repairs were sent to the author and root when found. All are present
in the finished snapshot:

- The CND logarithmic consequence needs a neighborhood inside `N`.
- The ND1 integral needs `gamma>0` and positive radii; division by a zero
  Taylor-remainder bound has an explicit infinite-radius convention.
- Local exactness needs `w_0>0` and a positive chosen mesh; CND uses positive
  segment radius and root maximum side length.
- The original eleven-node certificate proof named a tight knot outside its
  middle interval. It now uses the simpler valid certificate and correct
  minima, with both automatic outside-test-knot cases in the no-two proof.
- The root information obstruction now states “for every rule, at least one
  instance,” rather than reversing those quantifiers.
- Fairness, the three-square lower calculation, the phase budget extension
  to nonzero restricted minima, the definition of `N_A`, and the fixed
  minimizer-selection requirement are explicit.
- The smooth ambiguity proof establishes nonanalyticity of each objective,
  rather than merely excluding simultaneous analyticity of the pair.

There are no remaining mathematical repair requests for these files.

## Readability, reachability, and checks actually run

The chapter order is coherent: graph-dependent bounds precede scheduling
cost; certificate comparisons precede information and safeguard losses;
coordinate choice then motivates the restricted positive induction. The
long proofs are in the two appendices and are referenced from their claims.
Forward references have no circular proof dependence. In particular, the
two-piece bound is proved without the ambiguity pair, and the pair later
supplies attainment; the phase lemma uses the proved 1D split count before
the induction uses the phase lemma.

Source inspection used targeted `rg --files`, `rg -n`, `cat`, `nl -ba`, and
`sed -n` commands on the named evidence, source-note proof locations, and
four assigned TeX files. The final executable source check was:

```sh
python3 - <<'PY'
from pathlib import Path
import re
paths=[Path('sections/propagation.tex'),Path('sections/branching.tex'),Path('appendices/propagation-proofs.tex'),Path('appendices/branching-proofs.tex')]
texts={str(p):p.read_text() for p in paths}
labels={}
for path,s in texts.items():
    for label in re.findall(r'\\label\{([^}]+)\}',s):
        if label in labels: raise SystemExit('Duplicate label: '+label)
        labels[label]=path
for path,s in texts.items():
    for group in re.findall(r'\\(?:[cC]ref|eqref)\{([^}]+)\}',s):
        for label in group.split(','):
            if label not in labels: raise SystemExit('Unresolved owned-file reference: '+label+' in '+path)
    stack=[]
    for kind,name in re.findall(r'\\(begin|end)\{([^}]+)\}',s):
        if kind=='begin': stack.append(name)
        elif not stack or stack.pop()!=name: raise SystemExit('Environment mismatch in '+path)
    if stack: raise SystemExit('Unclosed environment in '+path)
main=Path('main.tex').read_text()
for p in paths:
    target=str(p.with_suffix(''))
    if '\\input{'+target+'}' not in main: raise SystemExit('Unreachable source: '+str(p))
print('PASS: all four sources reachable from main.tex; owned references resolve; labels are unique; environments are balanced.')
print('Owned labels checked:',len(labels))
PY
sha256sum sections/propagation.tex sections/branching.tex appendices/propagation-proofs.tex appendices/branching-proofs.tex
```

Both commands exited zero. The final static check found 50 unique owned
labels, resolved every owned `cref`, `Cref`, and `eqref`, balanced all
environments, and confirmed all four inputs in `main.tex`. The earlier
static check was repeated because repairs and a new dimension result
changed the source. Mathematical inequalities, counts, and exact rational
values were reviewed by hand. A separate hand cross-check of the ND1 face
integral and expanded-quadratic round argument confirmed their constants
and schedule dependencies.

No literature browsing, experiment rerun, manuscript edit, LaTeX build,
project-wide verification, formal proof rebuild, or CI status/log inspection
was performed by this reviewer. This review wrote only the present evidence
record. The targeted results above are local review results, not CI results.
