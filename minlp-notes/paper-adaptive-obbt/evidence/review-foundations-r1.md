# Foundations review, round 1

Reviewed `sections/foundations.tex` read-only from 2026-10-06 01:20:12 UTC.
The SHA-256 digest was
`142794fe2ce968496d153747132377d96a63d595dc428b964d42992c81419a5f`;
it was unchanged when checked at 01:24:09 UTC. Line references below refer
to that snapshot. The section is being written concurrently, so later
edits can resolve these findings.

I read `BRIEF.md`, the foundations and construction passages of
`audit-rates.md`, `INTEGRATION-NOTES.md`, and the applicable `AGENTS.md`.
I checked the formal arguments independently. The order, sublevel-hull,
persistence, and conditional greatest-fixed-box results are sound. The
remaining false inclusion identified by the root still needs correction.
The additional findings below concern the update scheme used for an
archived numerical comparison, the scope of selective-update bounds, and
the scope of the closing rate summary.

## Additional findings

### 1. The archived sequential factor uses a different update scheme

Lines 185–187 quote a sequential factor near `0.705` for the two-variable
quadratic and call it a direct computation of the exact sequential rounds
defined here. The supporting archived file is
`research-20260922/iterated-obbt/code/review_checks/exp_gauss_seidel.py`.
Its `tighten` function builds `P = affine_pieces(a, lo, hi)` once, computes
both endpoints of variable `i` using that same relaxation, and then changes
the two endpoints together. The outer sequential loop applies that
operation to variable 0 and then variable 1. It rebuilds after each
variable. Lines 125–130 of the manuscript rebuild after each signed
direction. These are different maps. The reported factor in the archived
review also belongs to a particular asymmetric initial rectangle and is a
numerically computed late-round ratio, without an accompanying exact-rate
proof.

**Required correction:** remove the numerical comparison, or explicitly
identify the archived variable-block scheme, its starting rectangle, and
the numerical scope of the value. The archive need not be rerun. The
round-comparison lemma itself is correct and does not depend on this value.

An optional analytic replacement fits the update scheme now defined.
Take one variable, `f(x)=x^2`, `U=0`, and

\[
 \phi_{[\ell,u]}(x)=x^2-\frac{(u-\ell)^2}{16}.
\]

This family is valid, convex, continuous, and monotone. A Jacobi round
started at `[-h,h]` gives `[-h/2,h/2]`, so its radius and width factor is
`1/2`. A lower-then-upper directional round on `[-a,b]` gives

\[
 a'=(a+b)/4,\qquad b'=(a+5b)/16
\]

whenever both optimized endpoints lie inside the input intervals. These
conditions hold along the trajectory from `a=b=h`: if `r=b/a` belongs to
`[1/2,1]`, then the support conditions `r<=3` and `r>=1/11` hold, and

\[
 r'=(1+5r)/(4(1+r))\in[7/12,3/4]\subset[1/2,1].
\]

Thus the directional-round recurrence is exactly

\[
 \binom{a'}{b'}=
 \begin{pmatrix}1/4&1/4\\1/16&5/16\end{pmatrix}\binom{a}{b}.
\]

Its eigenvalues are `(9+sqrt(17))/32` and `(9-sqrt(17))/32`.
The larger eigenvalue has positive left and right eigenvectors, and the
initial positive vector has a positive component in that eigendirection.
Consequently the sequential widths are
`Theta(((9+sqrt(17))/32)^k)`. This exact factor is strictly below `1/2`.
The example proves the intended distinction with analytic algebra alone.
It is an abstract valid relaxation family; it should be named as such.

### 2. Selective passes retain a Jacobi lower enclosure

Lines 187–189 say that a selective round is generally not contained in
`T_U(B)`, so it inherits neither kind of bound. Lack of that upper
inclusion does not remove every lower inclusion. The proof already given
at lines 170–173 applies to any sequence of `m` directional updates:

\[
 T_U^m(B)\subseteq C_m\subseteq B.
\]

Indeed, each individual directional result contains `T_U` of its input;
induction and monotonicity give the displayed lower enclosure. In
particular, a single selective directional update contains `T_U(B)` and
inherits every lower bound on its coordinate extents or width. With `m`
updates, a lower enclosure for `m` Jacobi rounds still applies. There is
generally no same-round upper enclosure `C_m subseteq T_U(B)` when some
directions are omitted.

**Required correction:** state that incomplete selective passes need not
inherit the one-round Jacobi upper bounds. If the general lower bound is
useful, state `T_U^m(B) subseteq C_m` explicitly. Exact Jacobi rates and
lower rates at the same round index still require care for complete
sequential passes.

### 3. The closing paragraph states a broader dichotomy than the local results prove

Lines 355–358 say that the next section describes when fixed boxes exist
at every small scale and “otherwise” how fast iterates contract to a
limit whose width is “of order” `sqrt(epsilon)`. The stall and contraction
criteria are sufficient conditions. They need not exhaust all valid
monotone families, even families with a uniform second-order expansion
and a cubic remainder. A positive-cutoff width upper bound also supplies
`O(sqrt(epsilon))`, rather than a matching lower order bound.

Here is an analytic counterexample to the broad reading. Let
`B_0=[-1/2,1/2]`, `X=R`, `f(x)=x^2`, and define, on every subbox,

\[
 E(w)=w^2/4-w^3/8,\qquad \phi_B(x)=x^2-E(w(B)).
\]

For `0<=w<=1`, `E(w)>=0` and
`E'(w)=w/2-3w^2/8>=0`. Hence the family is valid, continuous,
and monotone. Its sublevel sets are compact. For any positive-width box
at cutoff zero,

\[
 K_0(B)\subseteq[-\sqrt{E(w)},\sqrt{E(w)}],\qquad
 2\sqrt{E(w)}=w\sqrt{1-w/2}<w.
\]

There is no positive-width fixed box. Nevertheless, on a symmetric box
`[-h,h]`, the exact Jacobi recurrence is

\[
 h_{k+1}=h_k\sqrt{1-h_k}.
\]

The radii decrease to zero and their successive ratios tend to one.
Moreover,

\[
 \frac1{h_{k+1}}-\frac1{h_k}
 =\frac1{\sqrt{1-h_k}(1+\sqrt{1-h_k})}\longrightarrow\frac12,
\]

so `h_k~2/k`. The convergence is sublinear. This family also has the
required shape expansion: for `B=t[-d^-,d^+]` and `x=t xi`,

\[
 \phi_B(x)=t^2\left[\xi^2-(d^-+d^+)^2/4\right]
             +t^3(d^-+d^+)^3/8.
\]

At positive cutoff `U=epsilon`, the centered recurrence is

\[
 h_{k+1}=\min\{h_k,\sqrt{\epsilon+h_k^2-h_k^3}\}.
\]

If `0<epsilon<h_0^3`, the radii decrease to
`h_epsilon=epsilon^(1/3)`. To see this, the square-root function is
strictly increasing on `(0,1/2]`, takes value `h_epsilon` at that point,
and lies strictly between `h_epsilon` and `h` when `h>h_epsilon`.
Continuity identifies the limit. The limiting width is therefore
`2 epsilon^(1/3)`, which is not `O(sqrt(epsilon))` as the cutoff tends to
zero.

**Required correction:** write that the next section gives sufficient
conditions for local stalling and geometric contraction, and that its
contraction hypotheses give a positive-cutoff upper enclosure of
`O(sqrt(epsilon))`. The counterexample above need not be added to the
manuscript; it establishes why the conditional wording matters.

### 4. Clarify the incumbent cutoff at a node

Lines 31–32 define `f^*` as the node optimum when `B_0` is a node box.
Lines 116–118 say `epsilon=U-f^*` is nonnegative when `U` is the value of
a feasible point. This is correct for a point in `X cap B_0`. A global
incumbent can lie outside the node and have value below the node optimum.
For example, with `f(x)=x^2`, node box `[1,2]`, and global incumbent
`x=0`, one has `U=0` and node `f^*=1`.

**Correction:** say “a feasible point in `X cap B_0`,” and state that the
nonempty-limit and local-rate results explicitly use `U>=f^*`. The general
order statements remain applicable when the original sublevel set is empty.

## Status of the root's existing findings

| Finding | Status in the reviewed snapshot |
| --- | --- |
| `H_U subseteq P` for every fixed box | Still false at lines 345–346. Replace the chain by `H_U subseteq B_infty` and `P subseteq B_infty subseteq B_k`. The endpoint ceilings at lines 350–351 are correct. |
| Original sublevel-hull proof requires original face attainment | Resolved. Lines 210–215 take hulls of contained original sublevel points and do not require continuity of `f` or attainment of original sublevel supports. |
| Symmetry “defeats” root tightening | Still overbroad at lines 224–227. The proved consequence is an obstruction to singleton collapse; the preserved hull need not stop useful tightening or have a positive relaxation gap. Restrict “every cutoff” to the asserted range `U>=f^*`. |
| Fair schedules need decreasing-family closedness for the same intersection | The stated conditional conclusion is true. The stronger conclusion in `INTEGRATION-NOTES.md` is also correct under order and containment alone. Complete-block sandwiching gives `T_U^{t_j}(B_0) subseteq C_{t_j} subseteq T_U^j(B_0)` and the same intersection. Closedness is still needed for the fixed-box identification. |
| Non-fixed-limit example defines only boxes `[0,s]` | Resolved. Lines 319–320 define the projected objective on all subboxes `[r,s]`. Its monotonicity, lower semicontinuity, recurrence, and jump at the limiting box check directly. |

## Proof and assumption checks

| Statement | Independent check |
| --- | --- |
| Compact lifted projection and attained fiber objective, lines 55–61 | Correct. The lifted sublevel set is compact, its projection is compact, and its projection equals the projected sublevel set by attainment. This also proves lower semicontinuity. |
| Lifted monotonicity implies projected monotonicity | Correct for the same objective. Projected monotonicity alone permits box protection; literal auxiliary-coordinate reuse uses lifted nesting. |
| Termwise bilinear and finite square rows, lines 72–82 | Correct for the specified objective and fixed rows. Bilinear hull nesting proves the distinct-index case. For squares, tangents at the new endpoints dominate the corresponding old tangents on the new interval, and the new secant is below the old one. Degenerate intervals are included. |
| Clipped composite construction, lines 83–85 | Correct under the specified recursive rules, nested natural interval bounds, and scalar envelopes on a common valid domain. Include or cross-reference those assumptions, and credit the vetted Scott–Stuber–Barton result. Clipping by itself is not a definition of the whole construction. The literature lead owns source verification. |
| Relaxation bound monotonicity | Correct, including extended values for infeasible boxes. |
| Containment and order lemma | Correct. Validity preserves every original cutoff point; pointwise monotonicity gives the cutoff-set inclusion; closed box hulls preserve inclusion. |
| Complete sequential-round sandwich and iteration intersections | Correct. Both inductions use only containment and monotonicity. No monotonicity of a fixed ordered sequential map is needed. The same proof permits orders that change between complete rounds. |
| Original sublevel hull is fixed | Correct by taking the closed box hull of `S_U subseteq K_U(H_U) subseteq H_U`. |
| Face characterization and persistence of fixed boxes | Correct under compact support attainment. The proof works for all directional schedules and cutoffs bounded below by the certificate cutoff. |
| Limit contains every fixed box; closedness makes it the greatest one | Correct. Endpoint witnesses have convergent subsequences in `B_0`, and decreasing-family closedness puts their limits into the limiting cutoff set. For Jacobi, choose the witness on `B_k` that attains the face of `B_{k+1}` directly. |
| Continuous lifted rows in a common compact set imply closedness | Correct. Compactness supplies convergent lifts; continuity passes each row and the objective cutoff to the limit. |
| Endpoint movement ceilings | Correct after removing the false `H_U subseteq P` inclusion. They follow from `P subseteq B_infty subseteq B_k`. |

Two small conventions improve the proofs. Define `T_U(emptyset)=emptyset`
and make subsequent directional updates absorbing at the empty set;
otherwise the all-cutoff sequential lemma uses powers whose inputs can
leave the nonempty-box definition. Also fix the index convention in the
closedness proof: if `C_t` is the box after update `t`, the witness for
that update belongs to `K_U(C_{t-1})` and attains the face of `C_t`.
Alternatively describe `C_t` as the input and `C_{t+1}` as the output.

## Verification performed

This was a read-only mathematical review. The only file authored is this
report. I did not run experiments, project-wide verification, or inspect
CI status or logs. No independent literature search was performed.

The targeted commands actually used included:

- `cat evidence/BRIEF.md`, `cat evidence/INTEGRATION-NOTES.md`, and
  `cat /workspace/minlp-notes/AGENTS.md`.
- `cat sections/foundations.tex`, `nl -ba sections/foundations.tex`, and
  `sha256sum sections/foundations.tex`.
- `sed -n '159,260p' evidence/audit-rates.md`,
  `sed -n '615,664p' evidence/audit-rates.md`, and
  `sed -n '815,874p' evidence/audit-rates.md`.
- `sed -n '337,372p' ../research-20260922/iterated-obbt/theory.md` and
  `sed -n '70,88p' ../research-20260922/iterated-obbt/review-theory.md`.
- `cat ../research-20260922/iterated-obbt/code/review_checks/exp_gauss_seidel.py`.
- Targeted `rg` searches for clipping, monotonicity, squares, and the
  sequential factors in the audits and archived source; `rg --files`
  located the archived review implementation.

The searches confirmed the update-scheme mismatch. The algebraic
examples, support formulas, matrix eigenvalues, and asymptotic arguments
above were derived analytically without executing the archived solvers.

## Fully proved insertion proposal

At the root's request, `evidence/proposed-critical-example.tex` gives a
self-contained LaTeX insertion for the critical scalar family in finding
3. It defines the real-valued projected objectives on every subbox,
proves validity and monotonicity, excludes nonsymmetric positive-width
fixed boxes at cutoff zero, proves `h_k~2/k`, treats the positive-cutoff
boundary case `epsilon=h_0^3`, and calculates the tangent map and `r^*=1`.
It also shows that the tangent faces have zero value while the actual
finite-box face values are positive. No computational experiment was run.

For this supplement I read the definitions of `D`, `Phi_c`, and `r^*` in
the current `sections/local-rates.tex`, then compiled only the proposal in
a temporary minimal document with the shared notation. A Python heredoc
ran `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
critical-example.tex` twice in that temporary directory. Both passes
exited zero; the final log had no undefined references, LaTeX warnings,
or overfull boxes. The full manuscript was not compiled.
