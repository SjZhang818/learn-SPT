#!/usr/bin/env python3
"""Noise module: categorized runnable examples."""

import numpy as np
import deeptrack as dt


COMMANDS = [
    "dt.Gaussian(mu=..., sigma=...)",
    "dt.Poisson(snr=..., background=...)",
]

PHYSICS = "噪声模块模拟探测链路噪声：Gaussian近似读出噪声，Poisson近似光子计数散粒噪声。"


def main() -> None:
    np.random.seed(1)
    print("=== 01_noises ===")
    print("\n[调用命令]")
    for cmd in COMMANDS:
        print(f"- {cmd}")
    print(f"\n[底层物理逻辑]\n- {PHYSICS}")

    base_image = np.ones((64, 64), dtype=float) * 0.5
    gaussian = dt.Gaussian(mu=0.0, sigma=0.02)
    poisson = dt.Poisson(snr=15, background=0.05)

    gauss_img = gaussian.resolve(base_image)
    poisson_img = poisson.resolve(base_image)
    chained_img = (gaussian >> poisson).resolve(base_image)

    print(f"Gaussian result: shape={gauss_img.shape}, min={gauss_img.min():.6f}, max={gauss_img.max():.6f}")
    print(f"Poisson result: shape={poisson_img.shape}, min={poisson_img.min():.6f}, max={poisson_img.max():.6f}")
    print(f"Gaussian>>Poisson result: shape={chained_img.shape}, min={chained_img.min():.6f}, max={chained_img.max():.6f}")


if __name__ == "__main__":
    main()
