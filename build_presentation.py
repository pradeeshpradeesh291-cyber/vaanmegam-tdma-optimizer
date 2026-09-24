import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Ensure directories exist
os.makedirs("presentation", exist_ok=True)
os.makedirs("assets", exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# -------------------------------------------------------------
# Color Palette Constants
# -------------------------------------------------------------
C_DARK_BG       = RGBColor(15, 23, 42)      # #0F172A Slate 900
C_DARK_CARD     = RGBColor(30, 41, 59)      # #1E293B Slate 800
C_DARK_BORDER   = RGBColor(51, 65, 85)      # #334155 Slate 700
C_LIGHT_BG      = RGBColor(248, 250, 252)   # #F8FAFC Slate 50
C_CARD_BG       = RGBColor(255, 255, 255)   # #FFFFFF White
C_CARD_BORDER   = RGBColor(226, 232, 240)   # #E2E8F0 Slate 200
C_TEXT_DARK     = RGBColor(15, 23, 42)      # #0F172A
C_TEXT_MUTED    = RGBColor(100, 116, 139)   # #64748B
C_TEXT_LIGHT    = RGBColor(255, 255, 255)
C_TEXT_LIGHT_MUT= RGBColor(148, 163, 184)   # #94A3B8

C_PRIMARY_BLUE  = RGBColor(37, 99, 235)     # #2563EB Royal Blue
C_ACCENT_SKY    = RGBColor(2, 132, 199)     # #0284C7 Sky Blue
C_ACCENT_GREEN  = RGBColor(16, 185, 129)    # #10B981 Emerald
C_ACCENT_RED    = RGBColor(220, 38, 38)     # #DC2626 Red
C_ACCENT_AMBER  = RGBColor(245, 158, 11)    # #F59E0B Amber
C_ACCENT_PURPLE = RGBColor(124, 58, 237)    # #7C3AED Purple

TOTAL_SLIDES = 13

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
def set_slide_background(slide, color):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, badge_text, title_text, subtitle_text, dark=False):
    # Badge (Pill)
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(2.8), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(30, 58, 138) if dark else RGBColor(239, 246, 255)
    badge.line.color.rgb = RGBColor(96, 165, 250) if dark else RGBColor(191, 219, 254)
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.margin_top = Inches(0.04)
    p_b = tf_b.paragraphs[0]
    p_b.text = badge_text.upper()
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(147, 197, 253) if dark else C_PRIMARY_BLUE

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.7), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_LIGHT if dark else C_TEXT_DARK

    # Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.32), Inches(11.7), Inches(0.38))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = C_TEXT_LIGHT_MUT if dark else C_TEXT_MUTED

def add_footer(slide, current_idx, total_slides, dark=False):
    # Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(51, 65, 85) if dark else RGBColor(226, 232, 240)
    line.line.fill.background()

    # Footer Text
    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.06), Inches(9.0), Inches(0.3))
    tf_f = f_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Vaan Megam Networks | TDMA Schedule Planner & Optimizer | Wireless Protocol Development"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = C_TEXT_LIGHT_MUT if dark else C_TEXT_MUTED

    # Page Number
    p_box = slide.shapes.add_textbox(Inches(10.533), Inches(7.06), Inches(2.0), Inches(0.3))
    tf_p = p_box.text_frame
    p_p = tf_p.paragraphs[0]
    p_p.alignment = PP_ALIGN.RIGHT
    p_p.text = f"{current_idx} / {total_slides}"
    p_p.font.size = Pt(9)
    p_p.font.bold = True
    p_p.font.color.rgb = C_TEXT_LIGHT_MUT if dark else C_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_speaker_notes(slide, notes):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes

# =============================================================================
# SLIDE 1: TITLE SLIDE (Dark Elegance)
# =============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, C_DARK_BG)

# Organization Badge
badge1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(4.2), Inches(0.4))
badge1.fill.solid()
badge1.fill.fore_color.rgb = RGBColor(30, 58, 138)
badge1.line.color.rgb = RGBColor(96, 165, 250)
badge1.line.width = Pt(1.2)
tf_b1 = badge1.text_frame
p_b1 = tf_b1.paragraphs[0]
p_b1.text = "VAAN MEGAM NETWORKS  |  IITM PRAVARTAK"
p_b1.font.size = Pt(10)
p_b1.font.bold = True
p_b1.font.color.rgb = RGBColor(191, 219, 254)

# Main Title Box
t1_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.2))
tf1 = t1_box.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "Centralized TDMA Schedule Planner\n& Optimizer with EMANE Emulation"
p1.font.size = Pt(36)
p1.font.bold = True
p1.font.color.rgb = C_TEXT_LIGHT
p1.line_spacing = 1.15

p2 = tf1.add_paragraph()
p2.space_before = Pt(16)
p2.text = "Distance-2 Graph Coloring, Spatial Reuse Optimization, and Physical Layer Packet Enforcement for Tactical SDR & MANET Networks"
p2.font.size = Pt(14)
p2.font.color.rgb = RGBColor(147, 197, 253)

# Highlight Cards at Bottom
card_data_s1 = [
    ("Focus Domain", "Wireless Protocol Development\n5G Private Networks & SDR", C_PRIMARY_BLUE),
    ("Part 1: The Brain", "Python Distance-2 Graph Engine\nLargest Degree First Heuristic", C_ACCENT_GREEN),
    ("Part 2: The Emulator", "EMANE TDMA BDCE Integration\nAutomated XML Bridge Generation", C_ACCENT_AMBER)
]

for idx, (head, sub, clr) in enumerate(card_data_s1):
    c = add_card(s1, Inches(0.8 + idx * 4.0), Inches(4.2), Inches(3.7), Inches(1.8), bg_color=C_DARK_CARD, border_color=clr, border_width=1.5)
    tf_c = c.text_frame
    tf_c.margin_left = Inches(0.25)
    tf_c.margin_top = Inches(0.25)
    p_h = tf_c.paragraphs[0]
    p_h.text = head.upper()
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = clr
    p_s = tf_c.add_paragraph()
    p_s.space_before = Pt(8)
    p_s.text = sub
    p_s.font.size = Pt(11.5)
    p_s.font.color.rgb = C_TEXT_LIGHT_MUT

# Candidate Meta Line
meta_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.5))
tf_m = meta_box.text_frame
p_m = tf_m.paragraphs[0]
p_m.text = "Candidate: devpradeesh  |  Submission: Full-Time 6-Month Wireless Protocol Development Internship  |  Date: September 2026"
p_m.font.size = Pt(10.5)
p_m.font.color.rgb = C_TEXT_LIGHT_MUT

add_speaker_notes(s1, 
    "Good morning/afternoon respected evaluation panel members. "
    "Today, I am excited to present my complete solution for the Wireless Protocol Development Internship at Vaan Megam Networks. "
    "In this project, I have designed and implemented a centralized TDMA Schedule Planner & Optimizer. "
    "Part 1 develops the mathematical Brain using NetworkX to construct Distance-2 conflict graphs and solve collision-free time-slot assignment with aggressive spatial reuse using a greedy Largest Degree First heuristic. "
    "Part 2 implements the integration bridge for EMANE (Extendable Mobile Ad-hoc Network Emulator), translating the optimized schedule into native XML event profiles for physical layer enforcement. "
    "Over the next few slides, I will walk you through the RF interference physics, graph transformations, algorithm complexity, empirical results on the 16-node grid, and the EMANE emulation architecture."
)

# =============================================================================
# SLIDE 2: EXECUTIVE SUMMARY & ARCHITECTURE OVERVIEW (Light Theme)
# =============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, C_LIGHT_BG)
add_header(s2, "Executive Summary", "System Architecture: Mathematical Brain & Physical Emulator", "A closed-loop protocol optimization architecture bridging algorithmic graph theory with physical RF emulation.")
add_footer(s2, 2, TOTAL_SLIDES)

# Left Card: Part 1 The Brain
c_brain = add_card(s2, Inches(0.8), Inches(1.85), Inches(5.7), Inches(3.6), bg_color=C_CARD_BG, border_color=C_PRIMARY_BLUE, border_width=1.5)
tf_b = c_brain.text_frame
tf_b.margin_left = Inches(0.3)
tf_b.margin_right = Inches(0.3)
tf_b.margin_top = Inches(0.3)
p = tf_b.paragraphs[0]
p.text = "Part 1: The Network Brain (Python Engine)"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_PRIMARY_BLUE

bullets_b = [
    ("Mathematical Topology Formulation: ", "Models 16 SDR radio nodes using Euclidean distance <= 500m on NetworkX to build physical graph G1."),
    ("Distance-2 Conflict Graph (G2 = G1^2): ", "Explicitly models direct link collisions (1-hop) and hidden terminal receiver collisions (2-hop)."),
    ("LDF Greedy Heuristic: ", "Sorts nodes by conflict degree; assigns minimum valid slot index to minimize recurring frame duration."),
    ("Spatial Reuse Guarantee: ", "Enables nodes separated by >= 3 hops to safely transmit simultaneously on identical slots."),
    ("Verification Engine: ", "Performs exhaustive pairwise conflict verification across all conflict edges to ensure 100% collision-free schedules.")
]
for lead, body in bullets_b:
    p_b = tf_b.add_paragraph()
    p_b.space_before = Pt(6)
    r1 = p_b.add_run()
    r1.text = "• " + lead
    r1.font.bold = True
    r1.font.size = Pt(9.8)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_b.add_run()
    r2.text = body
    r2.font.size = Pt(9.8)
    r2.font.color.rgb = C_TEXT_MUTED

# Right Card: Part 2 The Emulator
c_emane = add_card(s2, Inches(6.8), Inches(1.85), Inches(5.7), Inches(3.6), bg_color=C_CARD_BG, border_color=C_ACCENT_AMBER, border_width=1.5)
tf_e = c_emane.text_frame
tf_e.margin_left = Inches(0.3)
tf_e.margin_right = Inches(0.3)
tf_e.margin_top = Inches(0.3)
p = tf_e.paragraphs[0]
p.text = "Part 2: The Physical Emulator (EMANE Setup)"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_ACCENT_AMBER

bullets_e = [
    ("EMANE TDMA Radio Model (BDCE): ", "Leverages EMANE's Basic Discrete Collision Event model for hardware-accurate MAC/PHY layer timing."),
    ("Automated Bridge (emane_bridge.py): ", "Parses the Brain's optimized Slot-Node schedule and compiles native tdmaschedule XML event documents."),
    ("Synchronized 1ms Slot Timing: ", "Configures 1000us time slots, frequency channels, and explicit <tx>/<rx> windows per Network Emulation Module (NEM)."),
    ("Deterministic Packet Control: ", "EMANE's OTA simulation engine drops packets that collide or violate schedule boundaries while forwarding valid transmissions."),
    ("Dockerized Emulation Architecture: ", "Supports isolated multi-node emulation in Linux network namespaces without specialized physical SDR hardware.")
]
for lead, body in bullets_e:
    p_e = tf_e.add_paragraph()
    p_e.space_before = Pt(6)
    r1 = p_e.add_run()
    r1.text = "• " + lead
    r1.font.bold = True
    r1.font.size = Pt(9.8)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_e.add_run()
    r2.text = body
    r2.font.size = Pt(9.8)
    r2.font.color.rgb = C_TEXT_MUTED

# 4 Metrics Callout Cards
metrics = [
    ("100% Conflict-Free", "Zero Collisions Verified", C_ACCENT_GREEN),
    ("9 Unique Slots", "Minimized Frame Length", C_PRIMARY_BLUE),
    ("Up to 4x Concurrency", "Aggressive Spatial Reuse", C_ACCENT_PURPLE),
    ("End-to-End Pipeline", "JSON -> Schedule -> XML", C_ACCENT_SKY)
]

for idx, (m_val, m_lbl, m_col) in enumerate(metrics):
    mc = add_card(s2, Inches(0.8 + idx * 2.98), Inches(5.65), Inches(2.78), Inches(1.15), bg_color=C_CARD_BG, border_color=C_CARD_BORDER)
    tf_mc = mc.text_frame
    tf_mc.margin_top = Inches(0.18)
    p_v = tf_mc.paragraphs[0]
    p_v.alignment = PP_ALIGN.CENTER
    p_v.text = m_val
    p_v.font.size = Pt(15)
    p_v.font.bold = True
    p_v.font.color.rgb = m_col
    p_l = tf_mc.add_paragraph()
    p_l.alignment = PP_ALIGN.CENTER
    p_l.space_before = Pt(3)
    p_l.text = m_lbl
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = C_TEXT_MUTED

add_speaker_notes(s2,
    "On Slide 2, we see the holistic system architecture. "
    "The solution is separated into two high-performance tiers: "
    "The Network Brain takes JSON coordinates, builds the 1-hop physical graph G1 for 500m range, elevates it into a 2-hop conflict graph G2, and applies Largest Degree First greedy graph coloring. "
    "The verifier ensures zero collisions across all 1-hop and 2-hop edges. "
    "Tier 2 takes this schedule and translates it into an EMANE XML profile with 1ms slots, configuring <tx> and <rx> permissions per NEM. "
    "In our 16-node dense grid benchmark, we achieve 100% collision avoidance, an optimal 9-slot frame, and up to 4 simultaneous concurrent transmissions."
)

# =============================================================================
# SLIDE 3: WIRELESS INTERFERENCE DYNAMICS & PROBLEM STATEMENT
# =============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, C_LIGHT_BG)
add_header(s3, "Problem Statement", "RF Interference Physics: Distance-1 vs. Distance-2 Collisions", "Understanding half-duplex radio constraints, receiver blinding, and the hidden terminal dilemma.")
add_footer(s3, 3, TOTAL_SLIDES)

# Diagram Image on Left
if os.path.exists("assets/diagram_1_interference.png"):
    s3.shapes.add_picture("assets/diagram_1_interference.png", Inches(0.8), Inches(1.85), width=Inches(11.733))

# Three explanation cards below diagram
cards_s3 = [
    ("Distance-1: Direct Link Interference", 
     "• Physical Constraint: Radios within 500m of each other.\n"
     "• Failure Mode: Half-duplex SDRs cannot transmit and receive simultaneously on the same channel.\n"
     "• Graph Condition: (u, v) in E1 => Slot(u) != Slot(v).\n"
     "• Impact: Node A transmits; local receiver at B is saturated/blinded.",
     C_PRIMARY_BLUE),
    ("Distance-2: Hidden Terminal Collision",
     "• Physical Constraint: Radios A and C are >500m apart, sharing common neighbor B.\n"
     "• Failure Mode: A and C cannot carrier-sense each other; both transmit to B at the same time.\n"
     "• Graph Condition: dist_G1(u, v) <= 2 => Slot(u) != Slot(v).\n"
     "• Impact: Signals collide destructively at B; packet corrupted.",
     C_ACCENT_RED),
    ("Spatial Reuse Principle (> 2 Hops)",
     "• Physical Constraint: Radios separated by >= 3 hops (dist_G1(u, v) >= 3).\n"
     "• Opportunity: No common 1-hop neighbor exists to suffer receiver interference.\n"
     "• Benefit: Radios can concurrently transmit on the exact same time slot.\n"
     "• Impact: Multiplies aggregate network throughput without RF collisions.",
     C_ACCENT_GREEN)
]

for idx, (t, body, col) in enumerate(cards_s3):
    c = add_card(s3, Inches(0.8 + idx * 4.0), Inches(4.7), Inches(3.733), Inches(2.1), bg_color=C_CARD_BG, border_color=col, border_width=1.5)
    tf = c.text_frame
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = t
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = col
    p_b = tf.add_paragraph()
    p_b.space_before = Pt(6)
    p_b.text = body
    p_b.font.size = Pt(9)
    p_b.font.color.rgb = C_TEXT_DARK
    p_b.line_spacing = 1.3

add_speaker_notes(s3,
    "Slide 3 breaks down the wireless interference physics that govern tactical ad-hoc networks. "
    "In wireless TDMA, we face two fundamental collision modes: "
    "First, Direct Link Interference (Distance-1): If Node A and Node B are connected by an edge in G1 (within 500m), they cannot use the same slot due to half-duplex hardware constraints. "
    "Second, the Hidden Terminal Collision (Distance-2): If Node A and Node C both transmit to Node B, they are out of range of each other, but their RF energy collides at Node B, destroying both frames. "
    "Therefore, any two nodes sharing a common neighbor must also have distinct time slots! "
    "However, if two nodes are separated by 3 hops or more, there is zero receiver overlap. "
    "They can safely reuse the same slot—this is the foundational mechanism of Spatial Reuse."
)

# =============================================================================
# SLIDE 4: MATHEMATICAL MODELING & GRAPH FORMULATION
# =============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, C_LIGHT_BG)
add_header(s4, "Mathematical Modeling", "Graph Theory: Transforming Physical Topology to Conflict Graph", "Reducing wireless two-hop collision avoidance to standard vertex coloring on G2 = G1^2.")
add_footer(s4, 4, TOTAL_SLIDES)

# 3 Column Cards
cols_s4 = [
    ("1. Physical Topology Graph G1",
     "Unit Disk Graph (UDG) Formulation",
     "• Vertices: V = {Node_01, ..., Node_16}, where each node has 2D Cartesian coordinates (x_i, y_i).\n\n"
     "• Euclidean Distance Metric:\n"
     "  d(u, v) = sqrt((x_u - x_v)^2 + (y_u - y_v)^2)\n\n"
     "• Physical Edge Set E1:\n"
     "  E1 = {(u, v) in V x V | u != v, d(u, v) <= 500.0m}\n\n"
     "• Captures direct wireless propagation limits. If two radios are within 500m line-of-sight, they form an edge in G1.",
     C_PRIMARY_BLUE),
    ("2. Interference Conflict Graph G2",
     "Graph Power Formulation (G2 = G1^2)",
     "• Vertices: Same vertex set V as G1.\n\n"
     "• Conflict Edge Set E2:\n"
     "  E2 = E1 U {(u, v) | exists w in V : (u, w) in E1 and (w, v) in E1}\n\n"
     "• Graph Power Equivalence:\n"
     "  G2 is mathematically identical to G1^2 (the square of G1), where an edge connects all nodes at distance <= 2.\n\n"
     "• Direct link collisions (Distance-1) and hidden terminals (Distance-2) are now unified into standard edge conflicts.",
     C_ACCENT_PURPLE),
    ("3. Algorithmic Reduction",
     "Distance-2 to Standard Coloring",
     "• Distance-2 Coloring on G1 is formally equivalent to Distance-1 (Standard Proper Vertex Coloring) on G2:\n"
     "  ProperColoring(G2): c(u) != c(v) for all (u, v) in E2\n\n"
     "• Objective Function:\n"
     "  Minimize Chi(G2) (Total Unique Slots)\n"
     "  subject to: Slot(u) != Slot(v) for all (u, v) in E2\n\n"
     "• Spatial Reuse Theorem:\n"
     "  Slot(u) = Slot(v) <=> (u, v) not in E2 <=> dist_G1(u, v) >= 3.",
     C_ACCENT_GREEN)
]

for idx, (t, sub, body, col) in enumerate(cols_s4):
    c = add_card(s4, Inches(0.8 + idx * 4.0), Inches(1.85), Inches(3.733), Inches(4.95), bg_color=C_CARD_BG, border_color=col, border_width=1.5)
    tf = c.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = t
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = col
    p_s = tf.add_paragraph()
    p_s.space_before = Pt(3)
    p_s.text = sub
    p_s.font.size = Pt(9.5)
    p_s.font.color.rgb = C_TEXT_MUTED
    p_b = tf.add_paragraph()
    p_b.space_before = Pt(12)
    p_b.text = body
    p_b.font.size = Pt(9.5)
    p_b.font.color.rgb = C_TEXT_DARK
    p_b.line_spacing = 1.3

add_speaker_notes(s4,
    "On Slide 4, we examine the mathematical reduction that powers our algorithm. "
    "We model the radio nodes as a Unit Disk Graph G1 where edges exist if Euclidean distance is within 500m. "
    "Then, we construct the conflict graph G2, which is mathematically the square of G1: G2 = G1^2. "
    "In G2, an edge exists between two nodes if and only if they are within 2 hops in G1. "
    "This elegant reduction allows us to convert the complex two-hop wireless scheduling constraint into a standard, well-studied vertex coloring problem on G2! "
    "Any proper coloring on G2 guarantees both 1-hop and 2-hop collision freedom, and automatically permits spatial reuse for any node pair not connected in G2."
)

# =============================================================================
# SLIDE 5: OPTIMIZATION ALGORITHM: LDF GRAPH COLORING
# =============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, C_LIGHT_BG)
add_header(s5, "Optimization Algorithm", "Greedy Largest Degree First (LDF / Welsh-Powell) Heuristic", "Heuristic slot minimization guaranteeing NP-hard conflict resolution in O(V log V + E) time.")
add_footer(s5, 5, TOTAL_SLIDES)

# Left Column: Problem Complexity & Algorithm Steps
c_alg = add_card(s5, Inches(0.8), Inches(1.85), Inches(6.8), Inches(4.95), bg_color=C_CARD_BG, border_color=C_PRIMARY_BLUE, border_width=1.5)
tf_a = c_alg.text_frame
tf_a.margin_left = Inches(0.3)
tf_a.margin_right = Inches(0.3)
tf_a.margin_top = Inches(0.25)
p = tf_a.paragraphs[0]
p.text = "Algorithmic Architecture: Largest Degree First (LDF)"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_PRIMARY_BLUE

steps = [
    ("Computational Complexity Reality: ", "Finding the optimal chromatic number Chi(G2) is NP-Complete (Garey & Johnson). An exhaustive combinatorial search requires O(S^|V|) evaluations, which is unacceptable for real-time tactical SDR protocols."),
    ("Step 1: Conflict Degree Calculation: ", "For every node v in G2, calculate its interference degree deg_G2(v) = |N_G2(v)|. Nodes with the highest degree possess the tightest scheduling constraints."),
    ("Step 2: Descending Degree Priority Ordering: ", "Sort nodes descending by degree: deg_G2(v1) >= deg_G2(v2) >= ... >= deg_G2(vn). This ensures bottleneck hubs are scheduled first."),
    ("Step 3: Greedy First-Fit Slot Assignment: ", "For each node v, inspect slots allocated to its neighbors in G2. Assign the smallest available slot index: Slot(v) = min(N_0 \\ {Slot(w) : w in N_G2(v)})."),
    ("Why LDF Outperforms Random Greedy: ", "Scheduling high-degree nodes first prevents them from fragmenting slot allocations late in the process, naturally enabling peripheral low-degree nodes to reuse early slots.")
]
for lead, body in steps:
    p_s = tf_a.add_paragraph()
    p_s.space_before = Pt(8)
    r1 = p_s.add_run()
    r1.text = lead
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_s.add_run()
    r2.text = body
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_TEXT_MUTED

# Right Column: Code Snippet & Complexity Card
c_code = add_card(s5, Inches(7.8), Inches(1.85), Inches(4.733), Inches(4.95), bg_color=C_DARK_CARD, border_color=C_DARK_BORDER)
tf_c = c_code.text_frame
tf_c.margin_left = Inches(0.25)
tf_c.margin_right = Inches(0.25)
tf_c.margin_top = Inches(0.25)
p_ch = tf_c.paragraphs[0]
p_ch.text = "Python Engine Implementation (src/tdma_optimizer.py)"
p_ch.font.size = Pt(10)
p_ch.font.bold = True
p_ch.font.color.rgb = RGBColor(147, 197, 253)

code_text = (
    "# 1. Priority sort by degree in G2 (descending)\n"
    "sorted_nodes = sorted(\n"
    "    G2.nodes(),\n"
    "    key=lambda n: G2.degree(n),\n"
    "    reverse=True\n"
    ")\n\n"
    "node_to_slot = {}\n"
    "for node in sorted_nodes:\n"
    "    # Identify forbidden neighbor slots in G2\n"
    "    neighbor_slots = {\n"
    "        node_to_slot[nbr]\n"
    "        for nbr in G2.neighbors(node)\n"
    "        if nbr in node_to_slot\n"
    "    }\n"
    "    # Assign smallest available slot (First-Fit)\n"
    "    slot = 0\n"
    "    while slot in neighbor_slots:\n"
    "        slot += 1\n"
    "    node_to_slot[node] = slot\n\n"
    "# Complexity Analysis:\n"
    "# • Degree Sorting: O(|V| log |V|)\n"
    "# • Neighbor Traversal: O(|E_2|)\n"
    "# • Total Time: O(|V| log |V| + |E_2|) -> < 2ms!"
)
p_cb = tf_c.add_paragraph()
p_cb.space_before = Pt(8)
p_cb.text = code_text
p_cb.font.size = Pt(8.5)
p_cb.font.name = "Consolas"
p_cb.font.color.rgb = RGBColor(226, 232, 240)

add_speaker_notes(s5,
    "Slide 5 details the core optimization heuristic. "
    "Since finding the minimal chromatic number is NP-hard, an exact solver like Integer Linear Programming scales exponentially and would freeze a tactical radio in the field. "
    "Instead, we apply the Welsh-Powell / Largest Degree First (LDF) heuristic. "
    "We compute the degree of each node in the conflict graph G2 and sort them in descending order. "
    "The node with the most 2-hop constraints is colored first. "
    "For each subsequent node, we perform a greedy first-fit lookup, choosing the lowest integer slot index not used by its conflict neighbors. "
    "This heuristic executes in under 2 milliseconds and packs slots tightly, maximizing spatial reuse."
)

# =============================================================================
# SLIDE 6: SPATIAL REUSE & MATHEMATICAL VERIFICATION ENGINE
# =============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, C_LIGHT_BG)
add_header(s6, "Verification & Metrics", "Spatial Reuse Quantification & Conflict Verification Engine", "Validating conflict-free correctness with zero regressions and measuring spectral gain.")
add_footer(s6, 6, TOTAL_SLIDES)

# Left Card: Spatial Reuse Breakdown
c_sr = add_card(s6, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.95), bg_color=C_CARD_BG, border_color=C_ACCENT_GREEN, border_width=1.5)
tf_sr = c_sr.text_frame
tf_sr.margin_left = Inches(0.3)
tf_sr.margin_right = Inches(0.3)
tf_sr.margin_top = Inches(0.25)
p = tf_sr.paragraphs[0]
p.text = "Spatial Reuse Metric & Throughput Gain"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_ACCENT_GREEN

sr_bullets = [
    ("Theoretical Upper Bound: ", "Without spatial reuse, 16 nodes require 16 dedicated orthogonal time slots (Frame Length = 16ms)."),
    ("Optimized Frame Length: ", "Our LDF heuristic compresses the 16-node schedule into just 9 unique time slots (Frame Length = 9ms)."),
    ("Spatial Reuse Factor (S_R): ", "S_R = |V| / S_total = 16 / 9 = 1.78x aggregate capacity improvement across the network."),
    ("Quad-Node Concurrency in Slot 8: ", "Nodes N00, N03, N12, and N15 concurrently transmit on Slot 8. Because they occupy the four corners of the grid, their mutual distance exceeds 2 hops (>= 900m), causing ZERO receiver interference."),
    ("Dual-Node Concurrency in Slots 4-7: ", "Slots 4, 5, 6, and 7 each support 2 concurrent transmissions, boosting spectral efficiency across tactical sub-clusters.")
]
for lead, body in sr_bullets:
    p_s = tf_sr.add_paragraph()
    p_s.space_before = Pt(8)
    r1 = p_s.add_run()
    r1.text = lead
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_s.add_run()
    r2.text = body
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_TEXT_MUTED

# Right Card: Conflict Verification Proof
c_ver = add_card(s6, Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.95), bg_color=C_CARD_BG, border_color=C_PRIMARY_BLUE, border_width=1.5)
tf_v = c_ver.text_frame
tf_v.margin_left = Inches(0.3)
tf_v.margin_right = Inches(0.3)
tf_v.margin_top = Inches(0.25)
p = tf_v.paragraphs[0]
p.text = "Mathematical Conflict Verification Engine"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_PRIMARY_BLUE

ver_bullets = [
    ("Automated Quality Gate: ", "Implemented verify_schedule(G2, node_to_slot) as a mandatory gatekeeper before output generation or EMANE export."),
    ("Rigorous Exhaustive Edge Proof: ", "Iterates across all edges (u, v) in E2. If node_to_slot[u] == node_to_slot[v], immediately raises violation."),
    ("Comprehensive Edge Coverage: ", "Because E2 includes all 1-hop links and all 2-hop paths, a pass confirms 0 direct collisions and 0 hidden terminal collisions."),
    ("Zero-Tolerance Exit: ", "If verification fails, CLI terminates cleanly with exit code 1 to protect physical SDR hardware from destructive transmissions."),
    ("Benchmark Result: ", "PASSED: 'Execution finalized cleanly. Schedule verified conflict-free.'")
]
for lead, body in ver_bullets:
    p_s = tf_v.add_paragraph()
    p_s.space_before = Pt(8)
    r1 = p_s.add_run()
    r1.text = lead
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_s.add_run()
    r2.text = body
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_TEXT_MUTED

add_speaker_notes(s6,
    "On Slide 6, we demonstrate proof of correctness and quantify spatial reuse. "
    "In a classical non-reused TDMA network, 16 nodes would take 16 time slots. "
    "Our optimizer packs this into 9 slots, giving an immediate 1.78x boost in aggregate network throughput. "
    "Crucially, Slot 8 achieves 4-way concurrent transmission across the four corner nodes of the deployment. "
    "Furthermore, we built a formal verification engine in verify_schedule(). "
    "It exhaustively checks every single edge in the conflict graph G2. "
    "If even one pair of radios in 1-hop or 2-hop proximity shared a slot, it would fail immediately. "
    "The verification passes 100%, proving mathematical correctness."
)

# =============================================================================
# SLIDE 7: EXPERIMENTAL EVALUATION: 16-NODE BENCHMARK TOPOLOGY
# =============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, C_LIGHT_BG)
add_header(s7, "Experimental Results", "16-Node Benchmark: Physical Topology vs. TDMA Slot Assignments", "Visual demonstration of 4x4 tactical mesh layout (500m radio range) and Distance-2 color distribution.")
add_footer(s7, 7, TOTAL_SLIDES)

# Embed Diagram 2 (G1 vs G2 scheduled)
if os.path.exists("assets/diagram_2_graphs.png"):
    s7.shapes.add_picture("assets/diagram_2_graphs.png", Inches(0.8), Inches(1.85), width=Inches(8.2))

# Right summary card
c_grid = add_card(s7, Inches(9.2), Inches(1.85), Inches(3.333), Inches(4.95), bg_color=C_CARD_BG, border_color=C_PRIMARY_BLUE, border_width=1.5)
tf_g = c_grid.text_frame
tf_g.margin_left = Inches(0.2)
tf_g.margin_right = Inches(0.2)
tf_g.margin_top = Inches(0.25)
p = tf_g.paragraphs[0]
p.text = "Benchmark Topology Specs"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_PRIMARY_BLUE

specs = [
    ("Grid Geometry: ", "4x4 regular grid over 900m x 900m tactical zone."),
    ("Node Spacing: ", "300m horizontal and vertical separation."),
    ("Link Reachability: ", "Adjacent: 300m <= 500m (Valid link)\nDiagonal: sqrt(300^2+300^2) = 424.3m <= 500m (Valid link)"),
    ("Total Physical Links: ", "42 bidirectional 1-hop edges in G1."),
    ("Optimized Slots: ", "9 unique time slots (0 to 8)."),
    ("Spatial Reuse Highlight: ", "Slot 8 shared by N00, N03, N12, N15 (all 4 corners).\nSlots 4, 5, 6, 7 shared by 2 nodes each.")
]
for lead, body in specs:
    p_s = tf_g.add_paragraph()
    p_s.space_before = Pt(6)
    r1 = p_s.add_run()
    r1.text = lead
    r1.font.bold = True
    r1.font.size = Pt(9)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_s.add_run()
    r2.text = body
    r2.font.size = Pt(9)
    r2.font.color.rgb = C_TEXT_MUTED

add_speaker_notes(s7,
    "Slide 7 shows the empirical results on the standard 16-node grid deployment specified in the problem statement. "
    "Nodes are positioned in a 4x4 grid with 300-meter spacing. "
    "At a 500m radio range, radios can communicate with horizontal, vertical, and diagonal neighbors. "
    "On the left, you see the physical network topology G1 with the transmission range circle illustrated. "
    "On the right, you see the nodes colored by their optimized TDMA time slots. "
    "Notice how the corner nodes—N00 at (0,0), N03 at (900,0), N12 at (0,900), and N15 at (900,900)—are all safely assigned Slot 8. "
    "Because they are separated by 3 hops across the grid, none of their neighbors interfere with each other."
)

# =============================================================================
# SLIDE 8: CLI DELIVERABLE & STRUCTURAL TDMA SCHEDULE MATRIX
# =============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, C_LIGHT_BG)
add_header(s8, "Deliverable Execution", "CLI Delivery & Structural Slot x Node Concurrency Heatmap", "Strict compliance with prompt CLI specification: JSON parsing, ASCII matrix, and concurrency analysis.")
add_footer(s8, 8, TOTAL_SLIDES)

# Diagram 3 Matrix on Left
if os.path.exists("assets/diagram_3_schedule_matrix.png"):
    s8.shapes.add_picture("assets/diagram_3_schedule_matrix.png", Inches(0.8), Inches(1.85), width=Inches(7.8))

# Right Column: CLI compliance card
c_cli = add_card(s8, Inches(8.8), Inches(1.85), Inches(3.733), Inches(4.95), bg_color=C_CARD_BG, border_color=C_PRIMARY_BLUE, border_width=1.5)
tf_cli = c_cli.text_frame
tf_cli.margin_left = Inches(0.2)
tf_cli.margin_right = Inches(0.2)
tf_cli.margin_top = Inches(0.2)
p = tf_cli.paragraphs[0]
p.text = "Strict CLI Deliverable Compliance"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_PRIMARY_BLUE

cli_bullets = [
    ("Standardized JSON Argument: ", "Accepts coordinates via command line: '{\"Node_01\":[0.0,0.0], ...}'"),
    ("Ascii Boolean Matrix: ", "Generates formatted Slot x Node binary grid where '1' denotes transmit permission and '0' denotes silence."),
    ("Direct Node-to-Slot Mapping: ", "Explicit human-readable output of node slot assignments."),
    ("Reproducible Execution: ", "CLI can be invoked seamlessly via:\npython src/tdma_optimizer.py '<JSON>'"),
    ("Clean Exit Codes: ", "Returns exit code 0 on verified conflict-free completion, 1 on JSON syntax or interference failure.")
]
for lead, body in cli_bullets:
    p_s = tf_cli.add_paragraph()
    p_s.space_before = Pt(6)
    r1 = p_s.add_run()
    r1.text = lead
    r1.font.bold = True
    r1.font.size = Pt(9)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_s.add_run()
    r2.text = body
    r2.font.size = Pt(9)
    r2.font.color.rgb = C_TEXT_MUTED

add_speaker_notes(s8,
    "Slide 8 displays the structural Slot x Node schedule matrix and verifies strict compliance with the prompt deliverables. "
    "The heatmap on the left visually illustrates concurrency: "
    "Slots 0 through 3 handle single-node transmissions for the dense central nodes. "
    "Slots 4 through 7 achieve 2x concurrency. "
    "Slot 8 achieves 4x concurrency with 4 nodes active simultaneously. "
    "The CLI accepts standard JSON coordinates and outputs both the node-to-slot mapping and the clean ASCII boolean matrix required by the specification."
)

# =============================================================================
# SLIDE 9: PART 2: EMANE PHYSICAL EMULATOR ARCHITECTURE
# =============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, C_LIGHT_BG)
add_header(s9, "Part 2: Physical Emulation", "EMANE TDMA BDCE Radio Model & Linux/Docker Architecture", "Emulating real-time RF propagation, MAC slot timing, and hardware-accurate packet dropping.")
add_footer(s9, 9, TOTAL_SLIDES)

# Diagram 4 on Top
if os.path.exists("assets/diagram_4_emane_architecture.png"):
    s9.shapes.add_picture("assets/diagram_4_emane_architecture.png", Inches(0.8), Inches(1.85), width=Inches(11.733))

# Three detail cards at bottom
c_emane_details = [
    ("EMANE Framework & NEMs",
     "• Standard US DoD / DARPA tactical wireless emulation tool.\n"
     "• Each radio is instantiated as a Network Emulation Module (NEM).\n"
     "• Implements realistic physical-layer path loss, antenna gain, and noise figures.",
     C_PRIMARY_BLUE),
    ("TDMA Radio Model (BDCE)",
     "• BDCE = Basic Discrete Collision Event model.\n"
     "• Discretizes continuous time into exact microsecond slots.\n"
     "• Enforces strict packet dropping if a packet arrives on an unauthorized slot or encounters collision.",
     C_ACCENT_AMBER),
    ("Docker / Linux Setup Approach",
     "• Single Linux host running consolidated Docker container.\n"
     "• Virtual network namespaces connect virtual Ethernet (veth) pairs.\n"
     "• Multicast Over-The-Air (OTA) channel distributes events without requiring physical radio hardware.",
     C_ACCENT_GREEN)
]

for idx, (t, body, col) in enumerate(c_emane_details):
    c = add_card(s9, Inches(0.8 + idx * 4.0), Inches(5.1), Inches(3.733), Inches(1.75), bg_color=C_CARD_BG, border_color=col, border_width=1.5)
    tf = c.text_frame
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    p = tf.paragraphs[0]
    p.text = t
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = col
    p_b = tf.add_paragraph()
    p_b.space_before = Pt(4)
    p_b.text = body
    p_b.font.size = Pt(8.8)
    p_b.font.color.rgb = C_TEXT_DARK
    p_b.line_spacing = 1.25

add_speaker_notes(s9,
    "Slide 9 transitions to Part 2: The Physical Emulator using EMANE. "
    "EMANE is the industry standard for tactical wireless protocol emulation. "
    "Each radio node is an independent NEM (Network Emulation Module) connected via virtual Ethernet interfaces. "
    "The TDMA BDCE (Basic Discrete Collision Event) model controls transmission and reception boundaries with microsecond precision. "
    "Our approach deploys EMANE in a consolidated Linux Docker container. "
    "This allows scalable multi-node testing on any Linux machine or VM without requiring expensive SDR RF front-ends."
)

# =============================================================================
# SLIDE 10: PART 2: INTEGRATION BRIDGE (PYTHON TO EMANE XML)
# =============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, C_LIGHT_BG)
add_header(s10, "Part 2: Integration Bridge", "Automated Translation: Python Schedule to EMANE XML Events", "Seamless bridge compiling node-to-slot dictionary into tdmascheduleevent.dtd conforming XML.")
add_footer(s10, 10, TOTAL_SLIDES)

# Left Card: Bridge Mechanics & Pipeline
c_br = add_card(s10, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.95), bg_color=C_CARD_BG, border_color=C_PRIMARY_BLUE, border_width=1.5)
tf_br = c_br.text_frame
tf_br.margin_left = Inches(0.3)
tf_br.margin_right = Inches(0.3)
tf_br.margin_top = Inches(0.25)
p = tf_br.paragraphs[0]
p.text = "Integration Bridge Mechanics (src/emane_bridge.py)"
p.font.size = Pt(12.5)
p.font.bold = True
p.font.color.rgb = C_PRIMARY_BLUE

bridge_bullets = [
    ("Dynamic Input Parsing: ", "Accepts JSON node coordinates via CLI, runs the Brain's optimizer, and verifies the schedule before XML generation."),
    ("EMANE XML DTD Conformance: ", "Generates valid XML adhering to the official tdmascheduleevent.dtd schema: <!DOCTYPE emaneevent SYSTEM '...'>."),
    ("Frame & Slot Structure: ", "Configures <structure frames='1' slots='9'>, defining an exact 9-slot repeating TDMA frame."),
    ("Microsecond Slot Duration: ", "Sets <slot index='0' duration='1000'/>, representing 1000 microseconds (1ms) per slot as mandated by VMN specs."),
    ("Automated NEM Mapping: ", "Extracts numerical NEM IDs from node names (e.g. 'Node_01' -> nem='1') and writes explicit <tx> and <rx> slot assignments."),
    ("Zero Manual Intervention: ", "Eliminates error-prone manual XML authoring; fully automated from coordinates to EMANE execution.")
]
for lead, body in bridge_bullets:
    p_s = tf_br.add_paragraph()
    p_s.space_before = Pt(7)
    r1 = p_s.add_run()
    r1.text = lead
    r1.font.bold = True
    r1.font.size = Pt(9.3)
    r1.font.color.rgb = C_TEXT_DARK
    r2 = p_s.add_run()
    r2.text = body
    r2.font.size = Pt(9.3)
    r2.font.color.rgb = C_TEXT_MUTED

# Right Card: Generated XML Artifact Snippet
c_xml = add_card(s10, Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.95), bg_color=C_DARK_CARD, border_color=C_DARK_BORDER)
tf_x = c_xml.text_frame
tf_x.margin_left = Inches(0.25)
tf_x.margin_right = Inches(0.25)
tf_x.margin_top = Inches(0.25)
p_xh = tf_x.paragraphs[0]
p_xh.text = "Generated XML Profile (config/emane_schedule.xml)"
p_xh.font.size = Pt(10)
p_xh.font.bold = True
p_xh.font.color.rgb = RGBColor(147, 197, 253)

xml_snippet = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    "<!DOCTYPE emaneevent SYSTEM \n"
    "  \"file:///usr/share/emane/dtd/tdmascheduleevent.dtd\">\n"
    "<emaneevent module=\"tdmaschedule\">\n"
    "  <tdmaschedule>\n"
    "    <structure frames=\"1\" slots=\"9\">\n"
    "      <!-- 1ms slot duration = 1000 microseconds -->\n"
    "      <slot index=\"0\" duration=\"1000\"/>\n"
    "    </structure>\n"
    "    <schedules>\n"
    "      <entry nem=\"0\">\n"
    "        <frequency slot=\"8\" channel=\"0\"/>\n"
    "        <tx slot=\"8\"/>\n"
    "        <rx slot=\"8\"/>\n"
    "      </entry>\n"
    "      <entry nem=\"3\">\n"
    "        <frequency slot=\"8\" channel=\"0\"/>\n"
    "        <tx slot=\"8\"/>\n"
    "        <rx slot=\"8\"/>\n"
    "      </entry>\n"
    "      <!-- Additional NEM schedules ... -->\n"
    "    </schedules>\n"
    "  </tdmaschedule>\n"
    "</emaneevent>"
)
p_xb = tf_x.add_paragraph()
p_xb.space_before = Pt(8)
p_xb.text = xml_snippet
p_xb.font.size = Pt(8.5)
p_xb.font.name = "Consolas"
p_xb.font.color.rgb = RGBColor(226, 232, 240)

add_speaker_notes(s10,
    "Slide 10 highlights the integration bridge emane_bridge.py. "
    "The bridge translates the abstract graph coloring output into EMANE's native XML event schema. "
    "It constructs the tdmaschedule structure with 1 frame and 9 slots, specifying a 1000-microsecond (1 millisecond) slot duration. "
    "It then iterates over each NEM, binding its allocated time slot to frequency channel 0 with explicit transmit (<tx>) and receive (<rx>) permissions. "
    "This automates the entire pipeline from raw Cartesian coordinates to a validated simulation event profile."
)

# =============================================================================
# SLIDE 11: ENGINEERING DESIGN DECISIONS & TRADE-OFF ANALYSIS
# =============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, C_LIGHT_BG)
add_header(s11, "System Design", "Engineering Trade-offs & Protocol Design Decisions", "Evaluating centralized vs. distributed control, latency vs. throughput, and dynamic mobility.")
add_footer(s11, 11, TOTAL_SLIDES)

tradeoffs = [
    ("Centralized vs. Distributed TDMA",
     "• Architectural Decision: Centralized coordinator chosen as specified in requirements.\n"
     "• Rationale: Eliminates control-channel contention, avoids multi-hop consensus overhead, and achieves globally optimized frame lengths.\n"
     "• Tactical Fit: Ideal for cluster-head architectures (e.g. Airborne UAV relay or tactical command vehicle).",
     C_PRIMARY_BLUE),
    ("Slot Duration (1ms) & Latency Trade-offs",
     "• Architectural Decision: 1ms slot duration with 9ms repeating frame.\n"
     "• Rationale: Guarantees deterministic upper-bounded latency (< 9ms jitter), essential for mission-critical tactical voice and telemetry.\n"
     "• Trade-off: Guard band overhead is kept minimal by tight GPS/PTP synchronization.",
     C_ACCENT_GREEN),
    ("Heuristic (LDF) vs. Exact ILP Solvers",
     "• Architectural Decision: Largest Degree First greedy heuristic over Integer Linear Programming.\n"
     "• Rationale: ILP is NP-hard with exponential execution time. LDF runs in < 2ms (O(V log V + E)), enabling sub-second dynamic re-planning.\n"
     "• Trade-off: Achieves near-optimal chromatic number without computational stall.",
     C_ACCENT_AMBER),
    ("Dynamic MANET Mobility Handling",
     "• Architectural Decision: Periodic topology state beaconing with delta-updates.\n"
     "• Rationale: Instead of re-coloring the entire network, when radios move, only newly formed 2-hop edges trigger localized slot reassignment.\n"
     "• Future Roadmap: Integration with distributed USAP or Kempe-chain local recoloring.",
     C_ACCENT_PURPLE)
]

for idx, (t, body, col) in enumerate(tradeoffs):
    row = idx // 2
    col_idx = idx % 2
    x = Inches(0.8 + col_idx * 6.0)
    y = Inches(1.85 + row * 2.55)
    c = add_card(s11, x, y, Inches(5.7), Inches(2.35), bg_color=C_CARD_BG, border_color=col, border_width=1.5)
    tf = c.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = t
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = col
    p_b = tf.add_paragraph()
    p_b.space_before = Pt(6)
    p_b.text = body
    p_b.font.size = Pt(9)
    p_b.font.color.rgb = C_TEXT_DARK
    p_b.line_spacing = 1.3

add_speaker_notes(s11,
    "Slide 11 addresses key architectural trade-offs that show mature engineering thinking. "
    "First, why centralized TDMA? It eliminates in-band control collision and provides globally optimal frame compression. "
    "Second, why 1ms slots? In tactical communications, voice and missile telemetry require bounded latency. A 9ms frame cycle guarantees maximum delivery delay under 9 milliseconds. "
    "Third, why LDF heuristic over exact ILP? An exact ILP solver cannot scale when radios move rapidly. Our heuristic solves the problem in 2 milliseconds. "
    "Finally, handling mobility: when topology changes, local delta-updates can adjust slots without full network recalibration."
)

# =============================================================================
# SLIDE 12: TECHNICAL DEFENSE & PANEL Q&A PREPARATION
# =============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, C_LIGHT_BG)
add_header(s12, "Technical Defense", "Technical Defense & Panel Discussion Preparation", "Anticipating rigorous technical inquiries from the VMN expert evaluation panel.")
add_footer(s12, 12, TOTAL_SLIDES)

qa_cards = [
    ("Q1: 'Why is Distance-2 graph coloring sufficient? What about Distance-3 interference?'",
     "Defense Explanation:\n"
     "• Distance-2 coloring eliminates all topological receiver collisions: direct transmission collisions and hidden terminal collisions.\n"
     "• Distance-3 radios do not cause direct protocol collisions; their signals act merely as background thermal noise / cumulative interference.\n"
     "• In EMANE, physical propagation models (Two-Ray Ground / Free Space) calculate the SINR (Signal-to-Interference-Plus-Noise Ratio). If aggregate interference from distant nodes exceeds threshold, EMANE drops the packet naturally at PHY layer.",
     C_PRIMARY_BLUE),
    ("Q2: 'What happens when two mobile nodes move into 2-hop range of an active slot?'",
     "Defense Explanation:\n"
     "• This creates a dynamic collision condition. In our production architecture, each radio periodically broadcasts GPS/neighbor heartbeats.\n"
     "• When the Centralized Brain detects a newly added edge (u, v) in G2 where Slot(u) == Slot(v), it executes a localized slot migration.\n"
     "• The lower-degree node is reassigned to an available reserve slot or Kempe chain, preserving ongoing traffic without interrupting the entire network.",
     C_ACCENT_AMBER),
    ("Q3: 'How does this work align with VMN's mission in 5G Private Networks & SDR?'",
     "Defense Explanation:\n"
     "• VMN builds tactical SDR, 5G Private Networks, and NTN communication systems for defense and critical infrastructure.\n"
     "• In tactical MANET (e.g. squad radios, airborne drones), deterministic TDMA scheduling provides collision-free guarantees where standard 3GPP cellular networks cannot deploy.\n"
     "• In 5G Sidelink (PC5 Mode 2) and NTN satellite constellations, Distance-2 spatial reuse optimizes spectrum utilization across vast geographical zones.",
     C_ACCENT_GREEN)
]

for idx, (q, a, col) in enumerate(qa_cards):
    c = add_card(s12, Inches(0.8), Inches(1.85 + idx * 1.7), Inches(11.733), Inches(1.55), bg_color=C_CARD_BG, border_color=col, border_width=1.5)
    tf = c.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.15)
    p = tf.paragraphs[0]
    p.text = q
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = col
    p_b = tf.add_paragraph()
    p_b.space_before = Pt(4)
    p_b.text = a
    p_b.font.size = Pt(8.8)
    p_b.font.color.rgb = C_TEXT_DARK
    p_b.line_spacing = 1.25

add_speaker_notes(s12,
    "Slide 12 prepares for the technical defense with the panel. "
    "If asked why Distance-2 is sufficient and what about Distance-3: Distance-2 eliminates hard collisions at the MAC layer. Distance-3 interference is cumulative noise, which EMANE's physical layer SINR curves evaluate accurately. "
    "If asked about node mobility: We propose periodic heartbeat monitoring and localized slot migration using Kempe chains so we don't disrupt the whole frame. "
    "If asked about relevance to Vaan Megam Networks: This scheduler applies directly to tactical MANET SDR waveforms, 5G NR Sidelink, and Non-Terrestrial Networks (NTN) where deterministic collision avoidance is paramount."
)

# =============================================================================
# SLIDE 13: CONCLUSION & DELIVERABLES ROADMAP (Dark Theme)
# =============================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13, C_DARK_BG)
add_header(s13, "Conclusion & Deliverables", "Project Summary: Ready for Deployment & Defense", "Complete submission package fulfilling Part 1 mandatory tasks, Part 2 bonus emulation, and strict PDF guidelines.", dark=True)
add_footer(s13, 13, TOTAL_SLIDES, dark=True)

# 3 Final Cards
final_cards = [
    ("Part 1: Network Brain Delivered",
     "• Python engine (src/tdma_optimizer.py)\n"
     "• NetworkX 500m topology modeling\n"
     "• Distance-2 conflict graph (G2 = G1^2)\n"
     "• Largest Degree First (LDF) heuristic\n"
     "• 100% collision-free verification\n"
     "• Formatted Slot x Node boolean matrix\n"
     "• Standardized JSON CLI argument handling",
     C_PRIMARY_BLUE),
    ("Part 2: EMANE Emulator Delivered",
     "• Automated bridge (src/emane_bridge.py)\n"
     "• Native XML profile (config/emane_schedule.xml)\n"
     "• 1ms slot duration (1000us) configuration\n"
     "• TDMA BDCE radio model integration\n"
     "• Containerized Linux/Docker deployment plan\n"
     "• Hardware-accurate MAC packet filtering\n"
     "• Reproducible end-to-end pipeline",
     C_ACCENT_AMBER),
    ("Repository & Defense Ready",
     "• Git Version Controlled Repository\n"
     "• Modular source code structure (/src)\n"
     "• Generated EMANE profiles (/config)\n"
     "• Comprehensive Technical PDF Report (/docs)\n"
     "• Professional 16:9 Presentation Deck (/presentation)\n"
     "• Detailed speaker notes on all 13 slides\n"
     "• Ready for live demonstration and panel Q&A",
     C_ACCENT_GREEN)
]

for idx, (t, body, col) in enumerate(final_cards):
    c = add_card(s13, Inches(0.8 + idx * 4.0), Inches(1.85), Inches(3.733), Inches(4.3), bg_color=C_DARK_CARD, border_color=col, border_width=1.5)
    tf = c.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = t
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = col
    p_b = tf.add_paragraph()
    p_b.space_before = Pt(10)
    p_b.text = body
    p_b.font.size = Pt(9.5)
    p_b.font.color.rgb = RGBColor(226, 232, 240)
    p_b.line_spacing = 1.35

# Bottom Thank You / Contact Box
thx_box = s13.shapes.add_textbox(Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.55))
tf_thx = thx_box.text_frame
p_thx = tf_thx.paragraphs[0]
p_thx.alignment = PP_ALIGN.CENTER
p_thx.text = "Thank You! Ready for Live Demo & Technical Discussion with the Vaan Megam Networks Panel."
p_thx.font.size = Pt(13)
p_thx.font.bold = True
p_thx.font.color.rgb = RGBColor(147, 197, 253)

add_speaker_notes(s13,
    "In conclusion, we have built a complete, robust, and mathematically verified centralized TDMA scheduling brain and EMANE emulation bridge. "
    "Part 1 fully satisfies the mandatory requirements with Distance-2 graph coloring, spatial reuse, and CLI reporting. "
    "Part 2 fulfills the physical emulation criteria by dynamically generating compliant XML profiles for EMANE's TDMA radio model. "
    "All code, documentation, and this presentation deck are organized within the Git repository. "
    "I am eager to demonstrate the software live, answer any technical questions, and contribute to Vaan Megam Networks' groundbreaking work in tactical communications. Thank you!"
)

# -------------------------------------------------------------
# Save Presentation
# -------------------------------------------------------------
output_pptx = "presentation/TDMA_Schedule_Optimizer_Presentation_VMN.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully to: {output_pptx}")
