# When can a trace cleaning product matter in styrene recycle?

2026-09-15. Analytical bounds for experimental design. No values below are measured properties of the proposed zirconia process.

## Why this calculation is needed

Artsiusheuski et al. infer that ethylbenzene removes water-derived surface titrants and restores active Zr–O pairs. Their model represents an unidentified product X as more weakly binding than water. Its formation was below the analytical detection limit under the reported dilute, low-conversion conditions. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.6-8; [DOI](https://doi.org/10.1021/acscatal.5c04904).

The proposed new concern is that some X returns with ethylbenzene recycle and inhibits sites over long operation. This requires **both** significant return and consequential site inhibition. Neither follows from the existence of an oxygenated product. A high-boiling product removed with a heavy purge may never accumulate in ethylbenzene recycle. A species that returns but hardly binds may be harmless. Test these simpler alternatives first.

## Steady-flow species balance

At fixed reactor throughput, define:

- `J0`: fresh-feed molar input rate of one identified impurity X.
- `G`: net rate at which the reactor produces X from other species in a pass.
- `s`: fraction of entering X that leaves that reactor pass as X, excluding newly generated X.
- `q`: fraction of outlet X returned to the reactor after separation and purge. This is a species-specific measured return fraction, not the ethylbenzene recycle fraction.

For a linear, time-invariant illustrative balance:

```text
Jout = s*Jin + G
Jin  = J0 + q*Jout
Jin  = (J0 + q*G)/(1 - q*s), when q*s < 1.
```

Use actual molar flows for J, not uncorrected concentrations across streams of different flow. Composition-dependent reaction, separation, or generation requires a coupled model; the formula is then only a local approximation. At `q*s=1`, a constant nonzero source has no finite steady solution in this approximation.

For `J0=0` and `s=1`, the following are mathematical examples, not predictions:

| X return fraction q | Recycled X entering per unit generation, Jin/G |
|---|---:|
| 0 | 0 |
| 0.5 | 1 |
| 0.9 | 9 |
| 0.99 | 99 |

The q=0.99 case does not become credible merely because bulk ethylbenzene is efficiently recycled. Measure or estimate X partition through the intended separation. If q is small, the proposed accumulation concern becomes weak and the program should narrow accordingly.

## Disappearance is not automatically protection

An apparently small s may mean X reacts to harmless volatile products. It may instead mean X accumulates on the catalyst or turns into a more strongly binding species Y. Distinguish these by solid inventories and product balances. During accumulation the stationary expression is invalid, and a clean effluent can coexist with growing catalyst damage.

The same warning applies to a guard material. A successful short test can reflect finite capacity rather than a regenerable removal mechanism. Compare cumulative admitted impurity against measured capacity and record the replacement/regeneration burden.

## Site balance separates water and organic inhibition

An intentionally simple candidate model has vacant sites V, water-blocked sites W, and X-blocked sites B, with `V+W+B=1`:

```text
dW/dt = kw*cwater*V - kclean*cethylbenzene*W
dB/dt = kx*cX*V - kremove*B
```

At a true steady state with positive kremove, the vacant fraction is

`V = 1/[1 + kw*cwater/(kclean*cethylbenzene) + kx*cX/kremove]`.

This is not a validated rate law. It shows why independently measuring water alone may be insufficient if organic blockage persists, and why a nominally weaker adsorbate can matter at a greater concentration or a much slower removal rate. If X does not measurably bind at the justified recycle concentration, stop that inhibition branch. If kremove is effectively zero, a fixed long-term vacant fraction is not predicted by this simple model; progressive damage and recovery have to be assessed explicitly.

## The first experiments that constrain the model

1. Identify or bound oxygen-containing outputs while observing activity recovery after calibrated water exposure. Measure water independently; the existing paper's estimated ppm values are not an independent inlet-water measurement.
2. Distinguish organic export, water desorption, isotope exchange with support oxygen, and retained oxygen. H2-18O product labeling alone cannot identify which event uncovered a catalytic pair.
3. At relevant ethylbenzene/styrene/H2 chemical potentials, measure dose-response, breakthrough, and recovery for any identified X. Avoid choosing a severe but unrealistic dose merely because it poisons the catalyst.
4. Obtain a species-specific separation/return estimate from measured partition or a defensible process model before building a recycle apparatus. The return fraction determines the exposure to test.
5. Compare water removal alone, ordinary product separation, and a targeted additional removal step on cumulative styrene output and regeneration demand. An extra purification operation is justified only if the first two fail in a consequential way.

## Decision consequence

The potentially useful advance is a validated impurity specification and regeneration/separation choice derived from the actual cleaning chemistry. It is not a presumption that recycle creates poisoning. Complete oxygen export to readily separated, noninhibiting products would be a valuable positive result for process viability, even though it rejects the accumulation hypothesis. A product too scarce to identify only justifies bounds that the analytical recovery and site inventory can support.
