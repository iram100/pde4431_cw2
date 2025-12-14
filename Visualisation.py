import numpy as np
from Kinematics import fk
from Env import SHELVES

def draw_scene(ax, q, objects):
    ax.cla()
    ax.set_xlim(-0.2, 0.8)
    ax.set_ylim(-0.5, 0.5)
    ax.set_zlim(0, 1.2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1,1,1])

    # Floor
    X, Y = np.meshgrid([-0.2, 0.8], [-0.5, 0.5])
    Z = np.zeros_like(X)
    ax.plot_surface(X, Y, Z, alpha=0.25, color="lightgray")

    # Shelf posts
    shelf_x, shelf_y = SHELVES[0][0], SHELVES[0][1]
    post_offsets = [(-0.05,-0.05), (-0.05,0.05), (0.05,-0.05), (0.05,0.05)]
    top_z = SHELVES[-1][2] + 0.08

    for dx, dy in post_offsets:
        ax.plot([shelf_x+dx, shelf_x+dx],
                [shelf_y+dy, shelf_y+dy],
                [0, top_z],
                color="dimgray", lw=3)

    # Shelf levels
    for s in SHELVES:
        ax.scatter(s[0], s[1], s[2], s=420,
                   c="sandybrown", edgecolors="k", zorder=5)

    # Robot
    pts = fk(*q)
    ax.plot(pts[:,0], pts[:,1], pts[:,2], "-o", lw=4)

    ee = pts[-1]
    ax.scatter(ee[0], ee[1], ee[2], s=120, c="darkred")

    # Objects
    for p in objects:
        ax.scatter(p[0], p[1], p[2],
                   s=140, c="royalblue", edgecolors="k", zorder=6)
