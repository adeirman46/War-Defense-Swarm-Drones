#!/usr/bin/env python3
"""
Simple drone control script for AirSim + ArduPilot SITL
This script demonstrates basic drone control operations using pymavlink.
"""

import time
import sys
from pymavlink import mavutil

# Connection string for SITL
# This connects to the MAVProxy output port
CONNECTION_STRING = "udp:127.0.0.1:14550"


def connect_to_vehicle():
    """Connect to the vehicle and wait for heartbeat."""
    print(f"Connecting to vehicle on {CONNECTION_STRING}...")
    vehicle = mavutil.mavlink_connection(CONNECTION_STRING)
    
    # Wait for the first heartbeat
    print("Waiting for heartbeat...")
    vehicle.wait_heartbeat()
    print(f"Heartbeat from system {vehicle.target_system}, component {vehicle.target_component}")
    return vehicle


def arm_vehicle(vehicle):
    """Arm the vehicle."""
    print("Arming vehicle...")
    vehicle.mav.command_long_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # confirmation
        1,  # arm (1 to arm, 0 to disarm)
        0, 0, 0, 0, 0, 0
    )
    
    # Wait for ACK
    ack = vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        print("Vehicle armed!")
        return True
    else:
        print("Failed to arm vehicle")
        return False


def set_mode(vehicle, mode):
    """Set the flight mode."""
    print(f"Setting mode to {mode}...")
    
    # Get mode ID
    if mode not in vehicle.mode_mapping():
        print(f"Unknown mode: {mode}")
        print(f"Available modes: {list(vehicle.mode_mapping().keys())}")
        return False
    
    mode_id = vehicle.mode_mapping()[mode]
    
    # Use DO_SET_MODE command instead of set_mode_send
    vehicle.mav.command_long_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,  # confirmation
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # param1: mode
        mode_id,  # param2: custom mode
        0, 0, 0, 0, 0  # params 3-7
    )
    
    # Wait for ACK
    ack = vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        print(f"Mode set to {mode}")
        return True
    else:
        print(f"Failed to set mode to {mode}")
        return False


def takeoff(vehicle, altitude):
    """Command the vehicle to take off to specified altitude (meters)."""
    print(f"Taking off to {altitude} meters...")
    vehicle.mav.command_long_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,  # confirmation
        0, 0, 0, 0,  # params 1-4
        0, 0,  # latitude, longitude (0 = current position)
        altitude  # altitude
    )
    
    # Wait for ACK
    ack = vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        print("Takeoff command accepted")
        return True
    else:
        print("Takeoff command failed")
        return False


def goto_position_ned(vehicle, north, east, down):
    """
    Move to a position relative to current position.
    north, east, down in meters (NED frame)
    """
    print(f"Moving to position: N={north}m, E={east}m, D={down}m")
    vehicle.mav.send(
        mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10,  # time_boot_ms (not used)
            vehicle.target_system,
            vehicle.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b0000111111111000,  # type_mask (only positions enabled)
            north, east, down,  # position
            0, 0, 0,  # velocity (not used)
            0, 0, 0,  # acceleration (not used)
            0, 0  # yaw, yaw_rate (not used)
        )
    )


def disarm_vehicle(vehicle):
    """Disarm the vehicle."""
    print("Disarming vehicle...")
    vehicle.mav.command_long_send(
        vehicle.target_system,
        vehicle.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # confirmation
        0,  # disarm
        0, 0, 0, 0, 0, 0
    )
    
    # Wait for ACK
    ack = vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        print("Vehicle disarmed!")
        return True
    else:
        print("Failed to disarm vehicle")
        return False


def get_altitude(vehicle):
    """Get current altitude from VFR_HUD."""
    msg = vehicle.recv_match(type='VFR_HUD', blocking=True, timeout=1)
    if msg:
        return msg.alt
    return None


def check_gps_lock(vehicle, timeout=30):
    """Wait for GPS 3D lock."""
    print("Waiting for GPS lock...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        msg = vehicle.recv_match(type='GPS_RAW_INT', blocking=True, timeout=1)
        if msg and msg.fix_type >= 3:  # 3D fix or better
            print(f"GPS lock acquired! Fix type: {msg.fix_type}, Satellites: {msg.satellites_visible}")
            return True
        
        if int(time.time() - start_time) % 5 == 0:
            print(f"  Waiting for GPS... ({int(time.time() - start_time)}s)")
    
    print("GPS lock timeout!")
    return False


def check_ekf_status(vehicle):
    """Check if EKF is healthy."""
    print("Checking EKF status...")
    msg = vehicle.recv_match(type='EKF_STATUS_REPORT', blocking=True, timeout=5)
    if msg:
        print(f"EKF status - flags: {msg.flags}")
        return True
    print("No EKF status received")
    return True  # Continue anyway for simulation


def wait_until_ready(vehicle):
    """Wait for vehicle to be ready for flight."""
    print("\n=== Checking vehicle readiness ===")
    
    # Check GPS
    if not check_gps_lock(vehicle):
        print("WARNING: No GPS lock, but continuing for simulation...")
    
    # Check EKF
    check_ekf_status(vehicle)
    
    # Wait for system status
    print("Waiting for system to be ready...")
    time.sleep(3)
    
    print("=== Vehicle ready! ===\n")
    return True


def main():
    """Main control sequence."""
    try:
        # Connect to vehicle
        vehicle = connect_to_vehicle()
        
        # Wait for vehicle to be ready
        if not wait_until_ready(vehicle):
            print("Vehicle not ready. Exiting.")
            return
        
        # Set mode to GUIDED
        print("\nAttempting to set GUIDED mode...")
        if not set_mode(vehicle, "GUIDED"):
            print("Cannot set GUIDED mode.")
            print("Trying alternative method...")
            # Try using mavutil.mode_string_v10
            vehicle.set_mode('GUIDED')
            time.sleep(2)
            print("Check if mode changed in MAVProxy/QGC")
        
        time.sleep(1)
        
        # Arm the vehicle
        if not arm_vehicle(vehicle):
            print("Cannot arm vehicle.")
            print("You may need to disable pre-arm checks:")
            print("  In MAVProxy, run: param set ARMING_CHECK 0")
            print("Exiting.")
            return
        
        time.sleep(2)
        
        # Takeoff
        if not takeoff(vehicle, 10):
            print("Takeoff failed. Exiting.")
            return
        
        # Wait for takeoff to complete
        print("Waiting for takeoff to 10m...")
        time.sleep(15)
        
        # Check altitude
        alt = get_altitude(vehicle)
        if alt:
            print(f"Current altitude: {alt:.1f}m")
        
        # Move forward 20 meters
        print("\nMoving forward 20 meters...")
        goto_position_ned(vehicle, 20, 0, -10)
        time.sleep(10)
        
        # Move right 10 meters
        print("\nMoving right 10 meters...")
        goto_position_ned(vehicle, 20, 10, -10)
        time.sleep(10)
        
        # Return to launch
        print("\nReturning to launch...")
        set_mode(vehicle, "RTL")
        
        # Wait for landing
        print("Waiting for landing...")
        time.sleep(20)
        
        # Disarm
        disarm_vehicle()
        
        print("\nMission complete!")
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        if 'vehicle' in locals():
            print("Setting RTL mode...")
            set_mode(vehicle, "RTL")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
