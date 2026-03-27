#!/usr/bin/env python3
"""运行全部“从浅到深”高级代码包脚本。"""

from pathlib import Path
import subprocess
import sys


SCRIPTS = [
    "00_api_catalog.py",
    "00_scatterers_optics.py",
    "01_noises.py",
    "02_math.py",
    "03_augmentations.py",
    "04_sequences.py",
    "05_sources.py",
    "06_integrated_advanced.py",
]


def main() -> None:
    # 逐个脚本串行执行，任何一个失败则立即抛错中断。
    base = Path(__file__).resolve().parent
    for script in SCRIPTS:
        script_path = base / script
        print(f"\n===== Running {script} =====")
        try:
            subprocess.run([sys.executable, str(script_path)], check=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"脚本执行失败：{script}") from exc

    print("\nAll categorized scripts ran successfully.")


if __name__ == "__main__":
    main()
