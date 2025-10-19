import networkx as nx
from itertools import combinations
import numpy as np

def generate_semigroup(generators, max_check=3000):
    S = set()
    frontier = [0]
    while frontier:
        current = frontier.pop(0)
        if current > max_check:
            continue
        if current not in S:
            S.add(current)
            for g in generators:
                frontier.append(current + g)
    return S

def compute_apery_set(S, m):
    apery = {}
    for i in range(m):
        k = i
        while k <= max(S) + m:
            if k in S:
                apery[i] = k
                break
            k += m
    return sorted(apery.values())

def build_apery_graph(apery_set, S):
    G = nx.Graph()
    for a in apery_set:
        G.add_node(a)
    edge_list = []
    for i, j in combinations(apery_set, 2):
        diff = abs(i - j)
        if diff in S:
            G.add_edge(i, j)
            edge_list.append((i, j, diff))
    return G, edge_list

def compute_security_number(G):
    if nx.is_connected(G) and G.number_of_nodes() > 1:
        return nx.node_connectivity(G)
    else:
        return 0  # disconnected graph

def get_layout(G, nodes):
    n = len(nodes)
    if nx.is_tree(G) and nx.is_connected(G) and all(G.degree(v) <= 2 for v in G.nodes):
        pos = {node: (i, 0) for i, node in enumerate(sorted(nodes))}
        return pos
    elif n <= 25:
        return nx.circular_layout(G)
    elif n <= 60:
        return nx.kamada_kawai_layout(G)
    else:
        return nx.spring_layout(G, seed=42)