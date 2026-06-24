# Gantry Crane Trolley-Pendulum System — Simulation & Animation using Modelica and Python

<img width="1920" height="1200" alt="gantry_advanced_multi_view_animation" src="https://github.com/user-attachments/assets/dcb0e8f1-9f36-4360-94da-24265046c254" />


> A complete physics-based simulation of an overhead gantry crane with a suspended container (pendulum), modelled in **Modelica** and visualized in **Python**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [System Description](#system-description)
- [Mathematical Model](#mathematical-model)
- [Parameters](#parameters)
- [Project Structure](#project-structure)
- [Simulation Cases](#simulation-cases)
- [Animations & Results](#animations--results)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Physics Deep Dive](#physics-deep-dive)
- [Author](#author)

---

## Project Overview

A physics-based Digital Twin of a gantry crane trolley-pendulum system, developed as part of the **BIP (Blended Intensive Programme) International Research Project** in Digital Twin Systems — University of Bordeaux & University of Antwerp, Belgium (2026).

The crane trolley moves horizontally along a fixed rail, and a container hangs from it via a rope. When a force is applied to the trolley, the container swings like a pendulum. This project:

- Derives and implements the **exact nonlinear equations of motion**
- Models the system in **Modelica** (industry-standard simulation language)
- Solves the ODEs numerically in **Python** using `scipy.integrate`
- Produces **professional animated GIFs** showing the crane in motion from multiple views

---

## System Description

```
         ═══════════════════════════════════  ← Fixed Gantry Rail
                    [  TROLLEY  ]             ← Moves horizontally (position x)
                         |
                         | r (rope length)
                         |
                     [Container]              ← Swings as pendulum (angle θ)
```

| Component   | Symbol | Description                          |
|-------------|--------|--------------------------------------|
| Trolley     | M      | Heavy cart sliding on the top rail   |
| Container   | m      | Hanging load (pendulum bob)          |
| Rope        | r      | Rigid rope connecting trolley to load|
| Control Force | u    | Horizontal force applied to trolley  |

---

## Mathematical Model

The system is governed by **two coupled second-order nonlinear ODEs** derived from the Lagrangian mechanics of the trolley-pendulum system.

### State Variables

| Variable | Symbol | Unit  | Description                      |
|----------|--------|-------|----------------------------------|
| Position | x      | m     | Trolley horizontal position      |
| Velocity | v      | m/s   | Trolley horizontal velocity      |
| Angle    | θ      | rad   | Pendulum angle from vertical     |
| Angular velocity | ω | rad/s | Rate of change of pendulum angle |

### Equations of Motion

**Trolley acceleration:**

```
dv/dt = [ r·(dc·v - m·(g·sin θ·cos θ + r·sin θ·ω²) - u) - dp·cos θ·ω ]
        ─────────────────────────────────────────────────────────────────
                          -r·(M + m·sin²θ)
```

**Pendulum angular acceleration:**

```
dω/dt = [ dp·ω·(m + M) + m²·r²·sin θ·cos θ·ω² + m·r·(g·sin θ·(m+M) + cos θ·(u - dc·v)) ]
        ────────────────────────────────────────────────────────────────────────────────────
                                    m·r²·(-M - m·sin²θ)
```

These equations account for:
- **Inertial coupling** between trolley and pendulum
- **Centripetal effects** from the swinging load
- **Viscous damping** on both trolley (`dc`) and pendulum (`dp`)
- **External control force** `u` on the trolley

---

## Parameters

| Parameter | Symbol | Value  | Unit  | Description                         |
|-----------|--------|--------|-------|-------------------------------------|
| Container mass | m | 0.2  | kg    | Mass of the hanging container       |
| Trolley mass   | M | 10.0 | kg    | Mass of the trolley cart            |
| Rope length    | r | 1.0  | m     | Length of the rope/cable            |
| Pendulum damping | dp | 0.5 | —   | Damping on pendulum swing           |
| Cart damping   | dc | 2.0 | —    | Damping on trolley motion           |
| Gravity        | g  | 9.81 | m/s² | Gravitational acceleration          |

**Initial Conditions:** All states start at zero (trolley at rest, pendulum vertical).

---

## Project Structure

```
gantry-crane-simulation/
│
├── GantryAssignment.mo              # Modelica model (Plant model)
├── GantryAssignment/                # Modelica package directory
│
├── animation.py                     # Python: single front-view animation
├── animation1.py                    # Python: dual-view (Top + Front) animation
├── animation2.py                    # Python: advanced multi-view animation
│
├── gantry_animation.gif                      # Basic animation output
├── professional_gantry_animation.gif         # Professional single-view GIF
├── professional_pendulum_gantry_animation.gif # Pendulum-focused animation
├── gantry_top_front_view_animation.gif       # Top + Front dual view GIF
├── gantry_advanced_multi_view_animation.gif  # Advanced multi-view GIF
│
├── x_vs_time.png                    # Plot: Trolley position over time
├── theta_vs_time.png                # Plot: Pendulum angle over time
│
├── .gitignore
└── README.md
```

---

## Simulation Cases

### Case 1: Free Response (u = 0)
The trolley receives no external force. This is used to **verify the model** — the system should remain at rest since all initial conditions are zero.

```modelica
u = 0;
```

### Case 2: Impulse Force (Task Assignment)
A large impulse force of **1000 N** is applied for the first **0.5 seconds**, then removed. This causes:
- The trolley to accelerate rapidly
- The container to swing (pendulum motion begins)
- Damping gradually brings the system back to equilibrium

```modelica
u = if time < 0.5 then 1000 else 0;
```

In Python:
```python
def u_pulse(t):
    return 1000.0 if t < 0.5 else 0.0
```

---

## Animations & Results

### Front View Animation
Shows the full gantry structure with the trolley moving along the top rail and the container swinging below.

![Front View](professional_pendulum_gantry_animation.gif)

### Top + Front Dual View Animation
Simultaneously shows:
- **Top View** — lateral sway of the container projected from above
- **Front View** — vertical pendulum swing with rope

![Dual View](gantry_top_front_view_animation.gif)

### Time Plots
| Plot | Description |
|------|-------------|
| `x_vs_time.png` | Trolley displacement over 20 seconds |
| `theta_vs_time.png` | Pendulum angle oscillation and decay |

---

## Requirements

### For Python Animations
```
Python >= 3.8
numpy
scipy
matplotlib
pillow
```

Install dependencies:
```bash
pip install numpy scipy matplotlib pillow
```

### For Modelica Simulation
- **OpenModelica** (free): https://openmodelica.org/
- Or **Dymola** (commercial)
- Or any Modelica-compatible tool

---

## How to Run

### Run Python Animation (Front View)
```bash
python animation.py
```
Generates: `professional_pendulum_gantry_animation.gif`

### Run Dual-View Animation (Top + Front)
```bash
python animation1.py
```
Generates: `gantry_top_front_view_animation.gif`

### Run Advanced Multi-View Animation
```bash
python animation2.py
```

### Run Modelica Simulation
1. Open **OpenModelica** (OMEdit)
2. Load `GantryAssignment.mo`
3. Select `GantryAssignment.Plant` model
4. Set simulation time to `20 seconds`
5. Click **Simulate**
6. Plot variables: `x`, `theta`, `v`, `omega`

To switch between cases, comment/uncomment in the `equation` section:
```modelica
// Case 1: No force
// u = 0;

// Case 2: Impulse
u = if time < 0.5 then 1000 else 0;
```

---

## Physics Deep Dive

### Why is this system nonlinear?

The `sin θ` and `cos θ` terms in the equations make this a **nonlinear system**. For small angles (θ ≈ 0), `sin θ ≈ θ` and `cos θ ≈ 1`, allowing linearization — but this project uses the **full nonlinear model** for accuracy.

### What is Inertial Coupling?

The trolley and pendulum are coupled — moving the trolley causes the pendulum to swing, and the pendulum's swing exerts reaction forces back on the trolley. This coupling is captured by the `m·sin²θ` term in the denominator of both equations.

### Damping Behavior

- **Cart damping `dc`**: Models friction between trolley wheels and the rail
- **Pendulum damping `dp`**: Models air resistance and rope flexibility
- Without damping, the pendulum would oscillate forever; with damping, it settles to vertical

### Numerical Integration

Python uses **RK45** (Runge-Kutta 4th/5th order) from `scipy.integrate.solve_ivp` with:
- Relative tolerance: `1e-6`
- Absolute tolerance: `1e-8`
- Max step size: `0.004 s`

This ensures high accuracy for the stiff nonlinear equations.

---

## Author

**Muhammad Usman Malik**
GitHub: [@Muhammadusmanmalik701](https://github.com/Muhammadusmanmalik701)

---

*This project was developed as part of a control systems / mechatronics assignment exploring dynamic modeling and simulation of underactuated mechanical systems.*
