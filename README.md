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
cd War-Defense-Swarm-Drones.git

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

**WASD Keyboard Control** (Easiest! ⭐)
```bash
# In a new terminal:
cd ~/War-Defense-Swarm-Drones.git

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


