# Contact regularity is not a standard IPM condition number

Status: Proved no-go boundary; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the stated pointwise no-go and conditional bridge

## Conclusion

The robust sphere-submersion obstruction has a genuine, coordinate-invariant
consequence for an approximate low-capacity cone factorization: its
*cross-contact sensitivity* must deteriorate.  In the \(C^{1,1}\) case,

\[
 \delta+K_A\sqrt{2H_B\epsilon}\geq\mu
 \quad\Longrightarrow\quad
 \boxed{
 H_B\geq{(\mu-\delta)^2\over2K_A^2\epsilon}
 }
                                                               \tag{1}
\]

whenever \(\delta<\mu\), \(\epsilon>0\), and \(K_A,H_B>0\).  Here
\(K_A=\|d\log\ell(A)\|_\infty\), and \(H_B\) uniformly bounds the
Lipschitz variation, with the first contact label held fixed, of the
one-sided partial covector

\[
 d_y\langle A(x),B(y)\rangle .                                \tag{2}
\]

More precisely, in normal coordinates \(y=\exp_x(v)\), \(H_B\) bounds the
variation in \(v\) of
\(d_y\langle A(x),B(y)\rangle\), with \(x\) fixed.  As in the parent
robust theorem, (1) assumes that the optimizing interpolation radius
\(\sqrt{2\epsilon/H_B}\) lies below the fixed normal radius \(r_0\) of the
contact sphere.  If \(K_A=0\) or \(H_B=0\), the antecedent
\(\delta<\mu\) is incompatible with the parent robust inequality, so the
displayed division loses no nontrivial case.

Equation (1) is not, by itself, a Newton/KKT condition-number or numerical-
precision lower bound.  Standard central-neighborhood, Nesterov--Todd
scaling, and barrier-Hessian measures are pointwise in one primal--dual
iterate.  The quantities in (1) differentiate a globally selected family
across different contact objectives.  Two explicit Lorentz-cone families
below keep all standard pointwise measures uniformly fixed while making,
respectively, \(K_A\) and the one-sided derivative in (2) arbitrarily large.

Thus no unconditional QIPM complexity consequence follows from the robust
topological theorem without an additional cross-objective sensitivity or
data-variation contract.  This is a no-go boundary, not a claim that a
well-conditioned approximate low-capacity lift exists.

## 1. The robust quantities are cone-coordinate invariant

Let \(K\subset V\) be proper, let
\(A:M\to\partial K\setminus\{0\}\),
\(B:M\to\partial K^*\setminus\{0\}\), and choose
\(\ell\in\operatorname{int}K^*\).  Under a fixed block isomorphism
\(G\in GL(V)\), transform

\[
 K'=GK,\qquad A'=GA,\qquad B'=G^{-T}B,
 \qquad \ell'=G^{-T}\ell.                                    \tag{3}
\]

Then

\[
 \begin{aligned}
 \langle A',B'\rangle&=\langle A,B\rangle,\\
 -dA'^*dB'&=-dA^*dB,\\
 A'^*dB'&=A^*dB,\\
 \ell'(A')&=\ell(A).
 \end{aligned}                                                \tag{4}
\]

Consequently \(K_A\), the one-sided contact derivative, its modulus
\(H_B\), the mixed-channel singular values, and the approximation error
\(\delta\) are unchanged when the normalization covector is transported
as part of the cone representation.  The sparse Lorentz-boost objection to
raw Euclidean factor norms therefore does not invalidate (1).

The missing bridge is different: pointwise IPM geometry does not control
derivatives across contact labels.

## 2. Exact centrality does not bound the radial derivative

Use the Lorentz Jordan algebra on

\[
 Q_3=\{(t,z)\in\mathbb R\oplus\mathbb R^2:t\geq\|z\|\},
 \qquad
 (t,z)\circ(s,w)=(ts+z^Tw,tw+sz).                             \tag{5}
\]

For fixed \(p_0\in S^1\), put

\[
 c_\pm={1\over2}(1,\pm p_0).
\]

These are orthogonal primitive idempotents:
\(c_++c_-=e=(1,0)\), \(c_+\circ c_-=0\).  On \(S^n\), define

\[
 h_k(x)=\sin(kx_1),\qquad a_k(x)=e^{h_k(x)},                   \tag{6}
\]

and boundary factors

\[
                  A_k=a_kc_+,qquad B_k=a_k^{-1}c_-.          \tag{7}
\]

They are exactly complementary.  Moreover

\[
 e^{-1}\leq a_k\leq e,qquad
 K_{A,k}=\|d\log a_k\|_\infty=k,                             \tag{8}
\]

because equality is attained on the equator \(x_1=0\).

For a fixed \(0<\tau<1\), regularize them to the interior pair

\[
 X_k=a_k(c_++\tau c_-),qquad
 S_k=a_k^{-1}(c_-+\tau c_+).                                 \tag{9}
\]

Then

\[
                         X_k\circ S_k=\tau e                 \tag{10}
\]

at every label: the pair is exactly central, not merely in a fixed
neighborhood.  The standard Lorentz barrier

\[
                    F(t,z)=-\log(t^2-\|z\|^2)                 \tag{11}
\]

obeys \(\nabla^2F(au)=a^{-2}\nabla^2F(u)\).  Hence the primal and
dual barrier-Hessian condition numbers in (9) depend only on \(\tau\), not
on \(k\); their norms are also uniformly bounded above and below because
\(a_k\in[e^{-1},e]\).  The Nesterov--Todd scaling-point spectral ratio is
likewise \(1/\tau\), independent of \(k\), and its overall scale stays
bounded because \(a_k\) does.

Thus exact centrality, distance to the cone boundary at a fixed \(\tau\),
scaling-point conditioning, and barrier-Hessian conditioning do not upper-
bound \(K_A\).

## 3. A fixed central neighborhood does not bound the one-sided derivative

Let

\[
 \phi_k(x)=kx_1,qquad
 p_k(x)=(\cos\phi_k(x),\sin\phi_k(x)),                         \tag{12}
\]

and, for a fixed angle \(0<\theta<\pi/2\), let
\(q_k=R_\theta p_k\).  Define the nonzero boundary factors

\[
                  A_k=(1,p_k),\qquad B_k=(1,-q_k).             \tag{13}
\]

Their diagonal contact defect is constant:

\[
 \sigma_k=\langle A_k,B_k\rangle=1-\cos\theta,
 \qquad d\sigma_k=0.                                         \tag{14}
\]

Nevertheless, with \(J\) the quarter-turn in \(\mathbb R^2\),

\[
 \begin{aligned}
 dB_k&=(0,-Jq_k\,d\phi_k),\\
 A_k^*dB_k&=\sin\theta\,d\phi_k,\\
 \|A_k^*dB_k\|_\infty&=k\sin\theta.                        \tag{15}
 \end{aligned}
\]

This also explicitly shows why the total derivative \(d\sigma\) cannot
replace a one-sided partial derivative in the rank-\(r\) robust theorem.

Regularize to

\[
 X_k=(1+\tau,p_k),\qquad S_k=(1+\tau,-q_k).                   \tag{16}
\]

At every label, this pair is obtained from one fixed pair by a common
spatial rotation, an orthogonal automorphism of \(Q_3\).  Therefore all
orthogonally invariant pointwise quantities---the spectra and condition
numbers of both barrier Hessians, the spectrum and condition number of the
Nesterov--Todd scaling point, and every standard scale-invariant proximity
measure---are independent of \(k\).

For completeness, its Jordan-product central residual is explicit.  Put

\[
 d_\tau=(1+\tau)^2-\cos\theta.
\]

Then

\[
 X_k\circ S_k-d_\tau e=(0,(1+\tau)(p_k-q_k)),
\]

and hence the relative spectral residual is

\[
 \rho(\tau,\theta)=
 {2(1+\tau)\sin(\theta/2)
  \over 2\tau+\tau^2+1-\cos\theta}.                          \tag{17}
\]

For any fixed \(\tau\) and any prescribed open central-neighborhood radius,
choose \(\theta>0\) sufficiently small.  The entire family then remains in
that neighborhood for every \(k\), while (15) diverges linearly in \(k\).
The barrier distance to the boundary is also fixed by \(\tau\).

The separation persists while the contact error vanishes: taking
\(\theta_k=k^{-1/2}\) gives
\(\sigma_k=1-\cos\theta_k=\Theta(k^{-1})\),
\(\rho(\tau,\theta_k)=O(k^{-1/2})\), but
\(\|A_k^*dB_k\|_\infty=\Theta(k^{1/2})\).  Thus improving pointwise
centrality does not control cross-contact sensitivity.

The mixed boundary channel in this example is

\[
                  -dA_k^*dB_k=cos\theta\,
                     d\phi_k\otimes d\phi_k,                  \tag{18}
\]

so its derivatives can also grow although all pointwise interior geometry
is unchanged.  At critical points of \(x_1\), the channel loses rank, as
the global phase theorem requires.

## 4. What the counterexamples prove

Call a cone-local IPM measure *pointwise* if it is a function of an interior
pair \((X,S)\), a fixed self-scaled barrier and its derivatives at that
pair, and their Nesterov--Todd scaling point, but not of derivatives with
respect to a family of objectives or contact labels.

### Theorem 1 (no pointwise conditioning bridge)

There is no universal upper bound on either \(K_A\) or
\(\|A^*dB\|_\infty\) in terms only of:

1. a standard primal--dual central-neighborhood radius;
2. primal and dual barrier-Hessian spectral condition numbers;
3. the Nesterov--Todd scaling-point spectral condition number; and
4. fixed interior distance parameter \(\tau\).

This remains false when all factor norms and all Hessian norms are bounded
above and below by constants independent of the family index.  Equations
(6)--(10) prove the claim for \(K_A\); equations (12)--(17) prove it for the
one-sided derivative.

The separation can even be embedded in a pointwise assembled KKT system.
For any displayed interior pair, use the identity equality \(Iz=X\), set
the objective vector so that the displayed \(S\) is dual feasible, and take
the current multiplier to be zero.  The Newton saddle matrix has the form

\[
              \begin{pmatrix}H_{\mu_c}(X)&I\\ I&0\end{pmatrix},
              \qquad H_{\mu_c}(X)=\mu_c\nabla^2F(X).          \tag{19a}
\]

Here the positive central scalar \(\mu_c\) may equivalently be absorbed
into the barrier Hessian.  For the fixed \(\tau\) families above it stays
bounded above and below.  Uniform upper and lower spectral bounds on
\(H_{\mu_c}(X)\) therefore give a uniform condition bound for (19a),
independent of \(k\).  This does not make the artificial
identity-constrained problems a single approximate lift; their right-hand
sides vary with the contact label, and that variation is precisely what a
cross-objective condition would have to charge.

The theorem is coordinate-invariant in the relevant sense.  It does not
rely on a badly chosen fixed cone basis: family (15) varies by orthogonal
cone automorphisms, and (4) shows that the contact quantities themselves
are invariant under a fixed block isomorphism.

The theorem does **not** construct an approximate forbidden low-capacity
lift of a fixed convex body with a well-conditioned assembled KKT system.
The factor kernels in Sections 2--3 isolate the missing implication.  They
prove that cone-local centrality and scaling data alone cannot supply it.
A stronger bridge could still follow from the affine constraints, a
specified objective-to-contact parametrization, and a uniform sensitivity
theorem for the full KKT solution map.

## 5. The exact conditional bridge that remains

Although standard pointwise measures are insufficient, (1) gives a clean
target for a future global sensitivity theorem.  Suppose a representation-
specific condition measure \(\chi\) is proved to control

\[
                   K_A\leq c_K\chi^a,
 \qquad H_B\leq c_H\chi^b                                   \tag{19}
\]

for fixed positive constants \(c_K,c_H,a,b\), after the contact parameter
metric and input-data normalization have been fixed.  Then the robust
obstruction rigorously implies

\[
 \boxed{
 \chi\geq
 \left({\mu-\delta\over c_K\sqrt{2c_H\epsilon}}\right)^{
       1/(a+b/2)}
 }
                                                               \tag{20}
\]

when \(\delta<\mu\).  This is algebraic substitution, not an assertion that
the Newton condition number currently satisfies (19).

Likewise, if a concrete finite-precision representation proves
\(H_B\leq C2^{qb}\) using \(b\) coefficient bits while \(K_A\leq K_0\),
then

\[
 b\geq {1\over q}\log_2
 \left({(\mu-\delta)^2\over2CK_0^2\epsilon}\right).           \tag{21}
\]

Equation (21) is a valid conditional precision ledger.  Without its
representation-specific upper bound on \(H_B\), large derivatives can be
encoded by a short arithmetic description, so no unconditional bit lower
bound follows.

## 6. Literature boundary and QIPM relevance

Nesterov and Todd's self-scaled framework defines central neighborhoods,
local barrier norms, and scaling points for a *single interior primal--dual
pair*; see
[*Self-Scaled Barriers and Interior-Point Methods for Convex
Programming*](https://doi.org/10.1287/moor.22.1.1) and
[*Primal-Dual Interior-Point Methods for Self-Scaled
Cones*](https://doi.org/10.1137/S1052623495290209).  Todd--Toh--Tutuncu
prove scale invariance of the NT direction in
[*On the Nesterov--Todd Direction in Semidefinite
Programming*](https://doi.org/10.1137/S105262349630060X).  These results do
not bound derivatives of a factor selection across changing objectives.

The symmetric-cone QIPM of Augustino--Nannicini--Terlaky--Zuluaga explicitly
pays for the spectral condition number of each NT Newton system, block
encoding, and tomography; see
[*An Infeasible-Inexact Quantum Interior Point Method for Convex Quadratic
Symmetric Cone Optimization*](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/21/21T_010.pdf).
Their complexity parameter is a per-iteration linear-system condition
number, not the derivative of the solution or contact-factor map across
instances.  The later SDP QIPMs likewise assume a condition-number bound for
the Newton systems; see
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://doi.org/10.22331/q-2023-09-11-1110).

There is an established, compatible route from regularity of the assembled
KKT equations to cross-instance sensitivity, but it requires hypotheses
absent from a central-neighborhood bound.  Alizadeh--Haeberly--Overton
formulate primal and dual nondegeneracy and relate them to uniqueness under
strict complementarity in
[*Complementarity and nondegeneracy in semidefinite
programming*](https://doi.org/10.1007/BF02614432).  Sturm--Zhang study the
analytic central path under right-hand-side perturbations, assuming
primal--dual Slater and strict complementarity; importantly, they also note
that the resulting directional-derivative bounds need not be uniform over
the parameter set.  See
[*On sensitivity of central solutions in semidefinite
programming*](https://doi.org/10.1007/PL00011422).  Any inverse-Jacobian
argument controls the solution derivative only after the norm of the data
path is fixed as well.  This is exactly the kind of additional contract
represented abstractly by (19); it is not a consequence of pointwise
centrality alone.

A targeted search of self-scaled IPM, NT scaling, QIPM conditioning, cone
factorization, and quantitative submersion literature found no theorem
implying (19) from a standard central-neighborhood or Newton-matrix
condition number.  The new rigorous conclusion is therefore the separation
in Theorem 1 and the intrinsic cross-contact lower bound (1), with (20)--
(21) explicitly conditional.  Novelty remains subject to specialist
review.

## Audit checklist

- Jordan products in (10) and the residual ratio (17) are explicit.
- Both counterexamples use bounded factor scales and fixed \(\tau\).
- Common spatial rotations are orthogonal cone automorphisms, so raw
  barrier-Hessian spectra as well as invariant NT measures are fixed.
- The boundary contact quantities in (4) are invariant under fixed block
  coordinate changes.
- No well-conditioned assembled KKT system for a single fixed lift,
  arbitrary-lift theorem, or unconditional bit-precision lower bound is
  claimed.

An independent hostile audit checked the Lorentz/Jordan algebra, NT and
barrier-Hessian conditioning, rotating-family signs, central residual,
artificial KKT embedding, coordinate-invariance scope, conditional
exponents, and sensitivity-literature wording.  It returned **PASS** after
the interpolation-radius, positive-denominator, and fixed-lift caveats were
made explicit.
