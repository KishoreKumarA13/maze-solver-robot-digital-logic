# Hardware Pinout and Wiring Guide

This guide details the exact electrical connections for the **Maze Solver Robot using Digital Systems** without a microcontroller.

---

## 1. Integrated Circuit (IC) Pinouts

### A. 7404 / 74LS04 / 74HCT04 (Hex Inverter IC)
14-pin Dual In-line Package (DIP). Contains 6 independent NOT gates.

| Pin Number | Pin Name | Description | Connection in Project |
|:---:|:---:|:---|:---|
| **1** | $1A$ | NOT Gate 1 Input | Connected to **Front IR Sensor Out ($F$)** |
| **2** | $1Y$ | NOT Gate 1 Output ($\overline{1A}$) | Output $F'$ (Connects to L293D Pin 2 / $R_f$) |
| **3** | $2A$ | NOT Gate 2 Input | Connected to **Right IR Sensor Out ($R$)** |
| **4** | $2Y$ | NOT Gate 2 Output ($\overline{2A}$) | Output $R'$ (Connects to L293D Pin 10 / $L_f$) |
| **7** | $GND$ | Ground Reference | Common Ground ($0V$) |
| **14** | $V_{CC}$ | Supply Voltage ($+5V$) | $+5V$ Rail (from 7805 or 5V source) |
| *5, 6, 8-13* | Unused | Gates 3 to 6 | Tie unused inputs to GND to prevent floating noise |

---

### B. L293D (Dual H-Bridge Motor Driver IC)
16-pin DIP. Drives 2 bidirectional DC motors up to 600mA per channel.

| Pin Number | Pin Name | Description | Connection in Project |
|:---:|:---:|:---|:---|
| **1** | $1,2EN$ | Enable Channel 1 & 2 (Right Motor) | Connected to $+5V$ ($HIGH$ - Always Enabled) |
| **2** | $1A$ (IN1) | Right Motor Forward Input ($R_f$) | Connected to **7404 Pin 2 ($F'$)** |
| **3** | $1Y$ (OUT1)| Right Motor (+) Terminal | Connected to **Right DC Motor (+)** |
| **4, 5** | $GND$ | Ground & Heat Sink | Common Ground ($0V$) |
| **6** | $2Y$ (OUT2)| Right Motor (-) Terminal | Connected to **Right DC Motor (-)** |
| **7** | $2A$ (IN2) | Right Motor Backward Input ($Rb$) | Connected directly to **Front IR Sensor ($F$)** |
| **8** | $V_{CC2}$ ($V_M$) | Motor Power Supply | Connected to Battery ($+9V$ / $+6V$) |
| **9** | $3,4EN$ | Enable Channel 3 & 4 (Left Motor) | Connected to $+5V$ ($HIGH$ - Always Enabled) |
| **10** | $3A$ (IN3) | Left Motor Forward Input ($L_f$) | Connected to **7404 Pin 4 ($R'$)** |
| **11** | $3Y$ (OUT3)| Left Motor (+) Terminal | Connected to **Left DC Motor (+)** |
| **12, 13**| $GND$ | Ground & Heat Sink | Common Ground ($0V$) |
| **14** | $4Y$ (OUT4)| Left Motor (-) Terminal | Connected to **Left DC Motor (-)** |
| **15** | $4A$ (IN4) | Left Motor Backward Input ($L_b$) | Connected to **$GND$ ($0V$)** (Never reverse left) |
| **16** | $V_{CC1}$ ($V_{SS}$) | Logic Supply Voltage | Connected to $+5V$ Rail |

---

## 2. Sensor Connections

### Front IR Obstacle Avoidance Sensor
- **$V_{CC}$**: Connect to $+5V$
- **$GND$**: Connect to Common Ground ($0V$)
- **$OUT$ ($F$)**:
  - Connect to **7404 Pin 1** ($1A$)
  - Connect to **L293D Pin 7** ($2A$ / $R_b$)

### Right IR Obstacle Avoidance Sensor
- **$V_{CC}$**: Connect to $+5V$
- **$GND$**: Connect to Common Ground ($0V$)
- **$OUT$ ($R$)**:
  - Connect to **7404 Pin 3** ($2A$)

---

## 3. Truth Table & Motor Actuation Matrix

| Front ($F$) | Right ($R$) | $F'$ | $R'$ | $R_f$ (Pin 2) | $R_b$ (Pin 7) | $L_f$ (Pin 10) | $L_b$ (Pin 15) | Right Motor | Left Motor | Resulting Movement |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **0** | **0** | 1 | 1 | **1** | **0** | **1** | **0** | Forward | Forward | **Move Forward** (Corridor clear) |
| **0** | **1** | 1 | 0 | **1** | **0** | **0** | **0** | Forward | STOP | **Slight Left Turn** (Avoid right wall) |
| **1** | **0** | 0 | 1 | **0** | **1** | **1** | **0** | Reverse | Forward | **Turn Right** (Front wall detected) |
| **1** | **1** | 0 | 0 | **0** | **1** | **0** | **0** | Reverse | STOP | **Move Backward & Pivot Left** (Corner escape) |

---

## 4. Power Distribution Architecture

1. **Battery**: 9V Hi-Watt or 7.4V 2S Li-ion pack.
2. **Motor Supply ($V_{CC2}$)**: Directly receives unregulated battery voltage for high torque.
3. **Logic Supply ($V_{CC1} / V_{CC}$)**: 5V DC regulated (via 7805 voltage regulator or step-down module) powering the 7404 IC, IR sensors, and L293D logic circuitry.
4. **Common Ground**: All sensor grounds, logic grounds, and motor battery grounds must be tied together.
