# Robot Arm v0 — Servo Elbow Blocks

Goal: baby-step robot arm prototype with two printed links joined by one hobby servo as an elbow.

Files:

- `sg90_elbow_v0.scad` — small SG90 9g micro-servo version.
- `mg996r_elbow_v0.scad` — larger MG996R servo version.

Each SCAD file has:

```scad
PART = "assembly"; // "fixed", "moving", "assembly"
```

Set `PART = "fixed"` to export the fixed servo-holder block.
Set `PART = "moving"` to export the horn/moving-link block.
Set `PART = "assembly"` for visual preview only.

## Design notes

The servo body mounts in the fixed block. The servo shaft points out sideways at the elbow. The plastic servo horn screws to the moving link.

The printed moving link should attach to the included servo horn using 2–4 small screws; do not rely only on the center spline screw to carry the whole load.

## Known approximations

These dimensions are based on Amazon screenshots plus typical SG90/MG996R sizes. Actual servo geometry varies.

Before final printing, measure with calipers:

- servo body length/width/height
- mounting tab hole spacing
- shaft center location from body edges
- servo horn hole pattern

Then tune parameters near the top of each SCAD file.

## Print recommendation

Start with SG90 first. It is smaller, safer, and faster to iterate. Use MG996R only after the hinge pattern works.

Suggested first print:

- SG90 fixed block
- SG90 moving link
- 0.2 mm layer height
- 3+ perimeters
- 25–40% infill
- PLA is fine for v0; PETG better if parts flex/crack.
