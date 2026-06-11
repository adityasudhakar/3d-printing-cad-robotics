from __future__ import annotations

import os
from math import atan2, cos, degrees, hypot, radians, sin
from pathlib import Path

from build123d import Axis, Box, Color, Compound, Cylinder, Location, import_step
from cadpy.assembly import AssemblyHelper, label_shape


# Coordinate convention:
# XY is the base plane, +Z is up. The fixed base origin is the plate center.
# This is a motion-layout assembly, not a final tolerance/print drawing.

HERE = Path(__file__).parent
PARTS = HERE / "parts"

pose_name = os.environ.get("GRIPPER_POSE", "mid").strip().lower()
pose_fraction_by_name = {
    "closed": 0.0,
    "mid": 0.5,
    "open": 1.0,
}
pose_fraction = pose_fraction_by_name.get(pose_name, 0.5)

base_length = 170.0
base_width = 95.0
base_thickness = 5.0

servo_axis_x = 0.0
servo_axis_y = 34.0
servo_axis_z = 24.0
servo_angle_deg = -38.0 + 76.0 * pose_fraction
servo_crank_radius = 13.0

rod_x = 0.0
rod_y = -1.0 + 12.0 * pose_fraction
rod_length = 54.0
rod_width = 7.0
rod_height = 5.0

gear_x = 32.0
gear_y = -12.0
gear_radius = 12.0
gear_height = 7.0
gear_tooth_count = 16
gear_tooth_length = 3.0
gear_tooth_width = 4.0

rack_module = 0.8
rack_length = 70.0
rack_width = 8.0
rack_height = 6.0
rack_y = -29.0
max_jaw_open_mm = 24.0
jaw_open_mm = max_jaw_open_mm * pose_fraction
pinion_rotation_deg = degrees((jaw_open_mm / 2.0) / gear_radius)

finger_length = 42.0
finger_width = 13.0
finger_height = 10.0

link_width = 5.0
link_height = 4.0
pin_radius = 2.4

WHITE = Color(0.92, 0.92, 0.88)
GRAY = Color(0.62, 0.66, 0.66)
DARK = Color(0.12, 0.12, 0.12)
PINK = Color(0.95, 0.42, 0.68)
YELLOW = Color(0.95, 0.78, 0.18)
BLUE = Color(0.10, 0.43, 0.86)
GREEN = Color(0.18, 0.62, 0.20)
ORANGE = Color(0.95, 0.45, 0.08)


def placed(shape, x: float, y: float, z: float, rz_deg: float = 0.0):
    return Location((x, y, z), (0, 0, rz_deg)) * shape


def place_on_base(shape, x: float, y: float, z: float, rz_deg: float = 0.0):
    bb = shape.bounding_box()
    centered = Location(
        (
            -((bb.min.X + bb.max.X) / 2.0),
            -((bb.min.Y + bb.max.Y) / 2.0),
            -bb.min.Z,
        )
    ) * shape
    return Location((x, y, z), (0, 0, rz_deg)) * centered


def bar_between(
    name: str,
    start: tuple[float, float],
    end: tuple[float, float],
    z: float,
    width: float,
    height: float,
    color: Color,
) -> Compound:
    sx, sy = start
    ex, ey = end
    length = hypot(ex - sx, ey - sy)
    angle = degrees(atan2(ey - sy, ex - sx))
    bar = label_shape(Box(length, width, height), name, color=color)
    body = placed(bar, (sx + ex) / 2.0, (sy + ey) / 2.0, z, angle)

    pins = []
    for pin_name, px, py in (("start", sx, sy), ("end", ex, ey)):
        pin = label_shape(Cylinder(radius=pin_radius, height=height + 2.0), f"{name}_pin", pin_name, color=color)
        pins.append(placed(pin, px, py, z))

    return label_shape(Compound(children=[body, *pins]), name)


def gear_crank_point(side: int) -> tuple[float, float]:
    crank_angle = radians(90.0 + side * 35.0 + side * pinion_rotation_deg)
    return (
        side * gear_x + cos(crank_angle) * 8.5,
        gear_y + sin(crank_angle) * 8.5,
    )


def make_base() -> Compound:
    plate = label_shape(Box(base_length, base_width, base_thickness), "base_plate", color=WHITE)

    guide_parts = []
    for side in (-1, 1):
        side_name = "left" if side < 0 else "right"
        jaw_center_x = side * (gear_x + 20.0 + jaw_open_mm / 2.0)
        for offset_y, rail_name in ((-7.0, "rear_guide"), (7.0, "front_guide")):
            rail = label_shape(Box(rack_length + 18.0, 3.2, 5.0), "printed_guide_rail", side_name, rail_name, color=GRAY)
            guide_parts.append(placed(rail, jaw_center_x, rack_y + offset_y, base_thickness / 2.0 + 2.5))

    posts = []
    for side in (-1, 1):
        post = label_shape(Cylinder(radius=3.4, height=12.0), "gear_post", "left" if side < 0 else "right", color=GRAY)
        posts.append(placed(post, side * gear_x, gear_y, base_thickness / 2.0 + 6.0))

    servo_mount = label_shape(Box(34.0, 28.0, 7.0), "sg90_mount_envelope", color=GRAY)
    servo_mount = placed(servo_mount, 0.0, 43.0, base_thickness / 2.0 + 3.5)

    rod_guides = []
    for y in (-7.0, 19.0):
        guide = label_shape(Box(18.0, 4.0, 10.0), "center_rod_guide", f"y{y:g}", color=GRAY)
        rod_guides.append(placed(guide, 0.0, y, base_thickness / 2.0 + 5.0))

    return label_shape(Compound(children=[plate, *guide_parts, *posts, servo_mount, *rod_guides]), "fixed_frame")


def make_rack_jaw(side: int) -> Compound:
    side_name = "left" if side < 0 else "right"
    center_x = side * (gear_x + 20.0 + jaw_open_mm / 2.0)
    z = base_thickness / 2.0 + rack_height / 2.0 + 1.5

    rack = label_shape(Box(rack_length, rack_width, rack_height), "generated_rack_bar", side_name, color=PINK)
    rack = placed(rack, center_x, rack_y, z)

    tooth_parts = []
    tooth_pitch = rack_module * 3.14159
    tooth_count = int(rack_length / tooth_pitch) - 2
    first_x = center_x - side * (rack_length / 2.0 - tooth_pitch)
    tooth_y = rack_y + rack_width / 2.0 + 1.8
    for i in range(tooth_count):
        tx = first_x + side * i * tooth_pitch
        tooth = label_shape(Box(tooth_pitch * 0.48, 3.4, rack_height), "rack_tooth_m0_8", side_name, i + 1, color=PINK)
        tooth_parts.append(placed(tooth, tx, tooth_y, z, side * 8.0))

    finger_x = side * (base_length / 2.0 - 18.0)
    finger = label_shape(Box(finger_width, finger_length, finger_height), "gripper_finger", side_name, color=PINK)
    finger = placed(finger, finger_x, rack_y - 24.0, base_thickness / 2.0 + finger_height / 2.0 + 1.5)

    pad = label_shape(Box(finger_width + 5.0, 8.0, finger_height + 2.0), "flat_grip_pad", side_name, color=PINK)
    pad = placed(pad, finger_x, rack_y - 48.0, base_thickness / 2.0 + (finger_height + 2.0) / 2.0 + 1.5)

    return label_shape(Compound(children=[rack, finger, pad, *tooth_parts]), "sliding_rack_jaw", side_name)


def make_pinion(side: int) -> Compound:
    side_name = "left" if side < 0 else "right"
    z = base_thickness / 2.0 + gear_height / 2.0 + 3.0
    phase = side * (15.0 + pinion_rotation_deg)

    core = label_shape(Cylinder(radius=gear_radius, height=gear_height), "pinion_pitch_body", side_name, color=YELLOW)
    core = placed(core, side * gear_x, gear_y, z)

    teeth = []
    for i in range(gear_tooth_count):
        angle = 360.0 * i / gear_tooth_count + phase
        tx = side * gear_x + cos(radians(angle)) * (gear_radius + gear_tooth_length / 2.0)
        ty = gear_y + sin(radians(angle)) * (gear_radius + gear_tooth_length / 2.0)
        tooth = label_shape(Box(gear_tooth_length, gear_tooth_width, gear_height), "pinion_tooth", side_name, i + 1, color=YELLOW)
        teeth.append(placed(tooth, tx, ty, z, angle))

    hub = label_shape(Cylinder(radius=4.6, height=gear_height + 4.0), "pinion_hub", side_name, color=YELLOW)
    hub = placed(hub, side * gear_x, gear_y, base_thickness / 2.0 + (gear_height + 4.0) / 2.0 + 3.0)

    crank_pin_x, crank_pin_y = gear_crank_point(side)
    crank_pin = label_shape(Cylinder(radius=2.8, height=gear_height + 5.0), "gear_crank_pin", side_name, color=ORANGE)
    crank_pin = placed(crank_pin, crank_pin_x, crank_pin_y, base_thickness / 2.0 + (gear_height + 5.0) / 2.0 + 7.0)

    return label_shape(Compound(children=[core, hub, crank_pin, *teeth]), "pinion_with_crank", side_name)


def make_servo_and_horn() -> Compound:
    servo = import_step(PARTS / "sg90_micro_servo.step")
    servo = place_on_base(servo, 0.0, 42.0, base_thickness, rz_deg=0.0)

    horn_angle = servo_angle_deg - 90.0
    horn = label_shape(Box(servo_crank_radius * 2.0 + 8.0, 5.5, 3.0), "documented_servo_horn_envelope", color=GREEN)
    horn = placed(horn, servo_axis_x, servo_axis_y, servo_axis_z, horn_angle)

    hub = label_shape(Cylinder(radius=4.5, height=4.0), "servo_output_axis_marker", color=GREEN)
    hub = placed(hub, servo_axis_x, servo_axis_y, servo_axis_z)

    crank_pin_x = servo_axis_x + cos(radians(horn_angle)) * servo_crank_radius
    crank_pin_y = servo_axis_y + sin(radians(horn_angle)) * servo_crank_radius
    crank_pin = label_shape(Cylinder(radius=2.6, height=5.0), "servo_crank_pin", color=ORANGE)
    crank_pin = placed(crank_pin, crank_pin_x, crank_pin_y, servo_axis_z)

    return label_shape(Compound(children=[servo, horn, hub, crank_pin]), "sg90_servo_and_documented_horn")


def make_rod_and_links() -> Compound:
    z = base_thickness / 2.0 + 13.0
    rod = label_shape(Box(rod_width, rod_length, rod_height), "center_sliding_rod", color=GREEN)
    rod = placed(rod, rod_x, rod_y, z)

    rod_front = (rod_x, rod_y - rod_length / 2.0 + 5.0)
    rod_rear = (rod_x, rod_y + rod_length / 2.0 - 5.0)

    horn_angle = servo_angle_deg - 90.0
    servo_pin = (
        servo_axis_x + cos(radians(horn_angle)) * servo_crank_radius,
        servo_axis_y + sin(radians(horn_angle)) * servo_crank_radius,
    )

    children = [rod]
    children.append(bar_between("servo_to_rod_link", servo_pin, rod_rear, z + 5.0, link_width, link_height, BLUE))

    for side in (-1, 1):
        gear_pin = gear_crank_point(side)
        children.append(bar_between("rod_to_gear_link", rod_front, gear_pin, z, link_width, link_height, BLUE))

    return label_shape(Compound(children=children), "center_rod_and_linkages")


def gen_step():
    asm = AssemblyHelper(f"servo_driven_rack_gripper_v0_{pose_name}")

    frame = asm.add(make_base(), "fixed_frame", "printed")
    asm.rigid_frame(frame, "base_origin", Location((0, 0, 0)))

    servo = asm.add(make_servo_and_horn(), "sg90_servo_with_documented_horn", "input_actuator")
    asm.revolute_frame(
        servo,
        "servo_output_axis",
        Axis((servo_axis_x, servo_axis_y, servo_axis_z), (0, 0, 1)),
        angular_range=(-45, 45),
    )

    rod_links = asm.add(make_rod_and_links(), "center_rod_and_linkages", "motion_pose")
    asm.linear_frame(
        rod_links,
        "center_rod_slide_axis",
        Axis((rod_x, rod_y, base_thickness / 2.0 + 13.0), (0, 1, 0)),
        linear_range=(-8, 12),
    )

    for side in (-1, 1):
        side_name = "left" if side < 0 else "right"
        jaw = asm.add(make_rack_jaw(side), "sliding_rack_jaw", side_name)
        asm.linear_frame(
            jaw,
            "rack_slide_axis",
            Axis((side * (gear_x + 20.0), rack_y, base_thickness / 2.0 + rack_height / 2.0), (1, 0, 0)),
            linear_range=(-jaw_open_mm / 2.0, jaw_open_mm / 2.0),
        )

        pinion = asm.add(make_pinion(side), "pinion_with_crank", side_name)
        asm.revolute_frame(
            pinion,
            "pinion_axis",
            Axis((side * gear_x, gear_y, base_thickness / 2.0 + gear_height / 2.0 + 3.0), (0, 0, 1)),
            angular_range=(-55, 55),
        )

    return asm.build()


if __name__ == "__main__":
    from build123d import export_step

    export_step(gen_step(), "servo_rack_gripper_v0.step")
