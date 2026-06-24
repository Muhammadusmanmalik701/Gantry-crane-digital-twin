import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
import matplotlib.transforms as mtransforms

# ================== PARAMETERS ==================
m = 0.2
M = 10.0
r = 1.0
dp = 0.5
dc = 2.0
g = 9.81

impulse_force = 1000.0
impulse_duration = 0.5
sim_time = 20
# =================================================


def plant(t, y, u_func, params):
    x, v, theta, omega = y
    m, M, r, dp, dc, g = params

    s = np.sin(theta)
    c = np.cos(theta)
    sin2 = s**2
    u = u_func(t)

    dvdt = (
        r * (dc * v - m * (g * s * c + r * s * omega**2) - u)
        - dp * c * omega
    ) / (-r * (M + m * sin2))

    domdt = (
        dp * omega * (m + M)
        + m**2 * r**2 * s * c * omega**2
        + m * r * (g * s * (m + M) + c * (u - dc * v))
    ) / (m * r**2 * (-M - m * sin2))

    return [v, dvdt, omega, domdt]


params = [m, M, r, dp, dc, g]

def u_pulse(t):
    return impulse_force if t < impulse_duration else 0.0


print("Simulation running...")
sol = solve_ivp(
    plant,
    [0, sim_time],
    [0, 0, 0, 0],
    args=(u_pulse, params),
    method='RK45',
    rtol=1e-6,
    atol=1e-8,
    max_step=0.004
)

t = sol.t
x = sol.y[0]
theta = sol.y[2]

print("Simulation complete! Animation starting...")


# ================== FIGURE + 2 SUBPLOTS ==================
fig, (ax_top, ax_front) = plt.subplots(2, 1, figsize=(16, 10))
fig.patch.set_facecolor("#eef3f8")

# leave extra space for top info text
fig.subplots_adjust(top=0.84, hspace=0.28, left=0.06, right=0.97, bottom=0.07)

# ================== TOP INFO TEXT ==================
static_text = (
    f"m={m:.2f} kg   M={M:.2f} kg   r={r:.2f} m   "
    f"dp={dp:.2f}   dc={dc:.2f}   g={g:.2f} m/s²   "
    f"Impulse={impulse_force:.0f} N for {impulse_duration:.1f} s"
)

fig.text(
    0.05, 0.97, static_text,
    fontsize=9,
    fontfamily="monospace",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.95)
)

live_text = fig.text(
    0.68, 0.97, "",
    fontsize=9,
    fontfamily="monospace",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.95)
)

# ================== TOP VIEW AXIS ==================
ax_top.set_facecolor("#fcfcfc")
ax_top.set_xlim(-15, 265)
ax_top.set_ylim(-8, 8)
ax_top.grid(True, alpha=0.18, linestyle='--')
ax_top.set_title("Top View", fontsize=16, fontweight='bold', pad=10)
ax_top.set_ylabel("Track Width")
ax_top.set_xlabel("Horizontal Position (m)")

# track rails
ax_top.plot([-10, 260], [2.5, 2.5], color="#555", lw=2.5)
ax_top.plot([-10, 260], [-2.5, -2.5], color="#555", lw=2.5)

# center guideline
ax_top.plot([-10, 260], [0, 0], color="#b0b0b0", lw=1.2, linestyle='--')

# trolley top view
cart_top = Rectangle(
    (-5, -1.8), 10, 3.6,
    fc="#1976d2", ec="black", lw=2.0, zorder=4
)
ax_top.add_patch(cart_top)

# container projection in top view
container_top = Rectangle(
    (-2.8, -1.2), 5.6, 2.4,
    fc="#ffb347", ec="black", lw=1.6, alpha=0.9, zorder=5
)
ax_top.add_patch(container_top)

# dashed connector between trolley center and container center
connector_top, = ax_top.plot([], [], color="black", lw=1.8, linestyle="--", zorder=3)

# motion trail top view
trail_top, = ax_top.plot([], [], color="#2ca02c", lw=1.6, alpha=0.7)


# ================== FRONT VIEW AXIS ==================
ax_front.set_facecolor("#fcfcfc")
ax_front.set_xlim(-15, 265)
ax_front.set_ylim(-4, 6)
ax_front.set_aspect('equal')
ax_front.grid(True, alpha=0.18, linestyle='--')
ax_front.set_title("Front View", fontsize=16, fontweight='bold', pad=10)
ax_front.set_xlabel("Horizontal Position (m)")
ax_front.set_ylabel("Vertical Position (m)")

# ground
ax_front.plot([-20, 270], [-2.8, -2.8], color="#6c757d", lw=2)

# gantry frame
ax_front.plot([-10, 260], [3.2, 3.2], color="#d4a017", lw=16, solid_capstyle='butt', zorder=1)
ax_front.plot([-8, -3], [-2.8, 3.2], color="#495057", lw=10, solid_capstyle='round', zorder=1)
ax_front.plot([253, 258], [-2.8, 3.2], color="#495057", lw=10, solid_capstyle='round', zorder=1)
ax_front.plot([-8, 258], [2.75, 2.75], color="#343a40", lw=3, alpha=0.8, zorder=1)

# moving parts front view
cart_width = 8
cart_height = 2
container_width = 4
container_height = 2.4

cart_front = Rectangle(
    (-cart_width / 2, 1.2),
    cart_width,
    cart_height,
    fc="#1976d2",
    ec="black",
    lw=2.2,
    zorder=4
)
ax_front.add_patch(cart_front)

wheel1 = Circle((0, 1.0), 0.28, fc="#212529", ec="black", zorder=5)
wheel2 = Circle((0, 1.0), 0.28, fc="#212529", ec="black", zorder=5)
ax_front.add_patch(wheel1)
ax_front.add_patch(wheel2)

rope, = ax_front.plot([], [], color="black", lw=3.2, zorder=3)
hook, = ax_front.plot([], [], 'o', color="#444", markersize=6, zorder=5)

container_front = Rectangle(
    (-container_width / 2, -1),
    container_width,
    container_height,
    fc="#ff9f1c",
    ec="black",
    lw=2.0,
    zorder=4
)
ax_front.add_patch(container_front)

container_label = ax_front.text(
    0, 0, "Container",
    ha="center", va="center",
    fontsize=9, fontweight="bold",
    color="black", zorder=6
)

trace_front, = ax_front.plot([], [], color="#2ca02c", lw=1.5, alpha=0.7, zorder=2)


# ================== TRACES ==================
trace_front_x = []
trace_front_y = []
trace_top_x = []
trace_top_y = []

def animate(i):
    idx = min(i * 8, len(t) - 1)

    cx = x[idx]
    th = theta[idx]

    # -------- TOP VIEW --------
    # in top view, pendulum sway is shown as lateral offset
    lateral_offset = 6.0 * np.sin(th)

    cart_top.set_x(cx - 5)
    cart_top.set_y(-1.8)

    container_top.set_x(cx - 2.8)
    container_top.set_y(lateral_offset - 1.2)

    connector_top.set_data(
        [cx, cx],
        [0, lateral_offset]
    )

    trace_top_x.append(cx)
    trace_top_y.append(lateral_offset)
    trail_top.set_data(trace_top_x, trace_top_y)

    # -------- FRONT VIEW --------
    cart_y = 1.2
    hook_x = cx
    hook_y = cart_y + 0.2

    bob_x = hook_x + r * np.sin(th)
    bob_y = hook_y - r * np.cos(th)

    cart_front.set_x(cx - cart_width / 2)
    wheel1.center = (cx - 2.0, 1.0)
    wheel2.center = (cx + 2.0, 1.0)

    rope.set_data([hook_x, bob_x], [hook_y, bob_y])
    hook.set_data([hook_x], [hook_y])

    container_front.set_x(bob_x - container_width / 2)
    container_front.set_y(bob_y - container_height / 2)

    rot = mtransforms.Affine2D().rotate_around(bob_x, bob_y, th * 0.75)
    container_front.set_transform(rot + ax_front.transData)
    container_label.set_position((bob_x, bob_y))
    container_label.set_transform(rot + ax_front.transData)

    trace_front_x.append(bob_x)
    trace_front_y.append(bob_y)
    trace_front.set_data(trace_front_x, trace_front_y)

    live_text.set_text(
        f"t={t[idx]:5.2f} s   x={cx:6.2f} m   θ={np.degrees(th):6.2f}°"
    )

    return (
        cart_top, container_top, connector_top, trail_top,
        cart_front, wheel1, wheel2, rope, hook,
        container_front, container_label, trace_front
    )


ani = animation.FuncAnimation(
    fig,
    animate,
    frames=max(1, len(t) // 8),
    interval=25,
    blit=False,
    repeat=True
)

ani.save("gantry_top_front_view_animation.gif", writer="pillow", fps=30, dpi=120)
print("✅ GIF saved! File: gantry_top_front_view_animation.gif")

plt.show()