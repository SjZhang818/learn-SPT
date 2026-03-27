#!/usr/bin/env python3
"""数据增强模块实战脚本。"""

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
    print("[代码意图] 展示几何增强对观测域的扰动，模拟实验条件变化。")
    print("[期望结果] 翻转/仿射/裁剪/填充分别改变方向、形状、视野与边界。")
    print("[运行逻辑] 以小矩阵为样例，逐个执行增强并打印结果。")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    # 使用可读性高的 4x4 数字矩阵，便于肉眼检查增强正确性。
    image = np.arange(1, 17, dtype=float).reshape(4, 4)

    # 左右翻转：模拟视野镜像变化。
    fliplr = dt.FlipLR(augment=True).resolve(image)
    # 仿射变换：包含缩放、平移、旋转。
    affine = dt.Affine(scale=(1.1, 0.9), translate=(0.5, -0.5), rotate=0.15).resolve(image)
    # 裁剪：保留局部区域。
    crop = dt.Crop(crop=(2, 2), corner=(1, 1)).resolve(image)
    # 填充：在图像外围补边。
    pad = dt.Pad(px=(1, 1, 2, 2), mode="constant", cval=-1).resolve(image)

    print("Input:\n", image)
    print("FlipLR:\n", fliplr)
    print("Affine shape:", affine.shape)
    print("Crop:\n", crop)
    print("Pad shape:", pad.shape)


if __name__ == "__main__":
    main()
