#!/usr/bin/env python3
"""
Diagnostic - Check if RC override is being received by ArduPilot
"""

import time
from pymavlink import mavutil

CONNECTION = "udp:127.0.0.1:14551"

print("="*60)
print("RC OVERRIDE DIAGNOSTIC")
print("="*60)

vehicle = mavutil.mavlink_connection(CONNECTION)
vehicle.wait_heartbeat()
print(f"\n✓ Connected to system {vehicle.target_system}")

# Set STABILIZE
mode_id = vehicle.mode_mapping()['STABILIZE']
vehicle.set_mode(mode_id)
time.sleep(2)
print("✓ STABILIZE mode")

# Arm
print("\nArming...")
vehicle.mav.command_long_send(
    vehicle.target_system, vehicle.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0)
time.sleep(3)
print("✓ Armed")

print("\n" + "="*60)
print("Sending RC override and monitoring servo output...")
print("If working, you should see SERVO_OUTPUT_RAW messages")
print("="*60 + "\n")

# Send RC override and listen for servo output
for i in range(10):
    # Send RC override
    vehicle.mav.rc_channels_override_send(
        vehicle.target_system, vehicle.target_component,
        1500, 1500, 1600, 1500, 0, 0, 0, 0)
    
    # Try to read servo output
    msg = vehicle.recv_match(type='SERVO_OUTPUT_RAW', blocking=True, timeout=0.5)
    if msg:
        print(f"Servo 1: {msg.servo1_raw}, Servo 2: {msg.servo2_raw}, " +
              f"Servo 3: {msg.servo3_raw}, Servo 4: {msg.servo4_raw}")
    else:
        print(f"{i+1}. No SERVO_OUTPUT_RAW received")
    
    time.sleep(0.5)

print("\n" + "="*60)
print("If you see servo values changing, RC override is working")
print("If you see 'No SERVO_OUTPUT_RAW', there's a communication issue")
print("="*60)
