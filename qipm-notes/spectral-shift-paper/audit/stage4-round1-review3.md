# Stage 4, round 1: independent review 3

**Findings: 0 major, 0 minor.** No repair is requested.

Reviewed the abstract, Sections 1, 7 and 8, overview figure and scripts,
README, Makefile, packaging script and archive, macros, bibliography, and final
source-coverage ledger. Read the Stage 4 author and literature audits, but no
peer reports. This checks the new framing against previously reviewed
mathematics; it does not replace the subsequent full-proof review.

## Framing, readership, and scope

The introduction states the target, error metric, spectral promise, allowed
public information, completion-uniform requirement, and query measure before
presenting the results. It explicitly says that reuse requires paying for
the conversion circuit's queries again. QSVT, GQSP, and LP are expanded when
introduced. The threshold definition and its integer indices precede the
staircase formula; the figure caption defines the plotted exponent.

The abstract, introduction, and conclusion agree with the reviewed theorems:

- Threshold equality selects the cheaper tier. The general coarse tier
  distinguishes a positive-width high interval from the singleton `{1}`.
- The even result uses the nonnegative thresholds F_r and their plateau,
  not the unconstrained approximation errors. The degree-six witness is
  expressly an upper bound on F_3, not an exact evaluation.
- The single-transform parity restriction is distinguished from arbitrary
  compositions. The odd logarithmic factor appears in both the overview
  and figure.
- The uniform high-accuracy law states positive K and fixed beta. The
  intermediate comparison retains the margin factor and does not claim
  an optimal multiplicative law. The conclusion records this remaining
  problem, higher even thresholds, and synthesis costs.
- The LP summary distinguishes the dual state, matrix-only compiler, and
  factor access. It retains the zero-query coarse exception, public primal
  predictor, digital-entry bypass, and absence of an LP-solving lower bound.

The proof roadmap matches the order of the manuscript. The introduction is
substantial but gives a quantum-algorithms reader enough information to
understand what is proved, which restrictions matter, and where to find
the precise statements.

## Literature and source ledger

The related-work discussion separates established implementation, sign
approximation, constrained approximation, and factor-access tools from the
specific thresholds and query laws. Its originality statement is qualified
and restricted to the stated problem. It does not claim to solve the general
sparse-value construction question of Orsucci--Dunjko.

I additionally inspected local primary-source introductory passages for
Dong--Larsen--Lin--Sarkar, Laneve, and Somma--de Wolf. The new comparisons
accurately describe, respectively, prescribed-parity constrained minimax
design and feasibility restoration; QSP through state conversion and
adversary feasibility; and guided energy/state bounds with overlap and
dimension assumptions. The last comparison does not transfer those bounds
to the present output task. Historical approximation references receive
broad descriptions rather than unsupported theorem-by-theorem exclusions.

The final source ledger agrees with the staged mathematical reviews and
records the substantive corrections: approximation-aware pairwise constants,
rounding uncertainty, the singleton coarse tier, stronger parity results,
growing-index tail constants, and the LP's public-projector exception.
Checked representative theorem numbers against `main.aux`; they match.
The integrated bibliography builds without undefined keys or warnings.

## Figure and numerical presentation

Inspected the overview image and rendered first page. Both are readable.
The left panel's threshold order, exponents, and filled/open markers match
the exact-threshold convention. Its final displayed interval remains above
the next threshold. The caption correctly explains that exponent zero can
hide a logarithmic cost.

On the right panel, the whole plotted range lies above G_1 and the proved
upper bound for F_3. Therefore the displayed unrestricted exponent one half,
even jump at one twenty-fourth, and odd exponent one with its logarithm are
all justified. Coincident even and unrestricted powers are shown without
an artificial vertical displacement. Numerical threshold locations are
distinguished from proved complexity statements and continuous-domain
contractivity.

## Reproduction and package checks

Used the qipm environment. Its actual Python, NumPy, SciPy, and Matplotlib
versions match the README. The archive passes its CRC check, contains the
18 intended source files, and every archived file matches the corresponding
workspace file byte-for-byte. It includes the required figure and generated
bibliography while excluding audits, local literature, logs, and previews.

Extracted the archive to a temporary directory outside the manuscript tree
and ran `conda run -n qipm --live-stream make`. The build succeeded with no
LaTeX/BibTeX warnings, undefined references, or overfull/underfull boxes.
Also ran the extracted overview script with the qipm interpreter from
`/tmp`, verifying its independence from the current working directory.
It regenerated the figure and reported the expected G_1 and witness bound.
The temporary extraction was removed afterward.

The Makefile and README accurately distinguish the Python-free paper build,
optional figure regeneration, and source packaging. No manuscript source,
figure, archive, or other frozen artifact was changed during this review.
