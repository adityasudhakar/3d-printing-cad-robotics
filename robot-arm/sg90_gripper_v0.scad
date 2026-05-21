// SG90 gripper - v0
// Step 1: movable gripper jaw as a simple L shape.

$fn = 48;

// Set true before STL/G-code export so preview rotation is ignored.
EXPORT_FOR_PRINT = true;

// "movable", "fixed", or "both"
PART = "fixed";

// Change this for easier OpenSCAD viewing.
// Examples: [90, 0, 0], [0, 90, 0], [0, 0, 90]
view_rotation = [0, 0, 0];

// L jaw dimensions.
// X is thickness through the part.
// Y/Z form the L profile.
short_leg_len = 10; // mm, protruding hook length in Z
long_leg_len = 30;  // mm, long leg length in Y
jaw_x = 10;          // mm
jaw_z = 2;         // mm

// Gripping pad on the far end of the long leg.
grip_pad_x = 25; // mm
grip_pad_y = 10; // mm
grip_pad_z = 2;  // mm

module movable_l_jaw() {
    union() {
        // Long leg of the L, 30 mm in Y and 10 mm in Z.
        cube([jaw_x, long_leg_len, jaw_z], center = false);

        // Short leg of the L, protruding 10 mm in Z from one end.
        cube([jaw_x, jaw_z, jaw_z + short_leg_len], center = false);

        // Raised gripping pad at the end of the long leg.
        translate([
            jaw_x,
            long_leg_len - grip_pad_y,
            0
        ])
            cube([grip_pad_x, grip_pad_y, grip_pad_z], center = false);
    }
}

module fixed_l_jaw() {
    union() {
        // Same long leg as movable jaw.
        cube([jaw_x, long_leg_len, jaw_z], center = false);

        // Same gripping pad, but no 10 mm short/upright leg.
        translate([
            jaw_x,
            long_leg_len - grip_pad_y,
            0
        ])
            cube([grip_pad_x, grip_pad_y, grip_pad_z], center = false);
    }
}

module selected_part() {
    if (PART == "movable")
        movable_l_jaw();
    else if (PART == "fixed")
        fixed_l_jaw();
    else if (PART == "both") {
        movable_l_jaw();
        translate([22, 0, 0])
            fixed_l_jaw();
    }
}

if (EXPORT_FOR_PRINT)
    selected_part();
else
    rotate(view_rotation)
        selected_part();
