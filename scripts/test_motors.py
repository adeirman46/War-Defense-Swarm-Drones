#!/usr/bin/env python3
"""
Motor Test - Direct throttle control to test if AirSim responds
This will arm and send throttle commands to verify motor output
"""

import sys
import time
from pymavlink import mavutil

CONNECTION = "udp:127.0.0.1:14551"

print("="*60)
print("MOTOR TEST - Testing AirSim Motor Response")
print("="*60)

# Connect
print(f"\n1. Connecting to {CONNECTION}...")
vehicle = mavutil.mavlink_connection(CONNECTION)
vehicle.wait_heartbeat()
print(f"✓ Connected to system {vehicle.target_system}")

# Set STABILIZE mode
print("\n2. Setting STABILIZE mode...")
mode_id = vehicle.mode_mapping()['STABILIZE']
vehicle.set_mode(mode_id)
time.sleep(2)
print("✓ STABILIZE mode set")

# Arm
print("\n3. Arming motors...")
vehicle.mav.command_long_send(
    vehicle.target_system, vehicle.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0)
time.sleep(3)
print("✓ Armed")

print("\n4. Sending RC override - Increasing throttle...")
print("   Watch AirSim window - motors should spin!\n")

# Send RC override with increasing throttle
for throttle in range(1400, 1800, 50):
    vehicle.mav.rc_channels_override_send(
        vehicle.target_system, vehicle.target_component,
        1500,  # Roll
        1500,  # Pitch
        throttle,  # Throttle
        1500,  # Yaw
        0, 0, 0, 0)
    
    print(f"   Throttle: {throttle}")
    time.sleep(1)

print("\n5. Holding throttle at 1700 for 5 seconds...")
print("   >>> WATCH THE AIRSIM WINDOW NOW <<<\n")

for i in range(5):
    vehicle.mav.rc_channels_override_send(
        vehicle.target_system, vehicle.target_component,
        1500, 1500, 1700, 1500, 0, 0, 0, 0)
    print(f"   {5-i} seconds remaining...")
    time.sleep(1)

print("\n6. Reducing throttle...")
for throttle in range(1700, 1200, -50):
    vehicle.mav.rc_channels_override_send(
        vehicle.target_system, vehicle.target_component,
        1500, 1500, throttle, 1500, 0, 0, 0, 0)
    print(f"   Throttle: {throttle}")
    time.sleep(0.5)

print("\n7. Disarming...")
vehicle.mav.command_long_send(
    vehicle.target_system, vehicle.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 0, 0, 0, 0, 0, 0, 0)
time.sleep(1)

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nDid you see the drone move in AirSim?")
print("  YES - Connection working! Use wasd_control.py")
print("  NO  - AirSim not receiving motor commands")
print("="*60)
