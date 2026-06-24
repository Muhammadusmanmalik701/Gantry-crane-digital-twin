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
sim_time = 20.0
time_step = 0.004
# =================================================


def plant(t, y, u_func, params):
    x, v, theta, omega = y
    m, M, r, dp, dc, g = params

    s = np.sin(theta)
    c = np.cos(theta)
    sin2 = s ** 2
    u = u_func(t)

    dvdt = (
        r * (dc * v - m * (g * s * c + r * s * omega ** 2) - u)
        - dp * c * omega
    ) / (-r * (M + m * sin2))

    domdt = (
        dp * omega * (m + M)
        + m ** 2 * r ** 2 * s * c * omega ** 2
        + m * r * (g * s * (m + M) + c * (u - dc * v))
    ) / (m * r ** 2 * (-M - m * sin2))

    return [v, dvdt, omega, domdt]


params = [m, M, r, dp, dc, g]


def u_pulse(t):
    return impulse_force if t < impulse_duration else 0.0


# ================== SIMULATION ==================
print("Simulation running...")

t_eval = np.arange(0, sim_time + time_step, time_step)

sol = solve_ivp(
    plant,
    [0, sim_time],
    [0, 0, 0, 0],
    args=(u_pulse, params),
    method="RK45",
    t_eval=t_eval,
    rtol=1e-6,
    atol=1e-8,
    max_step=time_step,
)

t = sol.t
x = sol.y[0]
v = sol.y[1]
theta = sol.y[2]
omega = sol.y[3]

print("Simulation complete! Animation starting...")


# ================== FIGURE LAYOUT ==================
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor("#eef3f8")

gs = fig.add_gridspec(
    2, 2,
    height_ratios=[1.0, 1.35],
    hspace=0.28,
    wspace=0.16
)

ax_top = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])
ax_front = fig.add_subplot(gs[1, :])

fig.subplots_adjust(top=0.86, left=0.05, right=0.97, bottom=0.07)

# ================== TOP INFO TEXT ==================
static_text = (
    f"m={m:.2f} kg   M={M:.2f} kg   r={r:.2f} m   "
    f"dp={dp:.2f}   dc={dc:.2f}   g={g:.2f} m/s²   "
    f"Impulse={impulse_force:.0f} N for {impulse_duration:.1f} s"
)

fig.text(
    0.05, 0.965, static_text,
    fontsize=9,
    fontfamily="monospace",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.96)
)

live_text = fig.text(
    0.64, 0.965, "",
    fontsize=9,
    fontfamily="monospace",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.96)
)

# ==========================================================
# TOP VIEW
# ==========================================================
ax_top.set_facecolor("#fcfcfc")
ax_top.set_xlim(-15, 265)
ax_top.set_ylim(-10, 10)
ax_top.grid(True, alpha=0.18, linestyle="--")
ax_top.set_title("Top View", fontsize=15, fontweight="bold", pad=10)
ax_top.set_xlabel("Horizontal Position (m)")
ax_top.set_ylabel("Lateral Sway")

# rails
ax_top.plot([-10, 260], [3.0, 3.0], color="#555", lw=2.5)
ax_top.plot([-10, 260], [-3.0, -3.0], color="#555", lw=2.5)
ax_top.plot([-10, 260], [0, 0], color="#bbbbbb", lw=1.2, linestyle="--")

cart_top = Rectangle(
    (-5, -2.0), 10, 4.0,
    fc="#1976d2", ec="black", lw=2.0, zorder=4
)
ax_top.add_patch(cart_top)

container_top = Rectangle(
    (-2.6, -1.1), 5.2, 2.2,
    fc="#ffb347", ec="black", lw=1.5, alpha=0.95, zorder=5
)
ax_top.add_patch(container_top)

connector_top, = ax_top.plot([], [], color="black", lw=1.8, linestyle="--", zorder=3)
trail_top, = ax_top.plot([], [], color="#2ca02c", lw=1.6, alpha=0.75, zorder=2)

# ==========================================================
# SIDE VIEW (LEFT/RIGHT VIEW)
# ==========================================================
ax_side.set_facecolor("#fcfcfc")
ax_side.set_xlim(-2.8, 2.8)
ax_side.set_ylim(-2.8, 2.5)
ax_side.grid(True, alpha=0.18, linestyle="--")
ax_side.set_title("Left / Right View", fontsize=15, fontweight="bold", pad=10)
ax_side.set_xlabel("Swing Direction")
ax_side.set_ylabel("Vertical Position")
ax_side.set_aspect("equal")

# trolley support in side view
ax_side.plot([-1.8, 1.8], [1.8, 1.8], color="#d4a017", lw=8, solid_capstyle="butt")
ax_side.plot([0, 0], [1.8, 1.2], color="#444", lw=3)

cart_side = Rectangle(
    (-0.75, 1.2), 1.5, 0.45,
    fc="#1976d2", ec="black", lw=1.7, zorder=4
)
ax_side.add_patch(cart_side)

rope_side, = ax_side.plot([], [], color="black", lw=2.4, zorder=3)
hook_side, = ax_side.plot([], [], "o", color="#444", markersize=5, zorder=5)
bob_side, = ax_side.plot([], [], "o", color="#ff9f1c", markersize=10, zorder=6)
trail_side, = ax_side.plot([], [], color="#2ca02c", lw=1.4, alpha=0.75)

# ==========================================================
# FRONT VIEW
# ==========================================================
ax_front.set_facecolor("#fcfcfc")
ax_front.set_xlim(-15, 265)
ax_front.set_ylim(-4, 6)
ax_front.set_aspect("equal")
ax_front.grid(True, alpha=0.18, linestyle="--")
ax_front.set_title("Front View", fontsize=15, fontweight="bold", pad=10)
ax_front.set_xlabel("Horizontal Position (m)")
ax_front.set_ylabel("Vertical Position (m)")

# ground
ax_front.plot([-20, 270], [-2.8, -2.8], color="#6c757d", lw=2)

# gantry frame
ax_front.plot([-10, 260], [3.2, 3.2], color="#d4a017", lw=16, solid_capstyle="butt", zorder=1)
ax_front.plot([-8, -3], [-2.8, 3.2], color="#495057", lw=10, solid_capstyle="round", zorder=1)
ax_front.plot([253, 258], [-2.8, 3.2], color="#495057", lw=10, solid_capstyle="round", zorder=1)
ax_front.plot([-8, 258], [2.75, 2.75], color="#343a40", lw=3, alpha=0.8, zorder=1)

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

rope_front, = ax_front.plot([], [], color="black", lw=3.2, zorder=3)
hook_front, = ax_front.plot([], [], "o", color="#444", markersize=6, zorder=5)

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

trail_front, = ax_front.plot([], [], color="#2ca02c", lw=1.5, alpha=0.75, zorder=2)

# ================== TRACES ==================
trace_top_x, trace_top_y = [], []
trace_side_x, trace_side_y = [], []
trace_front_x, trace_front_y = [], []

# ================== ANIMATION ==================
def animate(i):
    idx = min(i * 8, len(t) - 1)

    cx = x[idx]
    th = theta[idx]

    # ---------------- TOP VIEW ----------------
    lateral_offset = 6.0 * np.sin(th)

    cart_top.set_x(cx - 5)
    cart_top.set_y(-2.0)

    container_top.set_x(cx - 2.6)
    container_top.set_y(lateral_offset - 1.1)

    connector_top.set_data([cx, cx], [0, lateral_offset])

    trace_top_x.append(cx)
    trace_top_y.append(lateral_offset)
    trail_top.set_data(trace_top_x, trace_top_y)

    # ---------------- SIDE VIEW ----------------
    side_hook_x = 0.0
    side_hook_y = 1.2
    side_bob_x = r * np.sin(th)
    side_bob_y = side_hook_y - r * np.cos(th)

    rope_side.set_data([side_hook_x, side_bob_x], [side_hook_y, side_bob_y])
    hook_side.set_data([side_hook_x], [side_hook_y])
    bob_side.set_data([side_bob_x], [side_bob_y])

    trace_side_x.append(side_bob_x)
    trace_side_y.append(side_bob_y)
    trail_side.set_data(trace_side_x, trace_side_y)

    # ---------------- FRONT VIEW ----------------
    cart_y = 1.2
    hook_x = cx
    hook_y = cart_y + 0.2

    bob_x = hook_x + r * np.sin(th)
    bob_y = hook_y - r * np.cos(th)

    cart_front.set_x(cx - cart_width / 2)
    wheel1.center = (cx - 2.0, 1.0)
    wheel2.center = (cx + 2.0, 1.0)

    rope_front.set_data([hook_x, bob_x], [hook_y, bob_y])
    hook_front.set_data([hook_x], [hook_y])

    container_front.set_x(bob_x - container_width / 2)
    container_front.set_y(bob_y - container_height / 2)

    rot = mtransforms.Affine2D().rotate_around(bob_x, bob_y, th * 0.75)
    container_front.set_transform(rot + ax_front.transData)

    container_label.set_position((bob_x, bob_y))
    container_label.set_transform(rot + ax_front.transData)

    trace_front_x.append(bob_x)
    trace_front_y.append(bob_y)
    trail_front.set_data(trace_front_x, trace_front_y)

    # ---------------- LIVE TEXT ----------------
    live_text.set_text(
        f"t={t[idx]:5.2f} s   x={cx:7.2f} m   v={v[idx]:7.2f} m/s   "
        f"θ={np.degrees(th):6.2f}°   ω={np.degrees(omega[idx]):7.2f}°/s"
    )

    return (
        cart_top, container_top, connector_top, trail_top,
        rope_side, hook_side, bob_side, trail_side,
        cart_front, wheel1, wheel2, rope_front, hook_front,
        container_front, container_label, trail_front
    )


ani = animation.FuncAnimation(
    fig,
    animate,
    frames=max(1, len(t) // 8),
    interval=25,
    blit=False,
    repeat=True
)

# ================== SAVE OUTPUT ==================
gif_file = "gantry_advanced_multi_view_animation.gif"
print(f"Saving GIF as: {gif_file}")
ani.save(gif_file, writer="pillow", fps=30, dpi=120)
print(f"✅ GIF saved successfully: {gif_file}")

# Optional MP4 save (works only if ffmpeg installed)
try:
    mp4_file = "gantry_advanced_multi_view_animation.mp4"
    writer = animation.FFMpegWriter(fps=30, bitrate=1800)
    ani.save(mp4_file, writer=writer, dpi=140)
    print(f"✅ MP4 saved successfully: {mp4_file}")
except Exception as e:
    print("MP4 save skipped (ffmpeg not available).")
    print("Reason:", e)

plt.show()