# Independent source audit of the effective penalty upper bound

Date: 2026-09-25. Scope: the Basu–Roy source, formulas (5)–(7), and the
semialgebraic applications in `penalty-upper-bound.md`. This audit does not
verify the convex KKT argument or the complete penalty theorem.

**Verdict: corrections required, with the stated asymptotic bound preserved.**
The formulas in the initial draft match the linked 2009 manuscript, but a
later author version changes both constants and the bounded-component scope.
Use Saugata Basu and Marie-Françoise Roy, *Bounding the radii of balls meeting
every connected component of semi-algebraic sets*, Journal of Symbolic
Computation 45(12), 1270–1279 (2010), DOI
[10.1016/j.jsc.2010.06.009](https://www.sciencedirect.com/science/article/pii/S0747717110000891).
The inspected [final author manuscript, 5 June 2010](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf)
has Theorems 3–4 on printed page 5 and their proofs on pages 13–14.

## Required scope correction

The final Theorem 3 covers bounded components of **weak sign conditions**.
The final Theorem 4's concluding sentence mentions both ordinary and weak
sign conditions, while its Section 5 proof explicitly treats weak conditions.
The clean application here uses only weak conditions: conjunctions of
polynomial equalities and non-strict inequalities. The stray `Zer(Q)` in the
[2009 draft](https://www.math.purdue.edu/~sbasu/MEGA-submitted-07-11-09.pdf)
is absent from the final theorem statement. Its removal alone does not repair
the obsolete citation and constants.

Replace the general Boolean-combination claim by the following sufficient
statement: a nonempty finite union of weak basic closed sets has a point
inside the common meeting radius; if that union is bounded, it is contained
inside the common bounded-component radius. For the first claim select a
nonempty member. For the second, every member is bounded, so each of its
connected components lies inside that radius. This argument uses no
quantifier elimination, no closedness assertion about arbitrary Boolean
formulas, and no additional variables.

The KKT set in (8) is one weak basic closed set. The reciprocal graph (12)
is a union of at most `2m` weak basic closed sets, obtained by choosing one
equality `t r_j = 1` or `t r_j = -1`. Each chosen equality uses an existing
polynomial from the inequalities `-1 <= t r_j <= 1`. Every branch is bounded
because it is contained in the reciprocal graph. Thus the dimension and
polynomial counts already used for these applications remain valid.

## Corrected explicit exponents

Use the draft's convention `bit(a)` for the binary length of a positive
integer. For the bounded radius define

\[
 K=(2d+1)(2d)^{k-1},\qquad D_b=k(2d-1)+2,
\]

\[
 E_b=\operatorname{bit}(k)+\operatorname{bit}(K+1)
  +2KD_b\bigl[2\tau+\operatorname{bit}(K)
     +k\operatorname{bit}(d+1)+\operatorname{bit}(s_0)+3\bigr].
\]

Then `2^E_b` majorizes the final Theorem 3 radius. The factor
`sqrt(k)(K+1)` is bounded by the first two bit terms. This is a substantive
change from the old (6): for `k=1,d=2,tau=s_0=1`, the old exponent is 304
whereas this final-statement majorant is 554. Consequently the old formula
cannot simply be described as a conservative majorant of the final one.

For the meeting radius define

\[
 d'=\max\{2(d+1),6\},\quad D=k(d'-2)+2,\quad
 K'=d'(d'-1)^{k-1},
\]

\[
\begin{aligned}
 t_0&=2\tau+k\operatorname{bit}(d+1)
            +\operatorname{bit}(2d')+\operatorname{bit}(s_0),\\
 t_1&=D[t_0+4\operatorname{bit}(2D+1)+\operatorname{bit}(K')]
          -2\operatorname{bit}(2D+1)-\operatorname{bit}(K'),\\
 t_2&=t_1+2(k-1)\operatorname{bit}(K')+(2k-1)\operatorname{bit}(k),\\
 T&=K'[t_2+\operatorname{bit}(K')+2\operatorname{bit}(2D+1)+1].
\end{aligned}
\]

A conservative exponent, including a source inconsistency discussed below,
is

\[
\begin{aligned}
 E_m={}&\operatorname{bit}(2DK'(2K'-1)+1)\\
 &+(2K'-1)\bigl[T+\operatorname{bit}(2K'-1)
      +\operatorname{bit}(2DK'+1)+K'\operatorname{bit}(K')\bigr].
\end{aligned}
\]

The last summand inside the bracket is deliberate. The final Theorem 2/4
statements omit a factorial-bit term that occurs in the subresultant and
Cauchy bounds in the proof of Theorem 2, printed page 12. Including
`K' bit(K')` covers `bit(K'!)`, since `(K')! <= (K')^(K')`.
The displayed `E_m` also drops the outer square root, further enlarging the
radius. It therefore accommodates both the theorem-statement formula and
the larger proof formula. This avoids relying on an unexplained omission.

For completeness, to use a single radius for bounded and unbounded
components one may take `2^max(E_b,E_m)`. The source's proof treats bounded
components through its bounded-component theorem. Taking this maximum costs
nothing at the requested asymptotic scale and avoids needing a separate
comparison between the two numerical bounds.

## Asymptotic check

For `1 <= d <= 3`,

\[
 K\le7\cdot6^{k-1},\quad K'\le8\cdot7^{k-1},\quad
 D_b=O(k),\quad D=O(k).
\]

In particular, `bit(K), bit(K') = O(k)` and
`bit(D) = O(log(k+1))`. Direct substitution gives

\[
 E_b=O\!\left(6^k k[\tau+\log(s_0+1)+k]\right),
\]

\[
 E_m=O\!\left(49^k k[\tau+\log(s_0+1)+k+\log(k+1)]\right).
\]

Since `tau >= 1`, the extra polynomial factors in `k` can be absorbed into
`2^{O(k)}`. Both exponents therefore satisfy

\[
 \max\{E_b,E_m\}
 \le (\tau+\log(s_0+1)+1)2^{O(k)}.
\]

Thus switching to the final source, restricting to weak basic closed
branches, and including the omitted factorial term preserve the draft's
claimed exponential dependence on continuous dimension. This source audit
does not by itself establish the other hypotheses of the penalty theorem.

## Why the older proof should not be used unchanged

The 2009 proof of Theorem 3 asserts containment of a full algebraic
component chosen from active constraints at an extremal coordinate. That
intermediate assertion fails for the disk cut by `y >= -1/2`: at its
rightmost point `(1,0)`, only the circle constraint is active, but the full
circle leaves the cut disk. The final proof works within the extremal
coordinate fiber and then a nearby strip, avoiding that particular step.
This example refutes the old intermediate assertion, not the claimed
asymptotic radius bound.

## Verification record

The 2009 and 2010 primary PDFs were opened through the web tool and
downloaded to `/tmp/basu-roy-2009-source-audit.pdf` and
`/tmp/basu-roy-2010-source-audit.pdf`. The commands used included `curl`,
`pdftotext -layout`, and `pdftoppm -f 5 -l 5 -scale-to 2000 -png -singlefile`
for the final theorem page. The rendered page was inspected with
`view_image`; this confirms the exponent placement and outer square root
independently of PDF text extraction. The statement/proof factorial
discrepancy was checked in the extracted final text.

A separate reviewer independently checked scope and found the later author
version; its source corrections and formulas were then rechecked directly.
No main-file edits, full-repository verification, or CI inspection were
performed. No Lean or numerical verification was used or needed for these
source substitutions and elementary majorizations.
