# Intelligent-communication-channel-selection-for-heterogeneous-maritime-networks

##  Project Objective
This project is a software prototype designed to simulate real-time, dynamic communication channel selection for modern maritime vessels. Vessels operate in highly variable network environments (Satellite, 4G, Wi-Fi, etc.). This system utilizes a **Reinforcement Learning (Q-Learning)** algorithm to dynamically evaluate and select the most optimal channel based on latency, bandwidth, cost, stability, and data priority.


## System Architecture

### 1. Simulated Environment
The environment simulates five distinct communication links, each with fluctuating parameters:
* **Wi-Fi / Short-Range Radio:** Low latency, high bandwidth, zero/low cost, but highly unstable (short range).
* **4G Cellular:** Moderate latency and cost, good bandwidth, medium stability.
* **GEO / LEO Satellites:** High stability, global coverage, but very high latency and transmission costs.

### 2. Data Traffic Simulator
Generates simulated data packets with varying sizes and priorities:
* `Critical` (e.g., Distress signals, navigation telemetry)
* `Normal` (e.g., Operational logs)
* `Background` (e.g., Crew internet)

### 3. The Brain: Q-Learning Agent
The agent learns the optimal policy through trial and error using the Bellman Equation.
* **State (s):** A combination of the current network's Latency Bin, Bandwidth Bin, and the incoming Packet's Priority.
* **Action (a):** Selecting one of the available communication channels.
* **Reward (R):** The reward function is mathematically designed to penalize high latency and high cost, while rewarding high stability. Choosing an expensive satellite for background data results in a negative reward, teaching the agent to avoid such actions.

### 4. The Hysteresis Guard
Acts as a stability filter over the Q-Learning agent. It calculates the Q-value difference between the current channel and the proposed channel. A switch is only executed if `proposed_Q > current_Q + threshold`, or if the current channel goes completely offline.

## Directory Layout

project_root/
│
├── main.py                  # Main execution loop and simulation controller
├── channels/                # Network channel definitions
│   ├── channel.py           # Base class for all channels
│   ├── cellular.py          # 4G Cellular implementation
│   ├── radio.py             # Short-Range Radio implementation
│   ├── satellite.py         # GEO/LEO Satellite implementation
│   └── wifi.py              # Wi-Fi implementation
│
├── engine/                  # Core logic and AI
│   ├── decision.py          # Hysteresis Decision Engine
│   ├── evaluator.py         # Multi-criteria scoring
│   └── q_learning.py        # Reinforcement Learning Agent
│
├── simulator/               # Environment and Traffic generation
│   ├── data_packet.py       # Data prioritization and packet creation
│   └── environment.py       # Real-time network fluctuation simulator
│
└── utils/                   
  └── normalizer.py        # Helper functions for math normalization
