#!/usr/bin/env python3
"""Sources 模块实战脚本（参数采样与数据组织）。"""

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
    # 固定随机种子，确保 split 与示例输出可复现。
    np.random.seed(3)
    print("=== 05_sources ===")
    print("[代码意图] 演示 Source 如何组织参数并驱动成像流水线。")
    print("[期望结果] 不同 source 索引生成不同样本，product/split 正常工作。")
    print("[运行逻辑] 建立 Source -> 绑定到粒子属性 -> set_index 逐样本解析。")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层逻辑]\n- {PHYSICS}")

    # 定义参数源：位置与强度按样本索引变化。
    source = dt.sources.Source(
        position=[(16, 16), (32, 32), (48, 48)],
        intensity=[80, 120, 160],
    )

    # 定义成像系统。
    optics = dt.Fluorescence(
        NA=0.8,
        wavelength=680e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )
    # 将 source 字段直接绑定到粒子属性，形成“参数 -> 成像”链路。
    particle = dt.PointParticle(position=source.position, intensity=source.intensity)
    pipeline = optics(particle)

    # 逐个索引激活 source 条目并解析图像。
    for i in range(len(source)):
        source.set_index(i)
        image = pipeline.resolve()
        print(f"sample {i}: position={source[i]['position']}, intensity={source[i]['intensity']}, shape={image.shape}")

    # product：笛卡尔积扩展参数组合。
    product = source.product(snr=[10, 20])
    print(f"product length={len(product)}")
    print(f"product[0]={product[0]}")

    # random_split：按指定长度做可复现划分。
    train, val = dt.sources.random_split(
        source,
        [2, 1],
        generator=np.random.default_rng(0),
    )
    print(f"split lengths: train={len(train)}, val={len(val)}")


if __name__ == "__main__":
    main()
