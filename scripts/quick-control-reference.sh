#!/bin/bash
# Quick Manual Control Instructions for AirSim + ArduPilot SITL
# 
# After running ./scripts/run-simulation.sh, find the MAVProxy terminal window
# (it shows a "MAV>" prompt) and type these commands:

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║          QUICK CONTROL REFERENCE - MAVProxy Console          ║
╚═══════════════════════════════════════════════════════════════╝

IMPORTANT: Use the MAVProxy console (terminal with "MAV>" prompt)

BASIC FLIGHT SEQUENCE:
━━━━━━━━━━━━━━━━━━━━━━

1. mode GUIDED         ← Set autonomous mode
2. arm throttle        ← Start motors
3. takeoff 10          ← Takeoff to 10 meters
4. [watch drone fly in AirSim window]
5. setpos 20 0 10      ← Move forward 20m (North, East, Alt)
6. mode RTL            ← Return to launch
7. [wait for landing]
8. disarm              ← Stop motors

OTHER USEFUL COMMANDS:
━━━━━━━━━━━━━━━━━━━━━━

Flight Modes:
  mode STABILIZE    - Manual control (default)
  mode LOITER       - Hold current position
  mode LAND         - Land at current location
  mode POSHOLD      - Position hold

Movement:
  setpos N E ALT    - Move to position (meters from start)
                      Example: setpos 10 5 15
                      (10m North, 5m East, 15m altitude)

Status:
  status           - Show vehicle status
  arm check        - Check why vehicle won't arm

Parameters (for advanced users):
  param show PARAM_NAME        - View parameter
  param set ARMING_CHECK 0     - Disable pre-arm checks (testing only!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TROUBLESHOOTING:
━━━━━━━━━━━━━━━━

❌ Can't arm?
   → param set ARMING_CHECK 0   (disables safety checks for testing)
   → Make sure GPS has lock (wait 15-20 seconds after startup)
   → Run: arm check

❌ Mode won't change?
   → Try: mode STABILIZE first, then mode GUIDED
   → Check MAVProxy console for error messages

❌ Vehicle not responding?
   → Check MAVProxy shows "MAV>" prompt (connected)
   → Verify AirSim window is open and showing drone
   → Restart simulation: Ctrl+C then ./scripts/run-simulation.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE MISSION - Fly in a Square:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

mode GUIDED
arm throttle
takeoff 15
[wait 20 seconds]
setpos 20 0 15      ← Forward 20m
[wait 10 seconds]
setpos 20 20 15     ← Right 20m
[wait 10 seconds]
setpos 0 20 15      ← Back 20m
[wait 10 seconds]
setpos 0 0 15       ← Left to start
[wait 10 seconds]
mode RTL            ← Return and land
disarm

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For detailed documentation, see: docs/CONTROL_GUIDE.md

EOF
