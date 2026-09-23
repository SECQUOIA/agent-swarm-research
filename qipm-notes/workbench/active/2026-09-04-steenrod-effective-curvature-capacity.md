# Steenrod's plane-field theorem forces a near-full cone block

Status: Proved; primary-source verified; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Setting

Under the hypotheses of the
[global smooth-saturation theorem](2026-09-04-global-smooth-saturation-topology.md),
put

\[
 n=N-1,\qquad s=\rho(N)-1.
\]

Discard any zero-rank factors and let \(k\) denote the number of remaining
curvature-carrying factors.  Curvature-budget saturation gives a continuous splitting

\[
                  TS^n=\bigoplus_{i=1}^k E_i,\qquad
                  r_i:=\operatorname{rank}E_i=(m_i-2)_+,
                  \qquad \sum_i r_i=n.                          \tag{1}
\]

Here \(s\) is the span of \(S^n\), the maximum number of pointwise
independent tangent vector fields.

The later
[saturated-factor submersion theorem](2026-09-04-saturated-factor-submersion-obstruction.md)
uses the integrability of the factor maps, beyond the abstract splitting
(1), to exclude every rank-one block when \(n\geq2\).  The results below
remain relevant for ranks at least two and as sharp restrictions on the
tangent-bundle splitting itself.

## Plane-field and subset-sum obstruction

Steenrod's plane-field theorem says that, when \(2r\leq n\), \(S^n\)
admits a field of tangent \(r\)-planes if and only if it admits a field of
tangent \(r\)-frames.  Therefore every tangent subbundle \(E\subset TS^n\)
with

\[
                         0<\operatorname{rank}E\leq n/2
\]

forces

\[
                         \operatorname{rank}E\leq s.             \tag{2}
\]

The theorem does **not** say that the given \(E\) is trivial; it says that
the existence of \(E\) forces the existence of some trivial subbundle of
the same rank.

Apply (2) not only to one \(E_i\), but to the direct sum over an arbitrary
subset \(I\).  Writing \(r_I=\sum_{i\in I}r_i\), one obtains the exact
combinatorial restriction

\[
       \boxed{\quad 0<r_I\leq n/2\ \Longrightarrow\ r_I\leq s.\quad} \tag{3}
\]

Thus the rank multiset of any globally smooth saturated cone factorization
has no subset sum in the forbidden interval

\[
                              (s,n/2].                           \tag{4}
\]

This is much stronger than applying Adams's theorem only to line factors.

## Near-full-block theorem

Suppose

\[
                              s<n/3.                             \tag{5}
\]

Then (1) has a unique rank \(r_*>n/2\), and

\[
                              r_*\geq n-s.                       \tag{6}
\]

To prove this, suppose first that every \(r_i\leq n/2\).  Order the
summands arbitrarily and take the first partial sum that exceeds \(n/2\).
The preceding partial sum is at most \(n/2\), so (3) makes it at most \(s\).
The newly added summand is also at most \(s\) by (3).  The new partial sum
is therefore at most \(2s\).  Its complementary subset has rank below
\(n/2\), so (3) makes that rank at most \(s\); equivalently, the new partial
sum is at least \(n-s\).  Thus \(n-s\leq2s\), contradicting (5).  (If the
complement is empty, the stronger inequality \(n\leq2s\) gives the same
contradiction.)  Hence one summand has rank greater than \(n/2\), and it is
unique.  The direct sum of all other summands has rank \(n-r_*<n/2\), so
(3) gives \(n-r_*\leq s\), proving (6).

Since saturation identifies \(m_i=r_i+2\) for every positive-curvature
factor, (6) gives the cone-block lower bound

\[
                    \boxed{m_*\geq N+2-\rho(N).}                \tag{7}
\]

Consequently, whenever

\[
 \rho(N)-1<\frac{N-1}{3},
 \qquad d<N+2-\rho(N),                                         \tag{8}
\]

there is no globally \(C^2\), curvature-saturated slack factorization over
proper cone blocks of dimension at most \(d\).

This is an almost-unsplitness theorem.  The factorization may have many
other blocks, but together they can carry at most \(s=\rho(N)-1\) curvature
directions; one block must carry all remaining directions.

The Radon--Hurwitz formula shows that the first condition in (8) holds for
every

\[
                         N\geq3,\qquad N\notin\{4,8,16\}.       \tag{9}
\]

Indeed, write \(N=u2^a\) with \(u\) odd.  If \(u\geq3\), then
\(\rho(N)\leq2^a\), which gives
\(\rho(N)-1<(N-1)/3\).  If \(u=1\), direct calculation gives the three
exceptions \(2^2,2^3,2^4\), the inequality holds for
\(a=5,6,7,8\), and each increase \(a\mapsto a+4\) multiplies \(N\) by
\(16\) while adding only \(8\) to \(\rho(N)\).  Thus (7) holds in every body dimension \(N\geq3\)
except \(4,8,16\).

The elementary estimate

\[
                         \rho(N)\leq2\log_2N+2                  \tag{10}
\]

also follows directly from that formula.  Hence every globally smooth
saturated factorization outside the three exceptions contains a block with

\[
                         m_*\geq N-2\log_2N.                    \tag{11}
\]

In particular, no fixed-dimensional, polylogarithmic-dimensional, or more
generally \(d=o(N)\) cone-block dictionary can support such a global smooth
saturated factorization for all sufficiently large \(N\).

The rank bound is sharp as a statement about tangent-bundle splittings.
Adams's maximal \(s\)-frame gives a trivial rank-\(s\) tangent subbundle;
taking its orthogonal complement gives

\[
                         TS^n\simeq\mathbf1^s\oplus F^{n-s}.
\]

Thus the ranks \(s\) and \(n-s\) attain (6) whenever \(0<s<n\); at the
endpoints one summand has rank zero.  No stronger lower bound on the largest
summand can follow from tangent-bundle topology alone.  This does not assert
that a cone slack factorization realizes this splitting.

## Strict regularity penalty beyond saturation

The dominant-block theorem also strengthens the integer curvature budget.
Suppose \(N\geq3\), \(N\notin\{4,8,16\}\), and every block has dimension at
most

\[
                            d<N+2-\rho(N).
\]

For any exact slack factorization with the global \(C^2\) selections in the
parent theorem, the universal curvature bound says
\(S:=\sum_i(m_i-2)_+\geq N-1\).  Equality would invoke (7) and require a
block larger than the cap.  Since \(S\) is integral,

\[
                              \boxed{S\geq N}.                   \tag{12}
\]

Thus, if \(k_+\) and \(M_+\) denote the number and total dimension of the
positive-capacity blocks, then

\[
 k_+\geq\left\lceil\frac{N}{d-2}\right\rceil,\qquad
 M_+\geq N+2\left\lceil\frac{N}{d-2}\right\rceil,\qquad
 \nu\geq2\left\lceil\frac{N}{d-2}\right\rceil.                 \tag{13}
\]

The last inequality is for any logarithmically homogeneous
self-concordant barrier on the ambient cone product, including a coupled
barrier.  A bi-contact-regular lift supplies the global selections, so
(12)--(13) extend the earlier lift-level one-unit granularity penalty from
odd \(N\) to every \(N\geq3\) outside \(4,8,16\), under the displayed
Radon--Hurwitz-dependent cap.

## Effective capacity and factor/barrier lower bounds

Let the block dimension cap be \(d\geq3\), and put \(c=d-2\).  If

\[
                              c\leq n/2,                         \tag{14}
\]

then every positive \(r_i\leq c\) falls under Steenrod's theorem.  Thus,
when \(s>0\),

\[
                 r_i\leq c_{\mathrm{eff}}:=\min\{c,s\},
 \qquad
                 k\geq
                 \left\lceil\frac{n}{c_{\mathrm{eff}}}\right\rceil.
                                                                    \tag{15}
\]

If \(s=0\), no positive summand is possible under (14), so the saturated
global splitting is impossible; one must not interpret (15) by dividing by
zero.

For a product of the \(k\) curvature-carrying proper cones, (15) also gives
the representation-size and barrier consequences

\[
 M\geq n+
     2\left\lceil\frac{n}{c_{\mathrm{eff}}}\right\rceil,
 \qquad
 \nu\geq
     2\left\lceil\frac{n}{c_{\mathrm{eff}}}\right\rceil,        \tag{16}
\]

using \(M=\sum_i(r_i+2)=n+2k\) for the positive factors and the established
coupled product-barrier lower bound \(\nu\geq2k\).  Extra zero-curvature
factors only increase these quantities.

Compared with the unrestricted curvature count
\(\lceil n/c\rceil\), global smoothness replaces the nominal per-block
capacity \(c\) by at most the sphere span \(s\).  If

\[
 \left\lceil\frac{n}{\min\{c,s\}}\right\rceil
 >
 \left\lceil\frac{n}{c}\right\rceil,                            \tag{17}
\]

then a universally count-optimal saturated lift cannot have one global
\(C^2\) choice of its primal and dual slack factors.

When (5) also holds, the near-full-block theorem is stronger: any cap
\(c\leq n/2\) is impossible outright, since (7) requires a rank greater
than \(n/2\).

## Two-block and equal-block corollaries

For a two-block saturated splitting \(n=r_1+r_2\), the smaller rank is at
most \(n/2\), so (3) gives

\[
                 \min\{r_1,r_2\}\leq s,\qquad
                 \max\{r_1,r_2\}\geq n-s.                      \tag{18}
\]

Thus one of the two cone dimensions is at least \(N+2-\rho(N)\), without
needing assumption (5).

If \(k\geq2\) blocks all have the same positive curvature rank \(r=n/k\),
then \(r\leq n/2\), and therefore

\[
                              r\leq s.                           \tag{19}
\]

Combined with the Euler obstruction, \(n,k,r\) must all be odd.  This rules
out equal-rank globally smooth saturated decompositions whenever the common
rank exceeds the Radon--Hurwitz span, even when stable \(KO\)-theory is
silent.

## Verification and literature boundary

The plane-field input was checked in a primary paper:
Dibag, [*Almost-complex substructures on the
sphere*](https://doi.org/10.1090/S0002-9939-1976-0423248-5),
Lemma 2.1, states explicitly that if \(2r\leq n\), then \(S^n\) admits a
field of \(r\)-planes if and only if it admits a field of \(r\)-frames.  It
cites Steenrod, *The Topology of Fibre Bundles*, Theorem 27.16.  Equality
\(2r=n\) is included.  Adams's sharp value \(s=\rho(N)-1\) is from
[*Vector Fields on Spheres*](https://doi.org/10.2307/1970213).

An independent hostile audit verified the direct implication (2), including
the equality case, the distinction between existence of frames and
triviality of the given subbundle, the subset-direct-sum argument (3), the
partial-sum proof of the dominant block (6)--(7), and the
Radon--Hurwitz exception list (9), the strict integer and
factor/dimension/barrier penalty (12)--(13), and the
effective-capacity/count formula (15).  It found no mathematical error.

The topology is classical.  A targeted search found no source connecting
Steenrod's plane-field theorem to saturated cone slack factorizations,
near-full cone blocks, or self-concordant barrier parameters.  As in the
parent topology theorem, all conclusions concern a single global \(C^2\)
choice of primal and dual slack-factor maps.  They do not rule out the cone
lift itself; nonsmooth selections and chart changes remain valid escape
routes.

The same conclusions apply whenever another theorem has already produced
the continuous direct-sum splitting (1).  In particular, they transfer
verbatim to the conditioned robust-saturation theorem on the event that its
projection fields remain complementary, and to any contact-regular lift
sheet that globally induces the required factor selections.  Those results
retain their own conditioning, regularity, and sheet hypotheses.
