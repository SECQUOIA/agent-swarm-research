# When do local-walk and statistical inverse-quadratic lower bounds multiply?

Status: Independently audited distributional constant-contrast and
constant-weight-path products; rigorous high-contrast conditional compiler
and two gadget-class obstructions
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

Audit record: An independent proof audit verified the Ben-David--Blais and
CKMPSS quantifiers, the one-form concentration reduction, full-SQ/box-LP
transfer, explicit constants, and the cyclic-resolvent algebra after the
corrections recorded below.  A separate independent audit passed the full
constant-weight-path theorem (10o)--(10t), including its exact inverse
formulas, genuine Forrelation depth, source denominator, full-SQ ledger, and
box-LP lift.  The restricted-interval witness calculation (C1)--(C5) has
also been independently audited, including the full-domain moments, explicit
inverse-Jacobi measure, endpoint index parity, and closed-form diagonal.

## Question

Two independently audited lower bounds are now available for relative
estimation of \(b^TH^{-1}b\) under sparse/full-SQ access:

\[
 L_{\rm walk}
 =s^{\Omega(\sqrt\kappa\log(1/\epsilon))}
\]

from the Montanaro--Shao/Forrelation clock, up to polynomial factors, and

\[
 L_{\rm stat}=\Omega(\min\{N,\kappa/\epsilon^2\})
\]

from the two-by-two sign blocks.  A direct sum of the two families proves
only \(\Omega(\max\{L_{\rm walk},L_{\rm stat}\})\).  This note records the
exact extra property needed to prove their product and why the present clock
theorem does not yet supply it.

## Block averaging preserves all structural promises

Let \(G_y\) be an inner family of SPD matrices with
\(\kappa^{-1}I\preceq G_y\preceq I\), sparsity at most \(s\), and a public
unit vector \(v\).  For \(M\) independent inner inputs
\(y^{(1)},\ldots,y^{(M)}\), set

\[
 H_{\boldsymbol y}=\bigoplus_{j=1}^M G_{y^{(j)}},
 \qquad
 b=\frac1{\sqrt M}\bigoplus_{j=1}^M v.                    \tag{1}
\]

Then

\[
 b^TH_{\boldsymbol y}^{-1}b
 =\frac1M\sum_{j=1}^M v^TG_{y^{(j)}}^{-1}v.               \tag{2}
\]

The condition number and row/column sparsity do not grow.  If every inner
block has the same public row/column norm tables, Frobenius norm, support,
and squared-magnitude sampling distributions, full SQ of the direct sum
first samples a uniform public block index and then invokes the inner
interface.  Hence it leaks no label for free.

If \(G_y=C_y^TC_y\) with equally public full-SQ metadata for \(C_y\), (1) is
also the exact analytic-center Hessian, up to the usual factor two, of the
block-diagonal box LP

\[
 \max_x\ \tau b^Tx,
 \qquad
 -\mathbf1\leq
 \left(\bigoplus_j C_{y^{(j)}}\right)x\leq\mathbf1.        \tag{3}
\]

At the public analytic center \(x=0\), its paired logarithmic barrier has
Hessian \(2H_{\boldsymbol y}\).  Hence the squared Newton decrement for the
displayed objective multiplier is exactly
\[
 \Lambda^2=\frac{\tau^2}{2}
 b^TH_{\boldsymbol y}^{-1}b.
\]
The block construction preserves the factor sparsity of \(C_y\); it does not
assert that this sparsity must equal that of \(G_y\).

Thus neither full SQ nor the box-LP realization is the obstruction to a
product theorem.

## Contrast is the necessary statistical resource

Suppose first that the inner scalar takes two exact values

\[
 v^TG_y^{-1}v=
 \begin{cases}
 q_0,&g(y)=0,\\
 q_1,&g(y)=1,
 \end{cases}
 \qquad R=\frac{q_1}{q_0}>1,\qquad D=R-1.                \tag{4}
\]

If a fraction \(p\) of the blocks have label one, (2) is

\[
 q_0(1+Dp).                                                \tag{5}
\]

In the high-contrast regime \(D\geq1\), take
\(p=\Theta(1/D)\).  The scalar remains \(\Theta(q_0)\), and disjoint
relative-\(\epsilon\) output intervals require changing \(p\) by
\(\Theta(\epsilon/D)\).  The classical Hamming-sphere lemma then gives outer
query complexity

\[
 \Theta\!\left(\min\left\{M,\frac{D}{\epsilon^2}\right\}\right).
                                                               \tag{6}
\]

This calculation is exact.  In particular, obtaining the desired
\(\kappa/\epsilon^2\) factor requires inner relative spread
\(D=\Theta(\kappa)\), equivalently \(R=\Theta(\kappa)\).  If
\(D=\Theta(1)\), the same calculation gives only
\(\Theta(\epsilon^{-2})\).  A constant *additive* label gap between two
\(\Theta(\kappa)\)-scale quadratic forms is even weaker:
\(D=\Theta(1/\kappa)\), so it cannot supply the desired statistical factor
and may not be resolvable at all when \(\epsilon\gtrsim1/\kappa\).

Approximate levels are enough only with a correspondingly narrow promise.
If every label-zero value is within \(\eta q_0\) of \(q_0\) and every
label-one value is within \(\eta q_1\) of \(q_1\), arbitrary within-label
variation contributes \(O(\eta)\) relatively to (5).  To resolve the outer
gap uniformly, one needs \(\eta=O(\epsilon)\).  Equivalently, if both level
intervals are instead specified by one absolute half-width
\(\delta q_1\), then one needs
\(\delta q_1=O(\epsilon q_0)\), or
\(\delta=O(\epsilon/R)=O(\epsilon/\kappa)\) in the target regime.

## A conditional product compiler

Let \(g\) be a partial Boolean inner problem with randomized query
complexity \(R(g)=L\).  Assume an oracle-preserving family satisfying (4)
with \(R=\Theta(\kappa)\), identical public full-SQ metadata, and one
inner-oracle query per queried matrix value.  Choose

\[
 M=\Theta(D/\epsilon^2)=\Theta(\kappa/\epsilon^2)
\]

and let the outer partial function distinguish the two Hamming weights used
in (6).  Its randomized query complexity is \(\Theta(M)\), linear in its
input length; choosing the hidden constants sufficiently large makes the
rounded weights satisfy the standard Hamming-sphere conditions.  Theorem 2 of
Chakraborty--Kayal--Mittal--Paraashar--Sanyal--Saurabh explicitly allows a
partial Boolean outer function and every partial inner function.  It
therefore gives

\[
 R(F\circ g^M)
 =\Omega\!\left(
     \frac{\kappa}{\epsilon^2}\,L
   \right).                                               \tag{7}
\]

Equations (1)--(5) reduce \(F\circ g^M\) to one relative inverse-quadratic
estimate.  Therefore (7) is a rigorous product compiler, conditional on an
inner clock with nearly extremal contrast.

The composition hypothesis matters.  There is no general theorem
\(R(F\circ g)=\Omega(R(F)R(g))\) for arbitrary partial functions: this
conjecture is false.  Here it is the special fact that the chosen outer
weight problem has randomized complexity linear in its number of inputs
that permits the product theorem.

## Why the current Forrelation clock does not instantiate the compiler

The Montanaro--Shao clock gives an off-diagonal matrix-function entry of the
form

\[
 z_y=c\,\Phi(y),                                          \tag{8}
\]

where the Forrelation promise is

\[
 \Phi(y)\geq3/5
 \quad\text{or}\quad
 |\Phi(y)|\leq1/100.                                      \tag{9}
\]

After affine shifting to an SPD inverse and polarization,

\[
 q_+-q_-=\frac{2}{a}z_y,\qquad a=\kappa^{-1}.             \tag{10}
\]

This proves that estimating the pair of positive forms is hard.  It does
not show that either single form has two narrow values with contrast
\(\Theta(\kappa)\):

- the high case in (9) ranges from \(3/5\) to \(1\);
- the diagonal baseline in \(q_\pm\) is positive and can itself be
  \(\Theta(\kappa)\); and
- polarization provides a large *difference*, not a lower bound on the
  ratio \(q_1/q_0\).

Consequently block-diagonal replication of the published hard clock does
not satisfy (4), and substituting \(L=L_{\rm walk}\) into (7) would be an
unsupported step.

## Distributional averaging gives an unconditional constant-contrast product

Pointwise narrow levels are necessary for the pointwise reduction above,
but they are not necessary for a distributional lower bound.  This yields a
genuine one-instance direct product, although not the desired extra
\(\kappa\) factor.

Fix a clock endpoint coefficient \(0<c\leq c_0\), where \(c_0\) is a small
universal constant, and let \(g_c\) be the Forrelation promise problem used
in the Montanaro--Shao reduction at additive scale \(c\).  Their construction
and the reciprocal approximate-degree calculation give

\[
 L_c:=R(g_c)
 =\Omega\!\left(
 \frac{
  ((s-1)/2)^{\,\Omega(\sqrt\kappa\log(1/c))}
 }{
  \log(s)\sqrt\kappa\log(1/c)
 }
 \right).                                                \tag{10a}
\]

For each hidden input \(y\), the clock matrix is block-diagonally gauge
equivalent to the same public weighted path tensored with the work-space
identity.  Hence its two endpoint diagonal inverse entries are public and
independent of \(y\).  If

\[
 d=\frac12\left(e_i^TH_y^{-1}e_i+e_j^TH_y^{-1}e_j\right),
 \qquad b_+=\frac{e_i+e_j}{\sqrt2},
\]

then the endpoint identity \(e_i^Tf_\kappa(A_y)e_j=c\Phi(y)\) and
\(f_\kappa(A_y)=\kappa^{-1}H_y^{-1}\) give the exact **single-form** formula

\[
 q_+(y):=b_+^TH_y^{-1}b_+
 =d+\kappa c\Phi(y).                                     \tag{10b}
\]

The vector \(b_+\) is public and two-sparse, \(d=d_c\) depends only on the
public clock, and
\(1\leq q_+(y)\leq\kappa\).  It is useful to retain the public normalized
signal-to-baseline ratio

\[
 \chi_c:=\frac{\kappa c}{d}.
\]

Positive-semidefinite Cauchy--Schwarz gives
\(|e_i^TH_y^{-1}e_j|\leq d\).  Applying this to a high Forrelation input
and also using \(d\leq\kappa\) shows

\[
 c\leq\chi_c\leq5/3,
 \qquad
 q_+(y)\leq(1+\chi_c)d<3d.                              \tag{10b'}
\]

Here is the distributional composition argument with all quantifiers made
explicit.  First choose distributions \(\mu_0,\mu_1\), supported
respectively on the zero and one inputs of \(g_c\), that witness
\(\operatorname{sfR}(g_c)=\Omega(R(g_c))\) in Ben-David--Blais Theorem 24.
For this fixed pair, their Theorem 35 lower-bounds
\(\operatorname{compR}_{1/3}(F_M,g_c)\) by
\(\operatorname{noisyR}_{1/3}(F_M)\operatorname{sfR}(g_c)\).
The minimax observation following their Definition 34 then supplies a
distribution \(\nu\) on \(\operatorname{Dom}(F_M)\) for which the hard
composed distribution has the product form

\[
 y\sim\nu,
 \qquad
 Y_j\sim\mu_{y_j}\ \text{ independently}.               \tag{10c}
\]

Here \(\nu\) may depend on \(F_M\) and on the fixed inner pair, while the
inner samples are independent conditional on \(y\).  For the two-level
gap-majority outer function \(F_M\), with Hamming weights

\[
 |y|=M/2\pm g_0\sqrt M                                  \tag{10d}
\]

for a sufficiently large fixed constant \(g_0\), the standard
Hamming-sphere bound gives \(R(F_M)=\Theta(M)\).
Chakraborty--Kayal--Mittal--Paraashar--Sanyal--Saurabh Observation 23
(equivalently, the key estimate in their proof of Theorem 2) gives
\[
 \operatorname{noisyR}(F_M)
 =\Omega(R(F_M)^2/M)=\Omega(M),
\]
and the reverse \(O(M)\) bound is immediate.  Thus
\(\operatorname{noisyR}(F_M)=\Theta(M)\).  Below we choose parameters that
make both levels in (10d) integral, so no rounding convention is needed.

Apply these theorems with \(g=g_c\).  Every point in the support of
\(\mu_0\) obeys \(|\Phi|\leq1/100\), and every point in the support of
\(\mu_1\) obeys \(\Phi\geq3/5\).  Therefore, writing

\[
 \Delta=\mathbb E_{\mu_1}\Phi-\mathbb E_{\mu_0}\Phi,
 \qquad \Delta\geq59/100,
\]

the conditional expectations of \(M^{-1}\sum_j\Phi(Y_j)\) in the two outer
cases differ by \(2g_0\Delta/\sqrt M\).  Since each summand lies in
\([-1,1]\), Hoeffding's inequality gives

\[
 \Pr\!\left[
  \left|\frac1M\sum_j\Phi(Y_j)
  -\mathbb E\frac1M\sum_j\Phi(Y_j)\right|
  >\frac{g_0\Delta}{4\sqrt M}
 \right]
 \leq 2e^{-g_0^2\Delta^2/32}.                            \tag{10e}
\]

Take \(g_0=24\), put \(n=\lceil\chi_c/\epsilon\rceil\), and take

\[
 M=4n^2=4\lceil\chi_c/\epsilon\rceil^2,
 \qquad 0<\epsilon\leq \chi_c/C,                         \tag{10f}
\]

where \(C\geq24\).  Then \(n\geq24\), so the two weights
\(M/2\pm g_0\sqrt M=2n^2\pm48n\) are valid integers.  The failure bound in
(10e) is less than \(0.004\).  The two conditional means of the averaged
form (2), using (10b), are separated by
\[
 S=\frac{24\Delta\kappa c}{n}
   =\frac{24\Delta\chi_c d}{n}
   \geq 13.59\,\epsilon d,
\]
where the last inequality uses \(\Delta\geq0.59\) and
\(n\leq(25/24)\chi_c/\epsilon\).  The scalar concentration radius in
(10e) is exactly \(S/8\).  A relative-\(\epsilon\) estimator has absolute
error below \(3\epsilon d\), by (10b'), and
\(S/8+3\epsilon d<S/2\).  First amplify its pointwise failure probability
to at most \(1/12\) by a constant number of repetitions and a median.
Thresholding at the public midpoint determined by
\(d,\mathbb E_{\mu_0}\Phi,\mathbb E_{\mu_1}\Phi\) therefore computes
\(F_M\) on the product hard distribution with error below \(1/3\).  This
constant amplification does not affect the asymptotic lower bound and is
separate from the small-error coherent amplification discussed below.  The
threshold may depend nonuniformly on the fixed hard distributions, exactly
as allowed in Yao's minimax argument.  Ben-David--Blais formulate the inner
bound using expected query cost; a worst-case \(Q\)-query estimator is
covered because its expected cost is at most \(Q\).

The distributional composition theorem now proves the unconditional lower
bound

\[
 \boxed{
 Q=\Omega\!\left(
 \frac{(\chi_c/\epsilon)^2
  ((s-1)/2)^{\,\Omega(\sqrt\kappa\log(1/c))}
 }{
  \log(s)\sqrt\kappa\log(1/c)
 }
 \right).
 }                                                        \tag{10g}
\]

This is a lower bound for one relative inverse-quadratic estimate, not for a
pair.  All blocks have the same public full-SQ metadata, so the direct-sum
interface remains constant-query simulable.  The box-LP factor construction
also direct-sums exactly as in (3), proving the same lower bound for one
analytic-center squared Newton decrement, up to its public scalar factor.

For fixed small \(c\), (10g) contains the simultaneous factor
\(\epsilon^{-2}s^{\Omega(\sqrt\kappa)}\), because then
\(c\leq\chi_c\leq5/3\) consists only of constants.  More generally, the
always-valid conservative substitution \(\chi_c\geq c\), followed by setting
\(c=c_0\epsilon^a\), for fixed \(0\leq a<1\), fixed \(c_0\), and
sufficiently small \(\epsilon\) so that
\(\epsilon^{1-a}\leq c_0/C\), gives, for \(s\geq5\),

\[
 \epsilon^{-2(1-a)}
 s^{\Omega(\sqrt\kappa(1+a\log(1/\epsilon)))}
\]

up to the denominator in (10g) and constants depending on \(c_0\).  The
logarithm of this interpolation is affine in \(a\) at leading order, so it
does not generally improve the existing maximum of the pure statistical
and full-accuracy local-walk lower envelopes.  Its content is instead a
rigorous simultaneous/direct-product family: the polynomial accuracy cost
and nontrivial local-walk cost occur in the same single scalar instance.

### Exact diagonal of an explicit restricted-interval witness clock

This subsection, including the moment-to-inverse-Jacobi realization, has
received an independent proof audit.

The restricted interval used below is not asserted to give the minimax
approximant to \(f_\kappa\) on all of \([-1,1]\).  Instead, it gives an
explicit valid dual witness for that full-domain problem: every polynomial
approximant on \([-1,1]\) also approximates on the restricted symmetric
set, and the symmetrized alternation functional annihilates every polynomial
of the required degree.  The corresponding Montanaro--Shao inverse-Jacobi
clock has a public diagonal in closed form.  This sharpens the general
bounds in (10b') and completely determines the tradeoff in (10g) for this
explicit realization.

Keep \(a=\kappa^{-1}\), and put

\[
 m=\frac{1+a}{2},\qquad h=\frac{1-a}{2},\qquad
 f_\kappa(x)=\frac{a}{m+hx}.
\]

The explicit even-part construction restricts \(y=x^2\) to
\([1/2,1]\) and uses \(t=4y-3\).  In this coordinate,

\[
 f_{\kappa,\mathrm{even}}(x)
 =\frac{am}{m^2-h^2x^2}
 =\frac{C}{A-t},
 \qquad
 C=\frac{4am}{h^2},\quad A=4(m/h)^2-3.                 \tag{C1}
\]

For \(r\geq1\), let \(p_r\) be the degree-\(r\) best uniform approximant to
\(q(t)=C/(A-t)\).  Write

\[
 \omega=\sqrt{A^2-1},\qquad \delta=A-\omega.
\]

The exact error is

\[
 q(t)-p_r(t)=E_rV_r(t),\qquad
 E_r=\frac{C\delta^r}{\omega^2},
\]

where, for \(t=\cos\varphi\),

\[
 V_r(t)=\cos(r\varphi+\psi),\qquad
 \tan\frac\psi2
 =\sqrt{\frac{A+1}{A-1}}\tan\frac\varphi2.
\]

The elementary half-angle identities give

\[
 V_r(t)=\frac{N(t)}{A-t},\qquad
 N(t)=(At-1)T_r(t)+\omega(t^2-1)U_{r-1}(t).             \tag{C2}
\]

The \(r+2\) alternation points \(t_0<\cdots<t_{r+1}\) are the
two endpoints and the \(r\) roots of

\[
 R(t)=(At-1)U_{r-1}(t)+\omega T_r(t).
\]

Consequently they are precisely the roots of
\(L(t)=(t^2-1)R(t)\).  This polynomial has positive leading coefficient,
and the ordering of the phase shows

\[
 V_r(t_j)=\operatorname{sgn}L'(t_j).
\]

The normalized alternation weights are therefore

\[
 \mu_j=
 \frac{|L'(t_j)|^{-1}}
      {\sum_k|L'(t_k)|^{-1}}.
\]

Here is the full-domain moment check.  Since \(L\) has degree \(r+2\),
partial fractions at infinity give

\[
 \sum_{j=0}^{r+1}\frac{P(t_j)}{L'(t_j)}=0
 \quad\text{for every }\deg P\leq r.                    \tag{C2'}
\]

Put \(x_j=\sqrt{(t_j+3)/4}\), and give each of \(\pm x_j\) signed mass
\(\operatorname{sgn}(L'(t_j))\mu_j/2\).  Odd polynomials cancel between
the two signs.  If \(p\) is even and \(\deg p\leq2r\), then
\(p(x)=P(4x^2-3)\) for a polynomial \(P\) of degree at most \(r\), so
(C2') annihilates it.  The signed masses therefore annihilate every
polynomial of degree at most \(2r\).  Alternation and the same identity
applied to \(p_r\) also give

\[
 \sum_j\mu_j\operatorname{sgn}(L'(t_j))
       f_{\kappa,\mathrm{even}}(x_j)=E_r.
\]

All \(x_j\) lie in \([1/\sqrt2,1]\).  This is therefore a valid
degree-\(2r\) dual witness for approximation on the full interval
\([-1,1]\), even though it was constructed on a strict subset.

The even inverse-Jacobi construction realizes this signed witness.  Under
\(t=4x^2-3\), the affine change contributes the same barycentric factor at
every node.  To see the realization explicitly, put

\[
 B=\left(2\sum_j\frac{\mu_j}{x_j^2}\right)^{-1},
 \qquad w_0=\frac12,
 \qquad w_{+j}=w_{-j}=\frac{B\mu_j}{2x_j^2}.
\]

These positive weights sum to one.  For the Jacobi matrix whose \(e_1\)
spectral measure is \(w_0\delta_0+\sum_jw_{+j}(\delta_{x_j}+
\delta_{-x_j})\), one has \(J e_1=\sqrt B\,e_2\).  It follows that the
spectral mass of \(e_2\) is \(\mu_j/2\) at each of \(\pm x_j\), while the
zero eigenvector has zero \(e_2\)-mass.  In the odd polynomial sector,
(C2') says that the last
normalized orthogonal polynomial takes the values
\(\operatorname{sgn}(L'(t_j))\).  The finite Stieltjes recurrence therefore
places the signed functional between \(e_2\) and \(e_{N-1}\), with spectral
mass \(\mu_j/2\) at each of \(\pm x_j\) for \(e_2\).  Hence, if \(J\) is
the resulting odd Jacobi matrix, its hard cross entry is
\((f_\kappa(J))_{2,N-1}=E_r\); in the notation above, set \(c=E_r\).  Its
endpoint diagonal is

\[
 d_c':=(f_\kappa(J))_{22}
 =\sum_j\mu_jq(t_j).
\]

Because the last normalized orthogonal polynomial has values of unit
magnitude on every support point, \(e_{N-1}\) has the same spectral masses
as \(e_2\).  Thus the two hard endpoint diagonals are equal, and averaging
them does not change \(d_c'\).

It remains to evaluate the displayed sum.  Since
\(V_r(t_j)=N(t_j)/(A-t_j)=\operatorname{sgn}L'(t_j)\), the partial-fraction
expansion of \(N/L\) gives

\[
 \begin{aligned}
 S_0&:=\sum_j\frac1{|L'(t_j)|}
     =\sum_j\frac{N(t_j)}{(A-t_j)L'(t_j)}
     =\frac{N(A)}{L(A)},\\
 S_1&:=\sum_j\frac{q(t_j)}{|L'(t_j)|}
     =C\sum_j\frac{N(t_j)}{(A-t_j)^2L'(t_j)}
     =-C\left(\frac NL\right)'(A).
                                                               \tag{C3}
 \end{aligned}
\]

Indeed, \(\deg N<\deg L\), so these identities are just the residues of
\(N(z)/L(z)\), followed in the second line by differentiation.  Now set

\[
 \mathcal S=T_r(A)+\omega U_{r-1}(A)=(A+\omega)^r.
\]

Then

\[
 N(A)=\omega^2\mathcal S,\qquad
 R(A)=\omega\mathcal S,\qquad
 L(A)=\omega^3\mathcal S.
\]

Using \(T_r'=rU_{r-1}\) and
\(\omega^2U_{r-1}'(A)=rT_r(A)-AU_{r-1}(A)\) yields

\[
 \frac{N'(A)}{N(A)}=\frac r\omega+\frac A{\omega^2},
 \qquad
 \frac{L'(A)}{L(A)}=\frac r\omega+\frac{2A}{\omega^2}.
\]

Therefore (C3) proves the degree-independent identity

\[
 \boxed{
 d_c'=\frac{S_1}{S_0}
 =C\left(\frac{L'}L-\frac{N'}N\right)(A)
 =\frac{CA}{A^2-1}.}                                    \tag{C4}
\]

Substitution from (C1) simplifies this to

\[
 d_c'
 =\frac{(\kappa+1)(\kappa^2+14\kappa+1)}
 {4\kappa(\kappa^2+6\kappa+1)}.
\]

For every \(\kappa\geq4\), direct comparison gives

\[
 \frac14<d_c'<\frac35.
\]

Since \(H=mI+hJ\) and \(f_\kappa(J)=\kappa^{-1}H^{-1}\), the baseline
in (10b) is \(d=\kappa d_c'\).  Thus the normalized signal is exactly

\[
 \boxed{
 \chi_c=\frac{\kappa c}{d}=\frac{c}{d_c'},
 \qquad \frac53c<\chi_c<4c.}                            \tag{C5}
\]

In particular, \(\chi_c=\Theta(c)\) uniformly in both \(\kappa\) and the
clock degree.  The explicit witness-clock distributional bound (10g)
therefore has statistical prefactor
\(\Theta((c/\epsilon)^2)\), not a hidden condition-dependent gain.  The
earlier interpolation obtained from \(\chi_c\geq c\) is sharp up to
universal constants for this explicit clock.  No claim about the diagonal
of a different full-domain minimax realization is needed or made.

One can coherently amplify the Forrelation decision so that an output
probability lies in \([0,\eta]\) or \([1-\eta,1]\).  Reaching
\(\eta=O(\epsilon/\kappa)\) costs
\(O(\log(\kappa/\epsilon))\) repetitions.  In the Feynman-clock reduction
those repetitions consume the same clock length that creates the
local-walk exponent.  More importantly, an additional positive Schur or
Green-function gadget is still needed to turn the narrow acceptance
probability into the extremal inverse-quadratic ratio (4) without worsening
the overall condition number.  No such condition-preserving gadget is
proved here.

There is a separate clock-budget reason why coherent amplification does not
upgrade (10g) to
\(\epsilon^{-2}s^{\Omega(\sqrt\kappa\log(1/\epsilon))}\) within the
Montanaro--Shao endpoint compiler.  At endpoint coefficient \(c\), that
compiler has only

\[
 N_{\rm clock}
 =\widetilde{\deg}_c(f_\kappa)+O(1)
 =\Theta(\sqrt\kappa\log(1/c))
\]

local circuit layers.  Reducing a constant promise error to
\(O(\epsilon/\kappa)\) by a black-box polynomial transformation of the
bounded-error acceptance amplitude costs
\(\Theta(\log(\kappa/\epsilon))\) uses of the base Forrelation decision
circuit.  The lower statement here is only for such black-box amplitude
amplification; it does not exclude a structure-aware small-error circuit.
Fitting those uses into the same clock leaves at most

\[
 O\!\left(
 \frac{\sqrt\kappa\log(1/c)}{\log(\kappa/\epsilon)}
 \right)
\]

Forrelation block layers and therefore divides the local-walk exponent by
\(\Theta(\log(\kappa/\epsilon))\).  For example, if
\(c=c_0\epsilon^a\), the exponent available to this proposed amplified
construction is capped by
\[
 O\!\left(
 \frac{\sqrt\kappa\,[\log(1/c_0)+a\log(1/\epsilon)]}
      {\log(\kappa/\epsilon)}
 \right).
\]
Its accuracy-dependent part is at most \(O(a\sqrt\kappa)\), and it can be
smaller when \(\log\kappa\) dominates.  This is an obstruction/cap, not a
separately proved hardness exponent.  Corollary 5.1 of Montanaro--Shao permits
padding a shorter circuit up to the endpoint degree; it does not provide
the same coefficient \(c\) for a circuit longer than that degree.  Thus
counting both the original full approximate-degree exponent and a separate
narrow-level amplification is double-counting the available clock length.

### Even exact holonomy is diluted by a long local cyclic clock

A complementary exact calculation rules out hiding the amplification cost
by replacing the path with the standard cyclic resolvent.  Let \(U\) be a
unitary transition on \(L\) clock positions, let \(e\) be a public clock-work
basis state, and suppose the full circuit holonomy is already exact:

\[
 U^Le=\sigma e,
 \qquad \sigma\in\{+1,-1\}.
\]

The vectors \(e,Ue,\ldots,U^{L-1}e\) are orthogonal because their clock
registers differ.  For \(0<\gamma<1\), put \(A=I-\gamma U\) and

\[
 G=\frac{AA^*}{(1+\gamma)^2},
 \qquad
 K=\frac{1+\gamma}{1-\gamma}.
\]

Then \(G\) is Hermitian positive definite,
\(\kappa(G)\leq K^2\), and finite geometric summation
gives

\[
 A^{-1}e
 =\frac1{1-\sigma\gamma^L}
   \sum_{t=0}^{L-1}\gamma^tU^te.
\]

Consequently the two exact single-form values
\(q_\sigma=e^*G^{-1}e\) have ratio

\[
 \frac{q_{+}}{q_{-}}
 =\left(\frac{1+\gamma^L}{1-\gamma^L}\right)^2
 =\coth^2\!\left(\frac L2
   \log\frac{K+1}{K-1}\right).                           \tag{10h}
\]

When the clock circuit is real, as in the Forrelation construction above,
\(U\) is real orthogonal and \(G\) is an ordinary real SPD matrix.

Since \(\log((K+1)/(K-1))\geq2/K\) and
\(\coth x\leq1+1/x\) for \(x>0\),

\[
 \boxed{
 \frac{q_+}{q_-}\leq\left(1+\frac K L\right)^2.
 }                                                        \tag{10i}
\]

Writing the allowed SPD condition as \(\overline\kappa=K^2\), this is
\(O(1+\overline\kappa/L^2)\).  Thus condition-scale contrast
\(\Theta(\overline\kappa)\) requires \(L=O(1)\), even if the hard
computation has somehow produced an exact \(\pm1\) phase.  A growing local
clock, which is necessary to retain the Forrelation walk exponent, dilutes
the contrast before any statistical composition is applied.

This calculation preserves locality: if each clock transition has at most
\(q\) nonzeros in every row and column, then \(G\) is
\((2q+1)\)-sparse.  Public scalar direct-sum
blocks can make its condition exactly \(K^2\) without changing (10h).
Hence (10i) is an obstruction for the standard first-order cyclic
Feynman-resolvent gadget, not merely for a dense unitary dilation.

### A constant-weight path recovers a \(\kappa^2\) outer factor at very high accuracy

The distributional theorem can be instantiated with a different clock whose
public baseline is exactly controlled.  This gives a stronger polynomial
factor than the preceding restricted-interval witness weights in a
restricted high-accuracy regime.

Let \(J_y\) be the length-\(n\) Feynman path for a 2-Forrelation circuit.
Here \(n\) denotes the number of clock vertices and is unrelated to the
temporary integer \(n=\lceil\chi_c/\epsilon\rceil\) used in (10f).  With
clock vertices labeled \(0,\ldots,n-1\), its exact normalization is
\[
 J_y=\frac12\sum_{t=1}^{n-1}
 \left(|t\rangle\langle t-1|\otimes U_t
       +|t-1\rangle\langle t|\otimes U_t^T\right),
                                                               \tag{10o}
\]
where each real orthogonal \(U_t\) is either a public block Hadamard, a
hidden diagonal sign query, or a public identity gate.  A block-diagonal
gauge maps \(J_y\) to the \(n\)-by-\(n\) scalar tridiagonal path \(J_n\),
whose off-diagonal entries are \(1/2\), tensored with the work-space
identity. In (10o), its endpoints are relabeled \(1,n\). Set

\[
 H_y=mI+hJ_y,
 \qquad
 a=\kappa^{-1},\quad m=(1+a)/2,\quad h=(1-a)/2.
\]

Although \(\kappa(H_y)<\kappa\) because the finite path has norm below one,
two public scalar pads at \(a\) and \(1\) make the condition exactly
\(\kappa\) without changing the endpoint forms.  Put

\[
 z_0=\frac mh=\frac{\kappa+1}{\kappa-1},
 \qquad
 R=z_0+\sqrt{z_0^2-1}
   =\frac{\sqrt\kappa+1}{\sqrt\kappa-1}.
\]

The determinant recurrence for the scalar endpoint block is

\[
 D_n=(h/2)^nU_n(z_0).
\]

Therefore, after choosing the public sign of the two-sparse polarization
vector to remove the alternating endpoint sign, the normalized endpoint
coefficient, normalized endpoint diagonal, and relative signal are exactly

\[
 \begin{aligned}
 c_n
   &=a\left|(mI+hJ_n)^{-1}_{1n}\right|
     =\frac{2a}{hU_n(z_0)},\\
 d_n'
   &=a(mI+hJ_n)^{-1}_{11}
     =\frac{2aU_{n-1}(z_0)}{hU_n(z_0)},\\
 \chi_n
   &=\frac{c_n}{d_n'}
     =\frac1{U_{n-1}(z_0)}.                              \tag{10p}
 \end{aligned}
\]

Writing \(\theta=\log R\), the identity
\(U_j(z_0)=\sinh((j+1)\theta)/\sinh\theta\) gives

\[
 \begin{aligned}
 c_n
 &=\frac{16\sqrt\kappa}{(\kappa-1)^2}
   \frac1{R^{n+1}-R^{-(n+1)}},\\
 \chi_n
 &=\frac{4\sqrt\kappa}{\kappa-1}
   \frac1{R^n-R^{-n}},\\
 \frac{\chi_n}{c_n}
 &=\frac{\kappa-1}{4}
   \frac{\sinh((n+1)\theta)}{\sinh(n\theta)}.            \tag{10q}
 \end{aligned}
\]

For \(\kappa\geq16\), \(\theta=\Theta(\kappa^{-1/2})\).  Uniformly once
\(n\theta\geq1\), (10q) implies

\[
 c_n=\Theta(\kappa^{-3/2}e^{-n\theta}),
 \qquad
 d_n'=\Theta(\kappa^{-1}),
 \qquad
 \chi_n=\Theta(\kappa c_n).                              \tag{10r}
\]

For the composition statement, take \(\kappa\geq128\) and
\(0<\epsilon\leq c_*\kappa^{-3/2}\), for a sufficiently small universal
constant \(c_*\).  For the unpadded circuit below, the admissible clock
lengths are exactly \(n=3(\ell+1)\): the three full Hadamards contribute
\(3\ell\) local layers, the two sign queries give \(3\ell+2\) transitions,
and the clock has one more vertex.  A convention adding only a fixed number
of public endpoint identities changes none of the estimates.  Among these
unbounded admissible lengths, choose the largest \(n\) for which
\(c_n\geq\epsilon\).  Consecutive admissible lengths
differ by at most a fixed constant, and (10q) shows that their \(c_n\)'s
differ by at most a universal constant factor.  Thus
\(\epsilon\leq c_n=O(\epsilon)\).  Moreover,
\(\chi_n/c_n\geq(\kappa-1)/4\), so the hypothesis
\(\chi_n\geq24\epsilon\) of (10f) holds.  Equations (10q)--(10r) give

\[
 n=\Theta\!\left(
  \sqrt\kappa\left[1+\log\frac1{\kappa^{3/2}\epsilon}\right]
 \right),
 \qquad
 \chi_n=\Theta(\kappa\epsilon).                          \tag{10s}
\]

Let each Hadamard layer act on \(r\) qubits and put \(q=2^r\), so the SPD
matrix has row/column sparsity at most \(2q+1\).  Here the work register has
exactly \(r\ell\) qubits and each of the three full Hadamards in the
2-Forrelation circuit is decomposed into \(\ell\) genuine \(q\)-sparse
block-Hadamard layers.  Thus the unpadded path has exactly
\(n=3(\ell+1)\) vertices; every growing part of its length is genuine
logical circuit depth, not padding of a shorter hard instance.  The
preceding admissible-\(n\) choice fixes \(\ell=n/3-1\); choosing the
Forrelation input size to be \(r\ell\) then gives the source randomized-query
lower bound \(\Omega(q^{\ell/2}/(r\ell))\).  Applying the
product-distribution theorem
above with

\[
 M=\Theta((\chi_n/\epsilon)^2)=\Theta(\kappa^2)
\]

independent blocks proves the one-form lower bound

\[
 \boxed{
 Q=\Omega\!\left(
   \frac{\kappa^2 q^{\ell/2}}{r\ell}
 \right),
 \qquad
 \ell=\Theta\!\left(
  \sqrt\kappa\left[1+\log\frac1{\kappa^{3/2}\epsilon}\right]
 \right).
 }                                                        \tag{10t}
\]

Every entry and full-SQ query still uses at most a constant number of hidden
sign queries.  Indeed, in (10o) each adjacent clock branch has squared row
mass exactly \(1/4\), whether \(U_t\) is block Hadamard, diagonal sign, or
identity.  In \(H_y=mI+hJ_y\), interior rows therefore have squared norm
\(m^2+h^2/2\), while boundary rows have squared norm
\(m^2+h^2/4\).  Conditional squared-entry sampling first chooses a public
forward, reverse, or diagonal branch; it is then uniform on a public
Hadamard support or deterministic for a sign/identity gate.  Global sampling
and the Frobenius norm are consequently public clock-only quantities, and a
requested hidden value uses one source-sign query.  The same statements hold
for columns because every \(U_t\) is orthogonal with the same row/column
magnitude pattern.

The explicit block-bidiagonal Cholesky recurrence (23)--(24) of the companion
clock note, specialized to the public weight \(1/2\), gives a factor with one
public diagonal block and one local \(U_t\) block per row.  Its norm tables
are public and its sparsity is \(O(q)\); no accumulated circuit product occurs
in the factor.  Hence the same construction is one analytic-center box-LP
Newton-decrement instance with hidden-input-independent full-SQ metadata.

Equation (10t) is a same-instance polynomial-factor refinement, not a new
leading exponential envelope.  Relative to the optimized minimax clock, it
spends the additive
\(\Theta(\sqrt\kappa\log\kappa)\) part of the clock exponent needed to
reach the small boundary coefficient \(\Theta(\kappa^{-3/2})\).  Its value
is that the remaining local-walk hardness and the explicit
\(\kappa^2\) outer factor are simultaneously unavoidable on one public
inverse quadratic.

## Two natural gadget classes cannot close the gap

The preceding obstruction can be made exact for the two most direct
compilers: a two-cluster polarization and a scalar Schur resonance.

### Direct two-cluster polarization still needs a narrow amplitude

Let \(J_y=J_y^T\) and \(J_y^2=I\), and take

\[
 G_y=mI+hJ_y,
 \qquad
 m=\frac{1+\kappa^{-1}}2,
 \qquad
 h=\frac{1-\kappa^{-1}}2.                                \tag{11}
\]

Thus \(G_y\) has only the two eigenvalues \(\kappa^{-1}\) and \(1\).
Suppose two public orthogonal unit vectors \(x,z\) obey

\[
 x^TJ_yx=z^TJ_yz=0,
 \qquad
 u_y=x^TJ_yz,
\]

as happens for opposite sides of the usual symmetric unitary dilation.
For \(b_+=(x+z)/\sqrt2\), direct calculation gives

\[
 b_+^TG_y^{-1}b_+
 =\frac{\kappa+1-(\kappa-1)u_y}{2}
 =1+\frac{\kappa-1}{2}(1-u_y).                            \tag{12}
\]

Consequently a low-amplitude case \(|u_y|\leq\eta\) has value
\(\Theta(\kappa)\), whereas a high-amplitude case has value \(O(1)\)
uniformly **only if**

\[
 1-u_y=O(1/\kappa).                                       \tag{13}
\]

For the unamplified Forrelation promise \(u_y\in[3/5,1]\), the worst
high-case value in (12) is
\((\kappa+1-3(\kappa-1)/5)/2=\kappa/5+O(1)\).  Its uniform
contrast against the low case is therefore
only constant.  This rules out the tempting idea that an exact
two-eigenvalue dilation plus polarization alone converts the published
constant-gap clock into the required \(\Theta(\kappa)\)-contrast family.
It also shows that the \(O(1/\kappa)\) coherent amplification accuracy
mentioned above is not merely an artifact of the Schur proposal.

### Resonance spends a multiplicative condition budget

There is a more general obstruction to appending one positive Schur
coordinate.  Normalize an SPD base matrix by
\(\lambda_{\max}(G)=1\), and consider

\[
 \mathcal H=
 \begin{pmatrix}
   \alpha&w^T\\
   w&G
 \end{pmatrix}\succ0,
 \qquad
 S=\alpha-w^TG^{-1}w>0.                                  \tag{14}
\]

Block inversion gives

\[
 e_0^T\mathcal H^{-1}e_0=S^{-1}.                         \tag{15}
\]

The vector \((1,-G^{-1}w)\) has Rayleigh quotient
\(S/(1+\|G^{-1}w\|^2)\), while interlacing gives
\(\lambda_{\max}(\mathcal H)\geq\lambda_{\max}(G)=1\).
Hence the following exact condition lower bound holds:

\[
 \boxed{
 \kappa(\mathcal H)
 \geq \frac{1+\|G^{-1}w\|^2}{S}.
 }                                                         \tag{16}
\]

Now write \(w=t v\) for a unit vector \(v\), and suppose the channel used
by the gadget is condition-scale,

\[
 v^TG^{-1}v\geq cK_0,
 \qquad K_0=\kappa(G),                                    \tag{17}
\]

while its scaled Schur subtraction is nonvanishing,

\[
 w^TG^{-1}w\geq c_0.                                     \tag{18}
\]

Cauchy--Schwarz for the spectral measure of \(v\) gives

\[
 v^TG^{-2}v\geq (v^TG^{-1}v)^2.
\]

Using \(t^2=(w^TG^{-1}w)/(v^TG^{-1}v)\), (17)--(18) imply

\[
 \|G^{-1}w\|^2
 =t^2v^TG^{-2}v
 \geq c_0cK_0.                                           \tag{19}
\]

If the resonant label sets \(S=\Theta(1/R)\), so that (15) has size
\(\Theta(R)\), then (16) and (19) force

\[
 \boxed{\kappa(\mathcal H)=\Omega(K_0R).}                \tag{20}
\]

Thus a Schur complement can indeed turn a narrow scalar gap into a large
inverse quadratic, but it cannot do so for free on the condition-scale
polarization channel required by the proposed saturation route.  Asking
simultaneously for base local-walk condition
\(K_0=\Theta(\kappa)\), contrast
\(R=\Theta(\kappa)\), and final condition \(O(\kappa)\) contradicts
(20); the naive gadget has final condition \(\Omega(\kappa^2)\).
Equivalently, imposing final condition \(O(\kappa)\) and contrast
\(R=\Theta(\kappa)\) leaves only \(K_0=O(1)\), eliminating the growing
local-walk exponent.

The assumptions in (17)--(18) are important.  This is not a no-go theorem
for every higher-dimensional or indefinite linearization.  It closes the
positive scalar Schur gadget, including its two-level/Wielandt-saturating
special case, and identifies the only possible escape: create the resonant
gap through a channel whose inverse second moment
\(\|G^{-1}w\|^2\) stays bounded even though the encoded hard signal remains
order one.  Cauchy--Schwarz shows that simple rescaling of a
condition-scale positive inverse quadratic cannot have that property.

There is also a useful optimization corollary.  Let \(\overline K\) be the
allowed final condition number.  Within this scalar-resonance class, (20)
forces

\[
 R=O(\overline K/K_0).                                    \tag{21}
\]

Write the clock factor abstractly as
\(L_{\rm walk}(K_0)=\exp(A\sqrt{K_0})\), with
\(A=\Omega(\log s)\) and with any accuracy logarithm absorbed into \(A\).
The largest formal product supplied by the conditional compiler under
(21) is bounded, apart from the common \(\epsilon^{-2}\) and
polylogarithmic factors, by

\[
 \max_{1\leq K_0\leq\overline K}
 \frac{\overline K}{K_0}\exp(A\sqrt{K_0}).                \tag{22}
\]

Putting \(t=\sqrt{K_0}\), the logarithm of the optimized factor is
\(\log\overline K-2\log t+At\).  Its only interior stationary point is a
minimum, so (22) is attained at an endpoint:

\[
 \max\left\{
   \overline K e^A,
   \exp(A\sqrt{\overline K})
 \right\}.                                                \tag{23}
\]

Thus the condition-dependent part of this gadget class interpolates between
the statistical endpoint and the local-walk endpoint; it never multiplies
the full \(\overline K\) statistical factor by the full
\(L_{\rm walk}(\overline K)\) factor at fixed final condition.  The common
outer \(\epsilon^{-2}\) factor is not ruled out if some separate
argument supplies constant-contrast levels.  The distributional construction
above obtains that factor at fixed \(c\) without pointwise narrowness; a
pointwise compiler would still need narrow levels.  This is a gadget-class
verdict, not an upper bound on the query complexity of arbitrary sparse SPD
families.

## Defensible present frontier

For \(0<c\leq c_0\) with \(\chi_c\geq C\epsilon\), let \(L_c\) denote the explicit inner
bound in (10a) and define

\[
 L_{\rm dist}
 =\sup_{\substack{0<c\leq c_0\\ \chi_c\geq C\epsilon}}
   (\chi_c/\epsilon)^2L_c,
 \qquad \chi_c=\kappa c/d_c.
\]

The currently justified lower envelope is therefore

\[
 \boxed{
 \Omega\!\left(
 \max\left\{
   L_{\rm walk},
   \min\{N,\kappa/\epsilon^2\},
   L_{\rm dist}
 \right\}\right),
 }                                                         \tag{24}
\]

using the union of the pure families and the distributional direct-product
family.  The third term need not exceed the maximum of the first two at
leading exponential order, but it certifies that both costs occur on one
single-form instance.  In the high-accuracy regime of (10t), for
\(q=2^r\) and matrix sparsity at most \(2q+1\), this union contains the
explicit additional specialization

\[
 L_{\rm path}
 =\Omega\!\left(\frac{\kappa^2q^{\ell_\epsilon/2}}
                       {r\ell_\epsilon}\right),
 \qquad
 \ell_\epsilon=\Theta\!\left(
  \sqrt\kappa\left[1+\log\frac1{\kappa^{3/2}\epsilon}\right]
 \right),                                                \tag{24'}
\]

valid for \(\kappa\geq128\) and
\(0<\epsilon\leq c_*\kappa^{-3/2}\).  This is a same-instance polynomial
refinement and is not claimed to improve the maximum lower envelope at
leading exponential order.  The stronger full
\(\kappa/\epsilon^2\)-factor product would follow
from the conditional compiler (7), but only after proving a
single-form, full-SQ-blind sparse clock with
\(\Theta(\kappa)\) inverse-quadratic contrast.  This contrast lemma, not
block-diagonal bookkeeping, is the concrete open problem.

## Literature boundary

[Chakraborty--Kayal--Mittal--Paraashar--Sanyal--Saurabh](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2023.63)
prove in their Theorem 2 that
\(R(F\circ g)=\Omega(R(F)R(g))\) whenever the partial outer function has
linear randomized complexity; this is the theorem used in (7).  Their
generic composed upper bound has the familiar amplification logarithm, but
that does not weaken the lower bound used here.

[Ben-David--Blais](https://arxiv.org/abs/2002.10809) disprove the unrestricted
randomized composition conjecture and characterize the strongest universal
replacement using noisy randomized complexity.  More specifically, their
Definitions 33--34 and Theorem 35 construct the product-form hard
distribution (10c), and their Theorem 24 supplies
\(\operatorname{sfR}(g)=\Omega(R(g))\); these are the distributional facts
used in (10g).  Thus an unqualified pointwise appeal to a product composition
theorem would be incorrect, while the distributional use above is covered
by their stated theorem.

The 2025 direct-product work of
[Ben-David--Blais](https://arxiv.org/abs/2512.08268) proves strong direct
product, list-decoding, and threshold theorems for many-copy computation.
Those results reinforce that many hard copies can tensorize, but they do not
remove the matrix-side contrast requirement (4): the scalar average in (2)
must first encode the required outer relation.
