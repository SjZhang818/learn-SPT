#!/usr/bin/env python3
"""高级与进阶整合示例：把核心高级模块串成一个完整仿真流水线。"""

# 说明：
# 该脚本用于“最终整合”要求，串联以下能力：
# 1) Source 参数化采样
# 2) MieSphere + Holography 物理成像
# 3) Zernike 像差 + Poisson/Gaussian 噪声
# 4) 数学归一化 + 增强 + 序列
# 5) 统计汇总（mean/std）

from __future__ import annotations

import numpy as np
import deeptrack as dt


def summarize_frame(tag: str, frame: np.ndarray) -> None:
    """打印帧统计信息，便于验证流水线是否按预期工作。"""
    arr = np.asarray(frame)
    print(
        f"[{tag}] shape={arr.shape}, min={arr.min():.6f}, "
        f"max={arr.max():.6f}, mean={arr.mean():.6f}, std={arr.std():.6f}"
    )


def main() -> None:
    """运行高级整合场景。"""
    # 固定随机种子，保证演示可重复。
    np.random.seed(42)

    print("=== 06_integrated_advanced ===")
    print("[代码意图] 将库里的高级能力组合为单条可执行链路，验证模块协同。")
    print("[期望结果] 得到一组可重复的全息时序图像，并输出统计特征用于后续学习/训练。")
    print("[运行逻辑] Source采样 -> Mie全息成像 -> 噪声/像差/增强 -> 序列化 -> 统计汇总。")

    # ---------- 1) 定义参数源（可扩展为批量实验配置） ----------
    source = dt.sources.Source(
        radius=[0.35e-6, 0.45e-6, 0.55e-6],
        refractive_index=[1.40 + 0.005j, 1.45 + 0.010j, 1.50 + 0.015j],
        z=[1.5e-6, 2.0e-6, 2.5e-6],
        snr=[18, 22, 26],
    )

    # ---------- 2) 定义全息成像系统 + 像差 ----------
    # Holography 体现干涉传播；Defocus 通过 pupil 注入焦面偏移像差。
    holography = dt.Holography(
        NA=0.8,
        wavelength=550e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
        pupil=dt.Defocus(coefficient=0.4),
        return_field=False,
    )

    # ---------- 3) 定义噪声与后处理 ----------
    # 先加泊松（光子统计）再加高斯（读出噪声），最后归一化并轻量增强。
    postprocess = (
        dt.Poisson(snr=source.snr, background=0.02)
        >> dt.Gaussian(mu=0.0, sigma=0.01)
        >> dt.NormalizeMinMax(min=0.0, max=1.0)
        >> dt.Affine(rotate=0.05, translate=(0.3, -0.2))
        >> dt.Clip(min=0.0, max=1.0)
    )

    # ---------- 4) 构建 Mie 粒子并做时间序列 ----------
    # 每一帧让 z 方向递增，模拟离焦/轴向运动。
    def z_step(sequence_length: int, previous_value: float) -> float:
        return previous_value + 0.2e-6

    mie = dt.MieSphere(
        radius=source.radius,
        refractive_index=source.refractive_index,
        position=(32, 32),
        z=source.z,
    ).to_sequential(z=z_step)

    # 完整链路：成像 + 后处理。
    pipeline = dt.Sequence(holography(mie) >> postprocess, sequence_length=5)

    # ---------- 5) 遍历 source，执行高级整合流程 ----------
    all_means: list[float] = []
    all_stds: list[float] = []

    for i in range(len(source)):
        # 设置当前 source 索引，让动态属性生效。
        source.set_index(i)
        frames = pipeline.resolve()

        # 输出样本级意图说明。
        print(
            f"\n[样本 {i}] radius={source[i]['radius']:.2e}, "
            f"n={source[i]['refractive_index']}, z0={source[i]['z']:.2e}, snr={source[i]['snr']}"
        )

        # 打印序列中首尾帧统计，确认时序变化。
        summarize_frame("frame[0]", frames[0])
        summarize_frame("frame[-1]", frames[-1])

        # 用统计模块做聚合（演示高级模块协作）。
        seq_stack = np.stack([np.asarray(f).squeeze() for f in frames], axis=0)
        seq_mean = float(dt.Mean().resolve(seq_stack))
        seq_std = float(dt.Std().resolve(seq_stack))
        print(f"  序列统计: mean={seq_mean:.6f}, std={seq_std:.6f}")

        all_means.append(seq_mean)
        all_stds.append(seq_std)

    # ---------- 6) 输出全局汇总 ----------
    print("\n[整合结果汇总]")
    print(f"全样本 mean 均值={float(np.mean(all_means)):.6f}")
    print(f"全样本 std 均值={float(np.mean(all_stds)):.6f}")
    print("说明：若参数变化与物理链路生效，样本间统计应出现可区分差异。")


if __name__ == "__main__":
    main()
