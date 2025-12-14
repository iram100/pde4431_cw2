import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ============================================================
# PRRR Robot Parameters
# ============================================================
L1 = 0.35
L2 = 0.30
L3 = 0.20

Z_MIN = 0.00
Z_MAX = 1.20
HOVER = 0.15

HOME_POS = np.array([0.15, 0.0, 0.15])

# ============================================================
# Environment
# ============================================================
OBJECTS_INIT = [
    np.array([0.35, -0.20, 0.02]),
    np.array([0.40,  0.00, 0.02]),
    np.array([0.35,  0.20, 0.02]),
]

SHELVES = [
    np.array([0.55, 0.35, 0.25]),
    np.array([0.55, 0.35, 0.40]),
    np.array([0.55, 0.35, 0.55]),
]

# ============================================================
# Forward Kinematics
# ============================================================
def fk(d, t1, t2, t3):
    p0 = np.array([0, 0, 0])
    p1 = np.array([0, 0, d])

    p2 = p1 + np.array([L1*np.cos(t1), L1*np.sin(t1), 0])
    g2 = t1 + t2

    p3 = p2 + np.array([L2*np.cos(g2), L2*np.sin(g2), 0])
    g3 = g2 + t3

    p4 = p3 + np.array([L3*np.cos(g3), L3*np.sin(g3), 0])
    return np.array([p0, p1, p2, p3, p4])

# ============================================================
# Inverse Kinematics
# ============================================================
def ik(x, y, z, phi=0.0):
    z = np.clip(z, Z_MIN, Z_MAX)
    d = z

    wx = x - L3*np.cos(phi)
    wy = y - L3*np.sin(phi)

    r = np.sqrt(wx**2 + wy**2)
    if r > (L1 + L2):
        raise ValueError("Target out of reach")

    c2 = (r**2 - L1**2 - L2**2) / (2*L1*L2)
    c2 = np.clip(c2, -1.0, 1.0)

    t2 = np.arccos(c2)
    t1 = np.arctan2(wy, wx) - np.arctan2(
        L2*np.sin(t2), L1 + L2*np.cos(t2)
    )
    t3 = phi - (t1 + t2)

    return np.array([d, t1, t2, t3])

# ============================================================
# Simulation Class
# ============================================================
class PRRRSim:
    def __init__(self):
        self.q = ik(*HOME_POS)
        self.objects = [o.copy() for o in OBJECTS_INIT]
        self.carry = None

        self.steps = 60

        self.fig = plt.figure(figsize=(9.5, 7))
        self.ax = self.fig.add_subplot(111, projection="3d")

        self.buttons = []
        self._make_buttons()
        self.draw()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------
    def _make_buttons(self):
        y = 0.78
        dy = 0.075

        # Pick buttons
        for i in range(3):
            axb = self.fig.add_axes([0.02, y - i*dy, 0.20, 0.06])
            btn = Button(axb, f"Pick Object {i+1}",
                         color="#CFE8FF", hovercolor="#9FCFFF")
            btn.on_clicked(lambda e, i=i: self.pick_and_place(i))
            self.buttons.append(btn)

        # Home
        ax_home = self.fig.add_axes([0.02, 0.52, 0.20, 0.06])
        btn_home = Button(ax_home, "HOME",
                          color="#CDEAC0", hovercolor="#A8D5A2")
        btn_home.on_clicked(self.go_home)
        self.buttons.append(btn_home)

        # Speed
        ax_slow = self.fig.add_axes([0.02, 0.42, 0.20, 0.06])
        btn_slow = Button(ax_slow, "Speed: Slow",
                          color="#E0E0E0", hovercolor="#C8C8C8")
        btn_slow.on_clicked(lambda e: self.set_speed(100))
        self.buttons.append(btn_slow)

        ax_norm = self.fig.add_axes([0.02, 0.34, 0.20, 0.06])
        btn_norm = Button(ax_norm, "Speed: Normal",
                          color="#D0D0D0", hovercolor="#B0B0B0")
        btn_norm.on_clicked(lambda e: self.set_speed(60))
        self.buttons.append(btn_norm)

        ax_fast = self.fig.add_axes([0.02, 0.26, 0.20, 0.06])
        btn_fast = Button(ax_fast, "Speed: Fast",
                          color="#C0C0C0", hovercolor="#A0A0A0")
        btn_fast.on_clicked(lambda e: self.set_speed(30))
        self.buttons.append(btn_fast)

        # Auto demo
        ax_demo = self.fig.add_axes([0.02, 0.14, 0.20, 0.07])
        btn_demo = Button(ax_demo, "AUTO STACK DEMO",
                          color="#E2C7FF", hovercolor="#CFA8FF")
        btn_demo.on_clicked(self.auto_demo)
        self.buttons.append(btn_demo)

    # --------------------------------------------------------
    # Drawing
    # --------------------------------------------------------
    def draw(self):
        self.ax.cla()
        self.ax.set_xlim(-0.2, 0.8)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_zlim(0, 1.2)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_box_aspect([1,1,1])

        # Floor
        X, Y = np.meshgrid([-0.2, 0.8], [-0.5, 0.5])
        Z = np.zeros_like(X)
        self.ax.plot_surface(X, Y, Z, alpha=0.25, color="lightgray")

        # Shelves
        for s in SHELVES:
            self.ax.scatter(s[0], s[1], s[2],
                            s=420, c="sandybrown", edgecolors="k")

        # Robot
        pts = fk(*self.q)
        self.ax.plot(pts[:,0], pts[:,1], pts[:,2], "-o", lw=4)

        ee = pts[-1]
        self.ax.scatter(ee[0], ee[1], ee[2],
                        s=120, c="darkred")

        # Objects
        for p in self.objects:
            self.ax.scatter(p[0], p[1], p[2],
                            s=140, c="royalblue", edgecolors="k")

        plt.pause(0.001)

    # --------------------------------------------------------
    # Motion
    # --------------------------------------------------------
    def move_to(self, target, carry=False):
        q_target = ik(*target)

        for s in np.linspace(0, 1, self.steps):
            self.q = (1 - s)*self.q + s*q_target

            if carry and self.carry is not None:
                ee = fk(*self.q)[-1]
                self.objects[self.carry] = ee.copy()

            self.draw()

    def go_home(self, event=None):
        self.move_to(HOME_POS)

    def set_speed(self, steps):
        self.steps = steps

    # --------------------------------------------------------
    # Pick & Place
    # --------------------------------------------------------
    def pick_and_place(self, idx):
        obj = self.objects[idx]
        shelf = SHELVES[idx]

        hover_pick = obj + np.array([0,0,HOVER])
        hover_place = shelf + np.array([0,0,HOVER])

        self.move_to(hover_pick)
        self.move_to(obj)

        self.carry = idx
        self.move_to(hover_pick, carry=True)
        self.move_to(hover_place, carry=True)
        self.move_to(shelf, carry=True)

        self.carry = None
        self.move_to(hover_place)
        self.go_home()

    # --------------------------------------------------------
    # Auto Demo (Independent Study Feature)
    # --------------------------------------------------------
    def auto_demo(self, event=None):
        self.go_home()
        for i in range(3):
            self.pick_and_place(i)

# ============================================================
# Run
# ============================================================
if __name__ == "__main__":
    PRRRSim()
    plt.show()
