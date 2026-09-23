# Pre-Stage-6 research reference

Files were copied before the production flat-chain upgrade. `manifest.json`
records original paths and SHA-256 hashes. Original baseline builders and
historical JSON data also remain unchanged in the repository.

The current benchmark loads `flat_chain.py` as
`network_simplex._stage06_unreduced`, resolving its relative import to the
unchanged exact separator. This keeps the full unreduced model and recovery
algorithm for research comparison, without a second public production API.
Historical runners use script-style imports; their flat-oracle import must
target this snapshot to reconstruct the historical algorithm.
