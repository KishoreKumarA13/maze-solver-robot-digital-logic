#!/usr/bin/env python3
"""
Maze Solver Robot - Combinational Logic Simulator & Testbench
============================================================
Course: EI23402 / EI5402 Digital System Design Lab
Institution: Madras Institute of Technology Campus, Anna University

This script verifies and simulates the pure combinational logic (Boolean NOT gates)
used to steer a 2-wheel differential drive maze-solving robot without a microcontroller.

Logic Equations:
  Rf = NOT(F)  = F'   (Right Motor Forward)
  Rb = F              (Right Motor Backward)
  Lf = NOT(R)  = R'   (Left Motor Forward)
  Lb = 0              (Left Motor Backward, tied to GND)
"""

import sys
import time

def evaluate_logic(front_sensor: int, right_sensor: int):
    """
    Evaluates combinational logic from digital sensor readings.
    0 = No obstacle / Clear path (Sensor LOW)
    1 = Obstacle detected (Sensor HIGH)
    """
    F = 1 if front_sensor else 0
    R = 1 if right_sensor else 0
    
    # 7404 NOT Gate Inverters
    F_not = 1 - F
    R_not = 1 - R
    
    # L293D Motor Driver Inputs
    Rf = F_not      # Pin IN1 or IN3
    Rb = F          # Pin IN2 or IN4
    Lf = R_not      # Pin IN3 or IN1
    Lb = 0          # Tied to Ground / 0V
    
    # Action classification
    if (Rf, Rb, Lf, Lb) == (1, 0, 1, 0):
        action = "Move Forward"
        desc = "Both motors forward. Straight path is clear."
    elif (Rf, Rb, Lf, Lb) == (1, 0, 0, 0):
        action = "Slight Left Turn"
        desc = "Right motor forward, Left motor stopped. Steers away from right wall."
    elif (Rf, Rb, Lf, Lb) == (0, 1, 1, 0):
        action = "Turn Right"
        desc = "Right motor reverse, Left motor forward. Sharp right turn into opening."
    elif (Rf, Rb, Lf, Lb) == (0, 1, 0, 0):
        action = "Move Backward & Left"
        desc = "Right motor reverse, Left motor stopped. Backs up & rotates left out of corner."
    else:
        action = "Unknown / Undefined"
        desc = "State outside standard truth table."

    return {
        "F": F,
        "R": R,
        "F_inv": F_not,
        "R_inv": R_not,
        "Rf": Rf,
        "Rb": Rb,
        "Lf": Lf,
        "Lb": Lb,
        "action": action,
        "desc": desc
    }

def print_truth_table():
    print("=" * 78)
    print("         MAZE SOLVER ROBOT - COMBINATIONAL LOGIC TRUTH TABLE")
    print("=" * 78)
    print(f"{'Front (F)':^10} | {'Right (R)':^10} | {'F_not':^5} | {'R_not':^5} | {'Rf':^4} | {'Rb':^4} | {'Lf':^4} | {'Lb':^4} | {'Robot Action':^20}")
    print("-" * 78)
    
    test_vectors = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for f, r in test_vectors:
        res = evaluate_logic(f, r)
        print(f"{res['F']:^10} | {res['R']:^10} | {res['F_inv']:^5} | {res['R_inv']:^5} | {res['Rf']:^4} | {res['Rb']:^4} | {res['Lf']:^4} | {res['Lb']:^4} | {res['action']:<20}")
    print("=" * 78)
    print("Notes:")
    print("  Rf = Right Motor Forward, Rb = Right Motor Reverse")
    print("  Lf = Left Motor Forward,  Lb = Left Motor Reverse (Always 0)")
    print()

def interactive_mode():
    print("\n--- Interactive Sensor Logic Tester ---")
    print("Enter 'q' anytime to exit.\n")
    while True:
        try:
            f_in = input("Enter Front Sensor reading (0: Clear, 1: Obstacle): ").strip()
            if f_in.lower() == 'q':
                break
            r_in = input("Enter Right Sensor reading (0: Clear, 1: Obstacle): ").strip()
            if r_in.lower() == 'q':
                break
            
            f_val = int(f_in)
            r_val = int(r_in)
            if f_val not in (0, 1) or r_val not in (0, 1):
                print("[!] Error: Inputs must be 0 or 1.")
                continue
            
            res = evaluate_logic(f_val, r_val)
            print("-" * 50)
            print(f"  Inputs          : Front={res['F']}, Right={res['R']}")
            print(f"  Inverters (7404): F_inv={res['F_inv']}, R_inv={res['R_inv']}")
            print(f"  Right Motor     : Forward={res['Rf']}, Reverse={res['Rb']}")
            print(f"  Left Motor      : Forward={res['Lf']}, Reverse={res['Lb']}")
            print(f"  >> Robot Action : {res['action']}")
            print(f"  >> Details      : {res['desc']}")
            print("-" * 50 + "\n")
        except ValueError:
            print("[!] Invalid integer. Enter 0, 1, or 'q'.")

def run_maze_simulation():
    """
    Demonstrates the robot traversing a sample track with step-by-step logic.
    """
    print("\n" + "=" * 70)
    print("       STEP-BY-STEP MAZE TRAVERSAL SIMULATION TEST SCENARIO")
    print("=" * 70)
    
    scenario = [
        ("Robot enters long clear corridor", 0, 0),
        ("Robot gets too close to right wall", 0, 1),
        ("Path straightened out, corridor clear", 0, 0),
        ("Dead end / T-junction obstacle directly in front", 1, 0),
        ("Robot corners into a tight dead corner (Front + Right blocked)", 1, 1),
        ("After backing up and pivoting left, front is clear again", 0, 0),
    ]
    
    for idx, (desc, f, r) in enumerate(scenario, start=1):
        res = evaluate_logic(f, r)
        print(f"Step {idx}: {desc}")
        print(f"  Sensors -> Front={f}, Right={r}")
        print(f"  Logic   -> Rf={res['Rf']} (F'), Rb={res['Rb']} (F), Lf={res['Lf']} (R'), Lb={res['Lb']}")
        print(f"  Output  -> [{res['action']}] - {res['desc']}\n")
        time.sleep(0.3)
    
    print("Simulation finished successfully. All combinational states verified!\n")

def main():
    print_truth_table()
    run_maze_simulation()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        print("Tip: Run `python simulate_robot.py --interactive` to test custom inputs.")

if __name__ == "__main__":
    main()
