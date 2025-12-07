#!/usr/bin/env python3
"""
Simple Manual Control for AirSim + ArduPilot SITL
Uses manual throttle and attitude commands instead of RC override.

Controls (hold keys down):
  W - Forward
  S - Backward
  A - Left
  D - Right
  I - Increase throttle (climb)
  K - Decrease throttle (descend)
  Space - Stop all movement
  ESC - Exit
"""

import sys
import time
import threading
from pymavlink import mavutil

try:
    from pynput import keyboard
except ImportError:
    print("Installing pynput...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import keyboard

# Connection
CONNECTION_STRING = "udp:127.0.0.1:14551"

class SimpleController:
    def __init__(self):
        self.vehicle = None
        self.running = True
        self.keys = set()
        
        # Current velocities (m/s)
        self.vx = 0.0  # Forward/backward
        self.vy = 0.0  # Left/right
        self.vz = 0.0  # Up/down
        self.yaw_rate = 0.0
        
        self.throttle = 0.5  # 0 to 1
        self.max_speed = 2.0  # m/s
        
    def connect(self):
        print(f"Connecting to {CONNECTION_STRING}...")
        self.vehicle = mavutil.mavlink_connection(CONNECTION_STRING)
        self.vehicle.wait_heartbeat()
        print(f"✓ Connected to system {self.vehicle.target_system}")
        
    def arm_and_takeoff(self, target_alt=3):
        """Simple arm and takeoff."""
        print("\nArming...")
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system, self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0)
        time.sleep(2)
        print("✓ Armed")
        
        print(f"\nTaking off to {target_alt}m...")
        # Set GUIDED mode
        mode_id = self.vehicle.mode_mapping()['GUIDED']
        self.vehicle.set_mode(mode_id)
        time.sleep(1)
        
        # Takeoff command
        self.vehicle.mav.command_long_send(
            self.vehicle.target_system, self.vehicle.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, target_alt)
        
        print("✓ Takeoff command sent")
        print(f"Climbing to {target_alt}m (wait 15-20 seconds)...")
        
    def send_velocity(self):
        """Send velocity command."""
        self.vehicle.mav.send(
            mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
                10, self.vehicle.target_system, self.vehicle.target_component,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                0b0000111111000111,  # Use velocity
                0, 0, 0,  # Position (not used)
                self.vx, self.vy, self.vz,  # Velocity
                0, 0, 0,  # Acceleration (not used)
                0, 0))  # Yaw, yaw rate
                
    def update_velocity(self):
        """Update velocities based on held keys."""
        # Reset velocities
        self.vx = 0
        self.vy = 0
        self.vz = 0
        
        # Forward/backward
        if 'w' in self.keys:
            self.vx = self.max_speed
        if 's' in self.keys:
            self.vx = -self.max_speed
            
        # Left/right
        if 'a' in self.keys:
            self.vy = -self.max_speed
        if 'd' in self.keys:
            self.vy = self.max_speed
            
        # Up/down
        if 'i' in self.keys:
            self.vz = -1.0  # Negative is up in NED
        if 'k' in self.keys:
            self.vz = 1.0  # Positive is down in NED
            
    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                c = key.char.lower()
                self.keys.add(c)
                
                # Special commands
                if c == 't':
                    threading.Thread(target=lambda: self.arm_and_takeoff(5), daemon=True).start()
                    
            elif key == keyboard.Key.space:
                self.vx = self.vy = self.vz = 0
                self.keys.clear()
                print("\n⏸  Stopped")
                
            elif key == keyboard.Key.esc:
                print("\nExiting...")
                self.running = False
                return False
                
        except AttributeError:
            pass
            
    def on_release(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                self.keys.discard(key.char.lower())
        except AttributeError:
            pass
            
    def run(self):
        self.connect()
        
        print("\n" + "="*60)
        print("🚁 SIMPLE MANUAL CONTROL")
        print("="*60)
        print("\n📍 Controls (hold keys):")
        print("  W - Forward    |  I - Climb")
        print("  S - Backward   |  K - Descend")
        print("  A - Left       |")
        print("  D - Right      |")
        print("\n🎮 Commands:")
        print("  T     - Arm and Takeoff to 5m")
        print("  Space - Stop")
        print("  ESC   - Exit")
        print("="*60)
        print("\n⚠️  Press 'T' to arm and takeoff first!")
        print()
        
        # Start keyboard listener
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        
        # Control loop
        last_heartbeat = time.time()
        while self.running:
            # Update and send velocity
            self.update_velocity()
            self.send_velocity()
            
            # Send heartbeat
            if time.time() - last_heartbeat > 1.0:
                self.vehicle.mav.heartbeat_send(
                    mavutil.mavlink.MAV_TYPE_GCS,
                    mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                    0, 0, 0)
                last_heartbeat = time.time()
            
            # Display status
            print(f"\r🎮 Vx:{self.vx:+.1f} Vy:{self.vy:+.1f} Vz:{self.vz:+.1f} m/s  ", end='', flush=True)
            
            time.sleep(0.1)
            
        listener.stop()
        print("\n✓ Done\n")

if __name__ == "__main__":
    controller = SimpleController()
    controller.run()
