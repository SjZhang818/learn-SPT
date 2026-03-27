#!/usr/bin/env python3
"""Augmentations module: categorized runnable examples."""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "dt.FlipLR(p=..., augment=...)",
    "dt.Affine(scale=..., translate=..., rotate=..., shear=...)",
    "dt.Crop(crop=..., corner=..., crop_mode='retain'|'remove')",
    "dt.Pad(px=..., mode='constant', cval=...)",
]

PHYSICS = "增强模块是观测域变换（几何扰动/视场变化），用于模拟实验波动与提升模型鲁棒性。"


def main() -> None:
    print("=== 03_augmentations ===")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    image = np.arange(1, 17, dtype=float).reshape(4, 4)

    fliplr = dt.FlipLR(augment=True).resolve(image)
    affine = dt.Affine(scale=(1.1, 0.9), translate=(0.5, -0.5), rotate=0.15).resolve(image)
    crop = dt.Crop(crop=(2, 2), corner=(1, 1)).resolve(image)
    pad = dt.Pad(px=(1, 1, 2, 2), mode="constant", cval=-1).resolve(image)

    print("Input:\n", image)
    print("FlipLR:\n", fliplr)
    print("Affine shape:", affine.shape)
    print("Crop:\n", crop)
    print("Pad shape:", pad.shape)


if __name__ == "__main__":
    main()
