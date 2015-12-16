$fn = 120;

outerdiameter = 105;
innerdiameter = outerdiameter - 4;

rotate([180,0,0]) {
    difference() {
        translate([0,0,5/2])
            cube([48,20,15], center=true);
    
        union() {
            cylinder(r=5.6/2, h=21, center=true);
            
            translate([18,0,4])
                rotate([90,0,0])
                cylinder(r=6/2, h=22, center=true);
            
            translate([-18,0,4])
                rotate([90,0,0])
                cylinder(r=6/2, h=22, center=true);
        
            translate([0,0,-outerdiameter/2])
                rotate([90,0,0])
                cylinder(r=innerdiameter/2, h=22, center=true);
            translate([0,6,-outerdiameter/2])
                rotate([90,0,0])
                cylinder(r=outerdiameter/2, h=10, center=true);
            translate([0,-6,-outerdiameter/2])
                rotate([90,0,0])
                cylinder(r=outerdiameter/2, h=10, center=true);
        }
    }
}