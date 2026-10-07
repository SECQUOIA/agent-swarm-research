# A polynomial-time certificate for every bounded-height quadratic margin

Date: 2026-10-03. Status: proved certificate lemma, independently reviewed.
The [complete recourse theorem](theorem.md) supplies the face and
probability arguments needed to use it.

The residual-convex cubic analysis has exponentially many possible
Hoffman minors. Each minor is a rational polynomial of degree at most two
in the core. This note gives a sound way to certify a common lower bound
without enumerating those minors. It uses ordinary integer lattice basis
reduction. It deliberately tests a larger family: every nonzero integer
quadratic with a specified coefficient bound.

The certificate must be run in the free coordinates of a **known exact
core face**. It does not identify that face. It cannot certify a point
lying on the zero set of one of the tested nonzero polynomials. Such
draws require a separate treatment; failure of this certificate is not a
claim that the optimization problem is difficult.

## 1. Inputs and the finite family

Let `a in [0,1]^m`, and let `phi(a)` list the `s=(m+1)(m+2)/2`
distinct monomials of total degree at most two, including the constant
one. Let `B>=1` be an integer. Define

```
P_B = { p_h(X)=h'phi(X) : h in Z^s, 0<||h||_infinity<=B }.
```

The input provides a certified Cauchy oracle for `a`. For an accuracy
request of `q` bits it returns a dyadic vector with `poly(I)+O(q)` bits
per coordinate, where `I` is its base input length. It can therefore
return a rational `b in [0,1]^m` with a specified maximum-coordinate
error. Clipping an approximation to the cube preserves its error guarantee.
No exact algebraic representation of `a` is required by the certificate.

For `m=0`, the family consists of nonzero integer constants, and the
margin one is immediate. The rest of the construction also works with
`s=1`; no geometric claim about positive-dimensional faces is implicit.

## 2. The lattice and its certificate

Choose a positive integer scale `T`, and obtain `b` with

```
||b-a||_infinity <= 1/(4T).
```

Every nonconstant monomial in `phi` is 2-Lipschitz in this norm on the
unit cube. Compute, with exact rational arithmetic,

```
w_j = nearest_integer(T phi_j(b)).
```

Either deterministic rule for rounding a half-integer is valid. For
every coordinate,

```
|w_j/T-phi_j(a)| <= 1/T.                              (1)
```

Let `L_T` be the rank-`s` integer lattice in `R^(s+1)` with basis rows

```
[ I_s | w ],
```

so its vectors are exactly `(h,h'w)` with `h in Z^s`. Apply standard
LLL reduction with parameter `3/4`, and let `ell_1` be the first reduced
basis vector. The usual reduced-basis guarantee is

```
||ell_1||_2 <= 2^((s-1)/2) lambda_1(L_T).              (2)
```

The algorithm accepts only if the following integer comparison holds:

```
||ell_1||_2^2 > 2^(s-1) (4sB)^2.                    (3)
```

If it accepts, its certificate is

```
|p(a)| > sB/T    for every p in P_B.                  (4)
```

**Proof of soundness.** Equation (2) and the strict test (3) imply
`lambda_1(L_T)>4sB`. Suppose `p_h in P_B` instead satisfied
`|p_h(a)|<=sB/T`. Equation (1) gives

```
|h'w| <= T |p_h(a)| + ||h||_1 <= 2sB,
||h||_2 <= sB.
```

The nonzero lattice vector `(h,h'w)` would then have length at most
`sqrt(5)sB<4sB`, a contradiction. This proves (4), including the
assertion that none of these polynomials vanishes at `a`.

A checker can verify a full LLL-reduced basis, its unimodular change of
basis, and (3) by exact rational arithmetic. The only oracle-dependent
premise is the certified coordinate enclosure used in (1). A claimed
coordinate approximation without its established error guarantee is
not sufficient.

## 3. A sufficient condition for success

The test is sufficient rather than necessary. Its success can be
controlled by the same type of margin after enlarging the coefficient
bound. Put

```
R = 2^s 4sB.
```

Suppose a number `mu_0>0` satisfies

```
|p(a)| >= mu_0    for every p in P_R.                 (5)
```

Then the test accepts whenever

```
T mu_0 > (s+1) R.                                   (6)
```

Indeed consider a nonzero lattice vector `(h,h'w)`. If `||h||_2>R`,
its length exceeds `R`. Otherwise `0<||h||_infinity<=R`, and (1),
(5), and (6) give

```
|h'w| >= T |p_h(a)| - ||h||_1
       >= T mu_0 - sR > R.
```

Thus `lambda_1(L_T)>R`. Since `ell_1` is itself a nonzero lattice
vector, `||ell_1||_2>R`; and
`R/2^((s-1)/2)>4sB`. This implies the exact acceptance test (3).

The use of `P_R` in (5) is essential. LLL may encounter a short vector
whose coefficient height exceeds `B`; a probability analysis based
only on `P_B` would not prove success of this test.

## 4. Bit complexity and repeated refinement

Each integer basis entry has `O(1+log T)` bits. LLL and its exact
verification take time polynomial in `s+log T`. The requested oracle
accuracy is `O(1+log T)` bits, and its dyadic output has polynomial
length in `I+log T`. A stage therefore takes polynomial time in
`I+s+log B+log T`, plus the cost of that oracle query. The polynomial
exponent is absolute; the number `(2B+1)^s-1` of tested polynomials
does not enter the running time.

Trying `T=1,2,4,...` reaches a successful stage under (5) after at most

```
O(s + log B + log(1/mu_0) + log(s+1))
```

stages. Summing polynomial costs over these stages is still polynomial
in the same bound. This statement is conditional on (5): if an exact
relation in `P_B` holds, the sound test never accepts. A complete
algorithm must cap this process and activate an independently justified
fallback, or otherwise resolve the exceptional relation.

## 5. Application to the residual cubic minors

On a fixed rational core face `A`, the prior
[residual-convex cubic note](../../research-20261002/new-direction/residual-convex-cubic-boundary.md)
uses the matrix

```
[ H_A ; g_A(v)' ; I_n ].
```

Its entries are rational polynomials in the free core coordinates.
Only the single row `g_A(v)'` varies, and its degree is at most two.
Every square minor is therefore a polynomial of degree at most two.

One can compute a common positive integer `D` and an integer height
bound `B` of polynomial binary length such that each minor `p` obeys

```
D p in Z[v_1,...,v_m],   coefficient_height(D p)<=B.
```

For example, first clear every entry coefficient denominator by a
common integer `d`; choose `D=d^n`. A minor of order `r<=n` has its
denominator cleared by `d^r`, hence also by `D`. If `C>=1` bounds all
cleared coefficient magnitudes and there are `s` monomials, the loose
integer bound `B=d^n n! (sC)^n` suffices for all minors. The varying
row is used at most once in any determinant term. These data are
computed from coefficient bounds, without listing the minors.

Every minor polynomial is either identically zero on the face or its
scaled polynomial belongs to `P_B`. On an accepting stage, every
minor nonzero at `a` has the certified lower bound

```
|p(a)| > sB/(DT).
```

There is no need to enumerate, identify, or decide which minors are
identically zero: the conclusion applies to all nonzero ones
automatically. A bound `min(1,sB/(DT))` supplies the minor margin used
by the conditional Hoffman estimate.

The same certificate includes the polynomials `v_i` and `1-v_i`
when `B>=1`. It therefore certifies a positive distance from each
boundary of the **known free face**. This does not certify that a
coordinate excluded from that face is exactly zero or one.

## 6. Scope and source

The lattice reduction ingredient is the classical algorithm of Lenstra,
Lenstra, and Lovasz, [*Factoring Polynomials with Rational Coefficients*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lovasz/LovaszLenstraLenstrafactor.pdf),
Mathematische Annalen 261 (1982), 515–534. Integer-relation lattices
are also classical. The result here is the explicit sufficient
certificate and its application to the implicit family of cubic
recourse minors; no novelty claim about lattice reduction is made.

This note removes the need to inspect exponentially many minors on a
nonexceptional known face. The [full smoothed theorem](theorem.md) supplies
an effective exact-face rule, bounds for the optimizer's probability
of small polynomial margins, and a finite-law fallback budget that
remains valid for every requested point accuracy. None of those steps
is implied merely by the lattice certificate.

## Verification

A separate agent read the actual file and checked the LLL inequality
direction, strict acceptance constants, enlarged height in the success
condition, common denominator and height bounds, and exact-relation
scope. Its only requested clarification was the encoding length of
Cauchy outputs; the statement now explicitly requires short dyadic
outputs.

An inline `python3 - <<'PY'` exact-arithmetic diagnostic used
`fractions.Fraction` and the installed SymPy LLL implementation. Across
three rational one-dimensional points and four scales it obtained nine
accepted stages, exhaustively checked 1,476 claimed bounded-height
polynomial margins, and checked all six stages satisfying the stated
sufficient condition. Nine further stages at points with exact tested
relations correctly rejected. Every computed change-of-basis matrix
was verified to be unimodular. These finite fixtures test certificate
arithmetic, not the smoothed theorem or a general core oracle. No
project-wide verification or CI inspection was run.
