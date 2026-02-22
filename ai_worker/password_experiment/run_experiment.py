# run_experiment.py
"""Orchestrate the full password hashing experiment pipeline.

Steps:
1. Generate password datasets (`generate_passwords.py`).
2. Hash passwords with various schemes (`hash_passwords.py`).
3. Simulate cracking (`crack_simulation.py`).
4. Collect and summarize metrics (`metrics.py`).

The script can be invoked with an optional path to a custom configuration JSON.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

def run_script(script_path: Path, args: list[str] = []):
    cmd = [sys.executable, str(script_path)] + args
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Error:", result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

def main(config_path: str = "experiment_config.json"):
    # 1. Generate passwords
    run_script(BASE_DIR / "generate_passwords.py")
    # 2. Hash passwords
    run_script(BASE_DIR / "hash_passwords.py", [config_path])
    # 3. Simulate cracking
    run_script(BASE_DIR / "crack_simulation.py")
    # 4. Summarize metrics
    run_script(BASE_DIR / "metrics.py")
    print("Experiment pipeline completed.")

if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "experiment_config.json"
    main(cfg)
