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


# ================== FIGURE SETUP ==================
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor("#eef3f8")

# axes ko neeche push kar diya
fig.subplots_adjust(top=0.72, left=0.05, right=0.97, bottom=0.08)

ax.set_facecolor("#fdfdfd")
ax.set_xlim(-15, 265)
ax.set_ylim(-4, 6)
ax.set_aspect('equal')
ax.grid(True, alpha=0.18, linestyle='--')

ax.set_title(
    "Gantry Crane Trolley–Pendulum System Animation",
    fontsize=18,
    fontweight='bold',
    pad=16
)

# ================== TOP TEXT OUTSIDE ANIMATION AREA ==================
static_text = (
    f"m={m:.2f} kg   M={M:.2f} kg   r={r:.2f} m   "
    f"dp={dp:.2f}   dc={dc:.2f}   g={g:.2f} m/s²   "
    f"Impulse={impulse_force:.0f} N for {impulse_duration:.1f} s"
)

fig.text(
    0.05, 0.96, static_text,
    fontsize=9,
    fontfamily="monospace",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.95)
)

live_text = fig.text(
    0.68, 0.96, "",
    fontsize=9,
    fontfamily="monospace",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.95)
)

# ================== GANTRY STRUCTURE ==================
ax.plot([-20, 270], [-2.8, -2.8], color="#6c757d", lw=2)

ax.plot([-10, 260], [3.2, 3.2], color="#d4a017", lw=16, solid_capstyle='butt', zorder=1)
ax.plot([-8, -3], [-2.8, 3.2], color="#495057", lw=10, solid_capstyle='round', zorder=1)
ax.plot([253, 258], [-2.8, 3.2], color="#495057", lw=10, solid_capstyle='round', zorder=1)
ax.plot([-8, 258], [2.75, 2.75], color="#343a40", lw=3, alpha=0.8, zorder=1)

# ================== MOVING PARTS ==================
cart_width = 8
cart_height = 2
container_width = 4
container_height = 2.4

cart = Rectangle(
    (-cart_width / 2, 1.2),
    cart_width,
    cart_height,
    fc="#1976d2",
    ec="black",
    lw=2.2,
    zorder=4
)
ax.add_patch(cart)

wheel1 = Circle((0, 1.0), 0.28, fc="#212529", ec="black", zorder=5)
wheel2 = Circle((0, 1.0), 0.28, fc="#212529", ec="black", zorder=5)
ax.add_patch(wheel1)
ax.add_patch(wheel2)

rope, = ax.plot([], [], color="black", lw=3.2, zorder=3)
hook, = ax.plot([], [], 'o', color="#444", markersize=6, zorder=5)

container = Rectangle(
    (-container_width / 2, -1),
    container_width,
    container_height,
    fc="#ff9f1c",
    ec="black",
    lw=2.0,
    zorder=4
)
ax.add_patch(container)

container_label = ax.text(
    0, 0, "Container",
    ha="center", va="center",
    fontsize=9, fontweight="bold",
    color="black", zorder=6
)

trace_line, = ax.plot([], [], color="#2ca02c", lw=1.5, alpha=0.7, zorder=2)

trace_x = []
trace_y = []

def animate(i):
    idx = min(i * 8, len(t) - 1)

    cx = x[idx]
    th = theta[idx]

    cart_y = 1.2
    hook_x = cx
    hook_y = cart_y + 0.2

    bob_x = hook_x + r * np.sin(th)
    bob_y = hook_y - r * np.cos(th)

    cart.set_x(cx - cart_width / 2)
    wheel1.center = (cx - 2.0, 1.0)
    wheel2.center = (cx + 2.0, 1.0)

    rope.set_data([hook_x, bob_x], [hook_y, bob_y])
    hook.set_data([hook_x], [hook_y])

    container.set_x(bob_x - container_width / 2)
    container.set_y(bob_y - container_height / 2)

    rot = mtransforms.Affine2D().rotate_around(bob_x, bob_y, th * 0.75)
    container.set_transform(rot + ax.transData)
    container_label.set_position((bob_x, bob_y))
    container_label.set_transform(rot + ax.transData)

    trace_x.append(bob_x)
    trace_y.append(bob_y)
    trace_line.set_data(trace_x, trace_y)

    live_text.set_text(
        f"t={t[idx]:5.2f} s   x={cx:6.2f} m   θ={np.degrees(th):6.2f}°"
    )

    return cart, wheel1, wheel2, rope, hook, container, container_label, trace_line


ani = animation.FuncAnimation(
    fig,
    animate,
    frames=max(1, len(t) // 8),
    interval=25,
    blit=False,
    repeat=True
)

ani.save("professional_pendulum_gantry_animation.gif", writer="pillow", fps=30, dpi=120)
print("✅ GIF saved! File: professional_pendulum_gantry_animation.gif")

plt.show()