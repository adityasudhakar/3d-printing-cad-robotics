# Servo-Driven Rack Gripper Trace Notes

This file is the working audit trail for a text-to-cad driven gripper assembly.
It maps design decisions and future actions to explicit instructions in the
`earthtojake/text-to-cad` repo.

## Goal

Create a hobby-scale gripper mechanism where:

1. An off-the-shelf servo rotates a horn/crank.
2. The crank drives a central sliding rod.
3. The sliding rod drives two linkage arms.
4. The linkage arms rotate two gears/pinions.
5. The gears actuate two rack-style gripper fingers.
6. The gripper fingers slide on rails/guides.

This replaces a pneumatic/hydraulic piston with a servo-driven linear rod.

## Text-to-CAD Instruction Map

### CAD Workflow

Source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md

Instruction used:
The CAD skill says to create a natural-language CAD brief, plan before coding,
prefer build123d Python with `gen_step()`, keep STEP as the primary artifact,
validate with `scripts/inspect`, and render snapshots after STEP generation.

Action for this project:
Before any geometry is generated, define the CAD brief, subassemblies,
interfaces, parameters, expected bounds, and validation gates in this file.

### Named Purchasable Components

Source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md

Instruction used:
When an assembly includes named off-the-shelf actuators, servos, motors,
electronics boards, connectors, or other purchasable components, search
`$step-parts` before creating simplified placeholder geometry. If no exact
match is found, record the miss and then use a documented envelope.

Action for this project:
Search `step.parts` before modeling these named components:

- SG90 micro servo, or another selected servo model.
- Servo horn, if a catalog part is available.
- Fasteners, likely M2/M3 screws.
- Bearings/bushings, if gear shafts need them.
- Linear rails/guides, if using catalog rails instead of printed guide slots.

If a part is not found, document the search terms and use a measured/spec-based
envelope only after recording the miss.

### step.parts Search And Download

Source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/step-parts/SKILL.md

Instruction used:
Use the hosted `https://api.step.parts` endpoints, search exact model strings
and aliases for named actuators, download exact or near-exact STEP files when
found, and verify SHA-256 when present.

Action for this project:
For each named component, record:

- search terms
- selected `step.parts` id
- page/API URL
- local downloaded STEP path
- SHA-256 verification result
- reason for using the real STEP or falling back to an envelope

### Assembly Positioning

Source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/positioning.md

Instruction used:
Positioning should be authored in source using part-local frames, datums,
build123d joints, `AssemblyHelper`, and parameterized transforms. CLI alignment
is validation, not a source-editing API.

Action for this project:
Use source-level datums for:

- servo output axis
- horn crank pin
- center sliding rod axis
- left and right gear axes
- left and right rack slide axes
- rail/guiding faces
- jaw closed/open reference positions

### Parameters And Motion

Source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/parameters.md

Instruction used:
For mechanisms, identify fixed pivots, moving pivots, link lengths, gear
ratios, axes, joint limits, and branch choices before creating controls.
Animation parameters should drive real degrees of freedom and derive dependent
transforms from constraints.

Action for this project:
Define `servo_angle_deg` or `jaw_open_mm` as the main mechanism parameter.
Derive rod travel, linkage positions, gear rotation, and rack displacement from
the chosen geometry rather than tuning each part by eye.

### Validation And Snapshot

Source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/inspection-and-validation.md

Instruction used:
Validate with facts/planes/positioning, then targeted measurement, alignment,
frame, or diff checks where needed. Include snapshots for visual verification.

Action for this project:
Each generated subassembly must have:

- STEP output
- `inspect refs --facts --planes --positioning`
- at least one snapshot PNG
- targeted checks for the interfaces that matter for that stage

## CAD Brief

Task type:
New mechanical assembly with moving subassemblies and off-the-shelf components.

Units:
Millimeters.

Coordinate convention:

- Base plane: XY.
- Up axis: +Z.
- Assembly origin: center of fixed base plate.
- Gripper open/close motion: along X unless later constraints suggest another axis.
- Servo and gear axes: +Z vertical for the first layout.

Primary output:
STEP assembly generated from build123d Python source.

Secondary outputs:
Snapshot PNGs. Optional animation GIF after static geometry works.

Manufacturing intent:
First-pass 3D-printable layout exploration, not final toleranced design.

## Proposed Subassemblies

### 1. Fixed Frame Subassembly

Components:

- base plate
- left/right rail or guide slots
- gear posts
- servo mount
- rod guide supports

Interfaces:

- rail spacing
- gear pivot positions
- servo output axis position
- central rod slide axis
- mounting holes for servo and posts

Validation:

- expected bbox
- rail axes parallel
- gear posts symmetric
- servo output axis aligns with horn/crank plane
- rod guide axis centered

### 2. Sliding Jaw / Rack Subassembly

Components:

- left rack jaw
- right rack jaw
- gripper pads
- rail engagement features
- rack teeth or simplified pitch references

Interfaces:

- rack pitch line
- rack tooth pitch/module
- slide axis
- jaw travel range
- rail clearance

Validation:

- left/right jaws symmetric
- jaws constrained to rail axes
- rack pitch lines tangent to gears
- open/closed travel stays inside rail guides

### 3. Gear / Pinion Subassembly

Components:

- left gear
- right gear
- gear hubs
- shaft holes or bearings
- optional gear teeth or simplified pitch circles

Interfaces:

- gear center distance to racks
- gear tooth pitch/module
- linkage crank radius on each gear
- shaft/post diameter

Validation:

- gear axes vertical and fixed
- gear pitch circles contact rack pitch lines
- crank pin radius matches linkage arm geometry
- left/right gears rotate opposite directions if needed

### 4. Servo + Horn Subassembly

Components:

- real servo STEP if available through `step.parts`
- servo horn/crank
- crank pin
- mounting screws or holes

Interfaces:

- servo output axis
- horn length
- allowable servo angle range
- crank pin location as a function of servo angle

Validation:

- servo body fits mount envelope
- horn clears base/frame
- crank pin stroke can drive the center rod target travel

### 5. Center Sliding Rod + Linkage Subassembly

Components:

- central sliding rod
- rod clevis/pivot at servo horn
- left and right linkage arms
- pivots from rod to gear crank pins

Interfaces:

- rod slide axis
- rod stroke
- left/right linkage length
- gear crank pin positions
- pivot hole diameters

Validation:

- rod remains on slide axis
- link lengths remain constant across sampled positions
- linkages do not cross impossible branches
- rod travel maps to expected gear rotation

### 6. Integration Assembly

Components:

- fixed frame
- jaws/racks
- gears
- servo/horn
- rod/linkages
- optional fasteners

Validation:

- closed pose
- open pose
- mid pose
- no obvious gross collision in snapshots
- rack displacement is symmetric
- gear rotations are mirrored or coordinated correctly
- jaw opening matches requested travel

## Initial Interface Guesses

These are placeholders for planning and must be revised after catalog part
searches and first geometry checks.

- Base plate: about `140 x 80 x 5 mm`.
- Jaw travel: `20-30 mm` total opening range.
- Gear pitch radius: `10-14 mm`.
- Gear axes: symmetric about centerline, about `+/-25 mm` X from origin.
- Rack slide axes: parallel to X, one above/beside each gear pitch line.
- Servo: SG90 or similar hobby servo, fixed to base.
- Servo horn crank radius: `8-14 mm`.
- Center rod stroke: likely `8-16 mm`.
- Pivot holes: M2/M3 scale, final diameter based on selected fasteners.

## Work Breakdown

### Stage A: Catalog Search

Search `step.parts` for the servo, horn, fasteners, bearings/bushings, and
optional rails. Record results in this file before geometry generation.

### Stage B: Fixed Frame

Generate and validate the base/rail/gear-post/servo-mount subassembly.

### Stage C: Rack Jaws

Generate and validate sliding jaws and rail interfaces.

### Stage D: Gear And Linkage Kinematics

Generate simplified pitch-circle gears and linkage geometry first. Add detailed
teeth only after motion relationships are correct.

### Stage E: Integrated Assembly

Combine subassemblies, run inspect/snapshot, and sample open/mid/closed poses.

## Subagent Plan

Use subagents only after this interface spec is stable enough that their outputs
will mate:

- Subagent 1: fixed frame, rails, gear posts, servo mount.
- Subagent 2: sliding rack jaws and gripper pads.
- Subagent 3: gear/linkage/servo horn kinematics.
- Subagent 4: integration, validation, snapshots, and notes updates.

The integration agent owns interface conflicts. Subagents should not silently
change shared dimensions without updating this file.

## Open Questions

- Servo choice: SG90 for continuity, or a stronger servo for actual gripping?
- Gear detail: true teeth now, or pitch-circle placeholders until kinematics work?
- Rails: printed guide slots, metal rods, or catalog linear guides?
- Target jaw opening distance?
- Target object size and grip force?
- Should the first assembly be visual/static, or include sampled open/mid/closed poses?

## Stage A Results: Catalog Search

Instruction source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md

Relevant instruction:
Search `$step-parts` before creating simplified placeholder geometry for named
off-the-shelf actuators, servos, motors, electronics boards, connectors, or
other purchasable components. If no exact match is found, record the miss and
then use a documented envelope.

Search API source:
https://github.com/earthtojake/text-to-cad/blob/main/skills/step-parts/SKILL.md

### Servo

Action:
Searched `step.parts` for `SG90 servo`.

Result:
Exact catalog part found and selected.

- id: `sg90_micro_servo`
- page: https://www.step.parts/parts/sg90_micro_servo
- api: https://api.step.parts/v1/parts/sg90_micro_servo
- local STEP: `parts/sg90_micro_servo.step`
- catalog SHA-256: `7e9aeb4eebf5565e8dd049bb2697a001f2bbaf6de86ca118cef7e66e6268c19c`
- local SHA-256: `7e9aeb4eebf5565e8dd049bb2697a001f2bbaf6de86ca118cef7e66e6268c19c`

Decision:
Use the real SG90 STEP in the assembly instead of a guessed servo envelope.

### Servo Horn

Action:
Searched `step.parts` for likely names: `servo horn`, `SG90 horn`,
`servo arm`, and `rc servo horn`.

Result:
No exact catalog part found.

Decision:
Model the servo horn as a documented parametric envelope: a flat crank arm with
an SG90 output-axis center, a crank pin radius parameter, and clearance above
the base. This is allowed only because the catalog miss is recorded here.

### Gear Racks

Action:
Searched `step.parts` for `gear rack`.

Result:
Catalog gear racks exist. Useful candidates include:

- `gear_rack_m0_5_l0100`: module `0.5`, length `100 mm`, width `8 mm`
- `gear_rack_m0_8_l0100`: module `0.8`, length `100 mm`, width `8 mm`

Decision:
Use catalog rack dimensions as the first source of truth for rack size and
pitch. For the first v0 assembly, generate simplified rack geometry in source
so jaw length and tooth engagement can be parameterized, but keep the module
choice tied to these catalog rack families.

### Linear Guides

Action:
Searched `step.parts` for `linear rail`.

Result:
Catalog linear rails exist, including MGN-style rail parts such as MGN7/MGN12
families and `mgn7_linear_rail_l0100`.

Decision:
Do not import a metal rail for the first printed mechanism. Use printed guide
slots in the frame and document rail axes/clearance. Keep MGN7 rail as a future
upgrade path if the printed guide is too sloppy.

### Fasteners

Action:
Searched `step.parts` for `M3 screw`.

Result:
Catalog fasteners exist, including ISO 4762 socket head cap screws such as
`iso4762_socket_head_cap_screw_m3x10` and `iso4762_socket_head_cap_screw_m3x12`.

Decision:
Do not import individual screws into the first motion-layout STEP. Add M3
clearance/reference holes and only import screws when the plate thickness and
stackup are fixed.

### Bearings / Bushings

Action:
Searched `step.parts` for `3mm bearing`.

Result:
No useful exact part found from that query.

Decision:
Use simple shaft/post holes for the first layout. If the gear shafts become a
real bearing interface, search exact bearing series next, for example `623`,
`MR63`, or another selected bearing model.

## Stage B Defaults

Based on Stage A, the first generated assembly should use:

- verified real STEP: SG90 micro servo
- documented envelope: servo horn/crank
- generated source geometry: frame, rods, links, gears, printed guide slots
- catalog-informed parameters: gear rack module `0.8` unless first inspection
  shows the teeth are too small for a printable v0
- validation pose: mid/open visible static pose first, then add closed/open
  samples after geometry exports cleanly

## Stage B/C/D Result: First Integrated V0

Instruction sources:

- CAD generation: https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/step-generation.md
- build123d source pattern: https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/build123d-modeling.md
- assembly positioning: https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/positioning.md
- inspection: https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/references/inspection-and-validation.md

Actions:

- Created build123d source: `servo_rack_gripper_v0.py`
- Generated STEP: `servo_rack_gripper_v0.step`
- Rendered snapshot: `servo_rack_gripper_v0_20260609T064936Z.png`
- Used `AssemblyHelper` and named source frames for:
  - `base_origin`
  - `servo_output_axis`
  - `center_rod_slide_axis`
  - `rack_slide_axis`
  - `pinion_axis`

Text-to-CAD mapping:

- The source defines `gen_step()` and returns a STEP-ready labeled assembly,
  matching the step-generation instruction.
- Major dimensions are named parameters at the top of the file, matching the
  build123d modeling instruction to avoid buried magic numbers.
- Imported the verified SG90 STEP from `step.parts`, matching the named
  purchasable component instruction.
- Modeled the servo horn as a documented envelope because `step.parts` searches
  for horn aliases missed.
- Used source-level datums/frames for moving axes, matching the positioning
  instruction.
- Ran `inspect refs --facts --planes --positioning` on the generated STEP,
  matching the validation instruction.

Inspection result:

- ok: `true`
- occurrence count: `130`
- shape count: `118`
- face count: `731`
- STEP bounds: `208.0 x 139.2 x 37.4 mm`
- reported errors: none

Visual check:

The snapshot shows the intended motion chain in one static pose:

1. SG90 servo and documented horn.
2. Horn link to a central sliding rod.
3. Rod links to two gear crank pins.
4. Pinions adjacent to rack teeth.
5. Two rack jaws/fingers constrained by printed guide rails.

Known limitations in v0:

- The horn is an envelope, not a catalog STEP part.
- The rack and gear teeth are visual/layout geometry, not a verified involute
  gear mesh.
- The link positions are a plausible static pose, not a solved kinematic loop.
- The guide rails are printed guide references, not imported metal rails.
- Fasteners are omitted; M3 hole/screw details should wait until stackup is
  fixed.

Next repair/refinement target:

Build a small kinematic parameter pass that derives rod position, gear crank
angle, pinion rotation, and rack displacement from one `jaw_open_mm` or
`servo_angle_deg` parameter, then generate closed/mid/open snapshots.

## Stage E Result: Pose Variants

Action:
Updated `servo_rack_gripper_v0.py` so `GRIPPER_POSE=closed|mid|open` drives a
single source model.

Generated outputs:

- `servo_rack_gripper_closed.step`
- `servo_rack_gripper_mid.step`
- `servo_rack_gripper_open.step`
- `servo_rack_gripper_closed_20260609T065120Z.png`
- `servo_rack_gripper_mid_20260609T065120Z.png`
- `servo_rack_gripper_open_20260609T065130Z.png`
- `servo_rack_gripper_pose_review.gif`

Inspection results:

- closed: ok, bounds `192.0 x 139.2 x 37.4 mm`
- mid: ok, bounds `204.0 x 139.2 x 37.4 mm`
- open: ok, bounds `216.0 x 139.2 x 37.4 mm`
- reported errors: none

Text-to-CAD mapping:

- This follows the parameter guidance by deriving visible pose changes from a
  pose parameter instead of editing three separate files by hand.
- This follows the validation guidance by checking generated STEP bounds for
  each pose. The X bounds grow from closed to open, which confirms that the
  rack/jaw displacement is being applied.
- The GIF follows the snapshot guidance to use GIFs for motion/animation
  review, but it is a pose-review GIF made from discrete generated STEP poses,
  not a CAD Viewer live-parameter animation.

Important mechanical caveat:

The current pose math is still approximate. It derives servo angle, rod
position, pinion rotation, and rack displacement from the same pose fraction,
but it does not yet solve the linkage loop with fixed-length constraints. The
blue rods are therefore useful for layout communication, not yet proof that the
real mechanism can move through those positions without binding.

Next refinement:

Replace the approximate pose mapping with a 2D linkage solver:

- fixed inputs: servo axis, gear axes, link lengths, crank radii, rod slide axis
- driven input: `servo_angle_deg`
- solved outputs: rod position, left/right gear crank angles, rack displacement
- validation: fixed link lengths across closed/mid/open poses

## Off-The-Shelf Hardware Decisions

Date:
2026-06-10

Decision:
Keep the proof-of-concept as close to junk-garage hardware as possible. Favor
off-the-shelf motion parts over custom fabrication, and cut only the gripper
faces from cardboard for the first bench build.

Chosen linear guide:

- 5 inch drawer slides
- Reason: least hassle, fewest parts, direct bolt-down mounting, no shaft
  blocks or bearing housings required for v0

Ordered parts:

- `HAOHIZE 5inch Drawer Slides, 2PCS Soft Close Balls Bearing Drawer Runners Full Extension Side Mount Sliding Furniture Guide Undermount Drawer Mini Drawer Rails Table Cabinet Dresse 12.5cm/5in`
- `MECCANIXITY 4Pcs Adjustable Turnbuckles Camber Link, 64-74mm Turnbuckle Rod Steering Servo Linkage with M3 Ball Head Rod Ends for RC Car Replace Parts`
- `860PCS Metric Screw Assortment Kit, M2 M3 M4 M5 Machine Screws with Lock & Flat Washers, 10.9 Grade Alloy Steel, Metric Hex Button Head Cap Nuts and Bolts Assortment Kit with 4 Wrenches`
- `Bestol 34 Kinds of Rack and Pinion Gear Bag Toy Model Pulley Plastic Worm Gear Reducer`

Related search terms used:

- `servo linkage connector`
- `M3 turnbuckle linkage`
- `M3 ball link`
- `M3 threaded rod`

Interpretation:

- The drawer slides replace the earlier shaft + LM3UU idea for this v0.
- The turnbuckle links are the first linkage hardware candidate for the servo
  to slider connection.
- The screw assortment covers the M2/M3/M4/M5 hardware already expected by the
  CAD notes.
- The rack and pinion assortment is a source of off-the-shelf gear hardware,
  but only if pitch/module compatibility is usable for the mechanism layout.

Open follow-up:

- Decide whether the drawer-slide carriage gets a simple bolt-through tab or a
  small printed bracket for the linkage pickup point.
- Measure the actual neutral pivot spacing after the hardware arrives, then
  choose the final turnbuckle length.
