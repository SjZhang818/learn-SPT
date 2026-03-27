#!/usr/bin/env python3
"""Run all categorized advanced DeepTrack examples."""

from pathlib import Path
import subprocess
import sys


SCRIPTS = [
    "00_scatterers_optics.py",
    "01_noises.py",
    "02_math.py",
    "03_augmentations.py",
    "04_sequences.py",
    "05_sources.py",
]


def main() -> None:
    base = Path(__file__).resolve().parent
    for script in SCRIPTS:
        script_path = base / script
        print(f"\n===== Running {script} =====")
        subprocess.run([sys.executable, str(script_path)], check=True)

    print("\nAll categorized scripts ran successfully.")


if __name__ == "__main__":
    main()
