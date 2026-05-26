# A 63-dimensional counterexample to Borsuk's conjecture

This repository contains a proof note and an exact finite verification script for a 63-dimensional construction related to Borsuk's conjecture. It gives

$$
d_B\le 63,
$$

where $d_B$ denotes the least dimension in which Borsuk's conjecture fails.

The construction starts from the $G_2(4)$ strongly regular graph described by Brouwer [[BroG24](#BroG24)] and used in Bondarenko's 65-dimensional two-distance counterexample [[Bon2014](#Bon2014)]. The previous best bound $d_B\le64$ is due to Jenrich and Brouwer [[JB2014](#JB2014)].

The construction and proof note were obtained with assistance from GPT-5.5 Pro.

The principle of the proof is as follows. In the standard $65$-dimensional representation of $G_2(4)$, an isotropic point $q_0$ defines a partition $B_1,B_2,B_3,C$ of the vertices. The $320$ points indexed by $C$ are orthogonal to a 2-dimensional space spanned by three block sums, hence lie in a 63-dimensional subspace. One then adds a single projected point $p$ in the same subspace, chosen so that the diameter remains the original large distance. The absence of a $6$-clique in $G_2(4)$ then implies that every smaller-diameter part has at most $5$ points, so $321$ points require at least $65>64$ parts.

Only the input configuration $\{x_v\}$ uses the standard two-distance $G_2(4)$ representation; after adjoining $p$, the final $321$-point set is not two-distance.

## 1. Quoted input

This part records the standard graph-theoretic and Euclidean facts used as input.

Let

$$
\Gamma\simeq \mathrm{srg}(416,100,36,20)
$$

be the $G_2(4)$ graph. We use its standard Euclidean representation [[Bon2014](#Bon2014), [BroG24](#BroG24)], namely vectors

$$
x_v\in\mathbb R^{65}\qquad (v\in V(\Gamma))
$$

such that

$$
x_u\cdot x_v=
\begin{cases}
90, & u=v,\\
18, & u\sim v,\\
-6, & u\not\sim v.
\end{cases}
$$

Equivalently, the Gram matrix is

$$
G=96I+24A-6J,
$$

where $A$ is the adjacency matrix of $\Gamma$. The eigenvalues of $G_2(4)$, as recorded by Brouwer [[BroG24](#BroG24)], give that $G$ is positive semidefinite of rank $65$. In this representation,

$$
\|x_u-x_v\|^2=
\begin{cases}
144, & u\sim v,\\
192, & u\not\sim v.
\end{cases}
$$

We also use the clique obstruction underlying Bondarenko's construction [[Bon2014](#Bon2014)]:

$$
\omega(\Gamma)=5.
$$

The script `verify_borsuk63.py` reconstructs the graph and verifies this obstruction again.

## 2. The finite partition

This part defines the partition, from an isotropic point $q_0$, whose verified degree data will be used for the dimension drop.

Fix an isotropic point $q_0$ in the projective model of $G_2(4)$ described by Brouwer [[BroG24](#BroG24)]. Let $B$ be the set of vertices containing a non-isotropic point orthogonal to $q_0$, and put

$$
C=V(\Gamma)\setminus B.
$$

The script then forms the partition $B,C$ and gives

$$
|B|=96,\qquad |C|=320.
$$

It also verifies that the induced graph on $B$ has three connected components

$$
B_1,B_2,B_3
$$

of size $32$, and verifies

$$
\begin{aligned}
&|N(u)\cap B_i|=20 &&(u\in B_i),\\
&|N(u)\cap B_j|=0 &&(u\in B_i,\ i\ne j),\\
&|N(u)\cap C|=80 &&(u\in B),\\
&|N(c)\cap B_i|=8 &&(c\in C,\ i=1,2,3),\\
&|N(c)\cap C|=76 &&(c\in C).
\end{aligned}
$$

## 3. Dimension reduction

This part shows that the $320$ points indexed by $C$ lie in a codimension-$2$ subspace of the standard $\mathbb R^{65}$ representation.

For $i=1,2,3$, set

$$
S_i=\sum_{y\in B_i}x_y.
$$

If $c\in C$, then $c$ has $8$ neighbors and $24$ non-neighbors in $B_i$. Hence

$$
x_c\cdot S_i
=8\cdot18+24\cdot(-6)
=0.
$$

Thus every $x_c$, $c\in C$, is orthogonal to $S_1,S_2,S_3$.

The same degree data give

$$
S_i\cdot S_i
=32(90+20\cdot18+11\cdot(-6))
=12288,
$$

and, for $i\ne j$,

$$
S_i\cdot S_j
=32^2(-6)
=-6144.
$$

The Gram matrix of $S_1,S_2,S_3$ has diagonal entries $12288$ and off-diagonal entries $-6144$, hence has rank $2$. Since the ambient representation has rank $65$, the orthogonal complement

$$
\mathrm{span}(S_1,S_2,S_3)^\perp
$$

has dimension $63$, and all points $x_c$, $c\in C$, lie in this subspace.

## 4. The added point

This part constructs one further point in the same 63-dimensional subspace and records its products with the points indexed by $C$.

Choose $b\in B_1$, and define

$$
z_b=x_b-\frac1{32}S_1.
$$

The verified degree data imply

$$
z_b\cdot S_i=0\qquad (i=1,2,3),
$$

so $z_b$ lies in the same 63-dimensional subspace. Moreover

$$
\|z_b\|^2
=90-\frac{2}{32}\cdot384+\frac{1}{32^2}\cdot12288
=78.
$$

For $c\in C$, since $S_1\cdot x_c=0$,

$$
z_b\cdot x_c=x_b\cdot x_c
=
\begin{cases}
18, & b\sim c,\\
-6, & b\not\sim c.
\end{cases}
$$

Let

$$
t=\frac{\sqrt{222}-1}{13},
\qquad
p=tz_b.
$$

Then

$$
78t^2+12t=102.
$$

Set

$$
X=\{x_c:c\in C\}\cup\{p\}.
$$

Since $\|p\|^2=78t^2\ne90=\|x_c\|^2$ for $c\in C$, the point $p$ is not one of the $x_c$. Thus $X\subset\mathbb R^{63}$ and $|X|=321$.

## 5. Diameter and clique obstruction

This part computes the diameter of the resulting $321$-point set and uses the clique obstruction to bound smaller-diameter subsets.

For $c,c'\in C$, the quoted two-distance representation gives

$$
\|x_c-x_{c'}\|^2=
\begin{cases}
144, & c\sim c',\\
192, & c\not\sim c'.
\end{cases}
$$

For the added point $p$,

$$
\|p-x_c\|^2=
\begin{cases}
192-48t, & b\sim c,\\
192, & b\not\sim c.
\end{cases}
$$

Therefore

$$
\mathrm{diam}(X)^2=192.
$$

The script verifies the required clique facts: there is no $6$-clique in $\Gamma$, no $6$-clique on $C$, and no $5$-clique in $N(b)\cap C$.

Let $Y\subset X$ have diameter strictly smaller than $\mathrm{diam}(X)$. If $p\notin Y$, then the corresponding vertices in $C$ must be pairwise adjacent, hence form a clique in $\Gamma$. Since the script verifies that $\Gamma$ has no $6$-clique, $|Y|\le5$.

If $p\in Y$, then every other point of $Y$ must be some $x_c$ with $b\sim c$, and these $c$'s must be pairwise adjacent. Hence

$$
\{b\}\cup\{c\in C:x_c\in Y\setminus\{p\}\}
$$

is a clique in $\Gamma$. Again using the verified absence of a $6$-clique, this gives $|Y|\le5$.

Thus every subset of $X$ of strictly smaller diameter has at most $5$ points. Any partition of $X$ into subsets of strictly smaller diameter therefore needs at least

$$
\left\lceil\frac{321}{5}\right\rceil=65
$$

parts. Since $65>64=63+1$, this gives a counterexample to Borsuk's conjecture in $\mathbb R^{63}$. Consequently,

$$
d_B\le63.
$$

## 6. Verification

This part gives the command reproducing the finite checks used above.

Run

```bash
python verify_borsuk63.py
```

The expected output is:

```text
projective points 273
isotropic 65 nonisotropic 208
vertices 416
degrees [100] edges 20800
lambda [36] mu [20]
B size 96 C size 320
B component sizes [32, 32, 32]
B1 internal [20]
B1 to B2 [0]
B1 to B3 [0]
B1 to C [80]
B2 internal [20]
B2 to B1 [0]
B2 to B3 [0]
B2 to C [80]
B3 internal [20]
B3 to B1 [0]
B3 to B2 [0]
B3 to C [80]
C to B1 [8]
C to B2 [8]
C to B3 [8]
C internal [76]
K5 full witness [0, 122, 126, 130, 134]
has K6 full False
has K6 on C False
b 0 NbC size 80 has K5 on NbC False
all exact verification checks passed
```

## References

<a id="Bon2014"></a>[Bon2014] A. V. Bondarenko, *On Borsuk's conjecture for two-distance sets*, Discrete & Computational Geometry 51 (2014), 509--515. Preprint: https://arxiv.org/abs/1305.2584

<a id="JB2014"></a>[JB2014] T. Jenrich and A. E. Brouwer, *A 64-dimensional counterexample to Borsuk's conjecture*, Electronic Journal of Combinatorics 21(4), P4.29 (2014). PDF: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v21i4p29/pdf

<a id="BroG24"></a>[BroG24] A. E. Brouwer, *The $G_2(4)$ graph*, graph data and construction notes. https://aeb.win.tue.nl/graphs/G24.html
