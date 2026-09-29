# Independent review of boxed mixed-integer SOCP optimization

Date: 2026-09-28. Reviewed manuscript:
[boxed-misocp-optimization.md](boxed-misocp-optimization.md).
I read the complete saved draft after independently reviewing its
[continuous optimization dependency](continuous-socp-optimization-review.md).
No mathematical or complexity gap was found. The result is a corollary
of the linked structural precision and exact decision results, not a
separate new finite-union or integer-selection method.

The statement correctly requires finite supplied integer bounds, an affine
objective, and fixed span of the **continuous** blocks of the squared
cone Hessians. The whole cone formulation remains the rational SOC input;
native squared Hessians need not be PSD. No conclusion for unbounded
integer variables is established.

## 1. Uniform bounds do not require enumerating assignments

Rounding each rational integer interval to its integer endpoints detects
empty intervals and bounds the bit length of every possible assignment.
Substituting an assignment into each affine cone map changes only rational
coefficients, with coefficient bits bounded by
\((\tau+1)S^{O(1)}\). Its continuous squared Hessians are exactly
the original continuous blocks. The value, optimizer-height, and
common-field bounds therefore hold uniformly over all assignments.

There are finitely many assignments, even though their count can be
exponential in the input length. For a nonempty globally bounded-below
problem, its infimum is the minimum of the finitely many nonempty slice
infima. Thus it equals one slice value and inherits that value's degree
and height bounds. Taking a product of all slice polynomials would be
unnecessary and would lose the stated precision bound.

Likewise, the global objective is unbounded below exactly when some
nonempty slice is unbounded below. Finiteness is indispensable: with
unbounded integer coordinates, escape through successively different
slices need not be unboundedness within any fixed slice.

## 2. The decision and function complexity claims are separated

A rational affine objective threshold leaves the continuous Hessian span
unchanged. The [SOCP projection theorem](socp-hessian-span-frontier.md)
constructs a rational MILP preserving feasible integer assignments and
adding no integer variables. For fixed \(h\), its construction has
polynomial size. MILP feasibility supplies the required NP language.
For fixed \(k,h\), the fixed-integer-dimension MILP algorithm instead
decides every such query in deterministic polynomial time.

The resulting MILP witness is not asserted to be an exact continuous
witness of the original cones. Its role is to decide whether an exact
original fiber exists. Continuous recovery occurs separately at the end.

The uniform finite-value bound justifies the threshold below \(-M\)
that distinguishes finite infimum from unboundedness. Rational bisection
and algebraic recognition remain valid if a threshold equals an
unattained infimum. The proof handles initial infeasibility separately.

The arithmetic outside the oracle, its number of queries, and their
encoding lengths retain the coefficient-sensitive bounds. Each threshold
only changes coefficient bits and adds one affine row. The precision-
dependent internal lift is not reused as structural input to another
algebraic theorem.

Repeated calls to a deterministic polynomial-time function algorithm with
an NP oracle remain within \(\mathrm{FP}^{\mathrm{NP}}\): the calls
can be expanded into polynomially many queries to the same NP oracle.
No NP computation with its own NP oracle is introduced. The manuscript
correctly states deterministic polynomial time for each fixed pair
\((k,h)\), without claiming a uniform exponent independent of \(k\)
or fixed-parameter tractability.

## 3. The compact mixed domain decides global attainment

The uniform optimizer radius contains a minimum-norm optimizer of every
fiber that attains its own finite infimum. If a global minimum is attained,
its fiber attains its infimum at the global value, so the radius retains
an optimizer with that value.

Intersecting with this continuous box yields a finite union of compact
fibers. This mixed domain is compact even though it need not be convex.
If empty, global attainment is impossible. If nonempty, its minimum
\(\beta\) is attained, and
\[
 \theta\text{ is attained in the original problem}
 \quad\Longleftrightarrow\quad \beta=\theta.
\]
The forward direction uses the optimizer bound; the reverse uses
compactness. Exact algebraic equality is sufficient. Every underlying
optimization query remains rational.

Adding the radius introduces only affine rows. Its large coefficients
have \((\tau+1)S^{O(h+1)}\) bits, while structural size stays
polynomial in \(S\). Since the dependency bounds apply an absolute
power to coefficient size, their reuse preserves the claimed form.
The proof does not treat the expanded bit length as a new structural
parameter and unnecessarily square the exponent in \(h\).

## 4. Integer selection preserves an attained optimizer

After global attainment is known, an interval-restricted compact domain
contains an original optimizer exactly when its attained minimum equals
\(\theta\). The algorithm uses this criterion throughout integer
bisection. It does not select a fiber merely because its unboxed
infimum equals \(\theta\).

The split
\([L,m]\cup[m+1,U]\), with \(m=\lfloor(L+U)/2\rfloor\),
is a disjoint partition of the current integer interval. If the lower
part contains no optimizer, the upper part must contain one. Storing
only the current endpoints retains all previous decisions and prevents
the row count from growing with bisection history. The number of steps
is polynomial in the endpoint bit lengths, not in the number of integer
assignments.

The final vector \(z^*\) therefore has an attained continuous optimum
equal to the original global value. Applying the continuous exact
optimization algorithm to that original unboxed fiber returns its unique
minimum-norm optimizer. Its joint algebraic degree and output size have
the uniform slice bounds. Integer coordinates are rational, so adjoining
them introduces no field extension. No global minimum-norm choice
across integer assignments is asserted.

## 5. Independent stress case and verification

I independently used the example that also appears in the manuscript:
\[
 z\in\{0,1\},\quad x,y\ge0,\quad
 \|(2(1-z),x-y)\|_2\le x+y,\qquad \min x.
\]
Its residual is \(4(1-z)^2-4xy\), and its continuous Hessian is
\[
 \begin{pmatrix}0&-4\\-4&0\end{pmatrix},
\]
so the continuous span is one. Both fibers have infimum zero.
For \(z=0\), \(xy\ge1\) prevents attainment; for \(z=1\),
the point \(x=y=0\) attains zero. Thus selecting a fiber by its
unboxed infimum alone would fail. In a box of radius \(R\ge1\),
the first fiber has minimum \(1/R\), achieved at \((1/R,R)\),
whereas the second still has minimum zero. The manuscript's compact
selection oracle makes the required distinction.

A targeted inline Python command using exact SymPy arithmetic checked
the expanded residual, both fiber substitutions, the continuous Hessian,
and the two displayed feasible-point substitutions. The minimum \(1/R\)
was checked separately from \(xy\ge1\) and \(y\le R\).
These finite checks challenge the selection boundary; they do not prove
the general complexity result.

An inline Python check passed for this review's local links, math
delimiter pairs, control characters, trailing whitespace, and final
newline. No project-wide verification, CI inspection, Lean formalization,
or solver experiment was performed.

The result should retain the manuscript's prior-art qualifications:
the mechanism combines reviewed structural precision with established
finite-union reasoning, MILP decision, recognition, and integer bisection.
This review makes no priority claim and establishes no practical speedup.

## 6. Separate completion audit, 2026-09-28

A separate reviewer read the complete saved boxed proof, this review, and
the continuous optimization dependency. A further reader independently
checked the finite-union value bound, conditional optimizer radius, compact
integer-selection oracle, and composition of the NP-oracle calls. Both
found no gap. The manuscript's two statements that review was pending
were stale and have been corrected; no mathematical step was changed.

The completion audit independently confirmed that an interval-restricted
compact minimum equal to the global value certifies an attained optimizer.
An unboxed infimum equal to that value would not suffice. Expanding the
nested deterministic value calculations gives polynomially many adaptive
queries to the same NP feasibility language, so the complexity remains
\(\mathrm{FP}^{\mathrm{NP}}\). Final continuous recovery is applied
only after an attained optimal fiber has been selected.

An exact SymPy check again verified the residual, continuous Hessian, and
the two boundary-point substitutions in Section 5. Its initial structural
comparison of expanded and unexpanded expressions was replaced by exact
polynomial subtraction; the corrected command passed. The proof of the
boxed minimum \(1/R\) follows directly from \(xy\ge1\),
\(0\le y\le R\), and the displayed feasible point. No further
mathematical assumptions, literature claims, or practical guarantees were
introduced. Targeted document and scoped whitespace checks passed; no
project-wide verification or CI inspection was performed.
