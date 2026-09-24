# Centralized TDMA Schedule Planner and Optimizer with EMANE Emulation

**Company:** Vaan Megam Networks Private Limited (VMN), IITM Pravartak Technology Foundation, Chennai  
**Domain:** Wireless Protocol Development | 5G Secure Private Networks, Tactical MANET & SDR  
**Candidate:** devpradeesh  
**Date:** September 2026  

---

## 1. Executive Summary

This project implements a centralized software brain and physical layer emulation pipeline for a Time Division Multiple Access (TDMA) wireless network. Operating in tactical shared-spectrum environments (e.g., Tactical MANET, SDR, 5G Private Networks), radios must communicate without collisions while maximizing spectrum utilization.

The system is delivered in two coordinated components:
1. **The Network Brain (Part 1 - Python Engine):** Formulates the wireless topology as a Unit Disk Graph ($G_1$) based on a 500-meter radio range and transforms it into a Distance-2 conflict graph ($G_2 = G_1^2$). It applies a greedy Largest Degree First (LDF / Welsh-Powell) heuristic to solve the NP-hard vertex coloring problem, achieving conflict-free time slot allocations with aggressive spatial reuse. An integrated verification engine mathematically validates zero 1-hop and 2-hop collisions before outputting a standardized Slot $\times$ Node boolean matrix.
2. **The Physical Emulator (Part 2 - EMANE Setup):** Translates the optimized TDMA matrix via an automated integration bridge (`emane_bridge.py`) into EMANE native XML schedule event documents adhering to `tdmascheduleevent.dtd`. It specifies 1ms slot duration, recurring TDMA frames, and frequency allocations to govern packet dropping and forwarding in real-time RF network emulation.

---

## 2. RF Interference Physics & Problem Formulation

### 2.1 The TDMA Principle
In TDMA networks, radios share a single frequency channel by dividing time into recurring frames, which are further divided into discrete time slots. If multiple radios in close geographic proximity transmit simultaneously, their signals collide at the receiver, corrupting data. However, radios sufficiently far apart can safely transmit on the same time slot—a principle termed **Spatial Reuse**.

### 2.2 Collision Scenarios
To guarantee collision-free communication, the scheduler must resolve two critical physical interference scenarios:

1. **Distance-1 Interference (Direct Link Collision):**
   - **Condition:** Node $A$ and Node $B$ are within direct communication range ($d(A, B) \le 500\text{m}$).
   - **Constraint:** Half-duplex SDR transceivers cannot transmit and receive on the same frequency simultaneously. Furthermore, simultaneous transmission by both nodes saturates local front-end LNAs.
   - **Graph Rule:** $(A, B) \in E_1 \implies \text{Slot}(A) \ne \text{Slot}(B)$.

2. **Distance-2 Interference (Hidden Terminal Collision):**
   - **Condition:** Node $A$ and Node $C$ are out of direct radio range ($d(A, C) > 500\text{m}$), but both share a mutual neighbor Node $B$ ($d(A, B) \le 500\text{m}$ and $d(C, B) \le 500\text{m}$).
   - **Constraint:** Because $A$ and $C$ cannot sense each other's carrier, they would transmit concurrently in classical CSMA networks. At receiver $B$, their electromagnetic waves arrive simultaneously, resulting in a destructive packet collision.
   - **Graph Rule:** $\exists B \text{ s.t. } (A, B) \in E_1 \land (C, B) \in E_1 \implies \text{Slot}(A) \ne \text{Slot}(C)$.

3. **Spatial Reuse Principle ($> 2$ Hops):**
   - **Condition:** Two nodes $u$ and $v$ have graph distance $\text{dist}_{G_1}(u, v) \ge 3$.
   - **Property:** No common neighbor exists that could suffer collision. Therefore, $\text{Slot}(u) = \text{Slot}(v)$ is completely safe.

---

## 3. Mathematical Modeling & Graph Algorithms (Part 1)

### 3.1 Graph Construction
1. **Physical Graph $G_1 = (V, E_1)$:**
   - $V = \{v_1, v_2, \dots, v_{16}\}$ representing radio nodes with 2D coordinates $(x_i, y_i)$.
   - $E_1 = \{(u, v) \mid u \ne v, \sqrt{(x_u - x_v)^2 + (y_u - y_v)^2} \le 500.0\text{m}\}$.
2. **Conflict Graph $G_2 = (V, E_2)$:**
   - Defined as the square graph $G_2 = G_1^2$.
   - $E_2 = E_1 \cup \{(u, v) \mid \exists w \in V : (u, w) \in E_1 \land (w, v) \in E_1\}$.
   - **Equivalence:** A Distance-2 coloring on $G_1$ is identically equivalent to a standard Distance-1 vertex coloring on $G_2$.

### 3.2 Optimization Heuristic: Largest Degree First (LDF)
Finding the minimal chromatic number $\chi(G_2)$ is NP-Complete. An exact brute-force search requires $O(S^{|V|})$ complexity, which cannot scale in dynamic tactical SDR environments.

We implement the **Largest Degree First (LDF / Welsh-Powell)** heuristic:
1. **Degree Sorting:** Compute degree $\deg_{G_2}(v)$ for all $v \in V$. Sort vertices descending: $\deg_{G_2}(v_1) \ge \deg_{G_2}(v_2) \ge \dots \ge \deg_{G_2}(v_n)$.
2. **Greedy First-Fit Allocation:** For each vertex $v$, determine the set of slots already used by its neighbors in $G_2$:
   $$\mathcal{F}(v) = \{\text{Slot}(w) \mid w \in \mathcal{N}_{G_2}(v) \land w \text{ is colored}\}$$
   Assign the smallest available integer slot:
   $$\text{Slot}(v) = \min(\mathbb{N}_0 \setminus \mathcal{F}(v))$$

**Why LDF minimizes frame length:** The most constrained nodes (highest 2-hop neighbor density) claim the lowest slots early. Peripheral nodes with lower degrees are evaluated later, allowing them to greedily reuse early slots without expanding the frame size.

### 3.3 Verification Engine (`verify_schedule`)
Before generating reports or exporting to EMANE, the scheduler executes an edge-level assertion:
$$\forall (u, v) \in E_2 : \text{Slot}(u) \ne \text{Slot}(v)$$
If any collision exists, execution halts immediately with error code 1.

---

## 4. Benchmark Results & 16-Node Grid Evaluation

### 4.1 Deployment Setup
- **Topology:** 16 nodes arranged in a $4 \times 4$ grid spanning $900\text{m} \times 900\text{m}$.
- **Grid Spacing:** $300\text{m}$ between adjacent nodes.
  - Horizontal/Vertical distance: $300.0\text{m} \le 500\text{m}$ (1 hop).
  - Diagonal distance: $\sqrt{300^2 + 300^2} \approx 424.3\text{m} \le 500\text{m}$ (1 hop).
  - Physical edges in $G_1$: 42 links.

### 4.2 Optimized Schedule
- **Frame Length:** 9 unique time slots (compressed from 16).
- **Spatial Reuse Factor:** $\mathcal{S}_R = \frac{16}{9} \approx 1.78\times$ network capacity increase.
- **Concurrency Breakdown:**
  - **Slot 8 (4x Concurrency):** `Node_00`, `Node_03`, `Node_12`, `Node_15` (The four grid corners, all $\ge 3$ hops apart).
  - **Slot 4 (2x Concurrency):** `Node_01` & `Node_13`.
  - **Slot 5 (2x Concurrency):** `Node_02` & `Node_14`.
  - **Slot 6 (2x Concurrency):** `Node_04` & `Node_07`.
  - **Slot 7 (2x Concurrency):** `Node_08` & `Node_11`.
  - **Slots 0, 1, 2, 3 (1x Concurrency):** Dense central nodes `Node_05`, `Node_06`, `Node_09`, `Node_10`.

### 4.3 Structural TDMA Matrix Output
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

## 5. Physical Emulator Architecture & EMANE Integration (Part 2)

### 5.1 EMANE Overview
EMANE (Extendable Mobile Ad-hoc Network Emulator) provides real-time emulation of link, MAC, and physical RF layers. In EMANE:
- Radios are modeled as **Network Emulation Modules (NEMs)**.
- The **TDMA Radio Model (BDCE - Basic Discrete Collision Event)** enforces strict slot timing.
- Over-the-air (OTA) packet delivery evaluates signal-to-interference-plus-noise ratio (SINR). Packets sent outside authorized slots or during collisions are dropped at the MAC/PHY boundary.

### 5.2 Integration Bridge (`src/emane_bridge.py`)
The bridge takes the optimized schedule dictionary and produces standard `tdmascheduleevent.dtd` compliant XML:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE emaneevent SYSTEM "file:///usr/share/emane/dtd/tdmascheduleevent.dtd">
<emaneevent module="tdmaschedule">
  <tdmaschedule>
    <structure frames="1" slots="9">
      <slot index="0" duration="1000"/> <!-- 1ms slot duration -->
    </structure>
    <schedules>
      <entry nem="0">
        <frequency slot="8" channel="0"/>
        <tx slot="8"/>
        <rx slot="8"/>
      </entry>
      <!-- Additional NEM entries ... -->
    </schedules>
  </tdmaschedule>
</emaneevent>
```

### 5.3 Dockerized Emulation Blueprint
To deploy without hardware:
1. Multi-NEM Docker container on Linux with network namespaces (`ip netns`).
2. Virtual Ethernet (`veth`) pairs bridging each NEM to a simulated tactical host application.
3. Multicast control daemon broadcasting the schedule XML event to all NEMs simultaneously.

---

## 6. Engineering Design Trade-offs & Panel Defense

| Design Decision | Chosen Approach | Alternative Considered | Technical Justification |
| :--- | :--- | :--- | :--- |
| **Control Architecture** | Centralized Brain | Distributed (e.g. USAP, DRAND) | Eliminates in-band contention overhead and achieves global frame minimization. Suitable for tactical UAV/Command post coordinators. |
| **Optimization Method** | Greedy LDF Heuristic | Integer Linear Programming (ILP) | ILP is $O(2^{|V|})$ and computationally intractable for real-time SDRs. LDF runs in $<2\text{ms}$ with near-optimal chromatic results. |
| **Slot Duration** | 1ms ($1000\,\mu\text{s}$) | 10ms or Dynamic | Guarantees deterministic upper bound on latency ($<9\text{ms}$ frame cycle) for tactical voice/C2 telemetry. |
| **Interference Boundary**| Distance-2 Graph ($G_1^2$) | Distance-3 / Physical SINR | Distance-2 eliminates hard MAC collisions. Distance-3 cumulative noise is handled dynamically by EMANE's physical layer path-loss models. |

---

## 7. How to Run & Verify

### 7.1 Running the TDMA Optimizer CLI (Part 1)
```bash
python src/tdma_optimizer.py '{"Node_01":[0.0,0.0],"Node_02":[300.0,0.0],...,"Node_16":[900.0,900.0]}'
```

### 7.2 Generating EMANE Schedule XML (Part 2)
```bash
python src/emane_bridge.py '{"Node_01":[0.0,0.0],"Node_02":[300.0,0.0],...,"Node_16":[900.0,900.0]}'
```

---

## 8. Submission Assets Checklist

- [x] **Source Code:** `src/tdma_optimizer.py`, `src/emane_bridge.py`
- [x] **EMANE XML Profile:** `config/emane_schedule.xml`
- [x] **Technical Documentation:** `docs/PROJECT_DOCUMENTATION.md`, `docs/TDMA_Optimizer_Documentation_VMN.pdf`
- [x] **Presentation Deck:** `presentation/TDMA_Schedule_Optimizer_Presentation_VMN.pptx`
- [x] **Speaker Notes & Panel Defense:** Fully embedded in presentation slides.
