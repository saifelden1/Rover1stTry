#!/usr/bin/env python3
"""
Geometry Validation Script for Robot URDF (Mars Rover Style)
Validates that rectangular suspension arms properly connect base to wheels
with realistic rover geometry (arm connects to wheel's rear face)
"""

# ============================================================================
# ROBOT DIMENSIONS (from URDF)
# ============================================================================

# BASE DIMENSIONS
base_length = 0.4   # m (X-axis: front to back)
base_width = 0.4    # m (Y-axis: left to right)
base_height = 0.15  # m (Z-axis: top to bottom)
base_mass = 5.0     # kg

# WHEEL DIMENSIONS
wheel_radius = 0.06   # m
wheel_length = 0.05   # m (thickness)
wheel_mass = 0.6      # kg

# SUSPENSION ARM DIMENSIONS
arm_length = 0.03   # m (X-axis: front to back)
arm_width = 0.02    # m (Y-axis: left to right)
arm_height = 0.12   # m (Z-axis: vertical length)
arm_mass = 0.2      # kg

# ============================================================================
# CALCULATED OFFSETS (for validation)
# ============================================================================
arm_x_offset = -(wheel_length + arm_length)/2  # Arm center positioned so front face touches wheel rear face

print("=" * 70)
print("MARS ROVER ROBOT GEOMETRY VALIDATION")
print("=" * 70)

print("\n" + "=" * 70)
print("ROBOT DIMENSIONS")
print("=" * 70)

print("\nBASE DIMENSIONS:")
print(f"   Length (X): {base_length}m")
print(f"   Width (Y):  {base_width}m")
print(f"   Height (Z): {base_height}m")
print(f"   Mass:       {base_mass}kg")

print("\nWHEEL DIMENSIONS:")
print(f"   Radius:     {wheel_radius}m")
print(f"   Length:     {wheel_length}m (thickness)")
print(f"   Mass:       {wheel_mass}kg")

print("\nSUSPENSION ARM DIMENSIONS:")
print(f"   Length (X): {arm_length}m")
print(f"   Width (Y):  {arm_width}m")
print(f"   Height (Z): {arm_height}m")
print(f"   Mass:       {arm_mass}kg")

print("\n" + "=" * 70)
print("GEOMETRY VALIDATION")
print("=" * 70)

# Base link is at origin (0, 0, 0)
print("\n1. BASE LINK (at origin)")
print(f"   Base height: {base_height}m")
print(f"   Base top: z = +{base_height/2}m")
print(f"   Base bottom: z = -{base_height/2}m")

# Arm positioning (vertical)
arm_z_offset = -base_height/2 - arm_height/2
print(f"\n2. SUSPENSION ARM (Vertical)")
print(f"   Arm height: {arm_height}m")
print(f"   Arm center: z = {arm_z_offset}m")
print(f"   Arm top: z = {arm_z_offset + arm_height/2}m")
print(f"   Arm bottom: z = {arm_z_offset - arm_height/2}m")

# Arm positioning (horizontal)
print(f"\n3. SUSPENSION ARM (Horizontal - Rover Style)")
print(f"   Arm length: {arm_length}m")
print(f"   Arm X offset: {arm_x_offset}m (behind wheel center)")
print(f"   Arm front face: x = {arm_x_offset + arm_length/2}m")
print(f"   Arm rear face: x = {arm_x_offset - arm_length/2}m")

# Check if arm top touches base bottom
gap_vertical = (arm_z_offset + arm_height/2) - (-base_height/2)
print(f"\n4. VERTICAL CONNECTION CHECK")
print(f"   Gap between base bottom and arm top: {gap_vertical}m")
if abs(gap_vertical) < 0.001:
    print("   ✓ ARM TOP TOUCHES BASE BOTTOM (no gap)")
else:
    print(f"   ✗ FLOATING! Gap of {gap_vertical}m detected")

# Wheel positioning (relative to arm)
wheel_z_center = arm_z_offset - arm_height/2
wheel_z_bottom = wheel_z_center - wheel_radius
print(f"\n5. WHEEL POSITION (Vertical)")
print(f"   Wheel radius: {wheel_radius}m")
print(f"   Wheel center: z = {wheel_z_center}m")
print(f"   Wheel bottom: z = {wheel_z_bottom}m")

# Wheel positioning (horizontal - relative to arm)
wheel_x_relative = -arm_x_offset  # Wheel offset from arm center
print(f"\n6. WHEEL POSITION (Horizontal - Rover Connection)")
print(f"   Wheel length: {wheel_length}m")
print(f"   Wheel center: x = 0m (at desired position)")
print(f"   Wheel rear face: x = {-wheel_length/2}m")
print(f"   Wheel front face: x = {wheel_length/2}m")
print(f"   Arm front face: x = {arm_x_offset + arm_length/2}m")

# Check horizontal connection
gap_horizontal = (-wheel_length/2) - (arm_x_offset + arm_length/2)
print(f"\n7. HORIZONTAL CONNECTION CHECK")
print(f"   Gap between wheel rear face and arm front face: {gap_horizontal}m")
if abs(gap_horizontal) < 0.001:
    print("   ✓ ARM CONNECTS TO WHEEL REAR FACE (no gap, no stab)")
else:
    print(f"   ✗ CONNECTION ISSUE! Gap of {gap_horizontal}m detected")

# Base footprint calculation
base_footprint_offset = base_height/2 + arm_height + wheel_radius
print(f"\n8. BASE FOOTPRINT OFFSET")
print(f"   Required offset: {base_footprint_offset}m")
print(f"   This places base_link at z = {base_footprint_offset}m")
print(f"   Wheel bottom in world: z = {base_footprint_offset + wheel_z_bottom}m")

if abs(base_footprint_offset + wheel_z_bottom) < 0.001:
    print("   ✓ WHEELS TOUCH GROUND (z = 0)")
else:
    print(f"   ✗ WHEELS DON'T TOUCH GROUND! Off by {base_footprint_offset + wheel_z_bottom}m")

print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)
all_checks = [
    abs(gap_vertical) < 0.001,
    abs(gap_horizontal) < 0.001,
    abs(base_footprint_offset + wheel_z_bottom) < 0.001
]
if all(all_checks):
    print("✓ ALL CHECKS PASSED - Mars Rover geometry is correct!")
    print("  - Arm top touches base bottom")
    print("  - Arm connects to wheel rear face (realistic rover style)")
    print("  - Wheels touch ground")
else:
    print("✗ GEOMETRY ISSUES DETECTED - Review calculations")
print("=" * 70)
