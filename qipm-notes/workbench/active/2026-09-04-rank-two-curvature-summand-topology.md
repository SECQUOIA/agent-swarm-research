# Rank-two curvature summands spend two vector fields

Status: Proved; targeted literature screen complete; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Use the hypotheses and notation of
[the global smooth-saturation theorem](2026-09-04-global-smooth-saturation-topology.md).
Thus a globally \(C^2\), curvature-budget-saturated slack factorization of a
positively curved \(N\)-body gives, on \(M\simeq S^{N-1}\),

\[
 TM=\bigoplus_i E_i,
 \qquad \operatorname{rank}E_i=r_i:=(m_i-2)_+ .                \tag{1}
\]

Let

\[
 a=\#\{i:m_i=3\},\qquad b=\#\{i:m_i=4\}.                      \tag{2}
\]

If \(N\geq4\), then

\[
                 \boxed{a+2b\leq \rho(N)-1}.                  \tag{3}
\]

Here \(\rho\) is the Radon--Hurwitz function, so that
\(\rho(N)-1\) is the maximum number of pointwise independent tangent vector
fields on \(S^{N-1}\).  The earlier line-factor bound counted only \(a\).
Equation (3) shows that a four-dimensional cone factor spends *two* units of
the same scarce vector-field budget.

Under the stronger factor-integrability hypotheses, the independently
audited
[saturated-factor submersion theorem](2026-09-04-saturated-factor-submersion-obstruction.md)
now excludes every three-dimensional block outright when \(N\geq3\).
Thus the \(a\)-term in (3) remains a correct tangent-bundle statement, but
is superseded for saturated factorizations that retain globally labelled
\(C^1\) primal and dual factors.  The rank-two conclusion for
four-dimensional blocks remains additional information.

For \(N\geq4\), every real line bundle on \(S^{N-1}\) is trivial.  Every rank-two
summand is orientable because \(H^1(S^{N-1};\mathbb Z_2)=0\).  An oriented
real two-plane bundle is the underlying real bundle of a complex line
bundle and is classified by its Euler/first Chern class in
\(H^2(S^{N-1};\mathbb Z)\).  This group is zero for \(N-1\geq3\).  Hence every
rank-two \(E_i\) is also trivial.  Their direct sum is a trivial
\((a+2b)\)-plane subbundle of \(TM\), and Adams's theorem gives (3).

The restriction \(N\geq4\) matters.  On \(S^2\), the tangent bundle itself
is a nontrivial oriented two-plane bundle.

## Consequences for bounded cone blocks

### Blocks of dimension at most four

If every curvature-carrying factor has \(m_i\leq4\), then saturation in (1)
makes all of \(TM\) a sum of trivial line and two-plane bundles.  Thus the
sphere is parallelizable.  Accounting separately for \(S^1\) and \(S^2\), a
necessary condition is

\[
                         \boxed{N\in\{2,3,4,8\}}.              \tag{4}
\]

For \(N=3\), one rank-two summand can be all of \(TS^2\), so this dimension
cannot be deleted from (4).  For \(N\geq4\), parallelizability leaves only
\(S^3\) and \(S^7\), hence \(N=4,8\).  This is a strict strengthening of the
all-three-dimensional-factor corollary: mixtures of three- and
four-dimensional factors are covered as well.

This is only a necessary condition for a globally smooth choice of slack
factors.  It neither constructs such choices in the four exceptional
dimensions nor rules out the underlying cone lifts in other dimensions.

### A forced supply of dimension-at-least-five blocks

Assume \(N\geq4\), all blocks have dimension at most \(d\), and saturation
holds.  The total curvature rank is \(N-1\), while (3) permits at most
\(\rho(N)-1\) of it to come from three- and four-dimensional factors.
Consequently

\[
 \sum_{i:m_i\geq5}(m_i-2)\geq N-\rho(N).                       \tag{5}
\]

For \(d\geq5\), the number \(h\) of factors of dimension at least five must
therefore obey

\[
             \boxed{h\geq
             \left\lceil\frac{N-\rho(N)}{d-2}\right\rceil}.    \tag{6}
\]

This restriction concerns the *composition* of a saturated factorization,
not just its total factor count.  When \(\rho(N)=O(\log N)\), almost all of
the curvature budget must be carried by blocks of dimension at least five.

For the especially sparse cap \(d=5\), write \(c=\#\{i:m_i=5\}\).  Equations
(1) and (3) give the sharper integer conditions

\[
 a+2b+3c=N-1,
 \qquad a+2b\leq\rho(N)-1.                                    \tag{7}
\]

These already rule out an infinite family.  If

\[
                            N\equiv6\pmod {12},                 \tag{8}
\]

then \(v_2(N)=1\), so \(\rho(N)=2\), whereas \(N-1\equiv2\pmod3\).
The first relation in (7) forces the nonnegative integer \(a+2b\) to be
congruent to \(2\pmod3\), hence to be at least \(2\); the second says it is at
most \(1\), a contradiction.  Therefore no globally \(C^2\) saturated slack
factorization over cones of dimension at most five exists in ambient body
dimensions \(N\equiv6\pmod {12}\).

For odd \(N>3\), the Euler-class obstruction is stronger: \(S^{N-1}\) is
even-dimensional, and its tangent bundle cannot split into two positive-rank
summands.  Thus a saturated factorization must have one curvature-carrying
factor of dimension \(N+1\); any cap \(d\leq N\) is impossible.

## Exact clutching formulation for higher ranks

There is a precise classical test for any proposed rank composition, though
it rapidly becomes a problem in unstable homotopy groups.  Put \(n=N-1\),
and let

\[
                     \tau_n\in\pi_{n-1}(SO(n))                 \tag{9}
\]

be the clutching class of \(TS^n\).  Since \(S^n\) is simply connected for
\(n\geq2\), all the positive-rank \(E_i\)'s in (1) are orientable.  Choose
their clutching classes

\[
                     \alpha_i\in\pi_{n-1}(SO(r_i)).            \tag{10}
\]

Choose orientations and hemisphere trivializations so that the direct-sum
orientation agrees with that of \(TS^n\).  Then (1) holds if and only if one
can choose the \(\alpha_i\)'s so that

\[
       \operatorname{blockdiag}_*(\alpha_1,\ldots,\alpha_k)
                         =\tau_n
       \quad\text{in }\pi_{n-1}(SO(n)).                        \tag{11}
\]

Necessity follows by clutching each summand over the two hemispheres.
Conversely, (11) says that their Whitney sum is isomorphic to \(TS^n\), and
transporting the summands through this isomorphism gives the splitting.
Thus (11), not stable \(KO\)-theory alone, is the exact remaining obstruction
for ranks at least three.

Stabilizing (11) only gives

\[
                  \sum_i [E_i]=[TS^n]=0
                  \quad\text{in }\widetilde{KO}(S^n),          \tag{12}
\]

because \(TS^n\oplus\mathbf1\) is trivial.  For odd \(n\), the group in
(12) is \(\mathbb Z_2\) when \(n\equiv1\pmod8\) and is zero when
\(n\equiv3,5,7\pmod8\).  Hence ordinary stable \(KO\)-theory is usually
silent: in the first case it only says that an even number of summands have
the nonzero stable class.  Ordinary characteristic classes are similarly
silent on proper-rank summands of an odd-dimensional sphere.  Stronger
general restrictions for rank at least three require genuinely unstable
information in (11), not merely a manipulation of Pontryagin or
Stiefel--Whitney classes.

One elementary equal-rank consequence is worth recording.  If \(k\geq2\)
positive summands all have rank \(r\), then \(n=kr\).  The Euler obstruction
forces \(n\) odd, so both \(k\) and \(r\) are odd.  Thus a globally smooth
saturated equal-block factorization with more than one factor can use only
an odd number of odd-capacity (equivalently, odd-dimensional) cone blocks.

## Literature boundary and scope

The topology in this note is classical.  Adams proved the sharp sphere span
in [*Vector Fields on Spheres*](https://doi.org/10.2307/1970213).
Classification of oriented two-plane bundles by the first Chern/Euler class
is standard; see Hatcher's open text
[*Vector Bundles and K-Theory*](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf).
Stong studied subbundles of tangent bundles from a cobordism viewpoint in
[*Subbundles of the Tangent Bundle*](https://doi.org/10.1090/S0002-9947-1974-0356102-0),
and Iberkleid studied cobordism representatives whose tangent bundles split
into line bundles in
[*Splitting the Tangent Bundle*](https://doi.org/10.1090/S0002-9947-1974-0348774-1).

A targeted title/keyword and citation search found no work connecting these
facts to curvature-budget saturation in cone slack factorizations.  The new
optimization consequence is the weighted bound (3), especially the cap-four
classification (4), forced-large-block bound (5)--(6), and cap-five infinite
family (8).  As throughout the parent theorem, these are obstructions to a
single globally \(C^2\) primal/dual factor selection on the full contact
manifold.  They are **not** nonexistence results for cone lifts, which may and
often do evade them through selection singularities or chart changes.

The independent hostile audit checked the orientation and rank-two bundle
classification, the Adams count, all exceptional low dimensions, the
Radon--Hurwitz and congruence arithmetic, the odd-sphere \(KO\) table, and
the equal-rank parity statement.  It found no mathematical error.
