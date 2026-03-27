#!/usr/bin/env python3
"""噪声模块实战脚本（含物理噪声解释）。"""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "dt.Gaussian(mu=..., sigma=...)",
    "dt.Poisson(snr=..., background=...)",
]

PHYSICS = "噪声模块模拟探测链路噪声：Gaussian近似读出噪声，Poisson近似光子计数散粒噪声。"


def main() -> None:
    # 固定随机种子，确保输出可复现，便于实验对比。
    np.random.seed(1)
    print("=== 01_noises ===")
    print("[代码意图] 展示成像噪声模型如何影响图像分布。")
    print("[期望结果] 高斯噪声与泊松噪声结果统计不同，串联后噪声更复杂。")
    print("[运行逻辑] 构造基准图 -> 分别加噪 -> 串联加噪 -> 对比统计。")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层物理逻辑]\n- {PHYSICS}")

    # 基准图像：常量灰度，便于观察噪声统计特性。
    base_image = np.ones((64, 64), dtype=float) * 0.5
    # 高斯噪声：近似读出噪声。
    gaussian = dt.Gaussian(mu=0.0, sigma=0.02)
    # 泊松噪声：近似光子计数散粒噪声。
    poisson = dt.Poisson(snr=15, background=0.05)

    # 分别执行单一噪声与串联噪声，比较输出范围与统计变化。
    gauss_img = gaussian.resolve(base_image)
    poisson_img = poisson.resolve(base_image)
    chained_img = (gaussian >> poisson).resolve(base_image)

    print(f"Gaussian result: shape={gauss_img.shape}, min={gauss_img.min():.6f}, max={gauss_img.max():.6f}")
    print(f"Poisson result: shape={poisson_img.shape}, min={poisson_img.min():.6f}, max={poisson_img.max():.6f}")
    print(f"Gaussian>>Poisson result: shape={chained_img.shape}, min={chained_img.min():.6f}, max={chained_img.max():.6f}")


if __name__ == "__main__":
    main()
