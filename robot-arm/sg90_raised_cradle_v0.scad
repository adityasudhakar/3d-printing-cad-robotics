// SG90 raised servo cradle - v0
// Fixed base for a simple elbow joint.
//
// Layout:
// - base flange with screw holes
// - raised pedestal
// - SG90 servo pocket/cradle
// - open shaft side
// - side wire exit

$fn = 64;

// ----- Servo assumptions -----
// Orientation for an elbow test:
// X = shaft axis / servo depth
// Y = mounting-ear span
// Z = thin servo thickness
servo_depth_x = 25.0;
servo_ear_span_y = 31.8;
servo_body_span_y = 22.4;
servo_thickness_z = 12.5;

// Approximate SG90 ear screw spacing derived from the product image.
// Tune this after measuring the real servo.
servo_ear_hole_spacing_y = 27.1;
servo_ear_pilot_d = 1.8; // pilot for tiny servo screws or M2 self-tapping
servo_ear_hole_z = servo_thickness_z / 2;

// Desired output shaft center height above the board.
shaft_height_above_board = 42.0;

// ----- Clearances and wall sizes -----
// Loose fit-check clearances. Product diagrams are nominal, and small FDM
// pockets routinely print tight, so this version intentionally gives room.
depth_clearance_x = 2.0;
body_clearance_y = 1.6;
ear_clearance_y = 1.2;
thickness_clearance_z = 1.2;
lead_in_extra = 1.2;
lead_in_depth = 1.2;
wall = 3.0;
floor_thickness = 3.0;
join_overlap = 0.2;

// ----- Base and pedestal -----
base_len = 72;
base_width = 56;
base_thickness = 4;
base_corner_r = 4;

pedestal_len = servo_depth_x + wall;
pedestal_width = servo_ear_span_y + ear_clearance_y;
pedestal_height = shaft_height_above_board
    - base_thickness
    - floor_thickness
    - servo_thickness_z / 2;

// ----- Mounting screw holes -----
mount_hole_d = 3.2;       // clearance for M3 or similar wood screw
mount_hole_inset_x = 8;
mount_hole_inset_y = 8;

// ----- Wire exit -----
wire_exit_width = 8;
wire_exit_height = servo_thickness_z + thickness_clearance_z + 0.5;
side_rail_width = (servo_ear_span_y - servo_body_span_y) / 2;

module rounded_box(size, r) {
    hull() {
        for (x = [r, size[0] - r])
            for (y = [r, size[1] - r])
                translate([x, y, 0])
                    cylinder(h = size[2], r = r);
    }
}

module base_flange() {
    difference() {
        rounded_box([base_len, base_width, base_thickness], base_corner_r);

        for (x = [mount_hole_inset_x, base_len - mount_hole_inset_x])
            for (y = [mount_hole_inset_y, base_width - mount_hole_inset_y])
                translate([x, y, -0.1])
                    cylinder(h = base_thickness + 0.2, d = mount_hole_d);
    }
}

module pedestal() {
    translate([
        (base_len - pedestal_len) / 2,
        (base_width - pedestal_width) / 2,
        base_thickness - join_overlap
    ])
        cube([pedestal_len, pedestal_width, pedestal_height + join_overlap], center = false);
}

module servo_cradle() {
    cradle_len = servo_depth_x + depth_clearance_x + wall;
    cradle_width = servo_ear_span_y + ear_clearance_y;
    cradle_height = servo_thickness_z + thickness_clearance_z + floor_thickness;

    cradle_x = (base_len - cradle_len) / 2;
    cradle_y = (base_width - cradle_width) / 2;
    cradle_z = base_thickness + pedestal_height - join_overlap;

    difference() {
        translate([cradle_x, cradle_y, cradle_z])
            cube([cradle_len, cradle_width, cradle_height], center = false);

        // Main servo body pocket, open at top.
        // This is narrower than the full ear span so the ears land on side rails.
        translate([
            cradle_x - 0.1,
            cradle_y + cradle_width / 2 - servo_body_span_y / 2 - body_clearance_y / 2,
            cradle_z + floor_thickness
        ])
            cube([
                servo_depth_x + depth_clearance_x + 0.2,
                servo_body_span_y + body_clearance_y,
                servo_thickness_z + thickness_clearance_z + 0.5
            ], center = false);

        // Extra top lead-in to reduce sharp-edge interference during fit checks.
        translate([
            cradle_x - 0.1,
            cradle_y + cradle_width / 2 - servo_body_span_y / 2 - body_clearance_y / 2 - lead_in_extra / 2,
            cradle_z + cradle_height - lead_in_depth
        ])
            cube([
                servo_depth_x + depth_clearance_x + 0.2,
                servo_body_span_y + body_clearance_y + lead_in_extra,
                lead_in_depth + 0.2
            ], center = false);

        // Side wire exit channel.
        translate([
            cradle_x + cradle_len * 0.55,
            cradle_y - 0.1,
            cradle_z + floor_thickness
        ])
            cube([
                wire_exit_width,
                side_rail_width + body_clearance_y / 2 + ear_clearance_y / 2 + 0.4,
                wire_exit_height
            ], center = false);

        // Servo ear screw pilot holes, horizontal through the cradle.
        // These align with the ears; they are not floor holes.
        for (y = [
            cradle_y + cradle_width / 2 - servo_ear_hole_spacing_y / 2,
            cradle_y + cradle_width / 2 + servo_ear_hole_spacing_y / 2
        ])
            translate([
                cradle_x - 0.1,
                y,
                cradle_z + floor_thickness + servo_ear_hole_z
            ])
                rotate([0, 90, 0])
                    cylinder(h = cradle_len + 0.2, d = servo_ear_pilot_d);
    }
}

module sg90_raised_cradle() {
    union() {
        base_flange();
        pedestal();
        servo_cradle();
    }
}

sg90_raised_cradle();
