# Independent review of the inertia slice integration

Reviewed `LowerNegativeSlice.lean` and `LowerPositiveSlice.lean` against the
quadratic inertia source note. The reviewer authored the underlying spectral
slice primitives, but did not author either integration module. The spectral
primitives receive a separate independent review in `spectral.md`.

The integration constructs a parameter space of exactly the relevant inertia,
using a finite equivalence with the actual negative or positive eigenvalue
indices. The affine restriction is injective and maps a full box with positive
side length into the original nondegenerate box. Neither a slice nor its
curvature is a premise of the resulting lower bounds.

The restricted polynomial has Hessian `Tᵀ * H * T`. Its linear coefficient is
`(1/2) • ((c ᵥ* H + H *ᵥ c) ᵥ* T) + a ᵥ* T`, and its constant is the original
polynomial at `c`. This identity is valid even before imposing symmetry.
Finite reindexing preserves the sum of squared parameter coordinates, so the
strict spectral curvature bound transfers without a dimension change.

Pullback preserves the number of integer coordinates and the one-sided
relaxation condition. The hypograph proof reflects the restricted output and
negates the restricted polynomial, using the positive eigenspace of the
original Hessian. It does not assume a correspondence between the separately
chosen eigenbases of `H` and `-H`.

The final logarithmic bounds quantify their additive constant before the error
tolerance and the lift. The constant therefore cannot depend on either.
The arguments also allow inertia zero: the zero-dimensional parameter box has
volume one. Exact zero-integer representations are supplied separately by
`SpectralConvex.lean`.

These integration theorems use the elementary coordinate-diameter volume bound,
which establishes the stated logarithmic coefficient with a weaker additive
constant. They do not by themselves verify the sharper Euclidean-ball-volume
constant in the source note; that is a separate geometric obligation.

No defect found. Targeted verification passed:

```sh
cd formal
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail \
  Formal.QuadraticPrecision.LowerNegativeSlice \
  Formal.QuadraticPrecision.LowerPositiveSlice
```

No project-wide build or CI inspection was performed.
