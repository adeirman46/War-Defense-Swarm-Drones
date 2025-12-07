# Drone Control Guide

This guide explains how to control the drone in the AirSim + ArduPilot SITL simulation.

## Prerequisites

Make sure the simulation is running:
```bash
./scripts/run-simulation.sh
```

This starts:
- **AirSim** - Provides the 3D visualization and physics simulation
- **ArduPilot SITL** - Flight controller software
- **MAVProxy** - Ground control station (console interface)
- **QGroundControl** - GUI ground control station

---

## Method 1: MAVProxy Console (Command Line)

When you run the simulation, MAVProxy opens a terminal window with a `MAV>` prompt. Type commands directly there.

### Basic Flight Sequence

```bash
# 1. Set GUIDED mode (required for autonomous commands)
mode GUIDED

# 2. Arm the motors
arm throttle

# 3. Takeoff to 10 meters
takeoff 10

# 4. Wait for the drone to reach altitude (watch in AirSim)

# 5. Move to a position (North, East, altitude)
setpos 10 0 10

# 6. Return to launch point
mode RTL

# 7. After landing, disarm
disarm
```

### Useful MAVProxy Commands

| Command | Description |
|---------|-------------|
| `mode GUIDED` | Enable autonomous control |
| `mode STABILIZE` | Manual control mode |
| `mode LOITER` | Hold position |
| `mode RTL` | Return to launch |
| `mode LAND` | Land at current position |
| `arm throttle` | Arm motors |
| `disarm` | Disarm motors |
| `takeoff ALT` | Takeoff to altitude (meters) |
| `setpos N E ALT` | Move to position (North, East, Altitude) |
| `rc 3 1500` | Set throttle to middle (1000-2000) |
| `status` | Show vehicle status |
| `param show PARAM_NAME` | Show parameter value |
| `param set PARAM_NAME VALUE` | Set parameter |

---

## Method 2: QGroundControl (GUI)

QGroundControl provides a graphical interface:

1. **Connect**: Should auto-connect to `127.0.0.1:14550`
2. **Fly View**: Main flight screen
3. **Plan View**: Create and execute missions
4. **Widgets**: Add altitude, speed, attitude indicators

### Quick Actions in QGC:
- Click **"Arm"** button to arm motors
- Use flight mode dropdown to change modes
- Click **"Takeoff"** action for quick takeoff
- Click **"RTL"** action to return home

---

## Method 3: Python Script (Programmatic)

Use the provided Python script for automated control:

```bash
# In a new terminal (while simulation is running)
cd ~/AirSim-ArduPilot-SITL-QGroundControl-with-Pixi
pixi shell

# Run the control script
python3 scripts/control_drone.py
```

This script will:
1. Connect to the vehicle
2. Set GUIDED mode
3. Arm the motors
4. Takeoff to 10 meters
5. Move forward 20 meters
6. Move right 10 meters
7. Return to launch
8. Land and disarm

### Customize the Script

Edit `scripts/control_drone.py` to create your own flight path:

```python
# Example: fly in a square pattern
goto_position_ned(vehicle, 20, 0, -10)   # Forward 20m
time.sleep(10)
goto_position_ned(vehicle, 20, 20, -10)  # Right 20m
time.sleep(10)
goto_position_ned(vehicle, 0, 20, -10)   # Back 20m
time.sleep(10)
goto_position_ned(vehicle, 0, 0, -10)    # Left 20m
time.sleep(10)
```

---

## Method 4: AirSim Python API (Advanced)

You can also control the drone using AirSim's native Python API:

```python
import airsim

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Takeoff
client.takeoffAsync().join()

# Move to position
client.moveToPositionAsync(10, 0, -10, 5).join()

# Land
client.landAsync().join()
```

> **Note**: AirSim API bypasses ArduPilot, so use either ArduPilot OR AirSim API, not both simultaneously.

---

## Connection Ports Reference

| Component | Port | Protocol | Purpose |
|-----------|------|----------|---------|
| MAVProxy Master | 5760 | TCP | ArduPilot → MAVProxy |
| MAVProxy SITL | 5501 | UDP | MAVProxy → SITL sensor input |
| MAVProxy Out 1 | 14550 | UDP | MAVProxy → QGC / Scripts |
| MAVProxy Out 2 | 14551 | UDP | MAVProxy → Additional GCS |
| AirSim JSON | 41451 | TCP | AirSim API server |

---

## Troubleshooting

### Drone won't arm
- Check GPS lock: `gps` in MAVProxy (should show 3D fix)
- Check EKF status: Must be initialized
- Disable pre-arm checks (for testing): `param set ARMING_CHECK 0`

### No GPS lock in simulation
- Wait 10-15 seconds after startup
- Check AirSim is running and connected
- Verify MAVProxy shows GPS messages

### Commands not working
- Ensure mode is GUIDED: `mode GUIDED`
- Check vehicle is armed: `arm throttle`
- Verify MAVProxy shows "MAV>" prompt (connected)

### Reset simulation
1. Press Ctrl+C in the terminal running `run-simulation.sh`
2. Wait for clean shutdown
3. Run `./scripts/run-simulation.sh` again

---

## Safety Notes

- This is a simulation - experiment freely!
- In real drones, ALWAYS:
  - Test in STABILIZE mode first
  - Verify GPS lock before arming
  - Have a safety pilot ready
  - Know your RTL failsafe settings

---

## Next Steps

- **Create missions** in QGroundControl Plan view
- **Write custom Python scripts** for autonomous behaviors
- **Tune parameters** for different flight characteristics
- **Test failsafes** (battery, GPS loss, RC loss)
- **Log analysis** using MAVProxy logs in `logs/` directory

For advanced control, see ArduPilot documentation: https://ardupilot.org/copter/
