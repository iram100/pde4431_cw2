
#  PRRR Robot Manipulator – Pick & Place Simulation

An interactive 3D simulation of a **4-DOF PRRR robotic manipulator** developed in Python.
The robot is capable of **picking three objects from the floor** and **placing them onto three shelves at different heights**, fully validated in simulation.

This project demonstrates **robot kinematics, inverse kinematics, trajectory animation, and user interaction**, developed as part of a robotic manipulation coursework.

---

##  Aim

The aim of this project is to demonstrate understanding of:

* Robotic manipulator kinematics
* Denavit–Hartenberg modelling
* Forward and inverse kinematics
* Simulation-based validation of robot designs

The robot is tested **purely in simulation**, following standard engineering practice before physical implementation.

---

## 📌 Task Description

The robot is required to:

* Pick **three objects from the floor**
* Place them onto **three shelves at different heights**
* Use **at least four joints**, including **one prismatic joint**
* Be visualised as a **stick-figure manipulator**
* Demonstrate reachability through **animated motion**

---

##  Robot Configuration

### Joint Structure (PRRR)

| Joint   | Type      | Function                      |
| ------- | --------- | ----------------------------- |
| Joint 1 | Prismatic | Vertical lift (Z-axis motion) |
| Joint 2 | Revolute  | Base rotation                 |
| Joint 3 | Revolute  | Elbow motion                  |
| Joint 4 | Revolute  | Wrist orientation             |

This configuration allows:

* Vertical access to floor and shelves
* Planar reach in the X–Y plane
* Smooth and stable pick-and-place motion

---

##  Denavit–Hartenberg Parameters

The manipulator is defined using **standard Denavit–Hartenberg (D–H) parameters**.

### D–H Table

| Joint | Type | θ (theta)         | d (offset)        | a (link length) | α (twist) |
| ----- | ---- | ----------------- | ----------------- | --------------- | --------- |
| 1     | P    | 0                 | **d₁ (variable)** | 0.00            | 0         |
| 2     | R    | **θ₁ (variable)** | 0.00              | 0.35            | 0         |
| 3     | R    | **θ₂ (variable)** | 0.00              | 0.30            | 0         |
| 4     | R    | **θ₃ (variable)** | 0.00              | 0.20            | 0         |

### Design Notes

* One **prismatic joint** enables vertical motion
* Three **revolute joints** form a planar articulated arm
* Zero twist angles simplify the kinematic chain
* Link lengths were selected to ensure:

  * Reachability of floor objects
  * Access to all shelf levels
  * Smooth motion without singularities

---

##  Kinematics

### Forward Kinematics

* Computes joint and end-effector positions from joint variables
* Used for:

  * Visualisation
  * Object attachment
  * End-effector tracking

### Inverse Kinematics

* Geometric IK solution
* Calculates joint variables from a desired Cartesian position
* Validates reachability before motion execution

---

##  Simulation Features

### Pick-and-Place Sequence

1. Move to hover position above object
2. Descend to object
3. Pick object (attached to end-effector)
4. Lift to safe height
5. Translate to shelf location
6. Descend to shelf height
7. Release object
8. Return to home position

### Visualisation

* Full 3D animation using `matplotlib`
* Stick-figure robot links and joints
* Floor plane and multi-level shelf structure
* Objects move realistically with the end-effector

---

##  User Interface

The simulation includes an interactive control panel with:

* **Pick Object 1 / 2 / 3** buttons
* **HOME** button to return to a safe pose
* **Speed controls** (Slow / Normal / Fast)
* **Auto Stack Demo** (runs the full task sequence automatically)

---

##  Independent Study Features

To demonstrate learning beyond core lectures, the project includes:

* Adjustable animation speed
* Automatic demonstration mode
* Multi-level shelf structure
* Clean modular code design
* User-friendly graphical interface

---

##  Validation

The simulation clearly demonstrates that the robot:

* Reaches all floor object locations
* Reaches all shelf heights
* Successfully completes pick-and-place operations
* Avoids unreachable targets through IK validation

---

##  Project Structure

```
.
├── main.py           # Program entry point
├── Kinematics.py     # Forward & inverse kinematics
├── Env.py    # Objects and shelves
├── Visualisation.py     # Robot motion and logic
├── UserInterface.py             # Control panel and buttons
├── README.md
```

---

## ▶ How to Run

### Requirements

```bash
pip install numpy matplotlib
```

### Run the simulation

```bash
python main.py
```

---

## Demonstration Video

**YouTube Link:**
https://youtu.be/Ew-VZKy9hUk?si=EfeEefxhy4_RicpM

The video includes:

* Full task demonstration
* Clear animation
* Voice-over explanation of code and kinematics

---

##  Conclusion

This project successfully demonstrates the design and simulation of a robotic manipulator capable of completing a structured pick-and-place task. The robot design satisfies all coursework requirements and clearly demonstrates understanding of robotic kinematics, simulation, and software implementation.

---

##  Author

**Name:** *Iram Mukri*

---

