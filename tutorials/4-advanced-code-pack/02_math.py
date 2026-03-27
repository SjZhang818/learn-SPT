#!/usr/bin/env python3
"""Math module: categorized runnable examples."""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "dt.Clip(min=..., max=...)",
    "dt.NormalizeMinMax(min=..., max=...)",
    "dt.NormalizeStandard()",
]

PHYSICS = "数学模块是数值后处理层：做动态范围约束、归一化和标准化，便于后续训练与对比。"


def main() -> None:
    print("=== 02_math ===")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    image = np.array([[-2.0, 0.5, 2.5], [3.2, -1.2, 0.0]], dtype=float)

    clipped = dt.Clip(min=0.0, max=1.0).resolve(image)
    minmax = dt.NormalizeMinMax(min=0.0, max=1.0).resolve(image)
    standard = dt.NormalizeStandard().resolve(image)

    print("Input:\n", image)
    print("Clip [0,1]:\n", clipped)
    print("NormalizeMinMax [0,1]:\n", minmax)
    print("NormalizeStandard:\n", standard)


if __name__ == "__main__":
    main()
