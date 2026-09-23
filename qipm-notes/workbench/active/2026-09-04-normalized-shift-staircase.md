# A sharp query staircase for unit-normalized two-band shifts

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate-to-high on apparent novelty  

## Phase diagram

Fix \(\rho>1\), \(c>0\), and require a unit-normalized reusable block encoding
of \(I-H\) to error \(K\delta\) under

\[
 \operatorname{spec}(H)
 \subseteq[\delta,\rho\delta]\cup[c,1].
\]

Let

\[
 G_r(\rho)=
 \inf_{\substack{\deg P\leq2r\\P\geq0\ {\rm on}\ \mathbb R}}
 \max_{y\in[1,\rho]}|P(y)-y|
\]

be the thresholds from the adaptive lower-bound note.  For fixed \(K>0\), let

\[
 \ell(K)=\min\{j\geq0:G_j(\rho)\leq K\}.
\]

This is finite because \(G_j(\rho)\downarrow0\), and the exact formula below
shows that the decrease is strict.  The complete phase diagram
is

\[
 \boxed{
 Q_{\rm shift}=\begin{cases}
 \Theta_{\rho,c,K}(\log(1/\delta)),&\ell(K)=0,\\[2mm]
 \Theta_{\ell,\rho,c,K}
 (\delta^{-(2\ell-1)/(2\ell)}),&\ell(K)\geq1.
 \end{cases}}                                                \tag{P}
\]

Equivalently, for every fixed integer \(r\geq1\),

\[
 \boxed{
 G_r(\rho)<K<G_{r-1}(\rho)
 \quad\Longrightarrow\quad
 Q_{\rm shift}
 =\Theta_{r,\rho,c,K}
 \left(\delta^{-(2r-1)/(2r)}\right),}                        \tag{P_r}
\]

and the same exponent holds at \(K=G_r\).  For
\(K\geq G_0(\rho)=(\rho-1)/2\),

\[
 Q_{\rm shift}=\Theta_{\rho,c,K}(\log(1/\delta)).             \tag{P_0}
\]

Thus every threshold point joins the cheaper tier with no logarithmic loss.
The staircase exponents tend to one as \(K\downarrow0\).  Together with the
adaptive lower theorem, (P) is a complete all-coherent-converter phase diagram
for every fixed positive relative-error constant.

## Exact threshold formula and calibration

The constrained approximation problem has a closed Chebyshev solution.  Put

\[
 n=2r,\qquad m=\frac{\rho+1}{2},\qquad
 h=\frac{\rho-1}{2},\qquad z_0=\frac mh=\frac{\rho+1}{\rho-1}.
\]

For every \(r\geq1\),

\[
 \boxed{
 G_r(\rho)=h\max_{z\geq z_0}\frac{z-z_0}{T_{2r}(z)},
 \qquad
 P_r^*(y)=y+G_r(\rho)
 T_{2r}\!\left(\frac{y-m}{h}\right).}                      \tag{C}
\]

Here \(P_r^*\) is a globally nonnegative optimal polynomial.  To prove the
lower bound, let \(P\) be admissible, put \(Q=P-y\), and suppose
\(\|Q\|_{[1,\rho]}\leq E\).  At
\(y=-h(z-z_0)\leq0\), global nonnegativity gives

\[
 Q(y)=P(y)-y\geq h(z-z_0).
\]

Exterior Chebyshev extremality, after mapping \([1,\rho]\) to \([-1,1]\),
gives \(|Q(y)|\leq E T_{2r}(z)\).  Maximizing over \(z\geq z_0\) proves
the lower half of (C).

For the upper half, write

\[
 e=\frac{G_r}{h}=\max_{z\geq z_0}\frac{z-z_0}{T_n(z)},
 \qquad x=\frac{y-m}{h}.
\]

Then \(P_r^*(y)/h=x+z_0+eT_n(x)\).  This is nonnegative for
\(x\leq-z_0\) by the definition of \(e\); for
\(-z_0\leq x\leq-1\) because \(y\geq0\) and evenness gives
\(T_n(x)\geq1\); and for \(x\geq1\) because both terms are nonnegative.
On \([-1,1]\), only a negative Chebyshev lobe needs attention.  Such a lobe
has

\[
 x\geq-\cos\frac{\pi}{2n},
 \qquad
 x+z_0\geq1-\cos\frac{\pi}{2n}\geq\frac1{n^2}.
\]

Convexity and the tangent at one give
\(T_n(z)\geq1+n^2(z-1)\) for \(z\geq1\), hence \(e<1/n^2\).
Since \(|T_n(x)|\leq1\), this proves positivity also on the negative lobes.
Finally, on \([1,\rho]\) the error is exactly
\(G_r|T_n(x)|\leq G_r\), completing the proof.

The maximizer \(z_*>z_0\) is unique.  Indeed,
\(g(z)=z-T_n(z)/T_n'(z)\) has
\(g'(z)=T_n(z)T_n''(z)/T_n'(z)^2>0\), and stationarity gives

\[
 z_*-z_0=\frac{T_n(z_*)}{T_n'(z_*)},
 \qquad G_r(\rho)=\frac{h}{T_n'(z_*)}.                       \tag{C1}
\]

Moreover \(T_{2r+2}(z)>T_{2r}(z)\) for every \(z>1\), so
\(G_{r+1}(\rho)<G_r(\rho)\): the threshold staircase has no plateaus.

Define

\[
 R_0(\rho)=\frac{\sqrt\rho+1}{\sqrt\rho-1}.
\]

Writing \(z_0=\cosh a\), where \(a=\log R_0\), and setting
\(z=\cosh(a+s/n)\) in (C), the maximizer has
\(s=1+O_\rho(1/n)\).  Therefore

\[
 \boxed{
 G_r(\rho)=\frac{\sqrt\rho}{e\,r}
 R_0(\rho)^{-2r}\left(1+O_\rho(r^{-1})\right).}             \tag{C2}
\]

Thus squaring a degree-\(r\) approximation to \(\sqrt y\), which only
directly gives an \(R_0^{-r}\) rate, is exponentially suboptimal for this
problem.  If \(L=\log(1/K)\), integer rounding aside,

\[
 \ell(K)=
 \frac{L-\log L+\log(2\sqrt\rho\log R_0/e)}{2\log R_0}
 +o_\rho(1),                                                \tag{C3}
\]

and consequently

\[
 1-\frac1{2\ell(K)}
 =1-\frac{\log R_0}
 {\log(1/K)-\log\log(1/K)+O_\rho(1)}.                       \tag{C4}
\]

The order of limits in the query theorem is fixed \(K\), then
\(\delta\to0\); its construction does not yet claim uniform constants when
\(K\) and \(\delta\) vanish jointly.

## Boundary-layer construction

Fix \(r\geq1\), choose

\[
 G_r(\rho)<K_0<K,
\]

and take a globally nonnegative polynomial \(P\) of degree at most \(2r\)
with

\[
 \max_{[1,\rho]}|P(y)-y|\leq K_0.
\]

Set

\[
 \alpha=\frac{2r-1}{2r},\qquad
 m=\text{an odd integer nearest }M\delta^{-\alpha},
\]

where the fixed constant \(M\) will be chosen large.  Define the even
polynomial

\[
 \kappa_m(x)=\frac{\sin(m\arcsin x)}{mx}.
\]

For odd \(m\), the apparent singularity at zero is removable,
\(\deg\kappa_m=m-1\), and

\[
 |\kappa_m(x)|\leq
 \min\left\{1,\frac1{m|x|}\right\}.                           \tag{3}
\]

Put

\[
 s=r+1,\qquad L=r+2,\qquad
 J(x)=1-(1-\kappa_m(x)^2)^s,\qquad
 W(x)=J(x)^L.
\]

Then \(0\leq W\leq1\).  On the low interval,

\[
 1-W(x)=O((m\delta)^{2r+2})
 =O(\delta^{1+1/r})=o(\delta),                               \tag{4}
\]

whereas for \(|x|\geq c\),

\[
 W(x)=O((mc)^{-2r-4}).                                      \tag{5}
\]

For the high band, use the positive truncated expansion

\[
 S_N(u)=u\sum_{j=1}^N d_j(1-u)^j,
\]

where

\[
 \frac{1-\sqrt{1-z}}{1-z}=\sum_{j\geq1}d_jz^j,\qquad
 0<d_j\leq1.
\]

It obeys

\[
 0\leq S_N(u)\leq1,\qquad
 |S_N(u)-(1-\sqrt u)|\leq(1-u)^{N+1}.                        \tag{6}
\]

Indeed the coefficients are positive and at most one, so the omitted tail is
bounded by \(u\sum_{j>N}(1-u)^j=(1-u)^{N+1}\).  This also proves the
pointwise bounds without an asymptotic argument.

Take \(N=\Theta_c(\log(1/\delta))\), and define

\[
 \boxed{
 q_\delta(x)=
 W(x)\left[1-\delta P(x/\delta)\right]
 +(1-W(x))S_N(x^2).}                                        \tag{7}
\]

This is the desired transform, approximating \(1-x\).

## Global contractivity

Write

\[
 q_\delta=B-\delta P(x/\delta)W,\qquad
 B=W+(1-W)S_N(x^2)\in[0,1].
\]

Since \(P\geq0\), one has \(q_\delta\leq1\).  Also
\(P(y)\leq C(1+|y|^{2r})\).  Splitting at \(|x|=1/m\) and using (3) gives

\[
 \delta P(x/\delta)W(x)
 \leq C\delta+C\delta^{1-2r}m^{-2r}
 \leq C\delta+CM^{-2r}.                                     \tag{8}
\]

Choosing fixed \(M\) sufficiently large makes (8) at most one, hence

\[
 |q_\delta(x)|\leq1\qquad(-1\leq x\leq1).                    \tag{9}
\]

On \(x=\delta y\), (4), (6), and the approximation property of \(P\) give

\[
 |q_\delta(x)-(1-x)|\leq K_0\delta+o(\delta)<K\delta.
\]

On \(x\in[c,1]\), the error is bounded by the tail in (6), \(O(W)\), and
\(\delta P(x/\delta)W\).  The last term is

\[
 O(\delta^{\,4-2/r})=o(\delta),
\]

and the first is \(O(\delta)\) by the choice of \(N\).  Enlarging constants
gives the required error on both bands.

The degree is

\[
 \deg q_\delta
 =O_r(m+N)
 =O_{r,\rho,c,K}\left(
 \delta^{-(2r-1)/(2r)}+\log(1/\delta)
 \right).                                                    \tag{10}
\]

The lower bound in \((P_r)\) is exactly the adaptive hierarchy at index \(r-1\),
because \(K<G_{r-1}\).

For \(r=0\), take a constant nonnegative approximant to \(y\), a fixed odd
\(m_0>1/c\), and
\(W=\kappa_{m_0}^{\,2L_\delta}\) with
\(L_\delta=\Theta(\log(1/\delta))\).  The same blend proves the upper bound
in \((P_0)\) for \(K>G_0\).  For the lower bound, take an arbitrary circuit matrix element
\(q(\sin t)\) and put
\(r(t)=q(\sin t)-(1-\sin t)\).  It is \(O(\delta)\) on the fixed arc
corresponding to \([c,1]\), while contractivity gives
\(|r(-\pi/2)|\geq1\).  A trigonometric Remez inequality for degree
\(O(Q)\) then gives \(Q=\Omega(\log(1/\delta))\).

## Exact threshold values

It remains to obtain the upper bound without a strict margin \(K_0<K\).
A minimizer \(P\) for \(G_r\) exists: values of a minimizing sequence at
\(2r+1\) fixed interval points bound all coefficients, and the globally
nonnegative cone is closed.  Write

\[
 e(y)=P(y)-y,\qquad
 A_+=\{y\in[1,\rho]:e(y)=G_r\}.
\]

The set \(A_+\) is nonempty, since otherwise a small upward constant shift of
\(P\) would reduce the minimax error while preserving nonnegativity.  It is
finite: \(e-G_r\) is a nonzero polynomial, because
\(P(y)=y+G_r\) identically would contradict global nonnegativity.

For odd \(m\asymp M\delta^{-(2r-1)/(2r)}\), put

\[
 D_{m,a}(\theta)=
 \frac{\sin(m(\theta-a))}{m\sin(\theta-a)},\qquad
 \theta_j=\arcsin(\delta y_j),
\]

and define

\[
 Z(\theta)=
 \prod_{y_j\in A_+}\prod_{\sigma=\pm1}
 \left(1-D_{m,\sigma\theta_j}(\theta)^{2(r+2)}\right)^{r+1},
 \qquad W=1-Z,qquad \theta=\arcsin x.                       \tag{11}
\]

Since \(|D_{m,a}|\leq1\), one has \(0\leq W\leq1\), and
\(W(\delta y_j)=1\) at every positive-error contact.  For odd \(m\),
\(D_{m,a}=U_{m-1}(\cos(\theta-a))/m\) is \(\pi\)-periodic.
Pairing \(a\) and \(-a\) makes (11) an even \(\pi\)-periodic trigonometric
polynomial, hence a real polynomial in
\(\cos2\theta=1-2x^2\).

Selecting the nearest contact factor gives, on the low band,

\[
 1-W\leq
 C\delta^{1+1/r}\operatorname{dist}(y,A_+)^{2r+2}.          \tag{12}
\]

The nonnegative polynomial \(G_r-e(y)\) has contact-root multiplicity at
most \(2r\); endpoint roots need not be even.  Consequently (12), with its
spare factor \(\delta^{1/r}\), implies for all sufficiently small \(\delta\)

\[
 1-W\leq\frac12W\delta\,[G_r-e(y)]                           \tag{13}
\]

near \(A_+\).  Away from \(A_+\), the slack has a positive minimum and
\(1-W=o(\delta)\), so (13) holds there as well.

Use the blend (7) with this pinned gate and put, on the positive low band,

\[
 d(x)=(1-x)-S_N(x^2)\in[0,1].
\]

Then

\[
 (1-x)-q_\delta(x)=W\delta e(y)+(1-W)d(x).                  \tag{14}
\]

The lower inequality
\(-G_r\delta\leq(1-x)-q_\delta(x)\) follows from
\(e\geq-G_r\) and \(d\geq0\).
For the upper bound, (13) gives

\[
 G_r\delta-[(1-x)-q_\delta(x)]
 =W\delta(G_r-e)+(1-W)(G_r\delta-d)\geq0.
\]

Thus (14) is bounded in absolute value by exactly \(G_r\delta\), with no
asymptotic overshoot.  On the high band,
\(W=O(m^{-2r-4})\).  Choose the truncation length \(N\) and then small
\(\delta\) so that the high-band tail plus both pinned-gate leakage terms are
at most \(G_r\delta\).  The global contractivity bound follows by splitting
\(|x|=O(\delta)\), \(O(\delta)<|x|<1/m\), and
\(|x|\geq1/m\); the symmetric negative pins lie in the first region and are
harmless.  The degree remains (10).

At \(K=G_r\), strict monotonicity gives \(K<G_{r-1}\).  The pinned
degree-\(2r\) construction and the index-\((r-1)\) lower bound therefore
match without a plateau convention.

At \(K=G_0\), use \(P=(\rho+1)/2\) and the gate

\[
 W(x)=\left[1-C(x^2-\delta^2)^2\right]^{L_\delta},
 \qquad L_\delta=\Theta(\log(1/\delta)),                    \tag{15}
\]

where fixed \(C>0\) makes the base lie in \([0,1]\).  Its low leakage
\(O(\delta^4L_\delta(y-1)^2)\) is dominated by the endpoint-linear error
slack, and a sufficiently large constant in \(L_\delta\) makes its high-band
leakage \(O(\delta)\).  The Remez lower bound completes \((P_0)\) at equality.

## Exact unit-normalized implementation

Mixed parity causes no normalization loss in the arbitrary controlled-query
model.  In the scalar sine convention, let \(d=\deg q_\delta\),
\(z=e^{it}\), and

\[
 R(z)=z^d q_\delta\!\left(\frac{z-z^{-1}}{2i}\right).
\]

This is an ordinary polynomial of degree at most \(2d\), and (9) gives
\(|R(z)|\leq1\) on the unit circle.  The generalized-QSP
Fejér--Riesz completion of
[Motlagh--Wiebe](https://doi.org/10.1103/PRXQuantum.5.020368)
implements \(R(V)\) with at most \(2d\) controlled signal-unitary calls.
Postmultiplying by \(V^{-d}\) uses another \(d\) calls and yields exactly
\(q_\delta(\sin t)\), with unit normalization.

For a Hermitian projected-unitary encoding, standard qubitization gives a
walk \(W_q\) with
\[
 (W_q+W_q^\dagger)/2
\]
equal to the encoded eigenvalue on each two-dimensional walk subspace.  The
same centered Laurent construction therefore implements \(q_\delta(H)\) in
at most \(3d\) walk calls.  An ordinary Hermitian block encoding can be
hermitianized and qubitized at constant overhead.  This claim assumes
controlled walk and inverse-walk access; it is not a free-postselection
construction.

## A polynomial GQSP--QSVT separation

The staircase exposes a concrete separation between mixed-parity generalized
QSP and every standard single-sequence definite-parity QSVT transform.  Take
\(\rho=2\) and \(K=1/32\).  Then

\[
 G_1(2)=\frac{3-\sqrt{17/2}}4\approx0.021131
 <\frac1{32}<\frac1{24}=E_2,
\]

where \(E_2\) is the even-QSVT affine threshold proved in the companion
two-interval note.  Therefore

\[
 \begin{array}{c|c}
 \text{converter class}&\text{optimal or necessary query order}\\ \hline
 \text{general coherent converter / centered GQSP}
     &\Theta(\delta^{-1/2})\\
 \text{single-sequence even QSVT}&\Omega(\delta^{-3/4})\\
 \text{single-sequence odd QSVT}&\Omega(\delta^{-1}).
 \end{array}                                                  \tag{16}
\]

The first line is optimal even among arbitrary coherent adaptive converters.
Thus arbitrary-parity synthesis is not merely a more convenient
parameterization here: it gives a polynomial query advantage for the same
unit-normalized promise and error contract.  The comparison concerns standard
definite-parity QSVT sequences, not arbitrary compositions of several QSVT
blocks, which already fall under the general coherent model in the first line.

## Novelty boundary

Trigonometric polynomial characterizations of arbitrary query circuits,
generalized QSP, Fejér--Riesz completion, Remez inequalities, and positive
polynomial approximation are prior art.  Boundary Carathéodory--Schur theory
also studies admissible higher-order jets of bounded analytic functions.

A targeted search found no shrinking-edge rescaling to the globally
nonnegative jet cone, no exact constrained-approximation formula (C), no
thresholds \(G_r(\rho)\), no matching query staircase
\((P)\), and no explicit GQSP-versus-QSVT polynomial separation of the form
(16).  The staircase and separation—not the polynomial/query characterization
or generalized-QSP implementation—are the defensible apparent novelty.
The lower-bound ingredient is the classical exterior Chebyshev inequality;
for a modern statement see Bos--Ma'u--Waldron,
[Proposition 2.1](https://doi.org/10.1007/s10476-020-0028-8).  The closest
constrained-approximation antecedents found were Taylor's
[restricted-range approximation](https://doi.org/10.1137/0705022), which
constrains the range on the same compact set where error is measured, and
Campos Pinto--Charles--Després's
[positive-polynomial algorithms](https://doi.org/10.1137/17M1131891), which
enforce positivity on the compact interpolation interval.  General
sum-of-squares representations for real-axis nonnegativity are also standard;
for example, Roh--Vandenberghe give the representation and its SDP form in
[Section 5](https://www.seas.ucla.edu/~vandenbe/publications/nnp.pdf).
Lewis's abstract theory of
[approximation with convex constraints](https://doi.org/10.1137/1015006)
also covers broad positivity constraints but supplies no explicit solution
of this problem.  None of these sources states the asymmetric problem used here—uniform error
only on \([1,\rho]\), but nonnegativity on all of \(\mathbb R\)—or its exact
Chebyshev extremizer.  This is evidence of apparent novelty, not a guarantee
against an older approximation-theory antecedent.
Relevant antecedents are Bessen's continuous-query trigonometric-polynomial
method, Gilyén's pairwise eigenvalue-transformation lower bound,
Motlagh--Wiebe generalized QSP, and higher-order boundary Schur interpolation.
Free nonlinear conditioning is excluded: postselection changes polynomial
query representations into rational ones and must be charged through its
success probability.

See also the companion notes
[adaptive all-circuit lower hierarchy](2026-09-04-adaptive-normalized-shift-hierarchy.md)
and [definite-parity QSVT thresholds](2026-09-04-two-cluster-interval-shift-upper.md).
