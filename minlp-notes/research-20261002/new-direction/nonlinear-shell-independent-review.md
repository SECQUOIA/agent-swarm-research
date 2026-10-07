# Independent review of the nonlinear mixed-shell certificate

Date: 2026-10-02. Status: final review and targeted checks complete. Reviewed the complete
[nonlinear shell draft](nonlinear-shell-certificate.md). This is a fresh
review of the polynomial extension, not an inference from the quadratic
theorem. No external search or index edit was made. The separate
[bit and input audit](nonlinear-shell-bit-review.md) checks the encoding
assumptions independently.

**Verdict.** No substantive gap was found in the sequential-rounding,
Taylor-remainder, or inner quadratic-certificate arguments. The result is
an independently checkable certificate for a supplied rational candidate,
with discovery under positive full-domain point growth. Curvature
verification, explicit bounded-degree input, and the positive-growth
condition are material assumptions.

## 1. Curvature verification is part of the certificate

For a polynomial objective, a claimed bound on its second coordinate
derivatives is not verified merely by inspecting a quadratic diagonal.
The bound must hold on the full real box, including intervals between
lattice labels. The draft correctly requires a checkable proof and gives
an elementary polynomial-time format: expand the coordinate second
derivatives, bound each monomial on the box by rational interval
arithmetic, and sum those bounds. Equal monomials may first be collected
to avoid losing cancellations. The parameter must use the bound this
verifier actually establishes.

The default format suffices to obtain a finite rational bound, although
it may be loose. A sharper supplied certificate is useful only if its
verification cost is also included. An unrestricted verifier's cost is
not automatically polynomial in its proof-file size. Accordingly, the
displayed FPT bit bound uses the default format or an explicitly
polynomial-time substitute; an arbitrary substitute's actual verification
cost is otherwise added separately. The final author draft explicitly
states this cost convention. The input length includes `L` and any
supplied curvature-proof data. The author corrected that input-length
omission during review.

The lattice-curvature counterexample in the draft is exact. For

```
h(x)=[5(x-1)^4-2(x-1)^6]/3,
```

the second derivative is `20(x-1)^2[1-(x-1)^2]`, which vanishes at
all three integer labels `0,1,2`. Yet rounding the middle label to the
two endpoints increases the expected objective by one. A curvature
bound asserted only at lattice points therefore does not justify the
rounding inequality between them.

## 2. Sequential semiconcavity replaces quadratic cancellation

Fix the independent rounding law for each coordinate at the original
target point. Conditional on the already rounded coordinates, subtracting
`L x_i^2/2` makes the current one-coordinate restriction concave. Its
mean-preserving endpoint rounding increases expectation by at most
`(L/2) Var(Y_i)`. Independence keeps the remaining coordinate laws
unchanged. Telescoping over the coordinates yields

```
E H(Y)-H(x) <= (L/2) sum_i Var(Y_i).
```

This proof controls higher-order interactions; it does not assume they
cancel in expectation. Every intermediate vector lies in the continuous
box where curvature was verified. The argument applies equally to
continuous endpoints and feasible lattice endpoints, with real curvature
used only to justify their one-dimensional chord inequality.

The previously reviewed mixed grids preserve feasibility, the shell
threshold, and the scalar relative variance bound. Applying the preceding
inequality to `F-F(v)-sigma||x-v||^2` gives the same outer correction
as in the quadratic theorem. The nonstrict finite check
`m_S>=sigma S^2/n` therefore certifies growth `sigma` on that shell
without a growth assumption.

## 3. The inner fixed-lattice argument is sound

At fixed lattice values, exact translation gives the continuous Taylor
quadratic `q` plus monomials of degree at least three. For
`||d||_infinity<=rho<=1`, any two factors of a monomial have absolute
product at most `||d||^2`; its remaining factors contribute at most
`rho`. Consequently the sum of absolute translated coefficients gives

```
|F(v+d)-F(v)-q(d)| <= M rho ||d||^2.
```

No derivative-remainder oracle is being assumed. Translation factor by
factor and summing absolute coefficients is safe even when it forgoes
cancellation. The choice `rho<=sigma/M` bounds the remainder by
`sigma||d||^2`.

The core radius is also no larger than every positive continuous side
width and half every lattice spacing. Thus all feasible points in the
core keep their lattice coordinates fixed, and the continuous signed
cube used by the inner test is feasible. This avoids applying a radial
identity along any nonzero lattice displacement.

On the continuous core boundary, endpoint rounding preserves a coordinate
with magnitude `rho`. Applying the variance argument to
`q-2sigma||d||^2` proves that the test

```
min_boundary_grid [q(z)-3sigma||z||^2] >= sigma rho^2/n
```

implies `q>=2sigma||d||^2` on the whole boundary. The continuous KKT
signs make the linear part of `q` nonnegative on every allowed ray.
Quadratic radial scaling therefore extends this bound to the core's
interior. Subtracting the certified remainder leaves
`F(v+d)-F(v)>=sigma||d||^2`. With no continuous coordinates, the core
contains only the candidate and this check is correctly omitted.

This local use of `q` is essential. The draft's example
`F=x-x^2+x^3` on `[0,2]` has exact growth one because
`F-x^2=x(x-1)^2>=0`, while its Taylor quadratic `x-x^2` is negative
on part of the original domain. The algorithm does not substitute the
Taylor quadratic outside its verified core.

## 4. Discovery constants and the changing radius

Under true growth `g`, the core remainder gives
`q(d)>=(g-sigma)||d||^2`. At a core grid point, subtracting the three
unary corrections gives `(g-4sigma)||d||^2`. Replacing the norm by
`rho^2` requires `g-4sigma>=0`; the author now states the sufficient
assumption `sigma<=g/5` before this step. Under that assumption the
core test passes, including its `sigma rho^2/n` residual. The outer
tests already pass for `sigma<=g/3`.

Quartering `sigma` between trials therefore proves

```
sigma >= min{L/32,g/20},
L/sigma <= max{32,20L/g}.
```

The full successful certificate additionally proves `sigma<=g`.
The scale remains the actually verified coordinate curvature; it is
not enlarged by endpoint increments or higher-order coefficient norms.
Higher-order coefficients instead shrink the core and increase the
number of physical shells logarithmically.

The dependence of `rho` on the trial does not create a precision loop.
The rational Taylor bound `M` is computed once. At trial
`delta=2^-r`, the known quantities give `rho` directly and determine
all shells. Their number is `poly(I)+O(r)`, while the first successful
`r` is controlled by `max{1,L/g}`. No unknown optimizer, unknown face,
or unverified stopping radius enters a trial.

## 5. Sparsity and exact arithmetic

The explicit monomial and fixed total-degree hypotheses do real work.
Translating a monomial of degree at most `d0` produces at most `2^d0`
monomials and never introduces a variable outside its original scope.
Substituting fixed lattice coordinates and keeping only Taylor terms
also preserves those scopes. Every resulting factor can stay in its
original bag; no dense global Hessian factorization is needed.

The coordinate shell grids have the same count as in the mixed quadratic
theorem. The outer DP evaluates the original polynomial factors; the
inner DP evaluates their quadratic Taylor factors. Unary corrections and
one owned-variable OR flag do not enlarge factor scopes. Shell count is
an outer multiplicative cost, not an exponentiated per-variable choice.

For fixed degree and explicit rational coefficients, translation, `M`,
factor evaluation, and a common denominator for all trial table entries
have polynomial bit bounds. Evaluating a degree-`d0` monomial raises
the common grid denominator only to the fixed power `d0`. Messages add
assigned terms and take minima, so denominators do not multiply with
tree depth. This supports the claimed absolute input exponent for each
fixed degree bound.

The succinct-input examples are valid limitations. In the binary-exponent
example, `65/64-2^-(3d+1)` has an exponentially long reduced denominator.
In the repeated-squaring circuit example, a huge constant gives an
exponentially long numerator while the actual degree, growth, and upper
curvature stay bounded. Fixed degree alone would not justify the bit
claim for arbitrary circuit input.

## 6. Solver capability and limits

The nonlinear extension does more than invoke the quadratic result as a
black box. The verified Taylor remainder closes a neighborhood where
ordinary additive grid error cannot certify a zero exactly. The result
therefore gives a concrete finite certificate for supplied rational
polynomial optima under point growth, including mixed points whose
lattice derivatives violate continuous KKT signs. The external prior-art
comparison is separate; rounding, Taylor estimates, and tree DP are not
new individually.

The candidate and promise remain significant limits. A generic continuous
polynomial optimum can be irrational, and a nearby rational numerical
candidate is not an exact optimum. The theorem does not recover such an
optimizer or turn an approximate solver output into exact optimality.
Moreover, a unique continuous polynomial optimum need not have positive
quadratic growth: `x^4` at zero is the basic example. Acceptance is sound
for every input, but finite termination is claimed only with `g>0`.
For purely lattice finite domains, uniqueness does imply some positive
point-growth modulus; that does not make its numerical conditioning small.

## Verification status

An independent inline Python `fractions.Fraction` diagnostic reused only
the scalar grid and rounding-law helpers from the mixed quadratic checker.
It tested `x^2+y^2+x^2 y^2` on a continuous box and
`z^2-z/2+u^2+z^2 u^2/4` with `z` integer on `[0,8]` and `u`
continuous on `[0,1]`. The global curvature bounds were four and 34,
respectively. All 495 conditional-rounding checks over 1,141 atoms passed;
314 cases had higher-order expectation terms beyond the constant quadratic
diagonal-variance identity. Thus these checks specifically exercise the
new sequential bound, not only the old quadratic cancellation.

The same diagnostic checked the incorrect KKT candidate zero for
`F=x^2-3x^3+2x^4` on `[0,1]`. Its local Taylor quadratic is positive,
but an outer shell correctly rejected the proposed global certificate.
This checks the need for both parts of the construction.

I also inspected and ran the author's full targeted checker:

```
python3 -B research-20261002/new-direction/check_nonlinear_shell_certificate.py
```

It passed six positive fixtures in seven trials and rejected three
wrong-candidate trials. Its actual owned-variable OR dynamic program
matched direct grid enumeration on 49 shell/core tables, comprising
2,154 bag assignments. It also checked 145 rounding cases and 66 core
cases. Fixtures include a polynomial path decomposition, nonunit rational
lattice spacing, a nonzero rational candidate, signed continuous core
directions, negative lattice derivative, and a pure integer quartic.
The local Taylor counterexample and lattice-curvature counterexample
also passed their exact assertions.

These finite checks support the implementation and algebraic identities;
the proof supplies the general complexity bound. No project-wide
verification or CI inspection was performed.
