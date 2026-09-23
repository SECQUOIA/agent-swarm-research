# Stage 5B author audit: active-constraint and entropy acquisition

Authored `sections/12e-active-compilers.tex`. All new labels use `active:`.
No shared main, bibliography, or source ledger was edited. This is author
verification; the five independent stage reviews remain required.

## Source disposition

- `quantum-barrier-compilation-socp`: exact radius consensus, Slater,
  zero/one acquisition, public reconstruction, natural versus compiled
  parameter and radial path, failure of uniform division, consensus KKT
  conditioning, homothetic extension, supplied chains, sharp independent OR
  family, and explicit-loading boundary are all included. General minimum
  finding keeps `log(2k)` joint-success amplification. The promised OR
  family uses exact known-cardinality amplification instead and has the
  claimed tight bound without hidden joint failure.
- `pareto-soc-barrier-compiler`: exact body and all essential-factor witnesses,
  adjacent-pair normal-cone witness, source-free reusable description model,
  exact-cardinality search and block restriction lower bound, explicit
  parameter ranges, path comparison, and arbitrary planar barrier caveat
  are included. Kept `1 <= k <= N/2`. Essentiality is explicitly only in
  the displayed intersection description, not a minimum over arbitrary
  lifts. Different bodies are decoded by finite public separating
  membership witnesses; mere input dependence is not used as a query proof.
- `kblock-pareto-soc-compiler`: rational Q4 family, bounded incidence and
  constant-width copied lift, exactly 2k essential displayed factors,
  coordinate decoder and feasible objective-gap decoder, quantum/classical
  costs, and natural versus compiled barrier/path comparison are included.
  Kept `m >= 2` and the separate objectives `sum q_j` and `y`. The theorem
  does not assert a value-only or amplitude-state lower bound. After
  acquisition the displayed decoding optimizer takes O(k) arithmetic.
- `blockwise-relative-entropy-source-compiler`: exact closed epigraph
  projection, symbolic/public coefficient encoding, source-erasing
  acquisition, readable feasible gap decoder, scalar treewidth, exact
  matched-gap metric identity, ambient 3N/3B and fixed-slice N/B distinction
  are included. The original natural length is in source slack coordinates;
  added its equivalent projected marginal metric explicitly to avoid
  confusing it with the compiled metric. Moving U,V is not covered by
  that fixed-slice calculation. The elementary identity reuses
  `eq:qre-compiler`; optimal ambient parameters reuse
  `thm:entropy-product`.

## Independent checks and corrections

- Recomputed the Pareto identity `(q(v)-q(w)) dot (2v,1)=(v-w)^2`
  and the adjacent identity `(q(r)-q(v)) dot (v+w,1)=(r-v)(w-r)`.
  Positivity of both squared coordinates and nonparallel normals yield
  genuine two-active-factor exposing objectives.
- The planar path statement is uniform for `0<epsilon<=1/4`, so the
  integration interval has a fixed positive length. With `M>=k`, the
  singular sentinel term dominates the natural order; the compiled
  integral is the sum order `sqrt(k)+log(1/epsilon)`. Endpoint barrier
  increase and the previously proved height lemma also give a path-
  independent natural distance lower bound at sufficiently small epsilon.
- Recomputed the growing-block decoder: reciprocal differences are
  `(u_(l+1)-u_l)/((3-u_l)(3-u_(l+1))) > 1/[18(m+1)]`; the requested
  `1/[40(m+1)]` is strictly below half. Feasibility makes every deficit
  nonnegative, so total objective excess controls each coordinate.
- Verified the consensus indefinite KKT condition estimate by eliminating
  negative eigenvalues: `A(D+tI)^(-1)A^T y=t y`. Its smallest root is
  Theta(N^-2); positive eigenvalues are >=1/2, all eigenvalues O(1).
  This avoids asserting indefinite KKT conditioning solely from an
  unproved analogy with the normal equations.
- Verified the shared independent-search adversary with input indices
  `[m]^b`: norm b(m-1), filtered norm sqrt(m-1). Standard nonnegative
  adversary suffices; no stronger unproved direct-product theorem is used.
- Full source oracle symbols are public functions of queried marks; exact
  entropy coefficients can be recorded symbolically or as the affine
  coefficient gamma rather than demanding a finite exact exponential.
- The entropy matched-gap length was independently obtained from the
  orthant metric: N copies versus B copies of `d Delta/Delta`. Marginal
  elimination gives `-m sum log(t_j-gamma_j)` plus a constant, not the
  compiled `-sum log(t_j-gamma_j)`.

## Literature checked

Read local packages `gondzio1997-presolve-linear-programming` and
`brassard2002-quantum-amplitude-amplification-and-estimation` without edits.
Opened the following primary material on 2026-09-20:

- BHMT, https://arxiv.org/pdf/quant-ph/0005055: Theorem 4 gives exact
  amplitude amplification with known probability; Theorem 16 gives exact
  zero-versus-known-cardinality search. Existing `BHMT2002` entry suffices.
- Ambainis--Childs--Le Gall--Tani, publisher full PDF
  https://www.rintonpress.com/xxqic10/qic-10-34/0181-0189.pdf:
  Theorems 3 and 4 give the nonnegative spectral adversary and direct sum.
  Existing `ACGT2010` suffices. Their printed pp.186--187 explicitly
  apply the direct sum to independent search.
- Montanaro, primary author manuscript
  https://people.maths.bris.ac.uk/~csxam/papers/0702196.pdf:
  introduction distinguishes concrete ordered-value and abstract
  comparison-oracle poset search. These are not identical to the present
  unsorted chain-key model. arXiv primary metadata
  https://arxiv.org/abs/quant-ph/0702196 verifies the journal reference.
- Gondzio, publisher abstract and metadata
  https://pubsonline.informs.org/doi/10.1287/ijoc.9.1.73:
  dominated-constraint elimination, sparsity improvement, and dependency
  removal are established presolve. Local package agrees. No claims about
  its current empirical performance are made.

The section does not claim new quantum search or entropy barrier theorems.
Its contribution is the explicit formulation/access/output/metric
conjunction, with full elementary construction proofs. Negative literature
search is not used to assert priority.

## Bibliography additions for integrating author

Add the following two entries (not yet inserted in shared bibliography):

```bibtex
@article{Gondzio1997,
 author={Gondzio, Jacek},
 title={Presolve Analysis of Linear Programs Prior to Applying an Interior Point Method},
 journal={INFORMS Journal on Computing}, volume={9}, number={1},
 pages={73--91}, year={1997}, doi={10.1287/ijoc.9.1.73}}
@article{Montanaro2009,
 author={Montanaro, Ashley},
 title={Quantum Search of Partially Ordered Sets},
 journal={Quantum Information and Computation}, volume={9}, number={7--8},
 pages={628--647}, year={2009}, eprint={quant-ph/0702196},
 archivePrefix={arXiv},
 url={https://people.maths.bris.ac.uk/~csxam/papers/0702196.pdf}}
```

All other citation keys already exist. A standalone syntax harness compiled
under qipm/pdflatex to 8 pages, with no errors or overfull boxes. Its missing
bibliography and external-reference warnings are expected in isolation.
The syntax check caught and fixed an accidental `inQ` token after notation
standardization. A regex scan also removed all bare `quad`/`qquad` tokens;
Lorentz notation now consistently uses the manuscript's `Q_m`.
Integration should compile the full manuscript and check labels; the author
only changed the two assigned files.
