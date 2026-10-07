# Prewriting audit: algebraic singletons and cyclic quartics

Date: 2026-10-05. This is an internal independent proof review. It is not a
literature or priority audit. No mathematical scripts, computational
experiments, project-wide checks, or CI checks were run.

## Verdict and manuscript decisions

The main constructions survive reconstruction. I found no blocking defect
in the compact irrational-zero example, the effective general realization,
the positive definite rational Hessian Gram construction, the shortened
power-coordinate realization, the cyclic field-degree construction, the
rational square compression, or the restricted binomial-network bound.
The expanded audit also reconstructs the rational-SOS degree upper bounds,
the sharp maximum 21 in five variables, the real SOS-length lower bound,
the univariate degree obstruction and compressed alternative, and the
quadratic graph lift. Their exact primary-source contracts remain for
the literature agent to vet. The recorded local-conditioning conclusions
are valid. The cyclic condition bound improves analytically from O(n^3)
to O(n^2). Canonical Gram covariance removes an unnecessary approximation
and projection from the rational Hessian-certificate algorithms.

The manuscript must state the following restrictions explicitly:

- The general polynomial-time realization takes a **dense** minimal
  polynomial as input. Irreducibility and the presence of exactly one real
  root may be promises. Reading and normalizing arbitrary rational input
  is charged to its original total bit length L.
- The dimension lower bound concerns the prescribed point
  `(alpha, alpha^2, ..., alpha^n)`. It is not a lower bound for arbitrary
  coordinate encodings of the same field.
- A positive definite **Hessian** Gram matrix on `(v, x tensor v)` is
  compatible with an irrational zero. A positive definite full Gram
  matrix for the polynomial itself is a different claim and is not made.
- The cyclic output lower bound concerns the minimal polynomial of a
  specified coordinate in the ordinary monomial coefficient basis.
  It does not exclude short rational-power expressions, arithmetic
  circuits, shifted bases, or sparse representations using an auxiliary
  primitive element and coordinate maps.
- Cyclic degree and list-output growth are exponential in n. The input
  has polynomial length in n, which proves a superpolynomial obstruction
  in L; it does not by itself prove a lower bound of the form 2^(cL).
- The one-real-conjugate restriction concerns rational convex singleton
  feasibility and the singleton zeros being constructed. Do not extend
  it without proof to arbitrary constrained unique optimizers.
- The conditioning statements concern the Hessian **at the optimizer**.
  They do not supply a global upper Hessian bound, a fixed neighborhood
  with uniform smoothness, or bounds on every conditioning notion.

Sections 12--17 below supply the extended audits. The universal degree
bounds retain the rational-SOS hypothesis; the SOS-length bound allows
arbitrary real square factors. These are different coefficient-field
contracts. The compressed cyclic family has minimum real SOS length
exactly n+1 by the audited length theorem.

## 1. Necessity of one real conjugate

A sound characterization is:

> A real algebraic number alpha occurs as a coordinate of a singleton
> defined by finitely many rational globally convex polynomial weak
> inequalities if and only if its minimal polynomial has exactly one
> real root. For irrational alpha, the constructive sufficiency can use
> three strictly convex quadratics, or one nonnegative globally strongly
> convex rational SOS-convex quartic with a rational Hessian certificate.

Here and below the point denoted by p is the optimizer; use P for its
coordinate's minimal polynomial so the manuscript does not overload p.

The necessity proof in `few-quadratic-unbounded-degree.md` is correct,
including its less immediate passage from a joint field to a coordinate
field. Include all of the following steps.

Let C={x: f_i(x)<=0 for i=1,...,r}={p}, where the f_i are rational
convex polynomials. The point p is algebraic. One sufficient justification
is real quantifier elimination: an isolated semialgebraic point over Q
has algebraic coordinates. Alternatively, an existential formula defining
this singleton holds in the real closed field of real algebraic numbers,
so its unique real solution lies in that field.

Let A be the constraints active at p. Their common weak sublevel is also
{p}. If z differs from p and satisfies all active constraints, then every
point p+t(z-p), for 0<=t<=1, satisfies those constraints by convexity.
Each inactive constraint is strictly negative at p; continuity and the
finiteness of the list make a sufficiently short common initial segment
satisfy every inactive constraint. This contradicts C={p}.

Put K=Q(p_1,...,p_n). Every real embedding of K preserves the active
equalities, hence maps p into the active weak sublevel {p}. It therefore
fixes all generators of K. Thus K has precisely one real embedding.
The signature identity [K:Q]=r_1+2r_2 makes its degree odd.

For a coordinate alpha, F=Q(alpha) is a subfield of K, and [K:F] is odd.
Every real embedding of F extends to a real embedding of K: choose a
primitive element of K/F, apply the embedding to its odd-degree minimal
polynomial, and choose a real root. The resulting quotient-field map
is the required extension. Distinct real embeddings of F would give
distinct real embeddings of K. Therefore F has exactly one real
embedding, equivalently the minimal polynomial of alpha has exactly one
real root. Merely asserting that a subfield of a field with one real
embedding also has one real embedding would omit the essential odd-degree
extension argument.

For a rational polynomial with a singleton zero, the embedding argument
already applies to its zero equality and needs no convexity. Convexity
is used to discard inactive inequalities in the more general statement.
The characterization must not be framed as a restriction on all
constrained optimizers: minimizing -x on the rational convex interval
{x: x^2<=2} has unique optimizer sqrt(2), whose minimal polynomial has
two real roots. For an unconstrained globally strongly convex rational
polynomial, an analogous necessity proof can use its rational gradient
equalities and uniqueness of its stationary point, but that is a
separate formulation.

## 2. The compact integer quartic

The displayed bivariate construction is sound. With

    q_1=x^2-y,  q_2=y^2-2x,
    A=12599x^2-10000xy+7937y^2-15874x-12599y+20000,
    F=A^2+10000(q_1^2+q_2^2),

the point p=(r,r^2), r^3=2, annihilates q_1,q_2 and
q_3=(x-y)^2-2x-y+4. The identity
A=7599q_1+2937q_2+5000q_3 gives F(p)=0 exactly.

Writing F/5000^2=G^2+epsilon(q_1^2+q_2^2), with
epsilon=1/2500, and translating by p gives a quadratic matrix H with
H>=I/2, norm H<5, gradient ell with norm ell<1/5000, and residual
Jacobian J satisfying J^T J>=I. The Jacobian determinant is 6 and
trace(J^T J)<23, so its least eigenvalue is greater than 36/23.
The rational enclosure
1259921/10^6<r<1259922/10^6 follows by cubing and implies the claimed
gradient error. These estimates give the scalar Hessian lower bound

    norm(u)^2-(63/1250) norm(u)+1/1250
      = (norm(u)-63/2500)^2+1031/6250000.

Multiplication by 5000^2 yields Hessian F>=4124 I. No local-to-global
inference or Hessian sampling is used.

The second proof with the supplied integer 6-by-6 matrix N proves the
weaker but useful rational certificate Hessian F>=4096 I. Its identity
has scale 16000000 in the v basis and scale 250000 in the w basis;
v=2Uw and U^T N U=16M account for the factor 64. All six stated
diagonal-dominance margins are positive. The decomposition

    v^T N v = sum_i delta_i v_i^2
               + sum_{i<j} |N_ij|(v_i+sign(N_ij)v_j)^2

is immediate by expansion and proves nonnegativity for every real
argument. Its affine coordinate change is invertible. Thus the compact
example has both a rational scalar SOS and a rational Hessian certificate.
For a self-contained manuscript, include the full matrix and identity
in an appendix if this proof is cited; a link to a checker or historical
note is not the proof.

The historical formalization record separately covers the actual second
directional derivative bound 4096 and convexity, not the analytic 4124
bound. A manuscript statement about formal verification must preserve
that distinction. I did not compile the formalization or rerun its checks.

## 3. The reusable quantitative convexification lemma

It is clearer and safer to state one lemma for n variables and r residuals,
so the cyclic application can use r=n+1 without changing dimension
factors silently.

Suppose rational quadratics G,h_1,...,h_r vanish at an algebraic point p.
For u=x-p write

    G(p+u)=ell^T u+u^T H u,
    h_j(p+u)=b_j^T u+u^T T_j u.

Assume H>=m I, norm H<=B, norm T_j<=1, norm b_j<=V,
sum_j b_j b_j^T>=nu^2 I, and norm ell<=epsilon, with positive rational
m,B,V,nu. Put D=B+rV. For a positive rational square epsilon=t^2 choose

    epsilon <= min(1, m^2/(2r), nu^2 m^2/(36 n D^2)).

Then Phi=G^2+epsilon sum_j h_j^2 has Hessian at least
(3/2)epsilon nu^2 I on all of R^n. Its normalized form

    F=Phi/(epsilon nu^2)
      =(G/(t nu))^2+sum_j(h_j/nu)^2

is a rational SOS quartic with Hessian at least (3/2)I. If H is positive
definite it has degree exactly four. All square factors vanish at p;
nonnegativity and strong convexity make p the unique zero and optimizer.

The necessary derivative identities are

    Hessian[2(b^T u)(u^T T u)]
      =4[(b^T u)T+b(Tu)^T+(Tu)b^T],
    Hessian[(u^T T u)^2]
      =8(Tu)(Tu)^T+4(u^T T u)T.

For a vector u of norm rho, the homogeneous pieces of Phi have Hessian
bounds respectively

    2 epsilon nu^2 I,
    norm(Hessian Phi_3)<=12 epsilon D rho,
    Hessian Phi_4>=4(m^2-epsilon r)rho^2 I.

The last line must retain the negative contribution of each indefinite
T_j. Squaring a quadratic does not make it convex. Completing the scalar
square gives

    Hessian Phi >=
      [2m^2(rho-3epsilon D/m^2)^2
         +2epsilon nu^2-18epsilon^2 D^2/m^2] I
      >=(3/2)epsilon nu^2 I.

The factor n in the final epsilon condition is unnecessary for this
ordinary Hessian bound, but is needed for the full Gram proof below.
All original applications meet this stronger shared condition.

## 4. Full rational Hessian Gram: proof and algorithm

Use the monomial vector z=(v,u tensor v), where the pair (k,j) means
u_k v_j. For each b,T put

    D(b,T)_{i,(k,j)}=2b_k T_ij+4b_i T_kj.

The cross term 2 v^T D(b,T)(u tensor v) is exactly the middle Hessian
biform in the preceding section. Its operator norm is at most its
Frobenius norm, which is at most 6 sqrt(n) norm(b) norm(T).
The block matrix M with

    C=2ell ell^T+2epsilon sum_j b_j b_j^T,
    D_0=D(ell,H)+epsilon sum_j D(b_j,T_j),
    Q=8 vec(H)vec(H)^T+4 H tensor H
        +epsilon sum_j[8 vec(T_j)vec(T_j)^T+4 T_j tensor T_j]

and blocks [[C,D_0],[D_0^T,Q]] satisfies the exact identity
v^T Hessian Phi(p+u) v=z^T M z.

Here Q>=2m^2 I and norm D_0<=6 sqrt(n)epsilon D. In particular
T_j tensor T_j can have negative eigenvalues and must be bounded below
by -I. The Schur complement is at least

    [2epsilon nu^2-18n epsilon^2 D^2/m^2] I
      >=(3/2)epsilon nu^2 I.

Therefore M is positive definite on its full n+n^2-dimensional vector
space, not only on tensors that can be produced by real u,v.

Removing the algebraic shift is a congruence:

    S_p=[[I,0],[-p tensor I,I]],  M_x=S_p^T M S_p.

With q=2m^2, s=(3/2)epsilon nu^2, B_D=6n epsilon D, and a rational
bound K>=norm p, a sufficient rational gap is

    mu=min(s,q)/[(2+2(B_D/q)^2)(2+K)^2].

Completing the block square proves the first denominator factor; the
bound norm(S_p^{-1})<=2+K proves the second. Its reciprocal has
polynomial bit length whenever the construction's data and reciprocals
do. Although the centered expression for M uses algebraic data, its
congruence M_x is in fact exactly rational. Canonical covariance proves
this and gives a simpler direct algorithm, detailed immediately below.
The historical approximation/projection argument that follows is valid
but unnecessary for these rational quadratic-square constructions.

For an arbitrary quadratic h(x)=d+b^T x+x^T T x, define its canonical
Hessian Gram by the preceding cross and quartic blocks, and constant
block C=2bb^T+4dT. The term 4dT is essential when the quadratic's value
at the chosen origin is nonzero. Write A_c=c tensor I and
S_c=[[I,0],[-A_c,I]]. Direct index contraction gives

    A_c^T Q(T)=D(2Tc,T),
    A_c^T Q(T) A_c=8(Tc)(Tc)^T+4(c^T Tc)T,
    D(b,T)A_c+A_c^T D(b,T)^T
      =4(b^T c)T+4b(Tc)^T+4(Tc)b^T.

Therefore S_c^T M(d,b,T) S_c is exactly the canonical Gram with

    b'=b-2Tc,  d'=d-b^T c+c^T Tc,

which are the coefficients of h(x-c). This is an identity of ordinary
matrices, not merely an identity after evaluation on special tensors.
It extends by linearity to every rational weighted sum of quadratic
squares. Applying it to the centered factors at their common zero shows
that the congruence of the positive definite centered Gram is precisely
the canonical Gram computed from the original rational factors.

Thus compute the output matrix directly from those factors by rational
arithmetic. It is positive definite by congruence, has polynomial bit
length, and requires neither approximating the optimizer again nor
projecting onto coefficient equations. The spectral gap above remains
a valid certificate bound. This simplification, communicated by
`audit_sos_fields` and independently checked here, applies to the general,
shortened, cyclic, circle, and graph-lift rational-square constructions.
It does not replace the earlier projection of a real exposing quadratic
onto its rational **vanishing space**; that projection serves a different
purpose and remains necessary in the corresponding construction.

For completeness, the historical conversion by approximation is also
valid and constructive.
For the unshifted monomial vector z_x=(v,x tensor v), assign **every**
ordered matrix entry to its product monomial gamma, including monomials
whose required coefficient is zero. Let E_gamma be the corresponding
symmetric zero-one matrix. These matrices have disjoint supports, are
Frobenius-orthogonal, and have squared norms between 1 and (n+n^2)^2.
With c_gamma the rational coefficient in the Hessian biform, set

    P(T)=T+sum_gamma E_gamma
                (c_gamma-<E_gamma,T>)/norm(E_gamma)_F^2.

This is orthogonal affine projection onto the coefficient equations.
It fixes M_x and is nonexpansive. A rational symmetric T with Frobenius
error less than mu/4 therefore gives an exact rational Gram P(T)
bounded below by 3mu I/4. Off-diagonal entries are counted twice by
the full Frobenius product, as required. Projection imposes identities;
it is not an SDP-feasibility subroutine.

For the dense general realization, entries of M_x can be written as
polynomials A_ij(alpha) of polynomial degree and rational coefficient
length, obtained from the rational quadratics. If the degree is at most
D_1 and the absolute coefficient sum is at most C_1, then on
[-R-1,R+1] the derivative bound
D_1 C_1(R+1)^(D_1-1) supplies polynomially many precision bits for
entrywise error mu/[4(n+n^2)]. Use the bound 1 when this derivative
bound is zero. Thus a certified rational approximation to alpha and
exact evaluation provide T in polynomial time. In the shortened
construction the same assertion applies to the Hessian Gram after its
quadratics have been made rational; the earlier exposing-template
construction additionally approximates all complex roots.

Rational elimination verifies positive definiteness and has polynomial
bit bounds by determinants of polynomial-size rational matrices. If a
matrix-SOS form is wanted, rational LDL^T gives positive rational
weights. A weight a/b is a sum of at most twice the bit length of ab
rational squares: expand ab in binary, divide the powers by b^2, and
replace each odd power by two identical squares. This avoids irrational
Cholesky weights and integer factorization. Factors remain linear in v,
so they give a rational polynomial matrix-SOS for the Hessian.

## 5. Effective general realization: two valid routes

### The d-1-variable companion route

Normalize the dense input to a primitive integer polynomial of degree d
and coefficient height tau, then divide by its positive leading
coefficient to obtain a monic P. Exactly one real root and d>1 imply
d is odd and d>=3. Set

    R=2^(tau+1), K=d R^(d-1),
    sigma=2^[-tau(d-1)] (2R)^[-d(d-1)/2].

The nonzero integer discriminant proves distinct-root separation greater
than sigma; nonreal roots consequently have imaginary part greater than
sigma/2. These are exponential numerical bounds with polynomial binary
length, which is all the construction needs.

Let W consist of the real root's power column and the real and imaginary
columns of each upper-half-plane root. With s=(d-1)/2,
norm W<=K and abs(det W)>=2^[-s-tau(d-1)]. Thus
norm(W^{-1})<=J_0=2^[s+tau(d-1)]K^(d-1).
The real template B_*=W^{-T}diag(0,1,...,1)W^{-1} has kernel the
real-root power column and is bounded below by K^{-2} on the span U
of the other real columns. It lies in the rationally defined space

    L={B: v(T)^T B v(T) is divisible by P(T)}.

Its values on a nonreal power column are zero because the corresponding
W-coordinates are (1,i), whose squares sum to zero. This is a bilinear
identity using transpose, not a Hermitian identity.

Remainder coefficient matrices E_0,...,E_{d-1} describe L. They are
independent because their entries in positions (0,j) are unit vectors.
Their rational Frobenius Gram inverse gives exact orthogonal projection
onto L. Remainders through degree 2d-2 and all projection entries have
polynomial bit length. Approximate the separated roots to polynomial
precision, compute a rational approximation to B_*, then project.
The final B need only be positive on U; it need not be globally positive
semidefinite. Error less than 1/(16K^2) yields B|_U>=I/(2K^2).

For the rational companion matrix C, the exposing member
(C-alpha I)^T B(C-alpha I) has kernel the real power column. On the
affine subspace z_0=0 its quadratic block is at least I/(2K^4): solve
z_{j+1}=alpha z_j+y_j from z_0=0 to bound norm z<=K norm y.
The rational pencil
C^TBC-u(C^TB+BC)+vB vanishes at the prescribed point for every u,v.
Approximating (alpha,alpha^2) to polynomial precision consequently
retains exact vanishing while making its gradient arbitrarily small.
The norm and gradient tolerances recorded in the notes are sufficient.

Use residuals x_1x_j-x_{j+1} and
x_1x_{d-1}+sum_{j=0}^{d-1}c_j x_j, with x_0=1. Their Jacobian
determinant is P'(alpha): replacing its first column by its product with
(1,2alpha,...,(d-1)alpha^(d-2)) gives only a final nonzero entry,
and the complementary chain minor has the required sign. Root separation
and a bound V on the Jacobian give
nu=sigma^(d-1)/V^(d-2). The convexification and Gram lemmas then apply.
The construction uses d rational squares.

The certified root-approximation theorem is an actual algorithmic input
to this proof. The source already identified in the repository is
Mehlhorn--Sagraloff--Wang, Theorem 5. The manuscript may invoke its
polynomial bit-complexity bound after the literature agent confirms the
primary-source formulation. An uncertified numerical root solver cannot
replace this theorem. No new source research was performed in this review.

### The shorter route and its exact dimension scope

The final realization can use n=(d+1)/2 variables, and its proof is sound.
Write d=2s+1, n=s+1, and factor over the real numbers

    P(T)/(T-alpha)=product_j[(T-u_j)^2+v_j^2].

Each factor has Gram B_j=[[u_j^2+v_j^2,-u_j],[-u_j,1]] bounded
below by bI, b=sigma^2/[4(1+R^2)]. The recursion
G_j=S_j^T(B_j tensor G_{j-1})S_j compresses the product onto consecutive
monomials at every step. Its matrices have polynomial dimension;
I<=S_j^T S_j<=2I gives
b^s I<=G_s and norm G_s<=[2(1+R^2)]^s.

The difference matrix D_alpha sends v_n(T) to (T-alpha)v_s(T).
Therefore Q_*=D_alpha^T G_s D_alpha represents (T-alpha)P(T), is
positive semidefinite with kernel R v_n(alpha), and has affine-block
gap

    gamma=b^s/[n^2 R^(2n-2)].

The inverse of D_alpha on z_0=0 is triangular with powers of alpha,
which proves that gap. Project a sufficiently accurate rational root-based
approximation of Q_* onto
{Q: v_n(T)^T Q v_n(T) is divisible by P(T)}. These d congruence
equations remain independent: every degree 0,...,d-1 occurs as some
i+j with 0<=i,j<=n and is unchanged by reduction. Only degrees through
2n=d+1 require reduction. Orthogonal projection preserves error and
exact vanishing. The explicit root-to-matrix bounds in the source give
H>=gamma I/2 and norm ell<=epsilon with polynomially many precision
bits. Forming a huge uncompressed tensor product is unnecessary.

For the terminal residual represent T^k, n<k<=d, by x_n x_{k-n};
use x_k for k<=n. Divide **every** residual by
kappa=1+sum_{k=n+1}^d abs(c_k). This makes all quadratic matrices
have norm at most one. Its Jacobian determinant is
P'(alpha)/kappa^n. The correct separation exponent in its lower bound
is d-1, not n:

    nu=sigma^(d-1)/(kappa^n V^(n-1)).

The reusable lemmas supply n+1 rational square factors and a rational
positive definite Hessian Gram in polynomial bit time. All logarithms
of required gaps and precisions are polynomial in d,tau; expansion has
O(n^4) possible quartic monomials. Primitive normalization and all root
processing are polynomial in the original dense input length L.

The dimension lower bound needs only rationality, global nonnegativity,
and a unique zero at the consecutive-power point. If a degree-at-most-four
F has that zero with q coordinates, restrict to the moment curve:
h(T)=F(T,T^2,...,T^q). This is a nonzero nonnegative rational polynomial.
It has h(alpha)=h'(alpha)=0. Irreducibility and separability give
P^2 dividing h, and consequently 2d<=deg h<=4q. Thus
q>=ceil(d/2)=(d+1)/2. The proof does not restrict arbitrary encodings
or imply an optimal degree bound for n-variable quartics.

The rational case can be stated separately: F(x)=(x-alpha)^2+(x-alpha)^4
has rational SOS structure and positive definite Hessian Gram
[[2+12alpha^2,-12alpha],[-12alpha,12]] on (v,xv), with determinant 24.

## 6. Cyclic family: exact degree and polynomial encoding

For n>=2 let m=n+1, eta=(-1)^m,

    d=(2^m-eta)/3,  s_i=((-2)^i-1)/3,
    a=2^(1/d),  p_i=a^s_i,  p_0=x_0=1.

The positive integer d is odd. Define cyclic residuals
q_i=x_i^2-2^k_i x_{i+1}x_{i+2}, where k_i=0 except
k_{m-2}=eta and k_{m-1}=-eta. The wrap identity
2s_i-s_{i+1}-s_{i+2}=d k_i proves exact vanishing.
Also abs(s_i)<d, so 1/2<p_i<2 and 1/4<w_i=p_i^{-2}<4.

The real exposing combination is the anchored cycle energy:

    sum_i w_i q_i(x)=1/2 sum_i(X_i-X_{i+1})^2,
    X_i=x_i/p_i, X_0=1.

It proves uniqueness of the common real zero, including possible
negative solutions. Since p_1=a^{-1} and every coordinate is a power
of a, Eisenstein applied to T^d-2 proves
[Q(p):Q]=[Q(p_1):Q]=d. The field-degree equality does not depend on
an experimentally computed determinant or a saturation assumption.

The anchored path estimate gives an exposing quadratic matrix between
I/(8n^2) and 8I. Each residual quadratic matrix has norm at most one,
and every residual gradient has norm less than eight. The exact Jacobian
is

    J=diag(p_i^2)(2I-S-S^2) E D_p^{-1},

where E inserts a zero at the anchor and S is a cyclic isometry.
Factorization (2I+S)(I-S), the reverse triangle inequality, and the
anchored path bound give J^T J>=I/(64n^2).

With M=10^6 n^5, epsilon=M^{-2}, Q=32mM^2, and integers z_i with
abs(z_i/Q-w_i)<=1/Q, the rational G=sum_i(z_i/Q)q_i satisfies
norm ell<=epsilon/4, H>=I/(16n^2), and norm H<=9.
Set D=9+8m<=17n. The shared lemma applies because

    epsilon<=min(1, [1/(16n^2)]^2/(2m),
                  nu^2[1/(16n^2)]^2/(36nD^2)),
    nu=1/(8n).

The last right-hand side is at least 1/(170459136 n^9), whereas
epsilon=1/(10^12 n^10). Use m in the residual count and n in the
Gram cross-block dimension. The integral quartic

    F_n=(2 sum_i z_i q_i)^2+sum_i[(2Q/M)q_i]^2
       =4Q^2(G^2+epsilon sum_i q_i^2)

has n+2 integer square factors and Hessian at least I. Every factor is
integral because 2q_i is integral and 2Q/M=64mM is even. Its support
has O(n^2) monomials and coefficients of polynomial magnitude, hence
O(log(n+1)) coefficient bits.

The rational Gram construction has an inverse-polynomial gap here. The
source's explicit unscaled gap 1/(1536 M^2 n^4) is sufficient. Gram
entries in unshifted coordinates have degree at most two in the bounded
coordinates p_i, with rational data of polynomial magnitude, so only
inverse-polynomial coordinate accuracy is needed for rational projection.

Polynomial construction time must avoid a dense degree-d root routine.
The series

    L_N=2 sum_{j=0}^{N-1} 3^[-(2j+1)]/(2j+1)

approximates log 2 with positive tail below 9^{-N}. Evaluate
exp[-(2s_i/d)L_N] by rational Taylor series on [-2,2]; for degree K>=2
the tail is at most 2^(K+2)/(K+1)!. Taking O(log Q) terms gives an
approximation within 1/(4Q), then rounding its product with Q gives
abs(z_i/Q-w_i)<1/Q. This rounds a rational approximation, so no exact
test at an algebraic rounding boundary is hidden. Although d and s_i
have exponential numerical magnitude, they have O(n) bits. Series
denominators raised to O(log n) powers and factorials have polynomial
bit length. The same method approximates p_i for the Gram construction.

The supporting n+1-ellipsoid construction also checks out. With
tau=1/(32n^2), c_i=z_i/Q, G=sum_i c_i q_i, use G+tau q_i.
Their quadratic matrices are at least I/(32n^2). The positive real
multipliers displayed in the source sum them to the exact energy G_*.
Their positivity follows from tau/4-8m/Q>0. Each individual rational
strictly convex quadratic has a rational minimizer different from p,
so its minimum is strictly negative and its sublevel is full dimensional.
The multipliers are proof data, not asserted rational input data.

## 7. Compression from n+2 squares to n+1

The rank-one rational factorization is valid; it does not assert a
rational square root of every rational positive definite matrix.
For a nonzero rational vector g with R=g^T g, choose positive rational
r<sqrt(R) and set

    t=(R-r^2)/(2r), s=(R+r^2)/(2r),
    A=t I+(r/R)g g^T.

Then A^2=t^2 I+g g^T, A is invertible, and
(g^T q)^2+t^2 sum_i q_i^2=sum_i(Aq)_i^2.
The identity is exact over Q. Rational bisection of
R-r^2-3tau r=0 selects r so that tau<=t<=2tau. The derivative
estimate for r(t)=sqrt(R+t^2)-t and the stated stopping width
R tau/[16(R+4tau^2)] ensure the bisection midpoint remains inside
the required parameter interval. All comparisons are rational.

Use g_i=z_i/Q and tau=1/M. The new epsilon=t^2 is between 1/M^2
and 4/M^2, a whole range satisfying the preceding curvature and Gram
conditions. The gradient error is unchanged and remains at most
epsilon/4. The common zero stays the same because A is invertible.

For integer output write r=a/b, S_0=sum_i z_i^2, so R=S_0/Q^2.
The shared denominator D_0=2abQ^2 S_0 clears the entries of A; an even
polynomial-magnitude scale such as 32MnD_0 clears q_i's halves and
normalizes the curvature. Bisection requires only O(log n) steps in
this family, so a,b,D_0 and every factor coefficient have polynomial
magnitude. There are n+1 integer square factors. Their common support
has O(n) monomials; the expanded quartic still has O(n^2) monomials
and O(log(n+1))-bit coefficients. The rational Hessian certificate,
field degree, and all representation restrictions persist.

## 8. Exact output costs and a useful stronger list bound

The unshifted first coordinate p_1 has primitive minimal polynomial
2T^d-1. Its dense coefficient list has d+1 slots, but its ordinary
sparse list has two terms and O(log d) bits. Large degree alone
therefore does not obstruct sparse minimal-polynomial output.

The rational substitution y_1=x_1+1 makes its primitive minimal
polynomial

    H(T)=2(T-1)^d-1.

Translation preserves irreducibility. Since d is odd, the constant
coefficient is -3; every positive-degree coefficient is twice a signed
nonzero binomial coefficient. The integer polynomial is primitive since
its leading coefficient is 2 and its constant coefficient is odd.
Thus both dense and ordinary sparse lists have d+1 nonzero entries.
The quartic substitution creates at most five terms per old monomial
and only constant-size new binomial factors, preserving the input size.

A stronger analytic statement is available: the total ordinary binary
coefficient length of H is Theta(d^2), not only Omega(d). The upper bound
uses binomial(d,j)<=2^d. For j between roughly d/3 and 2d/3, put
l=min(j,d-j). Then

    binomial(d,j)=binomial(d,l)>=(d/l)^l>=2^l,

with l>=d/3-O(1). There are Theta(d) such coefficients, each with
Omega(d) bits. The same order holds for the standard monic rational
minimal polynomial, whose constant coefficient is -3/2. This refinement
requires no experiment. It remains a lower bound in the specified
ordinary coefficient representation.

Do not claim that all sparse univariate descriptions must be large.
For example, take an auxiliary primitive element beta=a^{-1}, with
the two-term polynomial 2beta^d-1=0 and its unique real root. Each p_i
is a single monomial in beta of degree below d: if s_i<=0 use
beta^(-s_i), and if s_i>0 use 2beta^(d-s_i). The translated first
coordinate is 1+beta. Binary exponents make this a short sparse
primitive-element description even after the translation.

Likewise a nonminimal sparse annihilating polynomial is a different
output format; coefficient density of the minimal polynomial does not
automatically prove a term-count lower bound for every multiple. No
exact decision lower bound follows from any of these output results.

## 9. Restricted optimality in binomial networks

The source's restricted theorem is correct, conditional on the classical
interlace identities it states. Their bibliographic verification belongs
to the manuscript's literature agent; this review performed no source
research. The algebraic and graph-theoretic deductions can be reconstructed
without numerical enumeration.

Let a strongly connected directed graph on m=n+1 vertices have two
outgoing arcs at each vertex, possibly loops or repetitions. Include
the equation at the anchor x_0=1 as well as every other vertex:
x_i^2-c_i x_{a(i)}x_{b(i)}=0, c_i rational and nonzero.
Write L_D=2I-A and delete column zero to form the m-by-n exponent
matrix B. The gcd g of all rooted in-arborescence cofactors equals the
index of the row lattice of B. All complex solutions have nonzero
coordinates: nonzero x_0 and each equation propagate nonzeroness along
outgoing arcs, and strong connectivity reaches every vertex.

Normalize by any given real solution. Complex normalized solutions are
characters of the finite group Z^n/row_Z(B), hence number exactly g.
Its exponent proves rational powers for the original coordinates, so
they are algebraic, and all field embeddings give distinct complex
solutions. Thus [Q(p):Q]<=g. Real normalized solutions are characters
into {1,-1}; uniqueness is equivalent to g being odd. This full lattice
index is essential; a single grounded determinant is generally wrong
for a non-Eulerian graph.

The primitive positive stationary vector is tau_i/g. For a non-Eulerian
graph some entry is at least two, while every tau_i<=2^n by choosing
one of the two arcs at each nonroot vertex. Hence odd g<=2^(n-1)-1
for n>=2. For an Eulerian graph all cofactors equal g. The established
Euler-tour/interlace correspondence gives g=q_H(1), and the stated
classical identities give nonnegative coefficients, q_H(2)=2^m, and
q_H(-1)=(-1)^r 2^(m-r), r=rank_F2(I+A_H). Odd g forces r=m.
Since 2^j-(-1)^j>=3 for j>=1,

    3g<=q_H(2)-q_H(-1)=2^m-(-1)^m.

The cyclic family attains this bound by its separate Eisenstein proof.
This is an optimum within the specified network class, not a universal
quartic field-degree upper bound. Equality of cofactor order and largest
Smith invariant is not assumed.

The weighted energy extension and minimal-binomial normal form also
hold. A positive stationary vector gives the energy
sum_i w_i(Y_i^2-Y_{a(i)}Y_{b(i)})=
(1/2)sum_i w_i(Y_{a(i)}-Y_{b(i)})^2. Its undirected difference graph
is connected precisely when the exponent index is odd, by reduction of
B modulo two. For m binomials whose positive semidefinite exposing
combination has corank one at a point with all coordinates nonzero,
every diagonal coefficient is positive. Each summand can supply at most
one positive square monomial because it vanishes at that real point.
The m summands must therefore supply the m positive diagonal entries
one each, yielding the two-out form after rational equation scaling.
The kernel condition gives a positive stationary vector; its support
splits into closed strongly connected components, each giving an
independent energy-kernel vector. Corank one forces a single component.
These arguments justify the normal form under its exact assumptions.

## 10. Conditioning refinements

For the cyclic family at p,

    Hessian Phi(p)=2ell ell^T+2epsilon J^T J.

The historical O(n^3) condition bound is valid but can be improved with
the already proved operator factorization. Its factors have norms
less than 4, at most 4, at most 1, and less than 2, respectively, so
norm J<32. Hence, with epsilon<=1 and norm ell<=epsilon,

    kappa(Hessian Phi(p))
      <=(epsilon+1024)/nu^2
      <=65600 n^2,  nu=1/(8n).

This O(n^2) bound survives integer scaling, coordinate translation, and
square compression. It requires no change to the construction.

The shrinking-circle local-conditioning refinement is also sound.
The unit-circle chain z_j=[(3+4i)/5]^(2^j) has coordinate denominators
exactly 5^(2^j): 3+4i is idempotent modulo 5, so its real and imaginary
numerators never become divisible by 5. Scaling to radius 2^{-j}
cannot cancel these powers of 5. Thus the terminal rational coordinates
still need Omega(2^k) ordinary fraction bits.

The scaled gate coefficient c_j=2^(j-2) makes its derivative at the
point orthogonal, because 2c_j R_{j-1}=1. The full residual Jacobian
is J=I-T, with norm T<=1 and T^(k+1)=0. Thus norm J<=2 and
norm J^{-1}<=k+1. The exposing terms have current block I and
predecessor block with eigenvalues 0,-1; weights k+1-j give an exposing
matrix between I and (k+1)I. Approximating only coefficients multiplying
exact vanishing residuals preserves the zero. Uniform residual division
by C=max(1,2^(k-2)) gives norm-one quadratic parts and
nu=1/[C(k+1)], V=2/C. The reusable lemma does not require V>=1.

The supplied normalized SOS has exact Hessian at p

    2ell ell^T/(epsilon nu^2)+2(k+1)^2 J^T J.

Its first term has norm less than one by the epsilon condition; the
second lies between 2I and 8(k+1)^2 I. This proves the reported
polynomial local condition number while the optimizer's rational
denominator remains exponentially long. The small coefficient and Gram
construction uses dyadic simulation, not the exponentially long exact
fractions. Dyadic squaring errors obey e_j<=3e_{j-1}+2h on the unit
circle's unit neighborhood, so h<=eta/(2*3^k) gives the needed eta
accuracy using O(k+log(1/eta)) bits. This proof step should be included
if the shrinking-circle theorem is integrated here.

## 11. Verification and evidence scope

This audit used analytic reconstruction and targeted reads of the named
construction notes and their dependencies. Commands actually run were
`cat`, `sed`, and `rg` reads scoped to `research-20260927`, reads of
`AGENTS.md` and `paper-exact-arithmetic/evidence/BRIEF.md`, and a
directory existence check for this review's destination. A document-only
`python -c` command verified this review's final newline, absence of
trailing whitespace, and absence of unintended control characters; it
exited zero. `git diff --no-index --check /dev/null
paper-exact-arithmetic/evidence/reviews/prewrite-algebraic.md` emitted no
whitespace diagnostics and returned the new-file difference status one.
The existing review notes report finite exact checks and one formalization;
those records are supplementary evidence, not checks newly performed here.
No historical note, script, or manuscript file was edited.

The substantive manuscript additions recommended by this review are
the complete embedding-extension argument, a residual-count-independent
convexification lemma, exact canonical Gram covariance, explicit
encoding/output restrictions, the full residual/base proofs of the degree
bounds, the flat-direction reduction in the SOS-length theorem, and the
optional O(n^2) cyclic local-conditioning and Theta(d^2) translated
coefficient-list refinements. No unresolved mathematical gap in this
audited construction chain needs to remain as a main theorem hypothesis.

## 12. Universal degree bounds within rational SOS quartics

A sound combined statement is:

> Suppose F=sum_j h_j^2 with rational h_j of degree at most two,
> F^{-1}(0)={p}, and Hessian F(p)>0. Then the joint coordinate-field
> degree D is odd and D<=2^n-1. If F is also globally convex, then
> D<=2^n-3 for n>=3 and D<=2^n-5 for n>=4. The sharp maxima are
> 3,5,11,21 in dimensions 2,3,4,5, respectively.

The last five-variable bound uses Section 13. Rationality of the
individual factors, or equivalently existence of a rational PSD Gram,
is part of the degree theorem. A rational polynomial SOS only over R
does not meet that contract automatically.

At p, Hessian F(p)=2J(p)^T J(p) gives rank n. Select n equations
with nonsingular Jacobian; p and every conjugate are simple isolated
complex zeros of those equations. Isolated-point Bezout bounds their
number by 2^n even if other complex components are present. Their
coordinates are algebraic, and every real embedding gives a real
common zero of **all** original factors, so it must fix p. The joint
degree is odd and at most 2^n-1. The proof counts embeddings of the
joint field; it does not multiply separate coordinate degrees.

For the convex improvements, the flat-direction reduction is important.
The leading quartic F_4 is convex, even and nonnegative. If F_4(d)=0,
the limiting convexity argument from the SOS-length proof gives
F_4(x+td)=F_4(x). Thus its zero space is precisely the kernel of the
rational coefficient map d -> D_d F_4. It is a rational linear space.
Along such a direction the Hessian of the full polynomial is an affine
matrix pencil with coefficient Hessian(D_d F_3). Positivity for every
signed parameter forces that coefficient to zero. Since D_d F_3 is a
homogeneous quadratic, it vanishes. Hence the cubic is also independent
of all quartic-flat directions.

Use rational coordinates (y,t) splitting this space. Then

    F(y,t)=G(y)+t^T A t+t^T(By+c),  A>0,
    t_*(y)=-(1/2)A^{-1}(By+c).

The positive definiteness of A comes from the Hessian at p. Substitution
on this rational affine graph preserves rational SOS, global convexity,
unique zero, positive definite Hessian there, and the joint coordinate
field. In the remaining variables its leading quartic is positive on
every nonzero real direction. If any direction was removed, the ordinary
2^(n-1)-1 degree bound is already smaller than the degrees being excluded.
If no variable remains the zero is rational. This avoids unjustified
claims about real points at infinity when the leading quartic is flat.

The weighted projective count used next is correct. For every reduced
irreducible projective component X, assign weight 2^(dim X) deg X.
Start from P^n, of weight 2^n, and cut by the n quadrics one at a time.
Retain a component contained in the next quadric; otherwise proper
hypersurface Bezout bounds the total degrees of the dimension-lowered
components by twice the former degree. The total weight does not
increase. Keep duplicates as an overcount, so partial improper
intersections do not create a gap. Isolated points each contribute one.
Any remaining positive component contributes at least two.

To exclude D=2^n-1, this count forces the selected projective n-quadric
intersection Z to be finite, hence a complete intersection of length
2^n. Its simple orbit leaves a length-one residual defined over Q;
it is a reduced rational point b. Classical Cayley--Bacharach at degree
n-1 forces every original quadric to vanish at b: multiply it by
a rational linear form nonzero at b to power n-3. This use requires
n>=3. An affine b is a second real zero; an infinite b is a real
quartic-flat direction. Both contradict the reduced setup. Oddness then
gives D<=2^n-3.

To exclude D=2^n-3 for n>=4, let W be the full projective base of all
original quadrics. It has no real positive-dimensional component:
its only real affine point is p, which is isolated even over C, and its
leading form excludes real points at infinity. Generic rational
combinations can be chosen simple at all conjugates and with no positive
intersection outside W. Indeed on P^n minus W, the vector of evaluations
is nonzero. Each point imposes n independent linear conditions on the
combination matrix; the incidence variety has dimension equal to the
coefficient parameter space, so a generic fiber is finite or empty.
The nonsingular-Jacobian conditions are compatible nonempty open
conditions. Infinite Q is dense in a nonempty rational Zariski open.

In the weighted count, a conjugation-invariant collection of positive
components having no real points has weight at least four. Weight below
four would be a single invariant line, which has real points. Therefore
D=2^n-3 leaves insufficient weight for a positive component. The generic
Z is a proper complete intersection and its residual R has length three,
possibly nonreduced, disjoint from the simple orbit Gamma.

The degree-one Hilbert value H_R(1) must be three. Otherwise R lies
scheme-theoretically in a line (or point). A point cannot contain length
three. On a line every degree-two section vanishing on R is identically
zero, since a nonzero section has zero length two. All selected quadrics
would then contain the line, contradicting finiteness of Z. A linear
form nonzero on the support trivializes O_R(1), so surjectivity in degree
one propagates to all higher degrees, including n-3.

The exact residual Cayley--Bacharach contract needed is

    dim I_Gamma(2)-dim I_Z(2)
       =h^1(I_R(n-3))=length(R)-H_R(n-3)=0.

Thus every original quadric vanishes on R. An odd-length real finite
scheme has a real geometric point, even with nilpotents: nonreal local
factors occur in conjugate pairs of equal length. This gives a second
affine zero or a real point at infinity, both impossible. Therefore
D<=2^n-5. The source contract includes residual subschemes rather than
only reduced point sets; the manuscript must retain that feature.

The recorded degree-seven three-variable example with positive curvature
only at its zero is a valid boundary warning: global convexity enters
the infinity and flat-direction arguments. The manuscript can omit the
example if space is needed, but must not drop global convexity from the
improved bounds.

## 13. Sharp five-variable maximum: both necessary parts

The bound 21 is established by combining two different arguments. Neither
one alone proves the unconditional statement. The finite-residual theorem
must retain its proper-complete-intersection hypothesis; the geometric
base theorem supplies that hypothesis in the high-degree application.

### Finite residual, including nonreduced schemes

Suppose Z is a proper five-quadric complete intersection in P^5, of length
32, and Z=Gamma disjoint-union R, with Gamma reduced and residual length
in {1,3,5,7,9}. Choose a rational linear form nonzero on the finite
support and dehomogenize. The associated graded of its filtered affine
algebra A is the Artinian reduction of the homogeneous complete
intersection by that regular linear form; its Hilbert series is (1+t)^5.
Its degree-five socle pairing is perfect. A functional lambda annihilating
F_4 A and nonzero on A/F_4 A therefore gives a nondegenerate multiplication
pairing on A. To prove this directly, pair the leading filtration class
of a nonzero a with a complementary-degree class and lift that partner.

For a quadric q vanishing on Gamma, define
B=A_R/Ann(q). Its multiplication pairing lambda_R(qab) is nondegenerate.
The image V of affine linear polynomials is totally isotropic, because
q times two linear polynomials has degree at most four and vanishes on
Gamma. With ell=dim B and v=dim V, this gives 2v<=ell. The scheme of B
lies in its projective span P^(v-1), in a finite quadratic base, so
generic combinations and scheme-theoretic Bezout give ell<=2^(v-1).
If 1<=ell<=9 these inequalities force (v,ell)=(4,8). This is a result
about a support quotient of a functional, not a claim that every residual
of length nine is itself an eight-point complete intersection.

If all quadrics through Gamma had no common real point on R, choose a
rational combination q nonzero at every real geometric residual point.
It is a unit in each local real-residue-field factor, which then survives
unchanged in B. Every complex-residue-field factor and its quotients
have even real dimension. Thus ell has the same odd parity as length R,
contradicting ell=8. This proves that the quadrics through Gamma retain
a real residual point. The quotient-by-annihilator and local-factor
steps are precisely what prevents nilpotents from invalidating parity.

For the convex rational-SOS application with positive leading quartic,
such a point cannot be a second affine zero or a real point at infinity.
The finite theorem therefore excludes orbit degrees 23,25,27,29,31.

### Positive-dimensional complex base

Let Q be the full real quadratic space in P^5, W its complex base,
and Gamma a set of D>=23 points at which its projective Jacobian has
rank five. Suppose every positive-dimensional component of W has no
real point. Generic five-tuples in Q are simple at Gamma and have no
positive intersection component outside W, by the same incidence
argument as in Section 12. The weighted count leaves positive components
weight at most 32-D<=9.

Consequently the reduced maximal positive components are either surfaces
of total degree at most two, or curves of total degree at most four.
Dimensions at least three cannot occur: the only weight-below-sixteen
possibility would be one invariant linear three-space, which has real
points. Invariant odd-degree varieties have real points by a generic real
linear section and parity. The remaining possibilities are therefore
two conjugate planes; one invariant integral quadric surface; invariant
integral conics or quartics; or conjugate pairs of lines or conics.
This classification uses reduced supports only, not reducedness of the
actual base scheme.

For each case choose a reduced pure-dimensional local complete
intersection subbase Y with I_Y(2) globally generated. On Bl_Y P^5,
the divisor 2H-E is globally generated. Its top intersection is

    (2H-E)^5=32-e(Y),
    e(Y)=integral_Y {(1+2H)^5/c(N_(Y/P^5))}_{dim Y}.

Five generic quadratic sections through Y avoid the exceptional divisor
and have residual length 32-e(Y). The blowup may be singular: this
assertion is a generic residual-intersection/Segre-class statement, not
an assumption that the blowup is smooth. Each original simple zero away
from Y persists under sufficiently small complex coefficient
perturbations, by the implicit function theorem. This transfers the
generic bound to the original isolated points. It does not infer
nonnegative excess multiplicities for a special nonreduced base.

The complete list of contributions is:

| Subbase | e(Y) | Maximum isolated simple points |
| --- | ---: | ---: |
| Two disjoint conjugate planes | 32 | 0 |
| Smooth real-point-free quadric surface | 22 | 10 |
| Invariant smooth conic | 10 | 22 |
| Quartic curve of type (1,1,2,2) in P^5 | 16 | 16 |
| Rational normal quartic | 18 | 14 |
| Two disjoint conjugate lines | 12 | 20 |
| Two disjoint conics with quadratic ideal sheaf | 20 | 12 |

The Chern arithmetic follows directly from the displayed formula. For
a smooth curve of degree d and genus g, degree N=6d+2g-2 gives
e=4d-2g+2. For a plane, normal O(1)^3 gives e=16. For a quadric
surface of type (1,1,2), e=2[H^2](1+2H)^4/(1+H)^2=22. For a
possibly singular or reducible curve of type (1,1,2,2),
e=4[H](1+2H)^3/(1+H)^2=16, without a smoothness assumption.

The geometric completeness details must appear in the manuscript:

- Conjugate planes and conjugate lines are disjoint; an intersection
  would be an invariant linear space or point and would be real.
  Their unions have quadratic ideal sheaves using coordinate-block
  products, with linear span equations when needed.
- A real integral degree-two surface spans P^3. A singular quadric's
  invariant linear singular locus has real points, so the allowed
  surface is smooth.
- A real integral quartic curve spans at most P^4. A planar quartic
  forces all containing quadrics to contain its real plane. In P^3,
  zero or one independent containing quadric forces a span or surface
  into W. Two independent quadrics have no common surface component
  and their degree-four complete intersection equals the integral
  degree-four curve scheme-theoretically, by unmixedness and generic
  reducedness. In P^4 the minimal-degree classification gives a smooth
  rational normal quartic with quadratically generated ideal.
- For conjugate conics, equal planes force a real plane in W. Disjoint
  planes give quadratic generation from cross products and conic
  equations. Planes meeting at an external real point a give cross
  products plus c+c'-x_0^2 after normalizing each conic's coefficient
  of x_0^2 to one; this extra quadric is nonzero at a and cuts precisely
  the two disjoint conics locally elsewhere. Thus the ideal **sheaf**
  is generated even if a displayed homogeneous ideal needs saturation.
  Planes meeting along a line give the proper complete intersection
  of their plane-product quadric and a containing real quadric. Its
  two conic components account for degree four with generic multiplicity
  one, and unmixedness gives the reduced union, of type (1,1,2,2).

Every case leaves at most 22 simple points, contradicting D>=23.
Thus the full base is finite. In the rational-SOS application, flat
reduction either lowers the dimension to at most four, or the leading
form is positive and the hypotheses of this base theorem hold. Generic
rational combinations then give the proper Z needed by the finite
residual theorem. Therefore D<=21, and the cyclic degree-21 family
proves sharpness.

The primary contracts for the literature agent are: generic residual
intersection for a degree-two generated homogeneous ideal even when
unsaturated; the regular-embedding Segre class for a possibly singular
local complete intersection; and the integral minimal-degree curve
classification. The historical choices are Eklund--Jost--Peterson,
Theorem 3.2, and Eisenbud--Green--Hulek--Popescu, Theorems 0.1--0.2.
Nothing in this proof uses an unresolved general quadratic-Gorenstein
generation conjecture or a general Eisenbud--Green--Harris conjecture.

## 14. Minimum real SOS length n+1

The theorem is sound over R: a globally convex polynomial of degree
exactly four that is SOS, has value zero at p, and has positive definite
Hessian there needs at least n+1 polynomial squares. Global strong
convexity is sufficient but not necessary. The zero is automatically
unique by convexity, nonnegativity and nondegeneracy.

Every factor has degree at most two, since highest homogeneous squares
cannot cancel over R. At the zero, Hessian F=2Dq^T Dq, so the number
of factors is at least n. Assume for contradiction it equals n and q
is a square quadratic map. The leading squared norm H=norm(q_2)^2
is convex, and its zero set K is a linear space. The invariance argument
in Section 12 shows H(x+tv)=H(x) for v in K. Expanding the vector-valued
quadratic gives q_2(x+tv)=q_2(x)+2tB_2(x,v), and constant squared
norm forces B_2(x,v)=0. Thus each quadratic component is independent
of the flat directions.

In orthogonal coordinates (w,v), v in K and w in its complement,

    q(w,v)=q_2(w)+Aw+Bv+c.

Nonsingular Dq(p) makes B full column rank. The ww Hessian block of
norm(q)^2 is affine in every freely signed v coordinate. Global
convexity forces its linear coefficients to vanish, equivalently
B^T q_2(w)=0. This identity is essential; it makes the minimizing
fiber graph v_0(w)=-(B^T B)^{-1}B^T(Aw+c) affine rather than quadratic.
Orthogonal output projection yields

    F(w,v)=norm[B(v-v_0(w))]^2+norm[bar q(w)]^2.

The residual square map bar q has r=n-dim K>=1 components in r
variables, a unique regular zero, and a leading quadratic part satisfying
norm bar q_2(w)>=a norm w^2 for some a>0. Its squared norm is the
convex affine-graph restriction of F, with positive definite Hessian
at that zero. No rationality of these coordinate changes is needed.

The homotopy bar q_2+t(bar q_1+bar q_0) has the **uniform** lower bound
a norm w^2-b norm w-c. Therefore it is a proper homotopy and extends
continuously to one-point compactifications. Its degree is constant.
The unique regular zero makes degree(bar q)=+1 or -1. The even map
bar q_2 has even degree: choose a nonzero regular value, whose finite
fiber consists of pairs {w,-w}; local signs sum to an even number in
each pair. An empty fiber gives zero and also works. This contradiction
excludes n squares.

The uniform properness estimate is required; a homotopy of maps that
are individually proper is insufficient without uniform control.
Leading-map properness is obtained only after the flat-direction and
coupling reduction. Standard degree invariance, local-degree summation,
and Sard's theorem are the exact topological imports.

The sharp example norm(x)^4+norm(x)^2 has n+1 squares and Hessian
8xx^T+(4norm(x)^2+2)I. The compressed cyclic family therefore has
minimum length n+1 even over R. Retain the zero-value and nondegenerate
Hessian assumptions and degree **exactly four**: positive-minimum
quartics, degenerate zero quartics, nonconvex quartics, quadratics, and
even strongly convex sextics supply counterexamples if these respective
conditions are dropped. The descent-criterion agent independently
reconstructed this same theorem in `prewrite-descent-criterion.md`.

## 15. Univariate degree obstruction and compressed alternative

Use k for this family's input-height index, so ambient dimension n stays
one and does not collide with the manuscript's shared notation. Put

    epsilon_k=2^(-2k), P_k(T)=T^3-3T+2+epsilon_k.

The theorem gives (deg F)^2>(3/4)2^k for every rational globally convex
F whose only real zero is alpha_k. Thus degree is at least a constant
times 2^(k/2), which is exponential in k. The input length is O(k).
The conclusion does not assert a sparse-term or circuit-size lower bound.

The proof is correct. The cubic has just one real root alpha=-2-t with
t(3+t)^2=epsilon_k. Rational t=a/b in lowest positive terms would make
the reduced numerator a(a+3b)^2>1, impossible for epsilon_k, so the
cubic is irreducible. Its other roots beta plus/minus i eta satisfy

    beta=1+t/2, eta^2=3t+3t^2/4,
    beta-alpha=3+3t/2>3, eta<2^(-k).

The last inequality follows from the exact positive difference
epsilon_k-eta^2=t(6+21t/4+t^2).

For a real polynomial R of degree D with R(b)=1, 0<=R<=1 on [a,b],
and R(b+i eta)=0, iterated scaled Markov inequality gives
norm R^(j)<= [2D^2/(b-a)]^j. Taylor expansion at b implies
1<=sum_{j=1}^D q^j/j!, q=2D^2 abs(eta)/(b-a). If q<1/2,
the geometric sum upper bound is less than one, so
D^2>=(b-a)/(4abs(eta)). This uses only the ordinary first-derivative
Markov inequality, iterated with conservative fixed upper degree D.

A rational F vanishing at alpha also vanishes at the complex conjugate.
It cannot be affine. Global convexity and unique real zero make it
nonnegative: a nonaffine convex polynomial has positive even leading
degree and tends to positive infinity at both ends, so any negative
value would force two roots. Normalize by F(beta)>0. Convexity bounds
it above by its 0-to-1 chord on [alpha,beta], and nonnegativity bounds
it below. The interval estimate proves the theorem. The real normalization
need not be rational, because rationality has already forced the conjugate
zero before Markov is applied.

For a finite rational convex inequality description of {alpha}, some
nonzero active row has derivative at least zero at alpha; otherwise a
short right interval would remain feasible. Its supporting line makes
it nonnegative to the right. Its value at beta is positive, since a
zero there and convexity would force vanishing on the whole intervening
interval. The same normalization proves the degree obstruction for
one row, regardless of the number of rows. For an unconstrained rational
convex objective J with minimizer alpha, apply the interval lemma to
J'/J'(beta): convexity makes this derivative nondecreasing, between
zero and one, and rationality forces the complex root. Its degree is
deg J-1. Convexity of the normalized derivative itself is unnecessary.

Strongly convex univariate realizations nevertheless exist. The multiplier
lemma uses f=P^2 and f(1+(x-c)^2)^N. Choose N large enough to dominate
negative curvature on a compact middle region, **then** choose rational
c sufficiently close to alpha that abs(c-alpha)^2<=m/(8NM).
Differentiation gives

    g''/w=f''+[4Nz/(1+z^2)]f'
              +[2N/(1+z^2)+4N(N-1)z^2/(1+z^2)^2]f,
    z=x-c, w=(1+z^2)^N.

Near alpha the only potentially negative product occurs between c and
alpha and has magnitude at most 4NM abs(c-alpha)^2. Away from alpha
on the compact middle region, the positive N(N-1) term dominates.
In the tails f'' and zf' are positive. The resulting g'' is everywhere
positive and tends to infinity, so it has a positive minimum. A fixed
rational center is not justified; the recorded fixed-center counterexample
is valid and explains the order of choices.

The quantitative compressed construction also passes. With dense primitive
integer P of degree d and height tau, its conservative constants are

    R_0=2^(tau+1), sigma=2^[-4d^2(tau+1)], m=sigma^[2(d-1)],
    C_0=(d+1)2^(2tau), Q=(2d+1)^2 C_0,
    R=4(R_0+Q+1), H=(2d+1)^4 C_0 R^(2d), r=m/(2H),
    a=r^2(sigma/2)^[2(d-1)], b=a r^2/(1+4R^2)^2,
    N=2+ceil[(3H+1)/b], kappa=2/m.

The discriminant gives separation above sigma; f''(alpha)>=2m;
derivative bounds through order three on [-R,R] are at most H. Thus
f''>=m near alpha. Root products give f>=a whenever abs(x-alpha)>=r,
using the nonreal roots' imaginary parts. The coefficient bound Q and
R>4(Q+1) give f''>=1 and xf'>0 in the tails. Rational bisection chooses
c after N with width w<=r/2 and w^2<=m/(8NH). All quantities have
O(d^3(tau+log(d+1))) bits. Horner sign evaluation at those polynomial-bit
midpoints has polynomial cost. Binary powering with shared intermediate
values constructs a polynomial-size rational circuit for
kappa P^2(1+(x-c)^2)^N with g''>=1 and unique zero alpha.

The degree and dense expansion can be exponential; the circuit construction
does not give a cheap exact rational evaluation oracle. At the polynomial-bit
integer x_0=R+1 its value is at least 2^N, so the reduced numerator needs
at least N+1 bits. The lower-bound cubic family forces exponential N in
any successful representation of this form. Some sign queries remain
cheap: zero-sublevel membership is P(x)=0, and the derivative sign is
the sign of P(x)[2P'(x)(1+(x-c)^2)+2N(x-c)P(x)], since the factored
power and kappa are positive. Do not infer a general convex-circuit
oracle or optimization algorithm from this specialized factorization.

The two-variable rational strongly convex quartic realizes
(alpha_k,alpha_k^2) with polynomial encoding, so auxiliary coordinates
avoid the univariate expanded-degree cost. The quasiconvex quartic
T^4/4-3T^2/2+(2+epsilon_k)T has derivative P_k, hence decreases then
increases and has the same unique minimizer; its second derivative at
zero is -3. This is a valid distinction between convex and quasiconvex
objective encodings, not an approximate-optimization lower bound.

## 16. Quadratic graph lift and its simpler certificate algorithm

The theorem is valid under its supplied-certificate and zero-minimum
promises: a rational quartic f with positive definite rational full
Hessian Gram A has a polynomial-time rational SOS-convex quartic whose
unique zero is (p,(p_i p_j)_(i<=j)), where p is f's optimizer. The
expanded input and output include their certificates. Let n be f's
dimension and N=n+n(n+1)/2 the lifted dimension.

For h=n+n^2, rho=det(A)/trace(A)^(h-1)>0 satisfies A>=rho I and
Hessian f>=rho I. The minimizer obeys norm p<=
P=1+norm(nabla f(0))_1/rho. A rational approximate minimizer q within
eta follows by approximate convex optimization on [-P-1,P+1]^n
with additive objective tolerance min(1,rho eta^2/2). Strong convexity
turns that tolerance into a distance guarantee. The literature agent
must verify this algorithm's deterministic rational bit-model contract;
the historical choice is Slot--Steurer--Wiedmer, Corollary 1.2 with
Proposition 3.2 and Appendix D. No exact zero-value decision is needed;
minimum zero remains a promise.

For rational q set d=y-q and
s_ij=z_ij-q_i y_j-q_j y_i+q_iq_j. The duplication matrix C sends the
symmetric coordinate list (d_i d_j) to d tensor d. The rational quadratic

    G_q=f(q)+nabla f(q)^T d
       +integral_0^1 (1-t)(d,q tensor d+tCs)^T A
                               (d,q tensor d+tCs) dt

has exact graph restriction f(y), by Taylor's integral formula. Its
only integration constants are 1/2,1/6,1/12. In particular it vanishes
at the exact lifted optimizer for every q. At q=p its gradient also
vanishes. The integrated Euclidean moment block has least eigenvalue
at least 1/48 (the exact determinant/trace lower bound is 1/42).
The affine shear and its inverse have norm at most 2+2norm q. Thus
the stated uniform bounds m_0=rho/[48J^2],
L_0=10trace(A)(P+2)^2 J^2, J=4(P+2), are sufficient. The lifted
point's norm is at most K=2P^2.

The coefficient-sum derivative majorant for
Phi(q,t)=nabla_(y,z)G_q(t,(t_i t_j)) is an effective polynomial-bit
bound available **before** q is computed. Its fixed-degree rational
symbolic expansion gives norm(nabla G_q(w_*))<=D_Phi norm(q-p).
Choose q within min(1,epsilon/D_Phi), preserving exact zero and obtaining
the small gradient required by the shared convexification lemma.

Use graph residuals y_i y_j-z_ij and a quadratic version of nabla f(y),
replacing two factors of each cubic monomial by its corresponding z
coordinate. There are N residuals and their only real common zero is
w_*. Changing variables from (y,z) to (y,r) makes their Jacobian
block triangular with diagonal Hessian f(p) and identity, and coordinate
change determinant of absolute value one. Hence its determinant is
at least rho^n. Divide all residuals by C_0=2W_0, with
W_0=1+sum of their coefficient one-norms. A sufficient operator bound
is W=2N W_0(1+K); the normalized least singular value is bounded below
by min(1,rho^n/[C_0 W^(N-1)]). The single C_0 in this expression is
correct: the determinant scales by C_0^N but the other N-1 singular
values also scale by C_0. All these positive data and reciprocals have
polynomial bit length.

Choose square dyadic epsilon satisfying the shared lemma in N variables
with N residuals, then form

    B_*=G_q^2+epsilon sum_j h_j^2.

It has unique zero w_*, degree exactly four, and a centered positive
definite canonical Hessian Gram by the Schur estimate. By the exact
covariance in Section 4, its unshifted canonical Gram is already rational
and is computed directly from G_q and h_j. Therefore remove the historical
**second** minimizer approximation, formal-center matrix polynomial,
new precision majorant, and coefficient projection. The first approximation
to q remains essential to make G_q's gradient small; its Taylor lift still
preserves the exact zero. Normalize by epsilon nu^2 rather than by a new
projected-Gram margin. The output then has Hessian at least (3/2)I,
N+1 supplied rational quadratic square factors, and a positive definite
rational full Hessian Gram. Its real SOS length is exactly N+1 by
Section 14. This is a strict simplification of the algorithm within
the proved scope, not an additional promise.

The field-obstruction application of this graph lift is covered by the
SOS-fields reviewer. In particular a separated joint sum can have a
uniformly positive Hessian while **every** Gram on the full joint Hessian
basis is singular; independent-block cross monomials force those kernel
directions. Do not promote the separate blocks' full positive definite
Grams to a full positive definite joint Gram. Its variable count grows
quadratically in the tower parameter, so the inherited field degree is
exponential in its square root, not exponential in the lifted dimension.

## 17. Linked general node bound and the bivariate consequence

The elementary refinement in `quartic-zero-degree-prior.md` is also sound.
For a rational polynomial of degree at most four, globally nonnegative
with unique real zero p and nonsingular Hessian there, the safe general
joint-field bound without a rational-SOS assumption is

    D<=2*3^(n-1)-1.

Every conjugate of p is a zero of f and its gradient with nonsingular
Hessian. Choose n-1 generic rational linear combinations A nabla f.
At each conjugate b their differentials A Hessian f(b) have rank n-1,
so locally they define a smooth curve with tangent v. Generic A can
simultaneously make v^T Hessian f(b) v nonzero at all finitely many
conjugates: for any nonsingular symmetric Hessian the isotropic tangent
lines form a proper algebraic subset. Restricted to this smooth curve,
f has vanishing order exactly two. Each conjugate is therefore an
isolated intersection point of local length two in the system consisting
of f and those n-1 cubic combinations. Isolated-solution Bezout, with
multiplicities even in the presence of other components, gives
2D<=4*3^(n-1). The signature/unique-real-embedding argument makes D
odd, proving the displayed bound. For n=1 this is just double-root
multiplicity in a quartic. Actual lower degrees only weaken the Bezout
product. Generic critical-point degree 3^n alone does not reflect this
prescribed zero-value multiplicity.

For n=2 a stronger unconditional bound D<=3 follows from the specific
published ternary-quartic rational-SOS classification quoted in that
note. Its exact primary contract needs literature-agent confirmation:
a rational nonnegative ternary quartic that is not rational SOS is a
product of four complex lines in general position with Galois action
A_4 or S_4 on them. Their six pairwise intersections form a single
orbit of size six. Homogenizing the bivariate polynomial preserves
nonnegativity, including at infinity. Its real zero is singular, hence
in this exceptional case would be one of those six intersections and
would have field degree six. That contradicts oddness of D. The
homogenization is consequently rational SOS, so the quadratic-Jacobian
bound gives D<=3. This deduction is stronger than Hilbert's real-SOS
theorem and must cite the rational classification, not Hilbert alone.

Strong convexity does not supply rational SOS, or even real SOS, in
general dimension. The published rational convex quartic form H that
is not real SOS gives H(x)+norm(x)^2, with Hessian at least 2I and
unique zero zero. Its leading homogeneous part would be SOS if the
whole quartic were SOS, a contradiction. Adding this block to an
irrational-zero construction preserves its unique irrational zero and
still fails real SOS by specializing the original block at its zero.
These examples show why the rational-SOS degree proof cannot be
silently applied to all strongly convex rational quartics. They do not
disprove a base-two field-degree bound by some other argument.

Classical projective node bounds requiring only isolated singularities
are also not automatically applicable: norm(x)^4+norm(x)^2 has a
positive-dimensional complex singular locus at infinity after
homogenization in dimensions at least three. No such isolated-singularity
node theorem is used for the general bound above. The corresponding
general sharp bound remains unsettled by this audit.
