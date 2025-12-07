# AirSim + ArduPilot SITL Drone Simulation

Fully functional drone simulation with **keyboard control** (WASD) for AirSim and ArduPilot SITL. Currently configured for **Gasibu, Bandung, Indonesia** 🇮🇩.

## � Prerequisites

- **Linux** (Ubuntu 20.04+ recommended)
- **Python 3.8+**
- **Pixi** package manager
- ~10GB disk space

## 🔧 Setup

### 1. Install Pixi

```bash
# Install Pixi package manager
curl -fsSL https://pixi.sh/install.sh | bash

# Restart terminal or source your shell config
source ~/.bashrc  # or ~/.zshrc
```

### 2. Clone and Setup Environment

```bash
# Clone repository
git clone https://github.com/adeirman46/War-Defense-Swarm-Drones.git
cd AirSim-ArduPilot-SITL-QGroundControl-with-Pixi

# Install dependencies using Pixi
pixi install
```

### 3. Download Components

```bash
# Download AirSim binary
./scripts/download-airsim.sh

# Build ArduPilot SITL
./scripts/build-ardupilot-sitl.sh

# Download QGroundControl
./scripts/download-qground.sh
```

**Note:** These downloads are large (~5GB total) and may take 10-30 minutes depending on your connection.

### 4. Verify Setup

```bash
./scripts/check-simulation.sh
```

All components should show ✓ (checkmark).

## �🚀 Quick Start

### 1. Start Simulation
```bash
./scripts/run-simulation.sh
```

This will launch:
- ✅ **AirSim** - Visual simulation window
- ✅ **ArduPilot SITL** - Flight controller
- ✅ **MAVProxy** - Command console
- ✅ **QGroundControl** - Ground station with map

### 2. Control the Drone

**Option A: WASD Keyboard Control** (Easiest! ⭐)
```bash
# In a new terminal:
cd ~/AirSim-ArduPilot-SITL-QGroundControl-with-Pixi

# Activate Pixi environment
pixi shell

# Run control script
python3 scripts/wasd_control.py
```

Then:
- Press **`T`** → Auto takeoff
- **W/A/S/D** → Move forward/left/back/right
- **Up/Down arrows** → Climb/descend
- **Q/E** → Rotate left/right
- **Space** → Hover (neutral)
- **L** → Auto land
- **ESC** → Exit

**Option B: MAVProxy Console**

In the MAVProxy terminal (shows `MAV>` prompt):
```
mode GUIDED
arm throttle
takeoff 10
```

See [`docs/CONTROL_GUIDE.md`](docs/CONTROL_GUIDE.md) for detailed instructions.

## 📍 Location Configuration

**Current Location:** Gasibu, Bandung (-6.9003°, 107.6186°, 768m)

To change location, edit **BOTH** files:

1. **AirSim settings:**
```bash
nano config/airsim/settings.json
# Update OriginGeopoint -> Latitude, Longitude, Altitude
```

2. **Active AirSim settings (the one actually used):**
```bash
nano .airsim_ardupilot/airsim/settings.json
# Update OriginGeopoint -> Latitude, Longitude, Altitude
```

Then restart the simulation.

## 🛠️ Available Scripts

| Script | Purpose |
|--------|---------|
| `scripts/wasd_control.py` | **Main control script** - WASD keyboard flying ⭐ |
| `scripts/test_motors.py` | Test if motors respond (diagnostic) |
| `scripts/control_drone.py` | Automated flight script (GPS-based) |
| `scripts/simple_control.py` | Alternative velocity-based control |
| `scripts/quick-control-reference.sh` | Show MAVProxy command reference |

## 📚 Documentation

- **[Control Guide](docs/CONTROL_GUIDE.md)** - Complete control instructions
- **[Walkthrough](/.gemini/antigravity/brain/e20c1a2a-469a-4b55-9544-15c7672127b3/walkthrough.md)** - Fixes and solutions applied

## ✅ What's Working

- ✅ All components launch correctly
- ✅ AirSim ↔ ArduPilot connection working
- ✅ MAVProxy communication stable
- ✅ QGroundControl displays telemetry and GPS
- ✅ Drone responds to throttle/controls
- ✅ WASD keyboard control functional
- ✅ GPS location configurable (currently Bandung)

## 🔧 Troubleshooting

### Drone doesn't move after pressing T

**Cause:** Wrong settings file being used  
**Fix:** Edit `.airsim_ardupilot/airsim/settings.json` (not just `config/airsim/settings.json`)

### QGroundControl shows wrong location

**Cause:** Old coordinates in AirSim settings  
**Fix:** 
```bash
# Check current location:
cat .airsim_ardupilot/airsim/settings.json | grep -A 4 "OriginGeopoint"

# Update if needed, then restart simulation
```

### Control script connects but drone doesn't fly

**Solution 1:** Use `test_motors.py` to verify motors work:
```bash
python3 scripts/test_motors.py
```

**Solution 2:** Ensure simulation is fully started (wait 15-20 seconds)

**Solution 3:** Restart simulation completely

### MAVProxy errors on startup

Already fixed! The `run-simulation.sh` script now correctly:
- Sets `MAVPROXY_CMD` environment variable
- Uses Pixi environment's Python
- Configures proper paths

## 🎮 Controls Summary

### WASD Control Keys
| Key | Action |
|-----|--------|
| **T** | Auto takeoff ⭐ |
| **W/S** | Forward/Backward |
| **A/D** | Left/Right |
| **Q/E** | Rotate |
| **↑/↓** | Climb/Descend |
| **Space** | Hover |
| **L** | Land |
| **F** | Disarm |

### MAVProxy Commands
| Command | Action |
|---------|--------|
| `mode GUIDED` | Enable autonomous mode |
| `arm throttle` | Arm motors |
| `takeoff 10` | Takeoff to 10m |
| `setpos 20 0 10` | Move to position |
| `mode RTL` | Return to launch |
| `disarm` | Disarm motors |

## 🏗️ Project Structure

```
├── scripts/
│   ├── run-simulation.sh        # Main launcher ⭐
│   ├── wasd_control.py          # WASD keyboard control ⭐
│   ├── test_motors.py           # Motor test
│   └── quick-control-reference.sh
├── config/
│   ├── airsim/settings.json     # Template settings
│   └── ardupilot/airsim.parm    # ArduPilot parameters
├── docs/
│   └── CONTROL_GUIDE.md         # Detailed control guide
└── .airsim_ardupilot/
    └── airsim/settings.json     # Active settings (edit this!) ⭐
```

## 🔍 Key Features

1. **No GPS Required for Basic Flight** - Uses STABILIZE mode with RC override
2. **Real-time Control** - Immediate response to keyboard input
3. **Multiple Control Methods** - WASD, MAVProxy, QGC, or Python scripts
4. **Configurable Location** - Fly anywhere in the world virtually
5. **Pixi Environment** - Isolated, reproducible Python environment

## 📝 Notes

- Default mode is **STABILIZE** (manual control)
- **GUIDED** mode requires GPS lock (15-20 seconds wait)
- Bandung altitude is 768m above sea level
- RC override works without GPS
- AirSim reads settings from `.airsim_ardupilot/airsim/settings.json`

## 🎯 Mission Accomplished!

The simulation is fully functional with working:
- ✅ WASD keyboard flying
- ✅ ArduPilot SITL integration  
- ✅ AirSim motor response
- ✅ GPS location (Gasibu, Bandung)
- ✅ QGroundControl telemetry
- ✅ MAVProxy console control

**Ready to fly!** 🚁🎉

---

For detailed troubleshooting and advanced usage, see [`CONTROL_GUIDE.md`](docs/CONTROL_GUIDE.md)
