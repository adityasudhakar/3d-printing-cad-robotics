# 3D Printer Notes And CAD Practice

This repo is about exploring how AI can help with CAD for hobby 3D printing.

It combines printer setup notes, simple OpenSCAD models, exported print assets, and iteration on fit, adhesion, and slicer settings.

## Stack Summary

- Printer: `Creality Ender 3`
- CAD: `OpenSCAD`
- Editable model source: `.scad`
- Mesh export for slicing: `.stl`
- Slicer: `Cura`
- Printer file format: `.gcode`
- Material used so far: `PLA`

## Repo Contents

- `3d_printer_notes.md`: setup notes and lessons from getting the Ender 3 running
- `flanged nut/`: early OpenSCAD practice around a flanged-nut side-load block and a simple `M5` practice part
- `candy dispenser/`: AI-recreated candy dispenser CAD, print exports, and assembly images
- `robot-arm/vision-turret/`: chipboard `SG90` pan/tilt turret mockup for CV-guided laser pointer experiments

## Workflow

1. Design or edit the part in `OpenSCAD`.
2. Preview with `F5` and render with `F6`.
3. Export to `STL`.
4. Slice the `STL` in `Cura`.
5. Save the `G-code` to an SD card and print on the `Ender 3`.

## Notes From Setup

The current setup notes are in [3d_printer_notes.md](3d_printer_notes.md). The short version:

- the printer is a used `Ender 3`
- bed leveling was a critical early fix
- the first successful print was a door hook from an existing `G-code` file
- printer success mostly comes down to correct nozzle distance from the bed

## Current Focus

- learn how bolt and nut geometry maps into simple printed parts
- use AI to help draft and revise `OpenSCAD` models
- recreate simple mechanisms from reference images using AI-assisted CAD iteration
- iterate on practical print issues like fit, first-layer adhesion, and slicer temperatures

## Print Photo

Printed flanged nut side-load block test:

![Printed flanged nut side-load block](flanged%20nut/flanged-nut-side-load-block.jpg)

## Rotated CAD View (peek into side slot)

![Rotated CAD view (peek into side slot)](renders/flanged_peek_z270_x80.png)
