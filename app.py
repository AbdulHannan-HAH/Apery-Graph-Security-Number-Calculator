import matplotlib
matplotlib.use('Agg')  # Prevent tkinter GUI backend errors
from flask import Flask, request, jsonify, send_file, render_template
from io import BytesIO
import matplotlib.pyplot as plt
import networkx as nx
from graph_module import (
    generate_semigroup,
    compute_apery_set,
    build_apery_graph,
    compute_security_number,
    get_layout
)

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    generators = sorted(set(data.get("generators", [])))

    try:
        # Generate semigroup and Apéry set
        S = generate_semigroup(generators)
        m = min(generators)
        apery = compute_apery_set(S, m)
        
        # Build graph
        G, edges = build_apery_graph(apery, S)
        
        # Compute security number using the new algorithm
        security_num, secure_set = compute_security_number(G)

        result = {
            "generators": generators,
            "modulus": m,
            "apery_set": apery,
            "num_nodes": len(apery),
            "num_edges": len(edges),
            "security_number": security_num,
            "secure_set": sorted(secure_set) if secure_set else [],
            "sample_edges": edges[:5] if edges else [],
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/plot", methods=["POST"])
def plot_graph():
    data = request.get_json()
    generators = sorted(set(data.get("generators", [])))

    try:
        # Generate semigroup and Apéry set
        S = generate_semigroup(generators)
        m = min(generators)
        apery = compute_apery_set(S, m)
        
        # Build graph
        G, edges = build_apery_graph(apery, S)
        
        # Compute security number using the new algorithm
        security_num, secure_set = compute_security_number(G)
        
        # Create layout and plot
        pos = get_layout(G, apery)
        
        fig_size = min(8, 6 + len(apery) * 0.1)
        plt.figure(figsize=(fig_size, fig_size))
        
        # Draw all nodes
        nx.draw_networkx_nodes(G, pos,
                             node_color='lightblue',
                             node_size=500,
                             edgecolors='black')
        
        # Highlight secure set nodes if found
        if secure_set:
            nx.draw_networkx_nodes(G, pos, nodelist=list(secure_set),
                                 node_color='lightgreen',
                                 node_size=600,
                                 edgecolors='black',
                                 linewidths=2)
        
        # Draw edges and labels
        nx.draw_networkx_edges(G, pos,
                             edge_color='black', alpha=0.7)
        nx.draw_networkx_labels(G, pos,
                              font_size=8, font_weight='bold')

        title = f"Apéry Graph for S = <{', '.join(map(str, generators))}>\n"
        if security_num is not None:
            title += f"Security Number s(G) = {security_num}"
        else:
            title += "No Secure Set Found"
            
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150)
        plt.close()
        buf.seek(0)

        return send_file(buf, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_msg = data.get("message", "").lower()

    # Comprehensive responses for Security Number
    if any(word in user_msg for word in ["security", "number", "secure set"]):
        response = (
            "Security Number s(G):\n"
            "1. Minimum size of a secure set in the graph\n"
            "2. A set S' where for every subset X ⊆ S', |N[X] ∩ S'| ≥ |N[X] - S'|\n"
            "3. Measures defensive capability against attacks\n"
            "4. Higher security number means better defensive structure\n"
            "5. Computed using exact brute-force search algorithm"
        )
    
    elif any(word in user_msg for word in ["apéry", "apery", "set"]):
        response = (
            "Apéry Set:\n"
            "1. For modulus m, the set {a₀, a₁, ..., a₍m₋₁₎} where aᵢ ≡ i (mod m)\n"
            "2. Each aᵢ is the smallest element in S congruent to i modulo m\n"
            "3. Forms vertices of the Apéry graph\n"
            "4. Uniquely determines the numerical semigroup"
        )
    
    elif any(word in user_msg for word in ["edge", "edges", "rule"]):
        response = (
            "Edge Rule in Apéry Graphs:\n"
            "1. Connect two Apéry elements a and b if |a - b| ∈ S\n"
            "2. Represents distance relationships within the semigroup\n"
            "3. Example: If |4-7|=3 ∈ S, then edge between 4 and 7\n"
            "4. Edge count affects graph connectivity and security properties"
        )
    
    elif any(word in user_msg for word in ["graph", "structure"]):
        response = (
            "Apéry Graph Properties:\n"
            "1. Vertices = Apéry set elements\n"
            "2. Edges = {(a,b) | |a-b| ∈ S}\n"
            "3. Undirected simple graph\n"
            "4. Security number measures defensive capability\n"
            "5. Layout adapts to graph size automatically"
        )
    
    elif any(word in user_msg for word in ["algorithm", "compute", "calculation"]):
        response = (
            "Security Number Algorithm:\n"
            "1. Exact brute-force search through all subsets\n"
            "2. Checks closed neighborhood condition for security\n"
            "3. Searches from smallest to largest set sizes\n"
            "4. Guaranteed to find optimal security number\n"
            "5. Uses closed_neighborhood and is_secure_set functions"
        )
    
    elif any(word in user_msg for word in ["closed neighborhood", "neighborhood"]):
        response = (
            "Closed Neighborhood N[X]:\n"
            "1. For a set X, N[X] = X ∪ {neighbors of all vertices in X}\n"
            "2. Includes the set itself and all adjacent vertices\n"
            "3. Used in security condition: |N[X] ∩ S'| ≥ |N[X] - S'|\n"
            "4. Ensures defenders outnumber attackers in every local region"
        )
    
    elif any(word in user_msg for word in ["secure set", "defense"]):
        response = (
            "Secure Set Properties:\n"
            "1. A set S' where for every X ⊆ S', defenders ≥ attackers in N[X]\n"
            "2. Defenders = vertices in S' within closed neighborhood\n"
            "3. Attackers = vertices not in S' within closed neighborhood\n"
            "4. Provides robust defense against coordinated attacks"
        )
    
    elif any(word in user_msg for word in ["semigroup", "numerical"]):
        response = (
            "Numerical Semigroups:\n"
            "1. Additive submonoids of ℕ with finite complement\n"
            "2. Generated by coprime positive integers\n"
            "3. Apéry sets encode modular structure\n"
            "4. Applications in algebraic geometry and coding theory"
        )
    
    elif any(word in user_msg for word in ["hi", "hello", "how are you"]):
        response = "Hello! I can explain Security Numbers, Apéry graphs, numerical semigroups, and related concepts. What would you like to know?"
    
    elif any(word in user_msg for word in ["generator", "input"]):
        response = (
            "Generator Requirements:\n"
            "1. Positive integers (e.g., 3,5 or 4,7,9)\n"
            "2. Should be coprime for interesting structure\n"
            "3. Modulus = smallest generator\n"
            "4. Typical examples: <3,5>, <4,7>, <5,6,7>"
        )
    
    elif any(word in user_msg for word in ["application", "use", "practical"]):
        response = (
            "Applications of Security Number:\n"
            "1. Network security - optimal guard placement\n"
            "2. Facility protection - strategic defense positions\n"
            "3. Social networks - identifying key influencers\n"
            "4. Military strategy - defensive positioning\n"
            "5. Critical infrastructure protection"
        )
    
    else:
        response = (
            "I can explain these topics:\n"
            "1. Security Number s(G) and secure sets\n"
            "2. Apéry Set definition and properties\n"
            "3. Edge formation rules\n"
            "4. Graph structure and algorithms\n"
            "5. Numerical semigroup theory\n"
            "6. Closed neighborhood concept\n"
            "7. Applications in network defense\n"
            "Ask me anything about security numbers in Apéry graphs!"
        )

    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)