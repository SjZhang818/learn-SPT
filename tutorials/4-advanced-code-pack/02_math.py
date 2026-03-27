#!/usr/bin/env python3
"""数学后处理模块实战脚本。"""

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
    print("[代码意图] 演示图像后处理中的约束与归一化，建立可训练输入。")
    print("[期望结果] Clip 限幅、MinMax 线性归一化、Standard 标准化输出可区分。")
    print("[运行逻辑] 构造含负值与异常值的数组 -> 依次执行三种数学处理。")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    # 构造测试图像：包含负值与较大值，便于观察不同算子的效果。
    image = np.array([[-2.0, 0.5, 2.5], [3.2, -1.2, 0.0]], dtype=float)

    # Clip：将数据限制在 [0, 1]，常用于抑制异常值。
    clipped = dt.Clip(min=0.0, max=1.0).resolve(image)
    # MinMax：按最小值和最大值映射到 [0, 1]。
    minmax = dt.NormalizeMinMax(min=0.0, max=1.0).resolve(image)
    # Standard：标准化到零均值、单位标准差。
    standard = dt.NormalizeStandard().resolve(image)

    print("Input:\n", image)
    print("Clip [0,1]:\n", clipped)
    print("NormalizeMinMax [0,1]:\n", minmax)
    print("NormalizeStandard:\n", standard)


if __name__ == "__main__":
    main()
