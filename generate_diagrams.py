import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

# -------------------------------------------------------------
# 1. DIAGRAM: Wireless Interference & Spatial Reuse Dynamics
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 4.5), dpi=300)
ax.set_facecolor("#F8FAFC")
fig.patch.set_facecolor("#F8FAFC")

# Subplot 1: Distance-1 Direct Interference
ax.text(0.15, 0.95, "Distance-1: Direct Link Interference", fontsize=11, fontweight="bold", color="#1E293B", ha="center")
ax.text(0.15, 0.86, "Node A and B within 500m. Transmitting simultaneously\ncauses direct packet collision / receiver blinding.", fontsize=8.5, color="#64748B", ha="center")

circle_a = patches.Circle((0.08, 0.45), 0.045, facecolor="#3B82F6", edgecolor="#1D4ED8", linewidth=2)
circle_b = patches.Circle((0.22, 0.45), 0.045, facecolor="#EF4444", edgecolor="#B91C1C", linewidth=2)
ax.add_patch(circle_a)
ax.add_patch(circle_b)
ax.text(0.08, 0.45, "A", fontsize=11, fontweight="bold", color="white", ha="center", va="center")
ax.text(0.22, 0.45, "B", fontsize=11, fontweight="bold", color="white", ha="center", va="center")
ax.annotate("", xy=(0.20, 0.45), xytext=(0.10, 0.45), arrowprops=dict(arrowstyle="<->", color="#DC2626", lw=2.5))
ax.text(0.15, 0.52, "Direct Link (<= 500m)\nMust have DIFFERENT slots", fontsize=8, color="#DC2626", fontweight="bold", ha="center")
ax.text(0.08, 0.32, "Slot 0", fontsize=9, fontweight="bold", color="#2563EB", ha="center")
ax.text(0.22, 0.32, "Slot 1", fontsize=9, fontweight="bold", color="#DC2626", ha="center")

# Divider line
ax.axvline(x=0.31, color="#CBD5E1", linestyle="--", linewidth=1.2)

# Subplot 2: Distance-2 Hidden Terminal Interference
ax.text(0.50, 0.95, "Distance-2: Hidden Terminal Collision", fontsize=11, fontweight="bold", color="#1E293B", ha="center")
ax.text(0.50, 0.86, "A and C cannot hear each other (>500m), but both\ntalk to common neighbor B. Simultaneous TX collides at B.", fontsize=8.5, color="#64748B", ha="center")

c_a2 = patches.Circle((0.38, 0.45), 0.045, facecolor="#F59E0B", edgecolor="#D97706", linewidth=2)
c_b2 = patches.Circle((0.50, 0.45), 0.045, facecolor="#64748B", edgecolor="#334155", linewidth=2)
c_c2 = patches.Circle((0.62, 0.45), 0.045, facecolor="#8B5CF6", edgecolor="#6D28D9", linewidth=2)
ax.add_patch(c_a2)
ax.add_patch(c_b2)
ax.add_patch(c_c2)
ax.text(0.38, 0.45, "A", fontsize=11, fontweight="bold", color="white", ha="center", va="center")
ax.text(0.50, 0.45, "B (Rx)", fontsize=10, fontweight="bold", color="white", ha="center", va="center")
ax.text(0.62, 0.45, "C", fontsize=11, fontweight="bold", color="white", ha="center", va="center")

ax.annotate("", xy=(0.48, 0.45), xytext=(0.40, 0.45), arrowprops=dict(arrowstyle="->", color="#D97706", lw=2))
ax.annotate("", xy=(0.52, 0.45), xytext=(0.60, 0.45), arrowprops=dict(arrowstyle="->", color="#6D28D9", lw=2))
ax.text(0.50, 0.53, "COLLISION at B!", fontsize=8.5, color="#DC2626", fontweight="bold", ha="center")
ax.text(0.50, 0.38, "Distance-2: Slot(A) != Slot(C)", fontsize=8, color="#B91C1C", fontweight="bold", ha="center")
ax.text(0.38, 0.32, "Slot 2", fontsize=9, fontweight="bold", color="#D97706", ha="center")
ax.text(0.50, 0.32, "Slot 0", fontsize=9, fontweight="bold", color="#475569", ha="center")
ax.text(0.62, 0.32, "Slot 3", fontsize=9, fontweight="bold", color="#7C3AED", ha="center")

# Divider line
ax.axvline(x=0.69, color="#CBD5E1", linestyle="--", linewidth=1.2)

# Subplot 3: Spatial Reuse (> 2 Hops)
ax.text(0.85, 0.95, "Spatial Reuse (> 2 Hops Apart)", fontsize=11, fontweight="bold", color="#1E293B", ha="center")
ax.text(0.85, 0.86, "Nodes separated by >= 3 hops have zero receiver\noverlap. They can concurrently reuse the same slot!", fontsize=8.5, color="#64748B", ha="center")

c_u = patches.Circle((0.74, 0.45), 0.04, facecolor="#10B981", edgecolor="#047857", linewidth=2)
c_r1 = patches.Circle((0.815, 0.45), 0.035, facecolor="#E2E8F0", edgecolor="#94A3B8", linewidth=1.5)
c_r2 = patches.Circle((0.885, 0.45), 0.035, facecolor="#E2E8F0", edgecolor="#94A3B8", linewidth=1.5)
c_v = patches.Circle((0.96, 0.45), 0.04, facecolor="#10B981", edgecolor="#047857", linewidth=2)

ax.add_patch(c_u)
ax.add_patch(c_r1)
ax.add_patch(c_r2)
ax.add_patch(c_v)

ax.text(0.74, 0.45, "A", fontsize=10, fontweight="bold", color="white", ha="center", va="center")
ax.text(0.815, 0.45, "Hop1", fontsize=7.5, color="#475569", ha="center", va="center")
ax.text(0.885, 0.45, "Hop2", fontsize=7.5, color="#475569", ha="center", va="center")
ax.text(0.96, 0.45, "D", fontsize=10, fontweight="bold", color="white", ha="center", va="center")

ax.plot([0.74, 0.815, 0.885, 0.96], [0.45, 0.45, 0.45, 0.45], color="#94A3B8", linestyle=":", zorder=1)

ax.text(0.85, 0.55, "Safe Distance (>= 3 Hops)\nNo receiver interference", fontsize=8, color="#047857", fontweight="bold", ha="center")
ax.text(0.74, 0.32, "Slot 0", fontsize=9, fontweight="bold", color="#059669", ha="center")
ax.text(0.96, 0.32, "Slot 0 (REUSED!)", fontsize=9, fontweight="bold", color="#059669", ha="center")

ax.set_xlim(0, 1.02)
ax.set_ylim(0.2, 1.05)
ax.axis("off")
plt.tight_layout()
plt.savefig("assets/diagram_1_interference.png", bbox_inches="tight", dpi=300)
plt.close()
print("Saved diagram 1")

# -------------------------------------------------------------
# 2. DIAGRAM: Physical Graph G1 vs Scheduled Colors on Grid
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=300)
fig.patch.set_facecolor("#FFFFFF")

# 16-node 4x4 grid coordinates
nodes_coords = {f"Node_{i:02d}": ((i % 4) * 300.0, (3 - (i // 4)) * 300.0) for i in range(16)}

# Compute distance and construct G1
G1 = nx.Graph()
for node, pos in nodes_coords.items():
    G1.add_node(node, pos=pos)

for i in range(16):
    for j in range(i + 1, 16):
        u, v = f"Node_{i:02d}", f"Node_{j:02d}"
        p1, p2 = nodes_coords[u], nodes_coords[v]
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if dist <= 500.0:
            G1.add_edge(u, v)

# Construct G2
G2 = nx.Graph()
G2.add_nodes_from(G1.nodes())
for u, v in G1.edges():
    G2.add_edge(u, v)
for node in G1.nodes():
    nbrs = list(G1.neighbors(node))
    for i in range(len(nbrs)):
        for j in range(i + 1, len(nbrs)):
            G2.add_edge(nbrs[i], nbrs[j])

# Slot assignments from LDF
sorted_nodes = sorted(G2.nodes(), key=lambda n: G2.degree(n), reverse=True)
node_to_slot = {}
for node in sorted_nodes:
    neighbor_slots = {node_to_slot[nbr] for nbr in G2.neighbors(node) if nbr in node_to_slot}
    slot = 0
    while slot in neighbor_slots:
        slot += 1
    node_to_slot[node] = slot

# Palette for 9 slots
slot_colors = [
    "#3B82F6", "#EF4444", "#10B981", "#F59E0B", 
    "#8B5CF6", "#EC4899", "#06B6D4", "#F97316", "#14B8A6"
]

pos = {n: nodes_coords[n] for n in G1.nodes()}

# Left: Physical Topology G1 with transmission circles
ax1.set_title("Physical Network Topology $G_1$ (Range = 500m)", fontsize=13, fontweight="bold", pad=12, color="#0F172A")
for n, p in pos.items():
    # Draw faint transmission range circle for corner node 0
    if n in ["Node_00", "Node_15"]:
        circle = plt.Circle(p, 500, color="#3B82F6", fill=True, alpha=0.08, linestyle="--", linewidth=1.5)
        ax1.add_patch(circle)

nx.draw_networkx_edges(G1, pos, ax=ax1, edge_color="#94A3B8", width=1.8, alpha=0.8)
nx.draw_networkx_nodes(G1, pos, ax=ax1, node_color="#1E293B", node_size=600)
node_labels = {n: n.replace("Node_", "N") for n in G1.nodes()}
nx.draw_networkx_labels(G1, pos, labels=node_labels, ax=ax1, font_color="white", font_size=9, font_weight="bold")

ax1.set_xlim(-150, 1050)
ax1.set_ylim(-150, 1050)
ax1.set_aspect("equal")
ax1.grid(True, linestyle=":", alpha=0.5)
ax1.set_xlabel("X Coordinate (Meters)", fontsize=10, color="#475569")
ax1.set_ylabel("Y Coordinate (Meters)", fontsize=10, color="#475569")

# Right: Optimized Slot Assignments showing Spatial Reuse
ax2.set_title("Optimized TDMA Schedule (9 Slots, Distance-2 Conflict Free)", fontsize=13, fontweight="bold", pad=12, color="#0F172A")
nx.draw_networkx_edges(G1, pos, ax=ax2, edge_color="#CBD5E1", width=1.2, style=":")

node_colors_list = [slot_colors[node_to_slot[n] % len(slot_colors)] for n in G1.nodes()]
nx.draw_networkx_nodes(G1, pos, ax=ax2, node_color=node_colors_list, node_size=750, edgecolors="#1E293B", linewidths=1.5)

slot_labels = {n: f"{n.replace('Node_', 'N')}\nS{node_to_slot[n]}" for n in G1.nodes()}
nx.draw_networkx_labels(G1, pos, labels=slot_labels, ax=ax2, font_color="white", font_size=8, font_weight="bold")

# Annotate spatial reuse on corner nodes
ax2.text(0, 930, "Slot 8 Reuse", fontsize=8.5, fontweight="bold", color="#0D9488", ha="center")
ax2.text(900, 930, "Slot 8 Reuse", fontsize=8.5, fontweight="bold", color="#0D9488", ha="center")
ax2.text(0, -50, "Slot 8 Reuse", fontsize=8.5, fontweight="bold", color="#0D9488", ha="center")
ax2.text(900, -50, "Slot 8 Reuse", fontsize=8.5, fontweight="bold", color="#0D9488", ha="center")

ax2.set_xlim(-150, 1050)
ax2.set_ylim(-150, 1050)
ax2.set_aspect("equal")
ax2.grid(True, linestyle=":", alpha=0.5)
ax2.set_xlabel("X Coordinate (Meters)", fontsize=10, color="#475569")
ax2.set_ylabel("Y Coordinate (Meters)", fontsize=10, color="#475569")

plt.tight_layout()
plt.savefig("assets/diagram_2_graphs.png", bbox_inches="tight", dpi=300)
plt.close()
print("Saved diagram 2")

# -------------------------------------------------------------
# 3. DIAGRAM: TDMA Slot x Node Matrix & Frame Concurrency
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#F8FAFC")

total_slots = max(node_to_slot.values()) + 1
num_nodes = len(nodes_coords)
matrix = np.zeros((total_slots, num_nodes))

sorted_keys = sorted(nodes_coords.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
for j, node in enumerate(sorted_keys):
    matrix[node_to_slot[node], j] = 1

cax = ax.imshow(matrix, cmap="Blues", aspect="auto", vmin=0, vmax=1.2)

# Gridlines
ax.set_xticks(np.arange(-.5, num_nodes, 1), minor=True)
ax.set_yticks(np.arange(-.5, total_slots, 1), minor=True)
ax.grid(which='minor', color='#CBD5E1', linestyle='-', linewidth=1)

ax.set_xticks(range(num_nodes))
ax.set_xticklabels([f"N{i:02d}" for i in range(num_nodes)], fontsize=9, fontweight="bold", color="#1E293B")
ax.set_yticks(range(total_slots))
ax.set_yticklabels([f"Slot {s:02d} (1ms)" for s in range(total_slots)], fontsize=9.5, fontweight="bold", color="#1E293B")

for s in range(total_slots):
    active_nodes = []
    for n_idx in range(num_nodes):
        val = int(matrix[s, n_idx])
        color = "#1E293B" if val == 0 else "#FFFFFF"
        fontweight = "normal" if val == 0 else "bold"
        ax.text(n_idx, s, str(val), ha="center", va="center", color=color, fontsize=10, fontweight=fontweight)
        if val == 1:
            active_nodes.append(f"N{n_idx:02d}")
    # Annotation on the right side showing concurrency
    concurrency = len(active_nodes)
    tag = f"{concurrency}x TX" if concurrency > 1 else "1x TX"
    color_tag = "#059669" if concurrency > 1 else "#64748B"
    ax.text(num_nodes - 0.4 + 0.6, s, f"{tag} : {', '.join(active_nodes)}", va="center", fontsize=8.5, fontweight="bold", color=color_tag)

ax.set_title("Structural TDMA Schedule Matrix: Slot $\\times$ Node Concurrency Breakdown", fontsize=12.5, fontweight="bold", pad=15, color="#0F172A")
ax.set_xlabel("Radio Nodes ($V = 16$)", fontsize=10, fontweight="bold", color="#334155", labelpad=8)
ax.set_ylabel("TDMA Time Slots (Frame Duration: 9ms)", fontsize=10, fontweight="bold", color="#334155", labelpad=8)

plt.tight_layout()
plt.savefig("assets/diagram_3_schedule_matrix.png", bbox_inches="tight", dpi=300)
plt.close()
print("Saved diagram 3")

# -------------------------------------------------------------
# 4. DIAGRAM: End-to-End System Architecture (Part 1 + Part 2)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 5), dpi=300)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#F8FAFC")

# Draw 4 main stages
boxes = [
    ("Stage 1: Coordinates Input", "• JSON Payload\n• 16 Static Radio Nodes\n• X, Y (0-900m grid)", 0.03, 0.20, "#EFF6FF", "#3B82F6"),
    ("Stage 2: Python Brain (Part 1)", "• NetworkX 500m Topology ($G_1$)\n• Conflict Graph $G_2 = G_1^2$\n• Distance-2 LDF Coloring\n• Conflict Verification Engine", 0.27, 0.20, "#EEF2FF", "#6366F1"),
    ("Stage 3: Integration Bridge", "• `emane_bridge.py`\n• Schedule Matrix Ingestion\n• XML Generator (`tdmaschedule`)\n• Structure: 1 frame, 9 slots\n• 1000us slot duration", 0.51, 0.20, "#F0FDF4", "#10B981"),
    ("Stage 4: EMANE Emulator (Part 2)", "• EMANE TDMA Radio Model (BDCE)\n• Multi-NEM Docker Container\n• Hardware-accurate MAC timing\n• Collision-free packet filter\n• Drop/Permit Verification", 0.75, 0.20, "#FEF3C7", "#F59E0B"),
]

for title, desc, x, width, bg_color, border_color in boxes:
    # Outer box
    rect = patches.FancyBboxPatch((x, 0.15), width, 0.70, boxstyle="round,pad=0.03", 
                                  facecolor=bg_color, edgecolor=border_color, linewidth=2)
    ax.add_patch(rect)
    # Header bar
    ax.text(x + width/2, 0.78, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")
    ax.plot([x + 0.01, x + width - 0.01], [0.72, 0.72], color=border_color, linewidth=1.5)
    # Body text
    ax.text(x + 0.015, 0.45, desc, ha="left", va="center", fontsize=8.8, color="#334155", linespacing=1.6)

# Arrows between stages
arrow_coords = [(0.23, 0.50, 0.27, 0.50), (0.47, 0.50, 0.51, 0.50), (0.71, 0.50, 0.75, 0.50)]
for x1, y1, x2, y2 in arrow_coords:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=2.5, mutation_scale=18))

ax.text(0.5, 0.94, "Centralized TDMA Protocol Optimizer & EMANE Emulation Architecture", 
        ha="center", va="center", fontsize=13, fontweight="bold", color="#0F172A")
ax.text(0.5, 0.05, "Vaan Megam Networks | Technical Submission Architecture Flow", 
        ha="center", va="center", fontsize=9.5, color="#64748B", style="italic")

ax.set_xlim(0, 0.98)
ax.set_ylim(0, 1.0)
ax.axis("off")
plt.tight_layout()
plt.savefig("assets/diagram_4_emane_architecture.png", bbox_inches="tight", dpi=300)
plt.close()
print("Saved diagram 4")
