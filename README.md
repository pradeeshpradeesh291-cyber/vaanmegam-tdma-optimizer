# Centralized TDMA Schedule Planner and Optimizer with EMANE Emulation

**Vaan Megam Networks (VMN) — Full-Time Internship Technical Assessment**  
**Domain:** Wireless Protocol Development | 5G Secure Private Networks, Tactical MANET & SDR  
**Candidate:** Pradeesh R 
**Submission Date:** 24 September 2026  

---

## Overview

This repository contains the complete implementation and technical submission for the **Centralized TDMA Schedule Planner and Optimizer** with **EMANE (Extendable Mobile Ad-hoc Network Emulator)** physical layer emulation, designed for Vaan Megam Networks.

The project is structured in two major tiers:
1. **Part 1 (Mandatory) — The Network Brain (Python Engine):**
   - Mathematical topology representation using `networkx` with a 500-meter radio reachability threshold ($G_1$).
   - Distance-2 conflict graph transformation ($G_2 = G_1^2$) preventing both **Distance-1 (Direct Link)** and **Distance-2 (Hidden Terminal)** collisions.
   - **Largest Degree First (LDF / Welsh-Powell)** greedy graph coloring heuristic, enabling aggressive **Spatial Reuse** ($>2$ hops apart).
   - Automated mathematical verification engine (`verify_schedule`) guaranteeing 100% collision-free schedules.
   - Standardized CLI outputting direct node-to-slot mapping and a formatted Slot $\times$ Node ASCII boolean matrix.
2. **Part 2 (Bonus) — The Physical Emulator (EMANE Setup & Integration Bridge):**
   - Automated integration bridge (`emane_bridge.py`) converting the Python schedule matrix into official `tdmascheduleevent.dtd` XML event profiles.
   - Configuration for EMANE TDMA Radio Model (BDCE), specifying 1ms slot duration, recurring TDMA frames, and frequency allocations.
   - Blueprint for Linux / Docker multi-NEM container deployment to evaluate real-time packet dropping and forwarding without physical SDR hardware.

---

## Repository Structure

```
├── assets/                                  # High-resolution diagrams for presentation & documentation
│   ├── diagram_1_interference.png           # Direct vs. Hidden Terminal Interference & Spatial Reuse
│   ├── diagram_2_graphs.png                 # Physical Topology G1 vs. Scheduled G2 Mesh
│   ├── diagram_3_schedule_matrix.png        # Slot x Node Concurrency Heatmap
│   └── diagram_4_emane_architecture.png     # End-to-End System Architecture Block Diagram
├── config/
│   └── emane_schedule.xml                   # Generated EMANE TDMA XML schedule profile
├── docs/
│   ├── PROJECT_DOCUMENTATION.md             # In-depth technical specification and design process
│   └── TDMA_Optimizer_Documentation_VMN.pdf # Formatted PDF report for submission
├── presentation/
│   └── TDMA_Schedule_Optimizer_Presentation_VMN.pptx # 13-slide widescreen PPT deck with speaker notes
├── src/
│   ├── tdma_optimizer.py                    # Part 1: Centralized Python Schedule Optimizer (Brain)
│   └── emane_bridge.py                      # Part 2: Integration Bridge for EMANE XML events
├── build_presentation.py                    # PPTX generator script
├── generate_diagrams.py                     # High-res diagram generation script
├── generate_pdf_report.py                   # PDF documentation generator script
└── README.md                                # Project summary & execution guide
```

---

## 16-Node Benchmark Results

Evaluating on a $4 \times 4$ tactical mesh grid (300m inter-node spacing, 500m radio range, 42 physical links):
- **Configured Radio Range:** 500.0 meters
- **Optimized Frame Length:** **9 unique timeslots** (compressed from 16)
- **Spatial Reuse Factor:** **1.78x** aggregate throughput gain
- **Quad-Node Concurrency in Slot 8:** Four corners (`Node_00`, `Node_03`, `Node_12`, `Node_15`) transmit simultaneously without mutual interference ($\ge 3$ hops apart).
- **Dual-Node Concurrency in Slots 4–7:** 2 nodes transmit concurrently per slot.
- **Verification:** 100% PASS across all 1-hop and 2-hop edges in $G_2$.

### Structural Slot $\times$ Node Matrix
```
Slot \ Node | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15
-------------------------------------------------------------------------------------------
Slot 00    | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0
Slot 01    | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0
Slot 02    | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0
Slot 03    | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0
Slot 04    | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0
Slot 05    | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0
Slot 06    | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0
Slot 07    | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 1  | 0  | 0  | 0  | 0
Slot 08    | 1  | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 1
```

---

## How to Run

### Prerequisites
```bash
python -m venv venv
venv\Scripts\activate
pip install networkx matplotlib python-pptx reportlab
```

### 1. Run Part 1 (TDMA Optimizer CLI)
```bash
python src/tdma_optimizer.py '{"Node_01":[0.0,0.0],"Node_02":[300.0,0.0],"Node_03":[600.0,0.0],"Node_04":[900.0,0.0],"Node_05":[0.0,300.0],"Node_06":[300.0,300.0],"Node_07":[600.0,300.0],"Node_08":[900.0,300.0],"Node_09":[0.0,600.0],"Node_10":[300.0,600.0],"Node_11":[600.0,600.0],"Node_12":[900.0,600.0],"Node_13":[0.0,900.0],"Node_14":[300.0,900.0],"Node_15":[600.0,900.0],"Node_16":[900.0,900.0]}'
```

### 2. Run Part 2 (EMANE XML Bridge Generator)
```bash
python src/emane_bridge.py '{"Node_01":[0.0,0.0],"Node_02":[300.0,0.0],"Node_03":[600.0,0.0],"Node_04":[900.0,0.0],"Node_05":[0.0,300.0],"Node_06":[300.0,300.0],"Node_07":[600.0,300.0],"Node_08":[900.0,300.0],"Node_09":[0.0,600.0],"Node_10":[300.0,600.0],"Node_11":[600.0,600.0],"Node_12":[900.0,600.0],"Node_13":[0.0,900.0],"Node_14":[300.0,900.0],"Node_15":[600.0,900.0],"Node_16":[900.0,900.0]}'
```
This generates `config/emane_schedule.xml` ready for deployment into EMANE simulation instances.

---

## Submission Deliverables Summary

1. **Source Code (`src/`):** Clean, robust, production-quality Python code.
2. **Documentation (`docs/`):** Full PDF document detailing design process, thought process, and final values.
3. **Presentation (`presentation/`):** 16:9 widescreen PowerPoint deck (`TDMA_Schedule_Optimizer_Presentation_VMN.pptx`) equipped with slide-by-slide speaker notes, architectural diagrams, and defense Q&A preparation for the technical panel interview.
