# Certificates

This directory contains DIMACS certificates for the finite graphs used in the
proof.

- `g24_full.dimacs`: the full $G_2(4)$ graph on 416 vertices.
- `g24_C.dimacs`: the induced subgraph on the 320 vertices in $C$.
- `g24_NbC.dimacs`: the induced subgraph on $N(b)\cap C$.
- `borsuk63_metadata.json`: partition data, vertex maps, and SHA256 hashes.

The Sage script `../verify_borsuk63_sage.sage` gives an independent Sage
verification of the exported DIMACS certificates: it reads these files and
checks the strongly regular parameters, partition degree data, and clique
obstructions.
