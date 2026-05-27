from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from verify_borsuk63 import (
    check,
    bit_count,
    hermitian,
    line_points,
)


ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT / "certificates"


def build_instance():
    points = []
    seen = set()
    for v in product(range(16), repeat=3):
        if v == (0, 0, 0):
            continue
        from verify_borsuk63 import normalize

        p = normalize(v)
        if p not in seen:
            seen.add(p)
            points.append(p)
    points.sort()

    isotropic = [p for p in points if hermitian(p, p) == 0]
    nonisotropic = [p for p in points if hermitian(p, p) != 0]
    iso_index = {p: i for i, p in enumerate(isotropic)}

    orth = [[False] * len(nonisotropic) for _ in nonisotropic]
    for i, a in enumerate(nonisotropic):
        for j in range(i + 1, len(nonisotropic)):
            if hermitian(a, nonisotropic[j]) == 0:
                orth[i][j] = orth[j][i] = True

    vertices = []
    for i, j, k in combinations(range(len(nonisotropic)), 3):
        if orth[i][j] and orth[i][k] and orth[j][k]:
            vertices.append((i, j, k))

    triangles = []
    for tri in vertices:
        pts = set()
        for i, j in combinations(tri, 2):
            pts |= {p for p in line_points(nonisotropic[i], nonisotropic[j]) if p in iso_index}
        check(len(pts) == 15, f"expected isotropic triangle size 15, got {len(pts)}")
        mask = 0
        for p in pts:
            mask |= 1 << iso_index[p]
        triangles.append(mask)

    n = len(vertices)
    adj = [0] * n
    edges = []
    for i in range(n):
        ti = triangles[i]
        for j in range(i + 1, n):
            if bit_count(ti & triangles[j]) == 3:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
                edges.append((i, j))

    q0 = isotropic[0]
    B = []
    for idx, tri in enumerate(vertices):
        if any(hermitian(nonisotropic[i], q0) == 0 for i in tri):
            B.append(idx)
    Bset = set(B)
    C = [i for i in range(n) if i not in Bset]

    Bmask = sum(1 << i for i in B)
    seen_b = set()
    comps = []
    for start in B:
        if start in seen_b:
            continue
        q = deque([start])
        seen_b.add(start)
        comp = []
        while q:
            v = q.popleft()
            comp.append(v)
            nb = adj[v] & Bmask
            while nb:
                lsb = nb & -nb
                w = lsb.bit_length() - 1
                nb ^= lsb
                if w not in seen_b:
                    seen_b.add(w)
                    q.append(w)
        comps.append(sorted(comp))
    comps.sort(key=lambda x: (len(x), x[0]))
    B1, B2, B3 = comps
    b = B1[0]
    NbC = [v for v in C if (adj[b] >> v) & 1]

    return {
        "points": points,
        "isotropic": isotropic,
        "nonisotropic": nonisotropic,
        "vertices": vertices,
        "adj": adj,
        "edges": edges,
        "B": B,
        "B1": B1,
        "B2": B2,
        "B3": B3,
        "C": C,
        "b": b,
        "NbC": NbC,
    }


def induced_edges(edges, vertices):
    local = {v: i for i, v in enumerate(vertices)}
    out = []
    vertex_set = set(vertices)
    for u, v in edges:
        if u in vertex_set and v in vertex_set:
            out.append((local[u], local[v]))
    return out


def write_dimacs(path, vertex_count, edges, comment):
    with path.open("w", encoding="ascii") as f:
        f.write(f"c {comment}\n")
        f.write(f"p edge {vertex_count} {len(edges)}\n")
        for u, v in edges:
            f.write(f"e {u + 1} {v + 1}\n")


def file_sha256(path):
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    data = build_instance()
    CERT_DIR.mkdir(exist_ok=True)

    full = CERT_DIR / "g24_full.dimacs"
    c_graph = CERT_DIR / "g24_C.dimacs"
    nbc_graph = CERT_DIR / "g24_NbC.dimacs"

    write_dimacs(full, len(data["vertices"]), data["edges"], "G_2(4) graph used in the Borsuk 63 construction")
    write_dimacs(c_graph, len(data["C"]), induced_edges(data["edges"], data["C"]), "Induced subgraph on C")
    write_dimacs(nbc_graph, len(data["NbC"]), induced_edges(data["edges"], data["NbC"]), "Induced subgraph on N(b) cap C")

    metadata = {
        "description": "Certificates for the 63-dimensional Borsuk construction",
        "indexing": "All vertex lists are zero-indexed relative to g24_full.dimacs.",
        "graph": {
            "vertices": len(data["vertices"]),
            "edges": len(data["edges"]),
            "strongly_regular_parameters": [416, 100, 36, 20],
        },
        "partition": {
            "B": data["B"],
            "B1": data["B1"],
            "B2": data["B2"],
            "B3": data["B3"],
            "C": data["C"],
            "b": data["b"],
            "NbC": data["NbC"],
        },
        "subgraph_vertex_maps": {
            "g24_C.dimacs": data["C"],
            "g24_NbC.dimacs": data["NbC"],
        },
        "files": {},
    }

    metadata_path = CERT_DIR / "borsuk63_metadata.json"
    for path in [full, c_graph, nbc_graph]:
        metadata["files"][path.name] = {
            "sha256": file_sha256(path),
            "bytes": path.stat().st_size,
        }

    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="ascii")

    for path in [full, c_graph, nbc_graph, metadata_path]:
        print(f"{path.relative_to(ROOT)} {file_sha256(path)}")


if __name__ == "__main__":
    main()
