# Focused final review of the analytic rate figure

Status: passed. No correction is required in the new figure, its caption,
the explicit start-box premise in `cor:local-gap`, or the revised sufficient
stall wording. The accepted proofs from the second review were not repeated.
`structure-revision.md` records their preservation during consolidation.
The restricted tangent setup now points to the local shape definitions and
keeps the distinct outer domain `B_0` and starting box `B_0'`.

The review read the relevant parts of `sections/local-rates.tex`, all of
`figures/rates.py`, `evidence/figure-note.md`, and
`evidence/structure-revision.md`, and viewed the existing PNG rendering at
`/tmp/analytic-obbt-rates-review.png`.

| Location | Finding |
| --- | --- |
| `fig:analytic-rates`, caption lines 819–832; `rates.py`, lines 20–35 | The plotted formulas agree with the proved exact centered-cube factors and the scalar upper bound. The complete-graph formula is used only for `n>=3`; the script explicitly rejects smaller dimensions. |
| Caption lines 822–825; script lines 25–27, 39 | The specialization `mu=1-a^2/4`, `tau=a/4` is valid. Thus `q^2=a/(1-a^2/4)`, and `q<1` is equivalent on `0<a<2` to `a<2*sqrt(2)-2`. Failure of this sufficient bound is not presented as stalling. |
| Caption line 826; script lines 40–42, 85–88 | The scalar curve is deliberately truncated at `q=1.6`. The supplied inverse expression for its terminal parameter is correct; the truncated curve does not suggest that the bound stops increasing. |
| Caption lines 827–831; script lines 43, 106–122 | The exact cube factor is `min(1,t_n(a))`. Its threshold is `2/((n-1)(n-2))`, giving the marked values `1`, `1/3`, and `1/10` for `n=3,4,6`. The markers and overlapping plateaus match the formulas, including fixed cubes at equality. |
| Caption lines 820–821, 827–832 | The exact per-round interpretation is limited to centered cubes and Jacobi updates at zero slack. The caption does not assert successive-ratio convergence or fixedness for arbitrary boxes. Strong convexity is stated only on `0<a<2`; the endpoint values are correctly described as continuous limits. |
| `cor:local-gap`, lines 1222–1249 | Referring explicitly to `thm:tangent-contraction`(b) now includes `g_u(B_0)<=bar t`, which the limit-box inclusion in the proof needs. The separate positive-cutoff comparison-scale restriction and the sharp-growth entry condition remain explicit. |
| Lines 339–340, `cor:face-test`, and `ex:many-term` | The general stall result is a sufficient condition. The face tests remain sufficient, and the exact stall threshold is confined to the stated complete-graph cube family. No general dichotomy is restored by the figure. |

The scalar constants can be checked without a numerical run: completing
the square in either coordinate gives
`f >= (1-a^2/4)*max(x^2,y^2)`. The McCormick product gap on a rectangle is
at most `w_x*w_y/4`, so the objective gap is at most `(a/4)*w(B)^2`.
For the complete-graph family, the support polynomial at the cube face is
`1-a*(n-1)*(n-2)/2`; its nonpositive values give exactly the displayed
plateaus. The Hessian eigenvalues `2-a` and `2+a*(n-1)` are positive
throughout the stated open interval.

Reviewed SHA-256 snapshots:

| File | SHA-256 |
| --- | --- |
| `sections/local-rates.tex` | `de079f21574486bd3e0fa5f914d857279dc1a328b2c5bfda8f088a1337bfbd75` |
| `figures/rates.py` | `9f51ac9046efc64909380a5540c5b0b256b850fc99411b330dd96ac316692088` |
| `figures/rates.pdf` | `d6268d88002ac02a14c87f63ae40999d67039d636553cc39842fd9d55f71a2ab` |

Targeted commands were `rg -n`, `rg --files`, numbered `sed -n` reads,
`cat`, and `sha256sum`; the image-view tool read an existing rendering.
Only this evidence file was written. No plotting script, experiment,
solver, build, project-wide check, CI inspection, or literature search was
run by this reviewer.
