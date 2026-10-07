# Whole-paper integration review, round 1

Reviewed on 2026-10-05. This is a fresh independent Sol review of the
manuscript's mathematical and exposition interfaces. It is internal review,
not external peer review or a guarantee of journal acceptance.

The reviewed existing manuscript passes this integration round after four
small contract repairs described below. No unresolved mathematical or
algorithmic interface finding remains in Sections 00–11 and Appendices A–K
at the recorded snapshot. This conclusion does not claim that every proof
has been independently reproved in this round. The review reconstructed
shared interfaces and their uses, checked statements against the detailed
arguments, and read the relevant full earlier reviews and author responses
before assessing repaired items. The independent chapter proof reviews
remain separate evidence.

**The full submission is not yet cleared by this report.** All 97 inventory
entries are in scope. At this snapshot Appendix L is not yet present, so
Q13–Q14 and the new framing statements that describe them require a bounded
follow-up against the actual completed appendix. Bibliography and primary
source verification remain owned by the literature lead and root. An absent
bibliography entry is not treated here as a new proof defect, and a prior
source request is not treated as cleared merely because its theorem is
cited.

## Scope and method

I read BRIEF, CONVENTIONS, DECISIONS, both integration records, the current
final-coverage audit, main.tex, macros.tex, the main framing and model
passages, the point and upper-bound statements and their shared interfaces,
the algebraic statements, and all of Section 10 and Appendix I. I checked
the actual numerical attribution repairs after reading the full
opus-numerical-r1 review and repair-numerical-r1 response. I also read the
full framing-r1, recourse-r1/r2, and recourse repair reports. Earlier
observations were used to locate actual text, not as substitutes for it.

Two independent delegated read-only checks covered the remaining interfaces.
One examined output and bit models across 01/02/03/04/07/09 and A/B/C/F/H,
including the framing and actual repaired versions. The other examined
05–09 and D/E/G/H/J/K, with further read-only division of fields and
quadratic/boundary interfaces. They read the relevant full R1/R2 reports
and repair records. Their scope was integration, including the contracts
on each side of a cross-reference, rather than a new proof audit of every
already reviewed appendix theorem. Their findings and final dispositions
are incorporated below.

The review used analytic reconstruction and targeted text and hash
inspection. It did not research or retrieve literature, mutate the KB,
edit a manuscript file, run experiments, mathematical scripts, CAS,
historical diagnostics, builds, project-wide verification, or CI checks.
Only this review file was authored.

## Findings and actual repairs

Severity here describes the printed contract. Each finding was low severity
and is resolved; none invalidated the underlying theorem. This review found
items 1–3. Root's readability pass found item 4; I verified its repair
against the actual proposition and output definition.

1. **Degree cost in the point-summary table — resolved.** The old caption
   of Table tab:points-summary said every entry marked polynomial meant
   polynomial in L and q. Its globally convex column allows numerical
   degree D and invokes thm:global-point, whose time is polynomial in
   L,D,q and whose computed constants have polynomial length in L,D.
   Binary degrees are explicitly outside a polynomial-in-L guarantee.
   At [02-points.tex:732](/workspace/minlp-notes/paper-exact-arithmetic/sections/02-points.tex:732)
   the repaired caption charges L,D,q in that column and L,q in the
   fixed-degree columns. This matches the theorem and Appendix C's sparse
   evaluation and selector costs. Accepted initially at hash c46c9d01;
   the final 02 hash below includes item 4's later wording repair.

2. **Arbitrary integer scale in the denominator corollary — resolved.**
   Corollary cor:fields-tower-denominator(b) allowed any integer c above
   its threshold and transferred all conclusions of thm:fields-prime
   except its coefficient-bit bound. That also transferred the theorem's
   construction time polynomial in ell, which cannot cover an arbitrarily
   long supplied c: a nonzero quartic coefficient of
   c(f_ell+r^2)-r^2 grows linearly with c, so writing it needs at least
   order bits(c) work. At
   [09-certificates.tex:192](/workspace/minlp-notes/paper-exact-arithmetic/sections/09-certificates.tex:192)
   the repaired statement transfers only the monomial count and parts
   (b)–(d), charges construction polynomial in ell and the binary length
   of c, and gives coefficient and Gram-entry lengths O(log ell+log c).
   Multiplying the base integer data by c and subtracting the fixed
   r^2 data gives exactly these bounds. Accepted at hash d5488833 below.

3. **Rational scale in the supporting remark — resolved.** The same
   overtransfer occurred in rem:fields-prime-scales for rational lambda.
   It also inherited integer coefficients and an integer Gram from the
   prime theorem. For example, choose lambda=1+1/q with a prime q that
   does not divide a nonzero coefficient of f_ell+r^2; the corresponding
   coefficient of the scaled quartic is noninteger. The following clause
   already identified integer lambda as the intended integer case.
   [G-fields.tex:252](/workspace/minlp-notes/paper-exact-arithmetic/appendices/G-fields.tex:252)
   now transfers the monomial count and mathematical parts (b)–(d),
   states rational data in general and integer data for integer lambda,
   and charges construction and coefficient lengths to the supplied
   rational scale's binary length. The displayed curvature Gram and
   functional identity remain valid. Accepted at hash 0c4ddf55 below.

4. **A fixed selector versus the minimum-norm selector — resolved.** The
   summary following prop:points-selector said a fixed selector at
   constant accuracy decides Square Root Sum. The proposition itself
   supplies the easy fixed optimizer (z*,1) in both cases; it is the
   minimum-norm selector, with last coordinate 0 or 1, that decides the
   source problem. A fixed selector in def:models-points need only select
   the same optimizer at every precision. At
   [02-points.tex:495](/workspace/minlp-notes/paper-exact-arithmetic/sections/02-points.tex:495)
   the text now says the minimum-norm selector at accuracy 1/4 and that
   requiring minimum norm strengthens the output contract. The repaired
   summary matches the actual quantified proposition. Accepted at hash
   9255c3b5 below.

## Mathematical interfaces that survive the review

**Numerical outputs and exact decisions.** The global point theorem
charges numerical degree, evaluates sparse affine compositions without
expanding them, and selects minimum norm in the original coordinates.
Thin domains are reduced before ambient Hessian positivity is inferred.
The shared value interface returns an exactly feasible rational witness
and a lower bound; the upper and recourse arguments use both outputs
under its actual encoding contract. A small objective gap is not promoted
to a small point error without an effective modulus. The box-convex
quartic examples therefore do not contradict the global or cubic point
theorems.

The exact upper bound uses globally supplied strong curvature, explicit
unary or polynomially bounded numerical degree, and positive-denominator
circuit arithmetic. The one-block separation argument needs only a real
singleton projection and does not assume the complex critical set is
finite. The repaired numerical prose identifies an upper bound for all
six relations, with matching classifications restricted to strict and weak
order tests of certified quartics and their cubic gradient maps. Equality
remains an upper bound only. The min-sign argument needs the nonvanishing
auxiliary signal and its squared bound, now exactly what the compiler
statement supplies.

The rounded-cut warm start uses the queried center on oracle acceptance
and cuts preserving its fixed inner ball. This is the specific GLS
contract recorded as cleared by the literature lead; it does not follow
from an arbitrary approximate-membership output. The actual repaired
Appendix A prints this alternative. The optional JPT separation remark
was removed, so it creates no remaining source obligation.

**Constraints and arithmetic models.** General active-mask verification
stays unambiguous and co-unambiguous. A unique chart solution does not
provide a deterministic method to discover the chart. The ordinary
candidate lists contain all optimal integer blocks, including ties;
their construction is separated from exact selection between fiber
values. Product-fiber comparisons use the promised curvature and do not
assert a full joint positive definite Hessian Gram for an additive sum.
The rank method remains Las Vegas with expected work. The adaptive sign
compiler handles a clocked deterministic Boolean computation, one bit
per instance; it neither determinizes these randomized methods nor
collapses FPT or unambiguous work to an ordinary polynomial-time solver.

The expanded one-field QP result in Appendix J does not fill the open
Section 05 interface. Its algebraic coefficients and common field are
expanded input with charged degree and height, while Section 05 needs
polynomially many arithmetic operations for Taylor QPs whose Hessians are
shared circuits. The manuscript keeps these models and conclusions
separate. Its fixed-matrix LP contract also remains polynomial in the
rational constraint-matrix encoding, rather than a claim of strongly
polynomial LP for arbitrary matrices.

**Optimizer and certificate representations.** One-real-conjugate
coordinates concern rational polynomial singletons or unique
unconstrained convex minimizers. They do not restrict all constrained
optimizers. The sharp degree maxima through dimension five retain their
rational quadratic-square, unique-zero, nondegenerate-Hessian and global
convexity hypotheses. The cyclic condition-number bound is local to the
optimizer. Its supplied dense Hessian Gram is counted in
L=O(n^4 log n), so the printed expanded-output bound is correctly
2^{Omega((L/log L)^(1/4))}, not exponential in L.

Rational circuits describe rational outputs; root gates or explicit
algebraic inputs are used for irrational coordinates and tower
certificate coefficients. Joint field degree is distinguished from
coordinate degree and from coordinatewise algebraic description length.
Hessian Grams, polynomial Grams, maximal-rank optimal Grams, exposing
matrices and moment matrices have separate contracts. A positive
semidefinite Gram over a general real field is not silently factored
into squares over that field. The field proofs handle the two claims
separately. Interior and maximal-rank height bounds are not promoted
to all positive semidefinite Gram matrices.

The rational descent criterion is an abstract theorem under its printed
vanishing-space hypotheses. The finite cyclic stationary-space ranks
remain finite diagnostics, not a uniform application. The restored
minimal-dimension and qualitative finite radial-order arguments remain
actual proofs in E and H; neither is replaced by a diagnostic or
unquantified real-SOS existence assertion.

**Recourse.** I reconstructed the entire chain in Section 10 and I:
corner/secant cell bounds, two-pass pruning, all-scale count, finite-law
transfer, growth tail, cap accounting, exact selector fallback, supplied
convexifier completion, fixed cubic face kernels, neighboring tilts,
bounded-height lattice margins, and regularized residual completion.
The fallback factor is base-only; sampled coefficient length and q enter
polynomially. The finite-grid event bounds include ties and exact
relations, and one random factor controls all precisions. The count uses
the weak first-moment estimate in every core dimension, not the
growth-only moment that fails above dimension two.

Every ordinary branch and fallback approximates the same lexicographic
core and minimum-norm residual. Completion runs on the fixed original
domain or on an exactly certified core face, so approximate-core
substitution is not assumed to preserve residual selection. The lattice
test charges the supplied approximation length and clips to the unit
box. The quadratic completion first reduces thin fibers to their affine
hull. Empty residual spaces and zero restricted Hessians have explicit
branches. Rational margins and tolerance schedules remain computable
with polynomial encoding length. The numerical smoothing factor uses
the printed coordinate curvature bound; larger matrix bounds used for
margin probabilities enter only through bit lengths. V1–V5 and RQ1–RQ4
retain their unconditional contracts under the printed promises.
Quartic recourse and unsupplied coupled cubic completion remain
distinct open extensions.

## Contribution and source precision

The current framing credits the established Newton/separation/division
architecture, convex value approximation, exact conic hardness, SOS
descent, classical topology and algebraic sampling. It identifies the
added input restrictions, effective constants, fixed-selector outputs,
certified realizations, field restrictions and format bounds. The sign
compiler's classical numerical ingredients are credited and it carries
no priority claim. Hesse's comparison remains explicitly version-1,
unary-degree, nonempty-domain and finite-value where needed, with an
objective-gap output rather than a distance output.

This review found no additional precise primary-source obligation beyond
the root's existing literature queue. I accepted supplied verified
contracts for the cited tools, without independently retrieving the
sources. Bibliography completion, exact pinpoints and novelty assessment
must be reconciled with the literature lead's final inventory. In
particular this report does not infer novelty from a missing search hit.

## Snapshot and required follow-up

The hash snapshot below was collected at 20:36 UTC, with the repaired G
and 09 versions refreshed afterward. Sections 00/01/11 already include
prospective Appendix L framing and remain live for its final alignment.
At this snapshot main.tex includes A–K and the actual L file is absent.
The Appendix L summaries and their source/representation promises are
therefore pending, not accepted on the strength of an author plan.

The required follow-up is bounded: inspect the actual completed L and
its two independent proof reviews, reconcile its common-field,
finite-infimum, attainment, cone and mixed-integer interfaces with J,
the general input models and 00/01/11, verify the final inclusion in
main.tex, and refresh changed-file hashes. The separate coverage audit
owns the 97-row locator reconciliation. No prior exclusion of Q13–Q14
is adopted here.

```text
2667db36eb277b2669e8a0f5303dbfad3178763fc9f9638a692c360d98db4224  main.tex
1eb51a834c6285ec54212db5dffc0e85c7d0c59a131df32cd7741cc2a273ebf8  macros.tex
bd6215f3664c6c0e84155117d9dd0ee6fb74ba211bad0549c909105971a4871c  sections/00-introduction.tex
2effe216d08891db6ec5dea8ff6ba839c82273ef64df43d628a51840ff33e34f  sections/01-models.tex
9255c3b578fbef9981d96873db3effe3a0f65345fcab796bbed3e16d1f88e010  sections/02-points.tex
0db409d6a3b1e406e5e882d51311fb2df15ec345b23bea4667d61eaf7f6c2ee5  sections/03-upper.tex
0673ebfc72cfd606b7ce7d3f35d6e027520fa59188f4540b5c657f69b7ebd50e  sections/04-reductions.tex
78e9d62b533d19edabf1b4c144ccf8f75b2e1153b95c37e37c227edccff8572e  sections/05-constraints.tex
add45cc7abe70cba732e2c35b0f77ada4391e4c9c04663fc8247d6cb2ab82967  sections/06-algebraic.tex
59d80f97d0d99e05972c70ed37e1f56bf3effcb28621991db3f659bb6cd77901  sections/07-heights.tex
e2d740662a25da2d08bbccc6349411e417219f18e8b339891a0975e94f541b81  sections/08-fields.tex
d54888338ae9d221dfe9f0176fa9f2078a40e67c57686345a1147a09916afb34  sections/09-certificates.tex
b70d6f940a2df502ce61b5e4168ce1d7a3dadf59ced7244a17ea90e1299543b4  sections/10-recourse.tex
3d6c17ea2138af5ebf84a4dd7157ed5853a8f6bb990f70e1164e68111b6361bd  sections/11-discussion.tex
cb18f71fbfdfa85608984cc27f003306081105a5cf4a45baccfd02c822429bf7  sections/abstract.tex
e0a65e32b8d02c2b30d29882c71c37d8f781388a73aa53bbc13dba9fbad5269d  appendices/A-upper.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
0469412f5fc0bb8a9122329e673a30690a2c6ddf9eb577f3844e7b39f04bde90  appendices/C-points.tex
412eed3537513220a6b9249d0b693ede06de4657dee4c88f15ede03d00e06607  appendices/D-constraints.tex
a55ecca962308f61f3bf882af9fde23ab8f736a830ac83f0290052a2644d1f43  appendices/E-algebraic.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
0c4ddf55ba158ccd8c3857002eaea8805d15373d183f46b785777d50117cfeb1  appendices/G-fields.tex
37ca5a03d9cbb382b9ffe327ab6894e3b43664f9a2c9e405527a37fa47f1a7c5  appendices/H-certificates.tex
f4c21d1ad36fac74449315f3b4a20c4c1652e41e50797e657796c8b0e526d155  appendices/I-recourse.tex
21361c5eb3eefa2f4decf1ae3c6b3a08755ba1cb59a4d77873a08f341d4aae4a  appendices/J-quadratic-contrast.tex
ed88ea5a7c14d38370861141adb3a613a41f7e2cfd4fef42ef663af098568b82  appendices/K-boundaries.tex
```

## Targeted checks actually run

Read-only commands were `pwd`, `rg --files`, scoped `rg`, `cat`, `sed -n`,
`nl -ba`, `tail`, `wc -l`, and `sha256sum` on the named manuscript and
evidence files. The wall-clock tool supplied the snapshot time. After
writing this owned report, I ran a whitespace check of this file only.
The command was `git diff --no-index --check /dev/null
paper-exact-arithmetic/evidence/reviews/integration-r1.md`: it printed no
whitespace diagnostics; status 1 is the expected difference from an empty
file, not a failed whitespace check.
There was no compilation or executable mathematical check and no CI
inspection. These are local review checks, not CI results.
