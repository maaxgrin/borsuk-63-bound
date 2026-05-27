# A 63-dimensional counterexample to Borsuk's conjecture

This repository contains:

- [borsuk_63_counterexample.pdf](borsuk_63_counterexample.pdf): proof of $d_B\le 63$;
- [verify_borsuk63.py](verify_borsuk63.py): exact finite verification used in the proof;
- [certificates/](certificates): DIMACS graph certificates and SHA256 metadata;
- [verify_borsuk63_sage.sage](verify_borsuk63_sage.sage): independent Sage verification of the exported DIMACS certificates.

Here $d_B$ denotes the least dimension in which Borsuk's conjecture fails. The previous best published upper bound was $d_B\le 64$, due to Jenrich and Brouwer, building on Bondarenko's $G_2(4)$ construction.

The verification script reconstructs the $G_2(4)$ finite model over $\mathbb F_{16}$ and checks:

- the strongly regular parameters $(416,100,36,20)$;
- the partition $V=B\sqcup C$, with $|B|=96$ and $|C|=320$;
- the three $32$-vertex components $B_1,B_2,B_3$ of the induced graph on $B$;
- the degree data between $B_1,B_2,B_3$ and $C$ used for the dimension drop;
- the clique obstructions used to show that every smaller-diameter subset has size at most $5$.

Run:

```bash
python verify_borsuk63.py
```

To regenerate the DIMACS certificates, run:

```bash
python export_borsuk63_certificates.py
```

If Sage is available, the exported DIMACS certificates can be checked independently with:

```bash
sage verify_borsuk63_sage.sage
```

The GitHub Actions workflow runs the pure-Python verification and checks that
the exported certificates are reproducible. The Sage verifier is provided as
an optional independent check.

The construction and proof were obtained with assistance from GPT-5.5 Pro.

The corresponding optimization-problems entry is:
https://teorth.github.io/optimizationproblems/constants/28a.html

## References

- A. V. Bondarenko, *On Borsuk's conjecture for two-distance sets*, Discrete & Computational Geometry 51 (2014), 509--515. https://arxiv.org/abs/1305.2584
- T. Jenrich and A. E. Brouwer, *A 64-dimensional counterexample to Borsuk's conjecture*, Electronic Journal of Combinatorics 21(4), P4.29 (2014). https://www.combinatorics.org/ojs/index.php/eljc/article/view/v21i4p29/pdf
- A. E. Brouwer, *The $G_2(4)$ graph*. https://aeb.win.tue.nl/graphs/G24.html
