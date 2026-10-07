# Algebraic manuscript review, round 1

Date: 2026-10-05. This is an internal independent mathematical review of the
actual `sections/06-algebraic.tex` and `appendices/E-algebraic.tex`, with their
interfaces to Sections 01, 04, 07 and 08. The latest reread at the time of this
report found 676 lines in Section 06 and 2003 lines in Appendix E. The author
was still revising these files, so line numbers identify that snapshot.

I read BRIEF.md, DECISIONS.md, the macros and model definitions, and the
prewriting reports, but reconstructed the actual manuscript proofs rather than
treating earlier favorable audit labels as evidence. Two delegated independent
reviews covered the degree bounds/five-variable proof and the cyclic,
binomial-network and SOS-length proofs. The fixed bivariate matrices were
checked manually in that subreview. No mathematical scripts, computational
experiments, literature searches, project-wide checks, compilation or CI
checks were run. Tools were used only to read the assigned text and write this
report.

## Verdict

I found no unrepairable mathematical defect in the claimed algebraic
construction theorems. The singleton characterization, quantitative full-Gram
assembly, power-coordinate dimension bound, cyclic construction, minimum real
SOS length, binomial-network bound, sharp degrees through dimension five,
univariate obstruction and circuit alternative, and quadratic graph lift
survive reconstruction. The important remaining work is to correct a few
explanatory claims and confirm the exact imported contracts through the root's
Luna literature agent. In particular, the sharp degree 21 argument needs the
singular local-complete-intersection scope of AG5, not merely a smooth-variety
version of residual intersection.

The original dense-input length error, the false unrestricted AG3 contract,
and the omitted degree-two-surface import have been repaired in the latest
snapshot. They are recorded below because they materially affected the
mathematical scope before repair.

## Remaining findings

### R1 — Medium: the rational residual hypotheses force algebraicity

Location: `sections/06-algebraic.tex:309`.

The sentence that the realization point “need not be algebraic” is false under
the lemma's hypotheses. The bound
`sum_j b_j b_j^T >= nu^2 I` gives a choice of n rational residuals with
nonsingular Jacobian at p. Thus p is an isolated real common zero. A small
rational box isolates p; the rational system consisting of those equations
and the box has exactly one real solution. Real-algebraic transfer, already
used in Appendix E's one-real-conjugate proof, makes that solution algebraic.

Repair: say that **no algebraic representation of p is required**, and that p
need not be known or rational. The formal lemma can remain quantified over
p in R^n; its hypotheses enforce algebraicity. This correction does not change
the construction or any downstream reduction.

### R2 — Low, proof completeness: the curvature bound without n needs its own estimate

Locations: `sections/06-algebraic.tex:297` and
`appendices/E-algebraic.tex:407`.

The main text says that the factor n can be removed from the epsilon condition
for curvature part (b). That stronger assertion is true, but the printed proof
of (b) invokes the full-Gram Schur bound, which contains n.

A short direct proof completes the assertion. Write
Phi = g^2 + epsilon sum_j r_j^2 and s = ||u|| after centering at p. The degree-two
part has Hessian at least 2 epsilon nu^2 I. The degree-four part has Hessian at
least (4 mu^2 - 4 epsilon m) s^2 I, hence at least 2 mu^2 s^2 I. The norm of the
cubic Hessian is at most 12 epsilon (Lambda + m beta) s. Consequently

    Hessian Phi >= [2 epsilon nu^2 + 2 mu^2 s^2
                    - 12 epsilon (Lambda + m beta) s] I
                >= (3/2) epsilon nu^2 I

when epsilon <= nu^2 mu^2 / [36 (Lambda + m beta)^2]. Add this estimate or remove
the extra explanatory assertion. The theorem as stated with n is already proved.

### R3 — Low: the corrected graph explanation still excludes a permitted case

Location: `sections/06-algebraic.tex:645`–646.

The revised identity g_hatp(w_*) = f(p) = 0 is correct. Its new parenthetical
that g_hatp's zero set “is an ellipsoid, not a point” is too absolute. At
hatp = p, which is permitted when p is rational, the quadratic has zero
gradient at w_* and positive definite quadratic part, so its zero set is the
singleton w_*.

For an explicit example, f(x)=x^2+x^4 has full Hessian Gram diag(2,12) and
p=0. The graph lift at rational center a is

    g_a(y,z) = (1+2a^2)y^2 + z^2 - 2a^2 z.

For a != 0 its zero set is an ellipse through (0,0); for a=0 it is the single
point (0,0). Repair to “its zero set can be an ellipsoid” or omit the
parenthetical. The graph theorem and assembly use only exact vanishing, not
uniqueness of the exposing quadratic's zero.

### R4 — Low, substantive scope: convexity removes common real zeros at infinity

Locations: `sections/06-algebraic.tex:475` and 520.

The introductory sentence says convexity removes “the points at infinity.”
The proof removes common **real** zeros at infinity after flat-direction
reduction; complex base components can remain. For example,

    f(x) = (sum_i x_i^2)^2 + sum_i x_i^2

is globally strongly convex with a nondegenerate zero. Homogenizing its
rational square factors gives x_0 x_i and sum_i x_i^2, which have common
complex points at infinity for n >= 2. Qualify the sentence with “common real
zeros.”

Also replace “a complete intersection of n of the quadrics” at line 520 with
“a complete intersection of n rational linear combinations of the square
factors.” The first bound selects factors, but the second bound and degree-21
proof require generic combinations. The appendix uses the correct objects.

### R5 — Low: qualify the cyclic integer-magnitude claim

Location: `appendices/E-algebraic.tex:891`–892.

“All integers involved have magnitude polynomial in n” is correct for the
denominator-clearing and scaling integers in this paragraph. It is false for
the family as a whole: d_n and e_i have exponential magnitude and O(n) bits.
Use “All integers used in this denominator-clearing and scaling step…” The
coefficient-bit conclusion itself is sound.

### R6 — Low: the power-coordinate explanation needs the normalization

Location: `sections/06-algebraic.tex:336`–338.

The theorem accepts any rational multiple of the minimal polynomial, including
one with negative leading coefficient. Its explanation calls
(T-alpha)P(T) nonnegative and P(T)/(T-alpha) positive, which is false for that
negative multiple. The appendix correctly replaces P by the monic P_1 before
using the positive root product. State “after normalizing P to have positive
leading coefficient” in the paragraph, or use and define the monic P_1 there.
The formal proof and algorithm are sound.

## Repairs confirmed during the review

- **Certified input length:** Section 06 lines 396–402 now includes the full
  canonical Hessian Gram. Its order is n+n^2, and the matrix encoding in
  Section 01 sums the bit lengths of all entries. Thus
  L=O(n^4 log n) is a safe bound, and expanded polynomial output remains
  at least 2^{Omega((L/log L)^{1/4})}. The previous O(n^2 log n) length and
  square-root exponent did not apply to the stated dense certified input.
- **Cayley–Bacharach contract:** Appendix E lines 1194–1208 now restricts the
  residual formula to N>=3 and 0<=t<=s, and records the actual used range.
  The previous all-N/all-t statement was false: for N=1, a reduced quadric
  Z={a,b}, Gamma={a}, R={b}, s=0, t=2, its two sides are 1 and 2. The corrected
  range covers every application in this appendix.
- **Surface import:** Appendix E lines 1230–1234 now includes the general
  minimal-degree inequality deg X >= r-dim X+1. Lines 1645–1655 explicitly
  deduce that an integral degree-two surface spans P^3 and is a quadric, and
  exclude its rank-three case by the real singular vertex. The earlier AG6
  stated only the curve result.
- **Graph vanishing:** Section 06 lines 644–645 now says g_hatp(w_*)=0 exactly.
  The earlier wording “vanishes exactly at w_*” falsely claimed a singleton
  zero set for every rational center; R3 describes the remaining narrower issue.

## Proof reconstruction and readiness by topic

1. **One real conjugate.** Appendix E lines 302–335 proves algebraicity by
   transfer, discards inactive convex inequalities by the short-segment
   argument, and maps p to a second real zero under every real embedding.
   The joint field therefore has exactly one real embedding and odd degree.
   For a coordinate subfield, the odd extension degree and a primitive-element
   polynomial give a real extension of every real embedding. This correctly
   proves exactly one real conjugate for each coordinate. Unique unconstrained
   convex minimizers reduce to the real zero set of the squared gradient. The
   constrained sqrt(2) example correctly limits the claim's scope.
2. **Canonical full Hessian Gram and assembly.** The 4 g_0 T constant term,
   cross-block indices, tensor ordering, polarization, and translation
   covariance are exact matrix identities. The contractions in E54–97 prove
   covariance without relying on equality only on rank-one tensors or on a
   coefficient projection. In the assembly lemma, indefinite T_j tensor T_j
   terms are retained through Xi(T_j)>=-4I. The centered constant, quartic and
   cross bounds give the printed Schur complement and Gram margin. The direct
   unshifted matrix is rational, positive definite and computable from the
   supplied factors; no second approximation of p is needed.
3. **Bivariate integer example.** The vanishing identities, the elimination
   to x(x^3-2), the exclusion of (0,0), the rational-root obstruction and the
   4124I global Hessian estimate are sound. A delegated manual check verified
   every printed entry of Gamma_F, the complete N_F polynomial identity and
   all six diagonal-dominance margins, including the three Gram-kernel
   relations between full-basis monomials. The identity supplies the promised
   rational Hessian-square certificate.
4. **Power coordinates and dimension.** The recursion gives a positive
   definite Gram of the product of nonreal-root quadratic factors. The
   difference matrix produces an exposing PSD matrix with the exact power
   vector as its kernel. Root separation keeps the approximation precision
   polynomial in dense-input length. The rational orthogonal projection
   preserves exact vanishing. The residual determinant is P_1'(alpha)/kappa^n.
   The converse correctly substitutes the moment curve and uses P_1^2 | h,
   obtaining 2d<=4k and k>=(d+1)/2 because d is odd. The three-ellipsoid pencil,
   rational triangle and positive barycentric weights also check out.
5. **Cyclic construction and output formats.** The exact degree is
   d_n=(2^{n+1}-(-1)^{n+1})/3, with Eisenstein irreducibility of T^{d_n}-2.
   The anchored energy gives the unique real solution and polynomial bounds
   on the Jacobian and exposing quadratic. Weight approximation never expands
   a degree-d_n polynomial. The rational rank-one square-root identity
   compresses the initial n+2-square assembly to n+1 rational squares, and
   the printed integer clearing preserves that count. The translated
   polynomial 2(T-1)^{d_n}-1 is primitive and irreducible, has every coefficient
   nonzero, and has total length Theta(d_n^2). This distinguishes ordinary
   sparse/dense output from radical or shared-circuit output. The optimizer
   Hessian calculation gives 65540 n^2 < 65600 n^2; no uniform neighborhood
   condition bound is claimed. Large optimizer field degree does not force
   a large SOS coefficient field: this family has rational square factors.
6. **Minimum real SOS length.** The proof uses exactly the stated global
   convexity, quartic degree, zero-value and nondegenerate-Hessian hypotheses.
   Its flat-direction argument makes each q_2 invariant, and arbitrary signed
   fiber coordinates force B^T q_2=0. The minimizing fiber graph is therefore
   affine. After elimination, the square quadratic map has one regular zero
   and a proper leading part. The uniform growth bound makes the homotopy
   proper; its degree is both +/-1 and even, a contradiction. The sharpness
   and counterexamples to omitted hypotheses are correct.
7. **Binomial-network bound.** The Smith-normal-form lattice index is the gcd
   of the rooted directed tree counts. Complex solutions are characters of
   the quotient; unique real solvability forces its order odd. The
   non-Eulerian and interlace-polynomial inequalities give the printed bounds.
   The exposing converse correctly counts positive diagonal contributions,
   derives stationary positive flow and strong connectivity, and uses the
   corank-one PSD kernel to get uniqueness. It remains a theorem about this
   binomial exposing method, not all rational SOS singletons.
8. **General rational-SOS and sharp low-dimensional degree bounds.** The
   nonsingular quadratic Jacobian, weighted Bezout count and oddness give
   D<=2^n-1. Rational flat-direction reduction preserves the field and rational
   square representation. At the near-extremal degrees, the residuals of
   lengths one and three yield the required second real zero through the
   corrected Cayley–Bacharach contract. The cyclic examples attain 3,5,11,21
   in dimensions 2,3,4,5. All bounds explicitly retain the rational-SOS and
   nondegenerate-zero hypotheses.
9. **Five variables.** The finite residual proof constructs a nondegenerate
   filtered Gorenstein pairing. For the quotient by Ann(q_R), the image of
   linear polynomials is totally isotropic, so 2v<=ell, while a finite
   quadratic complete intersection in its span gives ell<=2^{v-1}. For
   1<=ell<=9 these force ell=8; real local-algebra parity instead makes ell
   odd. Separately, the weighted positive-base count limits the real-point-free
   components to the stated low-degree curves/surfaces. The conic, quartic CI,
   rational normal quartic, conjugate-plane/line and conjugate-conic cases all
   have quadratic sheaf generation and excess e>=10. The singular type
   (1,1,2,2) cases are reduced local complete intersections; degree comparison,
   unmixedness and generic multiplicity one justify their scheme equality.
   Perturbing the chosen quadrics preserves the D simple points, and AG5 then
   gives D<=22, contradicting odd D>=23. Thus the full base is finite and the
   finite-residual proposition gives D<=21. The finite and positive-base
   arguments are both necessary and both present.
10. **Univariate realization.** The three-region curvature proof, root-product
    bound and late choice of rational center are consistent. The dense-input
    construction outputs a polynomial-size shared circuit, not an expanded
    polynomial or a cheap exact evaluation oracle. The cubic lower-bound
    family is irreducible; its close nonreal roots and iterated scaled Markov
    inequality prove the stated degree bounds for a polynomial, a finite
    convex inequality system and a convex objective. The two-variable and
    quasiconvex quartic alternatives have the stated scope.
11. **Quadratic graph and interfaces.** Taylor integration gives the exact
    restriction g_hatp(y,(y_i y_j))=f(y). The duplication matrix and affine
    shear provide uniform positive quadratic-part bounds. The coefficient-sum
    derivative majorant is computable before choosing the approximate center.
    Graph residuals plus the quadratic gradient lift have determinant
    det Hessian f(p), and rational normalization gives the printed singular-value
    lower bound. Assembly produces N+1 rational squares and a rational full
    PD Hessian Gram in polynomial time, with minimum zero retained as a promise.
    The SOS-length theorem proves minimality. This matches the Taylor-SOS,
    strict-kernel and moment interfaces in Section 07 and the field arguments
    in Section 08. It does not promote separate-block Hessian certificates to
    a positive definite Gram on a full joint Hessian basis.

The bound without square factors was also checked: generic rational gradient
combinations give a smooth curve through each conjugate, f has a double zero
on it, and a small nonzero level splits it into two simple zeros. Weighted
Bezout gives D<=2*3^{n-1}-1. The bivariate rational descent argument correctly
uses the exceptional ternary-quartic classification rather than Hilbert's
real-SOS theorem. The explicit nonconvex degree-seven counterexample supplies
the stated boundary for global convexity.

## Exact external contracts for the root's Luna source audit

I did not search or independently verify source text. The following are the
contracts the mathematics actually uses, not an assertion that a citation's
label establishes them.

- **AG5, highest priority:** general five quadrics through a reduced,
  pure-dimensional lci Y in P^5 with I_Y(2) globally generated have finite
  residual outside Y, with sum of local lengths
  32 - integral_Y (1+2H)^5 cap s(Y,P^5), and the lci Segre class equals
  c(N)^{-1} cap [Y], including singular reduced type (1,1,2,2) curves.
  Current location: E1215–1229. A smooth-only contract is insufficient.
- **AG1/AG2/AG4/AG6:** hypersurface degree bounds, finite projective complete
  intersections and regular sequences, the quadratic Artin CI perfect
  pairings over Q, and the current general minimal-degree inequality plus
  the rational-normal-curve equality case. Current locations: E1182–1193,
  E1209–1214 and E1230–1234.
- **AG3:** the now restricted Cayley–Bacharach residual identity for N>=3,
  0<=t<=s, with schemes residual to one another. Actual nonreduced use has
  N>=4, t=2 and s-t=N-3>=1.
- **Scheiderer classification:** a rational nonnegative ternary quartic that
  is not rational SOS is a product of four distinct complex lines with no
  three concurrent. The proof needs this exact exceptional-form statement.
- **Numerical root subroutine:** deterministic certified simultaneous complex
  root approximation for square-free dense integer P, to 2^{-N_0}, in bit
  time polynomial in degree, coefficient height and N_0.
- **Network contracts:** matrix-tree minors count directed arborescences for
  loops and distinguished parallel arcs; BEST uses cyclic arc-sequence
  counting; the Euler-tour interlace polynomial has nonnegative coefficients,
  no constant term, q(1) equal to that circuit count, q(2)=2^m, and
  q(-1)=(-1)^rank(I+A) 2^{m-rank(I+A)}.
- **Topology and approximation:** Brouwer degree homotopy/local-Jacobian
  formulas, Sard regular values, the stated scaled Markov inequality, and
  the shared deterministic rational convex-value interface used to compute
  the graph lift's center. The proof supplies the properness, conditioning,
  rational boxes and fixed-degree sparse evaluation needed for these imports.

These contracts were sent to the root where gaps in their printed scope were
found. Once the remaining prose/proof-completeness repairs and source checks
are settled, I see no unresolved internal algebraic argument preventing the
section's use in a fully proved manuscript.

## Optional clarity only

AG2 at E1192 could say “does not vanish at **any** point of Z” to make the
nonzerodivisor condition unambiguous. This is separate from the substantive
findings above; the actual finite-residual proof chooses a linear form
nonzero at every point of Z.
