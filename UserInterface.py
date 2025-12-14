import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from config import HOME_POS, HOVER
from Env import OBJECTS_INIT, SHELVES
from Kinematics import ik, fk
from Visualisation import draw_scene

class PRRRSim:
    def __init__(self):
        self.q = ik(*HOME_POS)
        self.objects = [o.copy() for o in OBJECTS_INIT]
        self.carry = None
        self.steps = 60

        self.fig = plt.figure(figsize=(9.5, 7))
        self.ax = self.fig.add_subplot(111, projection="3d")

        self._make_buttons()
        self.update()

    def _make_buttons(self):
        y = 0.78
        dy = 0.075

        for i in range(3):
            axb = self.fig.add_axes([0.02, y - i*dy, 0.20, 0.06])
            Button(axb, f"Pick Object {i+1}",
                   color="#CFE8FF").on_clicked(
                lambda e, i=i: self.pick_and_place(i)
            )

        Button(self.fig.add_axes([0.02, 0.52, 0.20, 0.06]),
               "HOME", color="#CDEAC0").on_clicked(self.go_home)

        Button(self.fig.add_axes([0.02, 0.42, 0.20, 0.06]),
               "Speed: Slow").on_clicked(lambda e: self.set_speed(100))
        Button(self.fig.add_axes([0.02, 0.34, 0.20, 0.06]),
               "Speed: Normal").on_clicked(lambda e: self.set_speed(60))
        Button(self.fig.add_axes([0.02, 0.26, 0.20, 0.06]),
               "Speed: Fast").on_clicked(lambda e: self.set_speed(30))

        Button(self.fig.add_axes([0.02, 0.14, 0.20, 0.07]),
               "AUTO STACK DEMO", color="#E2C7FF").on_clicked(self.auto_demo)

    def update(self):
        draw_scene(self.ax, self.q, self.objects)
        plt.pause(0.001)

    def move_to(self, target, carry=False):
        q_target = ik(*target)
        for s in np.linspace(0, 1, self.steps):
            self.q = (1-s)*self.q + s*q_target
            if carry and self.carry is not None:
                self.objects[self.carry] = fk(*self.q)[-1].copy()
            self.update()

    def go_home(self, event=None):
        self.move_to(HOME_POS)

    def set_speed(self, steps):
        self.steps = steps

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

    def auto_demo(self, event=None):
        self.go_home()
        for i in range(3):
            self.pick_and_place(i)
