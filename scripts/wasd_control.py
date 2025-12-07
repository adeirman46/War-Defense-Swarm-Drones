#!/usr/bin/env python3
"""
WASD Control - EXACT copy of test_motors.py pattern with keyboard
"""

import time
from pymavlink import mavutil

try:
    from pynput import keyboard
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import keyboard

CONNECTION = "udp:127.0.0.1:14551"

# RC values
roll_val = 1500
pitch_val = 1500
throttle_val = 1500
yaw_val = 1500

# Keyboard state
running = True
armed = False

def send_rc(vehicle):
    """Send RC override - EXACTLY like test_motors.py"""
    vehicle.mav.rc_channels_override_send(
        vehicle.target_system, vehicle.target_component,
        roll_val, pitch_val, throttle_val, yaw_val,
        0, 0, 0, 0)

def on_press(key):
    global throttle_val, pitch_val, roll_val, yaw_val, running, armed
    try:
        if hasattr(key, 'char'):
            if key.char == 'w':
                pitch_val = max(1000, pitch_val - 50)
            elif key.char == 's':
                pitch_val = min(2000, pitch_val + 50)
            elif key.char == 'a':
                roll_val = max(1000, roll_val - 50)
            elif key.char == 'd':
                roll_val = min(2000, roll_val + 50)
            elif key.char == 'q':
                yaw_val = max(1000, yaw_val - 50)
            elif key.char == 'e':
                yaw_val = min(2000, yaw_val + 50)
        elif key == keyboard.Key.up:
            throttle_val = min(2000, throttle_val + 50)
        elif key == keyboard.Key.down:
            throttle_val = max(1000, throttle_val - 50)
        elif key == keyboard.Key.space:
            pitch_val = roll_val = yaw_val = 1500
        elif key == keyboard.Key.esc:
            running = False
            return False
    except:
        pass

# Connect - EXACTLY like test_motors.py
print("="*60)
print("WASD CONTROL - Based on test_motors.py")
print("="*60)

print(f"\n1. Connecting to {CONNECTION}...")
vehicle = mavutil.mavlink_connection(CONNECTION)
vehicle.wait_heartbeat()
print(f"✓ Connected to system {vehicle.target_system}")

# Set STABILIZE - EXACTLY like test_motors.py
print("\n2. Setting STABILIZE mode...")
mode_id = vehicle.mode_mapping()['STABILIZE']
vehicle.set_mode(mode_id)
time.sleep(2)
print("✓ STABILIZE mode set")

# Arm - EXACTLY like test_motors.py
print("\n3. Arming motors...")
vehicle.mav.command_long_send(
    vehicle.target_system, vehicle.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0)
time.sleep(3)
armed = True
print("✓ Armed")

print("\n4. Sending RC override - AUTO TAKEOFF...")
print("   Watch AirSim window!\n")

# EXACTLY like test_motors.py takeoff
for throttle in range(1400, 1700, 50):
    throttle_val = throttle
    send_rc(vehicle)
    print(f"   Throttle: {throttle}")
    time.sleep(1)

print("\n5. AIRBORNE! Now you can control with WASD")
print("   W/S - Pitch  |  A/D - Roll  |  Q/E - Yaw")
print("   Up/Down - Throttle  |  Space - Center  |  ESC - Exit\n")

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Main loop - EXACTLY like test_motors.py pattern
print("="*60)
try:
    while running:
        send_rc(vehicle)
        status = "🟢 ARMED" if armed else "🔴 DISARMED"  
        print(f"\r{status} | Thr:{throttle_val:4d} Roll:{roll_val:4d} Pitch:{pitch_val:4d} Yaw:{yaw_val:4d}    ",
              end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nInterrupted")

# Cleanup
listener.stop()

# Land - EXACTLY like test_motors.py
print("\n\n6. Landing...")
for throttle in range(throttle_val, 1200, -50):
    throttle_val = throttle
    send_rc(vehicle)
    print(f"   Throttle: {throttle}")
    time.sleep(0.5)

# Disarm - EXACTLY like test_motors.py
print("\n7. Disarming...")
vehicle.mav.command_long_send(
    vehicle.target_system, vehicle.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 0, 0, 0, 0, 0, 0, 0)
time.sleep(1)

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
