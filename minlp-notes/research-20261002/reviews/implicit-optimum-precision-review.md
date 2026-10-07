# Review of the rational rectangular-certificate precision obstruction

Date: 2026-10-02. Verdict: no blocking mathematical issue found in the
completed [precision-obstruction note](../new-direction/implicit-optimum-precision-obstruction.md).

This is an independent review of the actual file, including the constants,
binary encoding argument, and exact certificate scope. The constructions
and proofs are elementary. No literature comparison or priority assessment
is part of this review.

For every `n>=1`, the residual recurrence has the unique zero
`a_i=2^(-(4*2^i-2))`. Every coordinate is strictly between zero and `1/2`.
All original objective terms are squares, so this zero is the unique global
optimizer. With `e=x-a`, the residual vector is `(I-P)e`, where the
subdiagonal weights of `P` have magnitude at most `1/4`. Thus
`F>=9||e||^2/16` on the entire feasible box. This is a direct global
growth bound, rather than an inference from the weaker Hessian bound.

Direct differentiation gives

\[
 \partial_{ii}F=2+\tfrac34x_i^2-x_{i+1}\quad(i<n),
 \qquad \partial_{nn}F=2.
\]

The claimed upper coordinate curvature `35/16` follows. If `J` is the
residual Jacobian, its weighted subdiagonal shift has norm at most `1/4`,
so `||Jv||>=3||v||/4`. The exact formula

\[
 \nabla^2F=2J^\top J-\operatorname{diag}(r_1,\ldots,r_n,0)
\]

and `r_i<=1/2` therefore give `Hessian(F)>=5I/8`. The bounds hold on
the whole closed box and are independent of `n`.

The modified objective's global comparison can also be checked through
the exact nonnegative identity

\[
 \widetilde F-\tfrac{15}{16}(F+y^2)
 =\tfrac1{16}(F-r_n^2)+\tfrac1{16}(y+r_n)^2
  +\tfrac18yx_n.
\]

All terms on the right are nonnegative on the specified domain. It follows
that `(a,0)` is the unique optimizer and that
`g=135/256` is a valid global Euclidean growth constant. The coefficient
of `y^2` in this argument is `15/16`, which is larger than `135/256`,
so using the common constant in all variables is valid.

On the terminal coordinates `(x_(n-1),x_n,y)`, the perturbation Hessian is

\[
 E=\begin{pmatrix}
 -y/16&0&-x_{n-1}/16\\
 0&0&1/4\\
 -x_{n-1}/16&1/4&0
 \end{pmatrix}.
\]

Its absolute row sums are at most `1/16`, `1/4`, and `9/32`.
Symmetry therefore gives spectral norm at most `9/32`, proving the
claimed lower Hessian bound `11I/32`. The only changed free-coordinate
diagonal entry decreases, while the new `y` diagonal is `2`. Hence
`L=35/16` remains valid and `L/g=112/27`. These calculations include
`n=1`; the restriction `n>=1` correctly avoids an undefined terminal
predecessor. The original graph is a path. Adding the terminal triangle
gives maximum bag size three and treewidth two.

The first endpoint argument uses the stronger condition that a closed
enclosing rectangle lies inside the open feasible domain. It correctly
obtains `0<ell_n<=a_n=2^(-m)`, where `m=4*2^n-2`. For any ordinary
binary rational representation `ell_n=p/q`, positivity forces the integer
numerator to satisfy `p>=1`. Containment then forces `q>=p*2^m>=2^m`.
Consequently at least `m+1` denominator bits are necessary, whether or
not the fraction is initially reduced. The note correctly distinguishes
this condition from merely putting the optimizer in the interior of an
enclosing box. A zero or negative lower endpoint would invalidate this
specific argument.

The second endpoint argument does not require an enclosing rectangle to
avoid the feasible boundary in advance. For any product rectangle inside
the feasible domain, the exact derivative minimum is

\[
 \min_{x\in B}\partial_y\widetilde F(x,0)
 =\tfrac14(\ell_n-u_{n-1}^2/8).
\]

The indicated corner belongs to the rectangle, so this is the true range
minimum. Uniform weak nonnegativity therefore requires
`ell_n>=u_(n-1)^2/8>=a_(n-1)^2/8=a_n/2>0`. Containment also gives
`ell_n<=a_n`. Both facts are needed: positivity comes from the sign
condition, while the small upper bound comes from containing the optimum.
Together they imply exactly the same exponential denominator-bit bound.
At the optimum itself the derivative is `a_n/8>0`, consistent with its
active lower bound `y=0`. Thus the sign difficulty arises from replacing
the correlated optimizer by a whole rectangle; the sign at the optimizer
is not in doubt.

The scope is stated correctly. The lower bound is exponential in `n` and
superpolynomial in the indexed factor-list length `O(n log(n+1))`; it is
not stated as exponential in that total encoding length. It applies to
explicit integer numerators and denominators. Compressed binary exponents,
arithmetic circuits, and the stated recurrence can represent these
coordinates compactly. The result excludes a polynomial total runtime
only when the algorithm must output one of the specified rectangular
certificates in the ordinary rational format.

The exceptions described in the note are real. The recurrence map preserves
the closed feasible box and has Lipschitz constant at most `1/4`, so a
closed-box contraction proof gives a short exact certificate for the first
family. In the second family, the residual equations directly establish
the active derivative sign, and the displayed nonnegative identity proves
global optimality. The argument therefore does not rule out all implicit
root certificates, interval-Newton methods, Krawczyk methods, or exact
algorithms. It specifically obstructs strict-interior rational rectangles
and rectangles that certify the active sign uniformly across independent
free coordinates. Its exact-range calculation makes the latter obstruction
independent of interval-arithmetic overestimation.

A separate delegated algebra check independently approved the recurrence,
growth constants, diagonal curvature, both Hessian bounds, and the boundary
derivative. Its targeted command `python - <<'PY'` used exact symbolic
identities for `n=1,2,3,5` and passed. That finite check supplements the
all-dimension algebra above; it does not establish the result by sampling.
The construction author's
[checker](../new-direction/check_implicit_optimum_precision.py) was also
read for consistency with its stated finite scope. The targeted command

```text
python research-20261002/new-direction/check_implicit_optimum_precision.py
```

passed 120 exact-rational configurations at `n=1,2,3,5,8`, 45 terminal
sign boxes, recurrence denominator lengths, and both conditioning ratios.
It checks the residual and Hessian formulas, growth inequalities, exact
comparison identity, perturbation row sums, and positive-definite shifted
Hessians at those configurations. Its exact elimination uses positive
pivots; it does not infer a universal Hessian bound from finite samples.
A targeted inline Python check also passed review whitespace, paired math
delimiters, and local link targets. This review did not modify the main
note or run project-wide verification, CI inspection, or literature searches.
