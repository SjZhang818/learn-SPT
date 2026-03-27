#!/usr/bin/env python3
"""Sources module: categorized runnable examples."""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "dt.sources.Source(field_a=[...], field_b=[...])",
    "source.product(new_field=[...]) 或 dt.sources.Product(source, new_field=[...])",
    "dt.sources.random_split(source, [0.8, 0.2], generator=...)",
    "source.set_index(i) + 使用 source.field 作为特征输入",
]

PHYSICS = "Sources 模块是参数采样与数据组织层：把参数空间映射到可重复采样的数据流水线。"


def main() -> None:
    np.random.seed(3)
    print("=== 05_sources ===")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    source = dt.sources.Source(
        position=[(16, 16), (32, 32), (48, 48)],
        intensity=[80, 120, 160],
    )

    optics = dt.Fluorescence(
        NA=0.8,
        wavelength=680e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )
    particle = dt.PointParticle(position=source.position, intensity=source.intensity)
    pipeline = optics(particle)

    for i in range(len(source)):
        source.set_index(i)
        image = pipeline.resolve()
        print(f"sample {i}: position={source[i]['position']}, intensity={source[i]['intensity']}, shape={image.shape}")

    product = source.product(snr=[10, 20])
    print(f"product length={len(product)}")
    print(f"product[0]={product[0]}")

    train, val = dt.sources.random_split(
        source,
        [2, 1],
        generator=np.random.default_rng(0),
    )
    print(f"split lengths: train={len(train)}, val={len(val)}")


if __name__ == "__main__":
    main()
