import itertools
import networkx as nx

# ---------- Step 1: Generate Numerical Semigroup ----------
def generate_semigroup(generators, limit=2000):
    S = {0}
    added = True
    while added:
        added = False
        new = set()
        for s in S:
            for g in generators:
                if s + g <= limit:
                    new.add(s + g)
        if not new.issubset(S):
            S |= new
            added = True
    return S

# ---------- Step 2: Compute Apéry Set ----------
def compute_apery_set(S, m):
    apery = []
    for r in range(m):
        val = min(x for x in S if x % m == r)
        apery.append(val)
    return sorted(apery)

# ---------- Step 3: Build Apéry Poset Graph ----------
def build_apery_graph(apery_set, S):
    G = nx.Graph()
    for a in apery_set:
        G.add_node(a)
    edge_list = []
    for i, j in itertools.combinations(apery_set, 2):
        if abs(i - j) in S:
            G.add_edge(i, j)
            edge_list.append((i, j, abs(i - j)))
    return G, edge_list

# ---------- Step 4: Closed Neighborhood ----------
def closed_neighborhood(G, X):
    N = set(X)
    for v in X:
        N.update(G.neighbors(v))
    return N

# ---------- Step 5: Check if a set is Secure ----------
def is_secure_set(G, S_prime):
    for r in range(1, len(S_prime) + 1):
        for subset in itertools.combinations(S_prime, r):
            X = set(subset)
            N_X = closed_neighborhood(G, X)
            defenders = len(N_X & S_prime)
            attackers = len(N_X - S_prime)
            if defenders < attackers:
                return False
    return True

# ---------- Step 6: Compute Security Number ----------
def compute_security_number(G):
    V = list(G.nodes())
    for r in range(1, len(V) + 1):
        for subset in itertools.combinations(V, r):
            S_prime = set(subset)
            if is_secure_set(G, S_prime):
                return r, S_prime
    return None, None

# ---------- Step 7: Layout Function ----------
def get_layout(G, nodes):
    n = len(nodes)
    if n <= 25:
        return nx.circular_layout(G)
    elif n <= 60:
        return nx.kamada_kawai_layout(G)
    else:
        return nx.spring_layout(G, seed=42)