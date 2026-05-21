// Stage 1: simple dogleg forearm block
// X = length/reach, Y = width, Z = height
//
// First 10 mm runs straight along X.
// Remaining 30 mm bends 40 degrees in the XZ plane at [10, 0, 0].

length_x = 40;
width_y = 5;
height_z = 10;
bend_x = 10;
bend_angle = -40;

seg1_len = bend_x;
seg2_len = length_x - bend_x;

servo_body_clearance_y = 24.0;
servo_ear_hole_spacing_y = 27.1;
servo_ear_span_y = 31.8;
servo_ear_clearance_y = 1.2;
fork_prong_w = 5;
fork_gap_y = servo_body_clearance_y;
fork_total_w = fork_gap_y + 2 * fork_prong_w;
fork_upper_prong_len = 15;
fork_lower_prong_len = 15;
fork_back_len = 2;
fork_ear_pilot_d = 2.0;
fork_ear_pilot_x = 8;
fork_ear_pilot_depth = 3.5;
fork_back_guide_d = 2.0;
fork_back_guide_spacing_z = 5.0;
servo_body_cut_y = 26.0;
servo_body_cut_z = 5.0;
arm_tip_pilot_d = 2.0;
arm_tip_pilot_depth = 8;

// "both", "arm", "fork", "arm_print_side", or "fork_print_top_down"
show_part = "both";

module arm_segment(len) {
    cube([len, width_y, height_z], center = false);
}

module asymmetric_tuning_fork_jaw() {
    total_w = fork_total_w;
    center_y = width_y / 2;
    upper_y = center_y + fork_gap_y / 2;
    lower_y = center_y - fork_gap_y / 2 - fork_prong_w;

    difference() {
        union() {
            // Thin back bridge joins the narrow arm to the two prongs.
            translate([0, center_y - total_w / 2, 0])
                cube([fork_back_len, total_w, height_z], center = false);

            // Two straight prongs extend forward with the notch between them.
            translate([fork_back_len, upper_y, 0])
                cube([fork_upper_prong_len, fork_prong_w, height_z], center = false);

            translate([fork_back_len, lower_y, 0])
                cube([fork_lower_prong_len, fork_prong_w, height_z], center = false);
        }

        // Pilot holes for the SG90 ear screws, drilled vertically into shelves.
        for (y = [
            center_y - servo_ear_hole_spacing_y / 2,
            center_y + servo_ear_hole_spacing_y / 2
        ])
            translate([fork_back_len + fork_ear_pilot_x, y, height_z - fork_ear_pilot_depth])
                cylinder(h = fork_ear_pilot_depth + 0.1, d = fork_ear_pilot_d);

        // Servo body clearance cut inside the prong area.
        translate([
            fork_back_len,
            center_y - servo_body_cut_y / 2,
            0
        ])
            cube([fork_upper_prong_len + 0.2, servo_body_cut_y, servo_body_cut_z], center = false);

        // Guide holes through the thin back wall for screwing this fork to the arm.
        for (z = [
            height_z / 2 - fork_back_guide_spacing_z / 2,
            height_z / 2 + fork_back_guide_spacing_z / 2
        ])
            translate([-0.1, width_y / 2, z])
                rotate([0, 90, 0])
                    cylinder(h = fork_back_len + 0.2, d = fork_back_guide_d);
    }
}

module dogleg_arm() {
    difference() {
        union() {
            arm_segment(seg1_len);

            translate([bend_x, 0, 0])
                rotate([0, bend_angle, 0])
                    arm_segment(seg2_len);
        }

        translate([bend_x, 0, 0])
            rotate([0, bend_angle, 0])
                translate([seg2_len - arm_tip_pilot_depth, width_y / 2, height_z / 2])
                    rotate([0, 90, 0])
                        cylinder(h = arm_tip_pilot_depth + 0.2, d = arm_tip_pilot_d, center = false);
    }
}

if (show_part == "arm") {
    dogleg_arm();
} else if (show_part == "fork") {
    asymmetric_tuning_fork_jaw();
} else if (show_part == "arm_print_side") {
    // Rotate arm so the 5 mm Y width becomes print height Z.
    // This lays the 10 mm tall side face on the build plate.
    rotate([90, 0, 0])
        dogleg_arm();
} else if (show_part == "fork_print_top_down") {
    // Flip fork so the original top/shelf face sits on the bed.
    translate([0, 0, height_z])
        rotate([180, 0, 0])
            asymmetric_tuning_fork_jaw();
} else {
    dogleg_arm();

    translate([bend_x, 0, 0])
        rotate([0, bend_angle, 0])
            translate([seg2_len, 0, 0])
                asymmetric_tuning_fork_jaw();
}
