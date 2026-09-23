# Stage 4, round 1: root assessment

Root read all five completed independent reports in full and independently
checked each actionable finding against the frozen source. Reviewed snapshot:
`stage04-round01`, eleven files, manifest SHA256
`4ef85d87d33a7c0860e735f7daa7311f1bc61f20b3ae6a36585f05ffe268befe`.

## Decision

No accepted major issue. Four minor correction items are accepted below,
including one optional explanation that materially improves readability.
A separate correction agent must fix all four before stage acceptance.
The user's process does not require a second five-reviewer round for these
minor corrections; root will inspect the complete correction diff and build.
Stage 5 must not start before that verification is complete.

## Disposition of every review finding

| Report finding | Root disposition |
| --- | --- |
| Review01: nonlinear inverse argument degree omitted in upper substitution | Accept minor, S4-1. |
| Review02 R02-S04-01: direct polynomial solution-map regularity predecessor omitted | Accept minor, S4-2. |
| Review03 R03-1: stale stage 3 status and README opening omits current stage 4 | Accept minor, S4-3. |
| Review04 M1: nonlinear composition degree | Same valid issue as S4-1; merge. |
| Review04 M2: stage-status descriptions | Same valid issue as S4-3; merge. |
| Review05 R05-M1: stale coverage status | Same valid issue as S4-3; merge. |
| Review05 optional suggestion: display the gradient-splitting identity | Accept minor explanatory improvement, S4-4. |

No reviewer reported a major issue. No actionable finding is rejected.
All five independently checked the new sharp modulus, inverse construction,
resource/aggregate recovery and upper-feasibility qualifications. Their
finite diagnostics support specified steps and do not replace the proofs.

### S4-1: account for composition degree

At section04 lines 538--540 the text calls d_p the inverse-branch degree
but uses it as the degree after nonlinear composition. This is false as
written: g(z)=z, phi(w)=w^4/4, U=1 and incentive x give a linear inverse
branch but response polynomial x-w^3. With H=z, the actual composed degree
is three, not one. The exact candidate z=w=1/4, x=17/64 shows that this
example lies in the intended construction.

Introduce d_h for univariate branch degree and
d_a=max(1,max_i deg a_i). Then deg p_i <= d_h d_a and the upper substitution
degree is at most D_up max(1,d_h d_a). The inverse arguments obey
d_a<=max(1,deg phi-1), with zero/constant aggregate handled by the leading
one. Alternatively define d_p explicitly after composition and show this
product bound. All factors are polynomial in the stated numerical-degree
and accuracy parameters. Thus this is a local degree-accounting error, not
a failure of the polynomial-time theorem.

### S4-2: credit the directly relevant regularity result

Add a short comparison adjacent to the response-modulus proposition with
Jeyakumar--Lasserre--Li--Pham, Theorem 2.3. Root independently read its local
primary full text and visually inspected original.pdf p.5. Its displayed
property is ONE-SIDED inclusion of Y(x) in a Holder neighborhood of the
solution set Y(xbar), for a fixed reference leader and a compact,
leader-independent polynomial feasible set. The exponent depends on
polynomial degree, follower dimension and constraint count. Avoid implying
two-sided set-valued continuity or a uniform rational bit constant from
that theorem.

The manuscript proves, for its structured unique-response class, uniform
pairwise exponent 1/P, independent of follower count and aggregate degree,
with a computable rational polynomial-bit sufficient constant, allowing
affine moving resource right-hand sides. Attribute the general predecessor
without claiming publication priority for an entire regularity principle.
The existing bibliography entry is sufficient; one precise paragraph is
enough. Primary source package:
`literature/papers/jeyakumar2016-convergent-semidefinite-programming-relaxations-for/`.

### S4-3: reconcile stage-status documentation

Replace the obsolete pending-review sentence under stage 3 in coverage.md
with its actual accepted disposition. Update README's opening to identify
both accepted stages 1--3 and the present stage 4 draft/appendices, still
pending completion of its current correction gate. Root will mark stage 4
accepted only after checking the corrections. Preserve the distinction
between finite diagnostics and general algorithms.

### S4-4: expose the central gradient identity

The existing inequality is correct but asks the reader to reconstruct the
central cancellation. Add the intermediate identity, with e=z-z' and the
same active-row correction d:

    (grad F_x(z)-grad F_x(z'))' e
      = (grad F_x(z)-grad F_x'(z'))' d
        + (grad F_x'(z')-grad F_x(z'))' e.

The first gradient difference annihilates e-d. Its infinity norm is at
most A_z||e||+A_x Delta, while the second is at most A_x Delta. These are
exactly the two terms already used in the displayed inequality. Use clear
LaTeX subscripts for x' and break the display as needed. No theorem or
constant changes are required.

## Correction verification requirements

The separate fixer should read this assessment and the five reports, edit
only the assigned paper files, inspect the entire diff against the frozen
snapshot, compile cleanly, and record changes/source checks in
`process/stage04-corrections.md`. No broad repetition of already passing
diagnostics is needed for these local mathematical-accounting, attribution,
explanatory and documentation corrections. Root owns STATUS, acceptance,
and immutable snapshots. Unrelated repository work must remain untouched.

## Correction gate closed

The separate correction agent fixed S4-1 through S4-4. Root read its complete
report and every changed-file diff against stage04-round01. The composition
factor, primary-source scope, stage records and gradient identity now have
the intended meaning. Only the four assigned files changed; frozen hashes
remain intact. Root rebuilt the live manuscript successfully: 46 pages,
with no final warning, undefined citation/reference or box diagnostic.

All accepted minor issues are closed. No correction introduced a major
issue, so the required process permits stage acceptance without another
five-reviewer round. Stage 4 is accepted. Later stages and the final full
manuscript review remain mandatory.
