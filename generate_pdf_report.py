import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

os.makedirs("docs", exist_ok=True)
pdf_path = "docs/TDMA_Optimizer_Documentation_VMN.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=0.6 * inch,
    leftMargin=0.6 * inch,
    topMargin=0.6 * inch,
    bottomMargin=0.6 * inch
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    textColor=colors.HexColor("#0F172A")
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#2563EB")
)

meta_style = ParagraphStyle(
    "DocMeta",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#64748B")
)

h1_style = ParagraphStyle(
    "Heading1_Custom",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#0F172A"),
    spaceBefore=12,
    spaceAfter=6
)

h2_style = ParagraphStyle(
    "Heading2_Custom",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#1E293B"),
    spaceBefore=8,
    spaceAfter=4
)

body_style = ParagraphStyle(
    "Body_Custom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor("#334155")
)

bullet_style = ParagraphStyle(
    "Bullet_Custom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#334155"),
    leftIndent=15,
    firstLineIndent=-10
)

code_style = ParagraphStyle(
    "Code_Custom",
    parent=styles["Normal"],
    fontName="Courier",
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor("#0F172A")
)

story = []

# Title Section
story.append(Paragraph("Centralized TDMA Schedule Planner & Optimizer with EMANE Emulation", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("Distance-2 Graph Coloring, Spatial Reuse, and Physical RF Layer Packet Enforcement", subtitle_style))
story.append(Spacer(1, 6))
story.append(Paragraph("<b>Organization:</b> Vaan Megam Networks Private Limited (IITM Pravartak) &nbsp;|&nbsp; <b>Domain:</b> Wireless Protocol Development (5G/SDR/MANET)<br/><b>Candidate:</b> devpradeesh &nbsp;|&nbsp; <b>Submission Date:</b> September 2026 &nbsp;|&nbsp; <b>Evaluation:</b> Full-Time Internship Offer", meta_style))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=2, spaceAfter=10))

# 1. Executive Summary
story.append(Paragraph("1. Executive Summary", h1_style))
story.append(Paragraph(
    "This document details the engineering design process, algorithmic formulation, empirical results, and physical layer emulation for a centralized Time Division Multiple Access (TDMA) schedule optimizer. Operating in tactical shared-spectrum environments (MANET, SDR, 5G Private Networks), the simulator plans conflict-free transmissions while maximizing spatial reuse. The submission satisfies Part 1 (mandatory Python scheduling engine using Distance-2 graph coloring) and Part 2 (EMANE physical emulation architecture and XML event bridge).",
    body_style
))
story.append(Spacer(1, 8))

# 2. Problem Statement & RF Physics
story.append(Paragraph("2. RF Interference Physics & Problem Formulation", h1_style))
story.append(Paragraph(
    "In wireless networks, simultaneous transmissions cause collisions. Our scheduler models and eliminates two distinct collision modes while maximizing spatial reuse:",
    body_style
))
story.append(Spacer(1, 4))
story.append(Paragraph("• <b>Distance-1 Direct Link Interference:</b> Radios within 500m cannot transmit concurrently due to half-duplex radio hardware and receiver blinding. Rule: (u, v) in E1 => Slot(u) != Slot(v).", bullet_style))
story.append(Paragraph("• <b>Distance-2 Hidden Terminal Interference:</b> Two radios out of direct range transmitting to a shared common neighbor cause collision at the receiver. Rule: dist_G1(u, v) <= 2 => Slot(u) != Slot(v).", bullet_style))
story.append(Paragraph("• <b>Spatial Reuse (> 2 Hops):</b> Radios separated by 3 or more hops have zero receiver overlap and can safely reuse identical time slots, multiplying network capacity.", bullet_style))
story.append(Spacer(1, 8))

if os.path.exists("assets/diagram_1_interference.png"):
    story.append(Image("assets/diagram_1_interference.png", width=6.8 * inch, height=2.4 * inch))
    story.append(Spacer(1, 10))

# 3. Mathematical Modeling & Algorithm
story.append(Paragraph("3. Mathematical Modeling & Graph Algorithms (Part 1)", h1_style))
story.append(Paragraph(
    "The physical network of radios is modeled as a Unit Disk Graph G1 = (V, E1) with a 500.0m communication radius. We construct the conflict graph G2 = (V, E2) representing the graph square G1^2. Any Distance-2 conflict in G1 becomes a Distance-1 edge in G2.",
    body_style
))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Optimization Heuristic (Largest Degree First / Welsh-Powell):</b>", h2_style))
story.append(Paragraph(
    "Because graph vertex coloring is NP-Complete, we utilize the Largest Degree First (LDF) heuristic. Radios are sorted by descending degree in G2 (most constrained nodes first). Each node is assigned the lowest non-conflicting integer slot index. This greedy first-fit strategy ensures tightly packed recurring frames in O(|V| log |V| + |E_2|) time (< 2ms execution).",
    body_style
))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Conflict Verification Engine:</b> The verify_schedule() function traverses all edges in G2. If any 1-hop or 2-hop neighbor shares a slot, it aborts execution to protect physical radio hardware.", body_style))
story.append(Spacer(1, 8))

# 4. Experimental Results on 16-Node Grid
story.append(Paragraph("4. Experimental Results: 16-Node Tactical Grid Benchmark", h1_style))
story.append(Paragraph(
    "Evaluating on a 16-node 4x4 grid (300m inter-node spacing, 500m radio range, 42 physical links), the optimizer compresses the required frame from 16 slots down to <b>9 unique timeslots</b> (Spatial Reuse Factor = 1.78x). Slot 8 achieves 4-way concurrent spatial reuse across the four corner nodes (Node_00, Node_03, Node_12, Node_15).",
    body_style
))
story.append(Spacer(1, 6))

if os.path.exists("assets/diagram_2_graphs.png"):
    story.append(Image("assets/diagram_2_graphs.png", width=6.8 * inch, height=3.0 * inch))
    story.append(Spacer(1, 8))

# Concurrency Table
table_data = [
    [Paragraph("<b>Slot Index</b>", body_style), Paragraph("<b>Duration</b>", body_style), Paragraph("<b>Concurrency</b>", body_style), Paragraph("<b>Assigned Transmitting Nodes</b>", body_style)],
    [Paragraph("Slot 00 - 03", body_style), Paragraph("1ms each", body_style), Paragraph("1x TX", body_style), Paragraph("Node_05, Node_06, Node_09, Node_10 (Dense Central Cluster)", body_style)],
    [Paragraph("Slot 04", body_style), Paragraph("1ms", body_style), Paragraph("2x TX", body_style), Paragraph("Node_01, Node_13 (Spatial Reuse, 3 hops apart)", body_style)],
    [Paragraph("Slot 05", body_style), Paragraph("1ms", body_style), Paragraph("2x TX", body_style), Paragraph("Node_02, Node_14 (Spatial Reuse, 3 hops apart)", body_style)],
    [Paragraph("Slot 06", body_style), Paragraph("1ms", body_style), Paragraph("2x TX", body_style), Paragraph("Node_04, Node_07 (Spatial Reuse, 3 hops apart)", body_style)],
    [Paragraph("Slot 07", body_style), Paragraph("1ms", body_style), Paragraph("2x TX", body_style), Paragraph("Node_08, Node_11 (Spatial Reuse, 3 hops apart)", body_style)],
    [Paragraph("Slot 08", body_style), Paragraph("1ms", body_style), Paragraph("<b>4x TX</b>", body_style), Paragraph("<b>Node_00, Node_03, Node_12, Node_15 (4 Grid Corners)</b>", body_style)]
]
t_slots = Table(table_data, colWidths=[1.1 * inch, 0.9 * inch, 1.1 * inch, 3.7 * inch])
t_slots.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t_slots)
story.append(Spacer(1, 10))

# 5. Part 2: EMANE Setup & Integration Bridge
story.append(Paragraph("5. Part 2: Physical Emulator (EMANE Setup) & Integration Bridge", h1_style))
story.append(Paragraph(
    "To emulate physical RF propagation and MAC timing without specialized hardware, we interface the Python optimizer with EMANE (Extendable Mobile Ad-hoc Network Emulator) via <code>emane_bridge.py</code>. The bridge translates the schedule matrix into official <code>tdmascheduleevent.dtd</code> XML event profiles. EMANE instantiates each radio as a Network Emulation Module (NEM), enforcing 1ms slot boundaries and dropping out-of-slot or colliding packets.",
    body_style
))
story.append(Spacer(1, 6))

if os.path.exists("assets/diagram_4_emane_architecture.png"):
    story.append(Image("assets/diagram_4_emane_architecture.png", width=6.8 * inch, height=2.6 * inch))
    story.append(Spacer(1, 10))

# 6. Engineering Decisions & Defense
story.append(Paragraph("6. Architectural Trade-offs & Defense Summary", h1_style))
tradeoff_table = [
    [Paragraph("<b>Decision</b>", body_style), Paragraph("<b>Choice & Rationale</b>", body_style), Paragraph("<b>Tactical / VMN Impact</b>", body_style)],
    [Paragraph("Centralized Control", body_style), Paragraph("Centralized Python scheduler avoids in-band contention and achieves global slot minimization.", body_style), Paragraph("Ideal for UAV/Command airborne master nodes in defense networks.", body_style)],
    [Paragraph("1ms Slot Duration", body_style), Paragraph("1000us slot creates 9ms frame cycle, bounding latency under 9ms.", body_style), Paragraph("Guarantees deterministic jitter for mission-critical voice & telemetry.", body_style)],
    [Paragraph("LDF Greedy Heuristic", body_style), Paragraph("Solves NP-hard problem in <2ms (O(V log V + E)) vs exponential ILP.", body_style), Paragraph("Enables real-time dynamic re-planning on moving tactical platforms.", body_style)]
]
t_tradeoff = Table(tradeoff_table, colWidths=[1.4 * inch, 2.7 * inch, 2.7 * inch])
t_tradeoff.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t_tradeoff)
story.append(Spacer(1, 10))

story.append(Paragraph("<b>Conclusion:</b> All Part 1 and Part 2 constraints, deliverables, and documentation have been completed with rigorous verification, ready for submission and panel defense.", meta_style))

doc.build(story)
print(f"PDF documentation successfully built: {pdf_path}")
