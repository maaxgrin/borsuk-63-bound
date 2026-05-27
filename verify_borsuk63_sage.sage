#!/usr/bin/env sage -python

import hashlib
import json
from pathlib import Path

from sage.all import Graph


ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT / "certificates"
META_PATH = CERT_DIR / "borsuk63_metadata.json"


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_dimacs(path):
    n = None
    edges = []
    with path.open("r", encoding="ascii") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            parts = line.split()
            if parts[0] == "p":
                check(parts[1] == "edge", f"unsupported DIMACS type in {path}")
                n = int(parts[2])
                expected_edges = int(parts[3])
            elif parts[0] == "e":
                u = int(parts[1]) - 1
                v = int(parts[2]) - 1
                edges.append((u, v))
            else:
                raise RuntimeError(f"unknown DIMACS line in {path}: {line}")
    check(n is not None, f"missing p-line in {path}")
    check(len(edges) == expected_edges, f"edge count mismatch in {path}")
    graph = Graph()
    graph.add_vertices(range(n))
    graph.add_edges(edges)
    return graph


def common_neighbors(graph, u, v):
    return len(set(graph.neighbors(u)).intersection(graph.neighbors(v)))


def check_srg_416_100_36_20(graph):
    check(graph.order() == 416, "expected 416 vertices")
    check(graph.size() == 20800, "expected 20800 edges")
    check(set(graph.degree()) == {100}, "expected regular degree 100")

    lambdas = set()
    mus = set()
    vertices = list(graph.vertices(sort=True))
    for i, u in enumerate(vertices):
        for v in vertices[i + 1:]:
            common = common_neighbors(graph, u, v)
            if graph.has_edge(u, v):
                lambdas.add(common)
            else:
                mus.add(common)
    check(lambdas == {36}, f"expected lambda 36, got {sorted(lambdas)}")
    check(mus == {20}, f"expected mu 20, got {sorted(mus)}")


def check_partition_data(graph, meta):
    B1 = meta["partition"]["B1"]
    B2 = meta["partition"]["B2"]
    B3 = meta["partition"]["B3"]
    C = meta["partition"]["C"]
    B = meta["partition"]["B"]
    b = meta["partition"]["b"]
    NbC = meta["partition"]["NbC"]
    blocks = [B1, B2, B3]

    check(len(B) == 96, "expected |B|=96")
    check(len(C) == 320, "expected |C|=320")
    check([len(block) for block in blocks] == [32, 32, 32], "expected three blocks of size 32")
    check(sorted(B) == sorted(B1 + B2 + B3), "B is not the disjoint union of B1,B2,B3")
    check(sorted(B + C) == list(range(416)), "B and C do not partition the vertex set")

    for i, block in enumerate(blocks):
        H = graph.subgraph(block)
        check(H.is_connected(), f"B{i + 1} is not connected")
        check(set(H.degree()) == {20}, f"expected internal degree 20 in B{i + 1}")
        for j, other in enumerate(blocks):
            if i != j:
                cross = [sum(1 for w in other if graph.has_edge(v, w)) for v in block]
                check(set(cross) == {0}, f"expected no edges from B{i + 1} to B{j + 1}")
        to_c = [sum(1 for w in C if graph.has_edge(v, w)) for v in block]
        check(set(to_c) == {80}, f"expected 80 neighbors in C from B{i + 1}")

    for i, block in enumerate(blocks):
        c_to_b = [sum(1 for w in block if graph.has_edge(v, w)) for v in C]
        check(set(c_to_b) == {8}, f"expected 8 neighbors in B{i + 1} from C")
    c_internal = [sum(1 for w in C if graph.has_edge(v, w)) for v in C]
    check(set(c_internal) == {76}, "expected internal degree 76 in C")

    computed_nbc = [v for v in C if graph.has_edge(b, v)]
    check(sorted(computed_nbc) == sorted(NbC), "stored NbC does not match N(b) cap C")


def main():
    meta = json.loads(META_PATH.read_text(encoding="ascii"))
    for name, info in meta["files"].items():
        if name == META_PATH.name:
            continue
        path = CERT_DIR / name
        check(sha256_file(path) == info["sha256"], f"hash mismatch for {name}")

    graph = read_dimacs(CERT_DIR / "g24_full.dimacs")
    graph_c = read_dimacs(CERT_DIR / "g24_C.dimacs")
    graph_nbc = read_dimacs(CERT_DIR / "g24_NbC.dimacs")

    check_srg_416_100_36_20(graph)
    check_partition_data(graph, meta)

    C = meta["partition"]["C"]
    NbC = meta["partition"]["NbC"]
    check(graph.subgraph(C).size() == graph_c.size(), "C subgraph edge count mismatch")
    check(graph.subgraph(NbC).size() == graph_nbc.size(), "NbC subgraph edge count mismatch")

    check(graph.clique_number() == 5, "expected full graph clique number 5")
    check(graph_c.clique_number() <= 5, "unexpected 6-clique in C")
    check(graph_nbc.clique_number() <= 4, "unexpected 5-clique in N(b) cap C")

    print("Sage DIMACS verification passed")


if __name__ == "__main__":
    main()
