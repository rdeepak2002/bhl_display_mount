import math
import cadquery as cq
from cadquery.vis import show_object

# Parameters for the L-shaped mount
base_plate_length = 50.0  # Length of base plate (M3 side)
angled_plate_length = 25.0  # Length of angled plate (M2.5 side)
plate_width = 20.0   # Width of the plates
plate_thickness = 5.0  # Thickness of the plates
angle = 70.0  # Angle between the two plates in degrees

# Screw hole parameters
m3_hole_diameter = 3.2  # M3 clearance hole
m2_5_hole_diameter = 2.7  # M2.5 clearance hole
base_hole_offset = 15.0  # Distance from edge to M3 hole center
angled_hole_offset = 10.0  # Distance from edge to M2.5 hole center

# Create the first plate (base plate with M3 hole)
base_plate = (
    cq.Workplane("XY")
    .box(base_plate_length, plate_width, plate_thickness, centered=(True, True, False))
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .move(base_plate_length/2 - base_hole_offset, 0)
    .hole(m3_hole_diameter)
)

# Create the second plate (angled plate with M2.5 hole)
angled_plate = (
    cq.Workplane("XY")
    .box(angled_plate_length, plate_width, plate_thickness, centered=(True, True, False))
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .move(angled_plate_length/2 - angled_hole_offset, 0)
    .hole(m2_5_hole_diameter)
)

# Rotate and position the angled plate to form the L-shape at 70 degrees
# First, move it up so it rotates around the edge
angled_plate = angled_plate.translate((base_plate_length/2, 0, 0))
# Rotate around the Y-axis by the specified angle
angled_plate = angled_plate.rotate((0, 0, 0), (0, 1, 0), angle)
# Move it back to connect with the base plate
angled_plate = angled_plate.translate((-base_plate_length/1.707, 0, 12))

# Combine the two plates to form the L-shaped bracket
bracket = base_plate.union(angled_plate)

# Render the solid
show_object(bracket)
bracket.export("bhl_display_mount.stl")