#!/usr/bin/env python3
"""序列模块实战脚本（时间演化）。"""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "feature.to_sequential(property_name=callable)",
    "dt.Sequence(feature, sequence_length=...)",
]

PHYSICS = "序列模块用于时间演化仿真：每一帧按序更新属性，形成动态过程（旋转、位移、布朗运动等）。"


def rotation_step(sequence_length: int, previous_value: float) -> float:
    """每一步增加固定转角，构造可解释的时间演化规律。"""
    return previous_value + 2 * np.pi / sequence_length


def main() -> None:
    # 固定随机种子，保证演示一致。
    np.random.seed(2)
    print("=== 04_sequences ===")
    print("[代码意图] 将静态散射体转为动态序列，模拟时间变化过程。")
    print("[期望结果] 输出固定长度帧序列，并观察首帧统计。")
    print("[运行逻辑] 定义旋转更新函数 -> to_sequential -> Sequence 解析。")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    # 采用荧光成像系统，将序列散射体映射为图像帧。
    optics = dt.Fluorescence(
        NA=0.8,
        wavelength=680e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )

    # 定义初始椭圆散射体，后续通过 sequential 在时间上更新 rotation。
    ellipse = dt.Ellipse(
        radius=(1.0e-6, 0.5e-6),
        position=(32, 32),
        rotation=0.0,
        intensity=1,
    )

    # 将 rotation 属性变为“随时间递推”的属性，再生成序列。
    rotating = ellipse.to_sequential(rotation=rotation_step)
    sequence = dt.Sequence(optics(rotating), sequence_length=6)
    frames = sequence.resolve()

    print(f"frames: {len(frames)}")
    print("frame[0] shape:", np.asarray(frames[0]).shape)
    print("frame[0] min/max:", float(np.min(frames[0])), float(np.max(frames[0])))


if __name__ == "__main__":
    main()
