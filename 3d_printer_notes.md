# 3D Printer Setup Notes (Creality Ender 3)

## Session Summary
- Bought used printer
- Learned controls and SD card usage
- Fixed bed leveling issue
- Successfully completed first print 🎉

---

## Images from Setup


---

## Key Learnings

### SD Card
- Stores `.gcode` print files
- Files were from previous owner

### Controls
- Knob = scroll + click
- Menu: Print / Prepare / Control / Info

### Axes
- X: left/right
- Y: bed forward/back
- Z: nozzle height

---

## Bed Leveling (Critical)
Steps:
1. Lower bed via knobs (compress springs)
2. Auto Home
3. Disable steppers
4. Paper test → slight drag
5. Repeat for all 4 corners

---

## First Print
- Used `doorhook.gcode`
- Initial delay = heating
- Print succeeded

---

## Mechanical Notes
- Blue knobs = belt / wheel tension
- Should be snug, not tight

---

## Safety
- Don’t drag nozzle on bed
- Don’t force axes when motors active

---

## Mental Model
> Everything depends on nozzle distance from bed

---

## Status
- Printer working ✅
- First print done ✅

Next:
- Try new prints
- Learn slicing tools

---

# CAD Landscape Notes

## The Car/Engine Analogy

CAD tools are like cars built on different engines. The "engines" are geometric kernels — the core math libraries that handle geometry representation and operations.

---

## Geometric Kernels ("Engines")

| Kernel | Owner | Type |
|--------|-------|------|
| **Parasolid** | Siemens | Commercial, licensed widely |
| **ACIS** | Spatial (Dassault) | Commercial, licensed widely |
| **CGM** | Dassault | Proprietary, internal use |
| **Granite** | PTC | Proprietary, internal use |
| **Open CASCADE (OCCT)** | Open CASCADE SAS | Open source (LGPL) |
| **C3D** | C3D Labs | Commercial, Russian origin |

---

## CAD Applications ("Cars")

| Application | Kernel | Owner |
|-------------|--------|-------|
| **CATIA** | CGM | Dassault |
| **SolidWorks** | Parasolid | Dassault |
| **NX** | Parasolid | Siemens |
| **Solid Edge** | Parasolid | Siemens |
| **Creo** | Granite | PTC |
| **Onshape** | Parasolid | PTC |
| **Inventor** | ShapeManager (ACIS fork) | Autodesk |
| **Fusion 360** | Hybrid (Parasolid + custom) | Autodesk |
| **FreeCAD** | Open CASCADE | Community |
| **BRL-CAD** | Custom | US Army / OSS |

---

## Why SolidWorks vs NX? (Same Kernel, Different Product)

The kernel is ~20% of what you're paying for. What differentiates:

| Layer | What it is |
|-------|-----------|
| UI/UX | How you sketch, constrain, navigate |
| Feature tree logic | How operations stack, resolve, rebuild |
| Surfacing tools | Class-A, subdivision, lofting quality |
| Assembly architecture | 10 parts vs 100,000 parts |
| Simulation integration | FEA, CFD, tolerance analysis |
| CAM/manufacturing | Toolpaths, NC output, DFM checks |
| PLM/PDM integration | Version control, BOM management |
| Ecosystem | Plugins, libraries, community, training |

| | SolidWorks | NX |
|--|------------|-----|
| Target | Mid-market, SMBs | Enterprise, aerospace/auto |
| Learning curve | Approachable | Steep but deep |
| Price | ~$4-8k/yr | ~$15-25k+/yr |
| Assembly scale | Hundreds to low thousands | Full aircraft/vehicles |

Real moat = switching cost + ecosystem lock-in (trained workforce, file libraries, integrated toolchains, supplier compatibility).

---

## Open CASCADE in Practice

| Segment | OCCT presence |
|---------|---------------|
| Hobbyist/maker | Strong (FreeCAD, CadQuery, Build123d) |
| Niche/vertical tools | Common (shipbuilding, architecture) |
| Internal corporate tools | Quiet but real |
| Mid-market CAD | Rare |
| Enterprise CAD | Almost nonexistent |

**Why enterprises don't use it:**
1. Boolean operations fail on edge cases Parasolid handles
2. No vendor support when things break
3. You build everything else yourself (feature tree, constraints, assembly logic)
4. Talent pool is smaller

**Code-first CAD (CadQuery, Build123d):** Different use case — parametric parts libraries, generative design, automated fixtures. Not replacing GUI CAD.

---

## Hobbyist Path

**Do skills transfer from OCCT tools to Parasolid tools?**
Yes — you almost never "see" the kernel. What transfers:
- Sketch → constrain → extrude/revolve mental model
- Feature tree / design intent thinking
- Boolean operations intuition
- Assembly strategies

What doesn't: UI muscle memory, feature-specific quirks.

**Free/cheap Parasolid tools for hobbyists:**

| Tool | Price | Notes |
|------|-------|-------|
| Onshape | Free tier | Browser-based, projects public on free plan |
| Solid Edge Community | Free | Siemens' own, hobbyist license |
| SolidWorks Maker | ~$99/yr | For 3D printing/maker use |
| Fusion 360 | Free (personal) | Hybrid kernel, some features gated |

---

## "Thinking in Sketches and Constraints"

**Sketch:** 2D profile on a plane (lines, arcs, circles) that becomes 3D via extrude, revolve, sweep.

**Constraints:** Geometric relationships within the sketch (NOT physical constraints like weight/collisions):

| Constraint | Meaning |
|------------|---------|
| Horizontal | Line stays horizontal |
| Coincident | Point touches point |
| Equal | Two lines always same length |
| Tangent | Arc smoothly meets line |
| Concentric | Circles share center |
| Dimension | Edge = 10mm |

Fully constrained sketch = parametric. Change one number, everything updates while preserving relationships.

**Physical stuff (weight, collisions) = simulation/FEA, happens after geometry.**

---

## AI + CAD: Are Clicks Going Away?

Probably not entirely. Mix is shifting:

| Task | AI impact |
|------|-----------|
| Simple parts | Text-to-CAD getting real |
| Complex assemblies | Still needs human intent |
| Design iteration | AI proposes, human curates |
| Manufacturing-aware design | Human for now |

Code-CAD (Build123d/CadQuery) may become the intermediate representation — describe → AI writes code → tweak code → geometry updates.

Even with AI, need to review and constrain output. Knowing CAD concepts makes you a better AI wrangler.

---

## Learning Project: Side-by-Side Comparison

**Build:** Raspberry Pi Zero case
- Box with lid (snap fit or screw bosses)
- Cutouts for USB, mini HDMI, SD card
- Mounting holes matching Pi Zero pattern
- Ventilation slots
- 1.5-2mm walls (printable)

**Experiment:**
1. Text-to-CAD first — describe, iterate via prompts
2. Onshape second — build with proper constraints, then make changes

**Compare:**
| | Text-to-CAD | Onshape |
|--|-------------|---------|
| First draft speed | Faster | Slower |
| Making changes | Regenerate? | Change one dimension |
| Lid-to-box alignment | Hope | Defined relationship |
| Learning CAD | Not really | Yes |

Key question: when you need to change something, which workflow lets you do it without starting over?

---

# Project Plan: Pi Zero Case Comparison

## How text-to-cad Works

**Stack:**
```
You (natural language) → Claude Code/Cursor → Build123d Python → OCCT → STEP → CAD Explorer
```

**Workflow:**
1. Describe what you want in plain English
2. Agent converts to a "brief" (structured spec)
3. Agent writes `gen_step()` Python function using Build123d
4. Run `python scripts/step target.py` → generates `.step` file
5. Run `python scripts/inspect` → validates dimensions, geometry
6. Open in CAD Explorer → visual review
7. If broken → repair loop (agent reads errors, fixes code, regenerates)

**Key insight:** The AI writes code, not clicks. You can read/edit the generated Build123d code directly.

---

## Phase 1: Setup

| Task | Details |
|------|---------|
| **1.1 Install text-to-cad** | `npx skills add earthtojake/text-to-cad` in Claude Code |
| **1.2 Install Python deps** | `python3.11 -m venv .venv && .venv/bin/pip install -r skills/cad/requirements.txt` |
| **1.3 Install CAD Explorer** | `npm --prefix skills/render/scripts/viewer install` |
| **1.4 Create Onshape account** | Free tier at onshape.com (projects public) |
| **1.5 Get Pi Zero dimensions** | 65mm × 30mm × 5mm board, hole pattern, port locations |

---

## Phase 2: Design Spec (Same for Both)

**Pi Zero Case Requirements:**
- Two-part enclosure: base + lid
- Internal dimensions: 67mm × 32mm × 12mm (2mm clearance around board)
- Wall thickness: 2mm
- Snap-fit or screw bosses (4x M2.5) for lid attachment
- Cutouts: micro USB power, micro USB data, mini HDMI, SD card slot
- 4x mounting standoffs matching Pi Zero hole pattern (58mm × 23mm, 2.4mm holes)
- Ventilation slots on top
- Corner fillets: 2mm external

---

## Phase 3: Build in text-to-cad

| Step | What happens |
|------|--------------|
| **3.1** | Describe the case to Claude Code with CAD skill active |
| **3.2** | Agent writes brief, then Build123d Python code |
| **3.3** | Generate STEP: `python scripts/step pi_zero_case.py` |
| **3.4** | Inspect: `python scripts/inspect refs pi_zero_case.step --facts --planes` |
| **3.5** | View in CAD Explorer |
| **3.6** | Iterate via natural language ("move the USB cutout 2mm left") |
| **3.7** | When lid doesn't fit base → observe repair loop |

**Log these:**
- Time to first "looks right" geometry
- Number of regeneration cycles
- What broke and how it got fixed
- Did you understand the generated code?

---

## Phase 4: Build in Onshape

| Step | What happens |
|------|--------------|
| **4.1** | Create new document |
| **4.2** | Sketch base profile, constrain fully |
| **4.3** | Extrude, shell, add features |
| **4.4** | Create lid as new part, reference base dimensions |
| **4.5** | Add cutouts, standoffs, snap fits |
| **4.6** | Make a change ("wall thickness 2.5mm instead of 2mm") |
| **4.7** | Observe what updates automatically |

**Log these:**
- Time to first complete model
- How many constraints did you set?
- What happened when you changed a dimension?
- Did lid-to-base alignment break?

---

## Phase 5: Compare

| Dimension | text-to-cad | Onshape |
|-----------|-------------|---------|
| Time to first draft | | |
| Time to make a change | | |
| Confidence parts will fit | | |
| Understood what you built | | |
| Could you edit without AI | | |
| What broke | | |
| How it recovered | | |

---

## Phase 6: Document

Add findings back here:
- Which workflow felt better for what
- Where AI helped vs hindered
- Whether you'd use text-to-cad for real projects
- What you learned about parametric CAD concepts

---

## Phase 7 (Optional): Print It

Export STL from both, slice in Cura, print on Ender 3. See if the parts actually fit a real Pi Zero.
