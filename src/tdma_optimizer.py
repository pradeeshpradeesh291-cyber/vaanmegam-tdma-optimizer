import argparse
import json
import math
import sys
import networkx as nx

def calculate_distance(coord1, coord2):
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def build_topology_graphs(nodes_dict, communication_range=500.0):
    """
    Builds the 1-hop physical graph G1 and 2-hop interference graph G2.
    - G1 edge: Distance <= communication_range (1-hop)
    - G2 edge: Distance-1 OR Distance-2 (Nodes within 2-hops in G1 share an edge in G2)
    """
    G1 = nx.Graph()
    for node, coords in nodes_dict.items():
        G1.add_node(node, pos=coords)
    
    nodes = list(nodes_dict.keys())
    # Add 1-hop edges based on 500m distance threshold
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, v = nodes[i], nodes[j]
            dist = calculate_distance(nodes_dict[u], nodes_dict[v])
            if dist <= communication_range:
                G1.add_edge(u, v)
    
    # Construct Distance-2 Conflict Graph G2
    G2 = nx.Graph()
    G2.add_nodes_from(G1.nodes())
    
    # Distance-1 conflict: Direct links
    for u, v in G1.edges():
        G2.add_edge(u, v)
        
    # Distance-2 conflict: Hidden terminals (nodes sharing a common 1-hop neighbor)
    for node in G1.nodes():
        neighbors = list(G1.neighbors(node))
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                G2.add_edge(neighbors[i], neighbors[j])
                
    return G1, G2

def optimize_tdma_schedule(G2):
    """
    Performs Distance-2 Graph Coloring using Greedy Largest Degree First (LDF) heuristic.
    Minimizes slots while allowing spatial reuse across nodes farther than 2 hops apart.
    """
    # Sort nodes by degree in G2 (descending) to prioritize highly constrained nodes
    sorted_nodes = sorted(G2.nodes(), key=lambda n: G2.degree(n), reverse=True)
    
    node_to_slot = {}
    for node in sorted_nodes:
        # Find slots used by adjacent nodes in the conflict graph G2
        neighbor_slots = {node_to_slot[nbr] for nbr in G2.neighbors(node) if nbr in node_to_slot}
        
        # Assign the smallest available slot (enables spatial reuse)
        slot = 0
        while slot in neighbor_slots:
            slot += 1
        node_to_slot[node] = slot
        
    return node_to_slot

def verify_schedule(G2, node_to_slot):
    """Verifies that no two adjacent nodes in G2 (1-hop or 2-hop) share a slot."""
    for u, v in G2.edges():
        if node_to_slot[u] == node_to_slot[v]:
            return False
    return True

def generate_report(nodes_dict, node_to_slot, comm_range=500.0):
    """Formats and prints the report strictly matching the required CLI output format."""
    sorted_nodes = sorted(nodes_dict.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    total_slots = max(node_to_slot.values()) + 1 if node_to_slot else 0
    
    print("==================================================")
    print("        TDMA TOPOLOGY OPTIMIZATION REPORT         ")
    print("==================================================")
    print(f"Total Nodes Processed : {len(nodes_dict)}")
    print(f"Configured Radio Range: {comm_range} meters")
    print(f"Optimized Frame Length: {total_slots} unique timeslots (Lower is better)")
    print("\nNODE -> SLOT ASSIGNMENTS:")
    for node in sorted_nodes:
        print(f"{node}: Slot {node_to_slot[node]}")
        
    print("==================================================")
    print("STRUCTURAL TDMA SCHEDULE MATRIX (Slot x Node Boolean Matrix):")
    
    node_headers = [f"{int(''.join(filter(str.isdigit, n)) or 0):02d}" for n in sorted_nodes]
    header_str = "Slot \\ Node | " + " | ".join(node_headers)
    print(header_str)
    print("-" * len(header_str))
    
    for slot_idx in range(total_slots):
        row_bits = []
        for node in sorted_nodes:
            row_bits.append("1" if node_to_slot[node] == slot_idx else "0")
        print(f"Slot {slot_idx:02d}    | " + "  | ".join(row_bits))
        
    print("==================================================")
    print("Execution finalized cleanly. Schedule verified conflict-free.")
    print("==================================================")

def main():
    parser = argparse.ArgumentParser(description="Centralized Python TDMA Schedule Optimizer")
    parser.add_argument("json_input", type=str, help="JSON string containing node coordinates")
    args = parser.parse_args()
    
    try:
        nodes_dict = json.loads(args.json_input)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}")
        sys.exit(1)
        
    G1, G2 = build_topology_graphs(nodes_dict, communication_range=500.0)
    node_to_slot = optimize_tdma_schedule(G2)
    
    if not verify_schedule(G2, node_to_slot):
        print("Schedule verification failed! Interference detected.")
        sys.exit(1)
        
    generate_report(nodes_dict, node_to_slot)

if __name__ == "__main__":
    main()
