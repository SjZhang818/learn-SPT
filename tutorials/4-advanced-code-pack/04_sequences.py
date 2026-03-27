#!/usr/bin/env python3
"""Sequences module: categorized runnable examples."""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "feature.to_sequential(property_name=callable)",
    "dt.Sequence(feature, sequence_length=...)",
]

PHYSICS = "序列模块用于时间演化仿真：每一帧按序更新属性，形成动态过程（旋转、位移、布朗运动等）。"


def rotation_step(sequence_length: int, previous_value: float) -> float:
    return previous_value + 2 * np.pi / sequence_length


def main() -> None:
    np.random.seed(2)
    print("=== 04_sequences ===")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    optics = dt.Fluorescence(
        NA=0.8,
        wavelength=680e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )

    ellipse = dt.Ellipse(
        radius=(1.0e-6, 0.5e-6),
        position=(32, 32),
        rotation=0.0,
        intensity=1,
    )

    rotating = ellipse.to_sequential(rotation=rotation_step)
    sequence = dt.Sequence(optics(rotating), sequence_length=6)
    frames = sequence.resolve()

    print(f"frames: {len(frames)}")
    print("frame[0] shape:", np.asarray(frames[0]).shape)
    print("frame[0] min/max:", float(np.min(frames[0])), float(np.max(frames[0])))


if __name__ == "__main__":
    main()
