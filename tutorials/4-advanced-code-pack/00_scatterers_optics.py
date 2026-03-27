#!/usr/bin/env python3
"""散射体 + 光学模块实战脚本（从浅到深）。"""

import numpy as np
import deeptrack as dt


COMMANDS = {
    "scatterers": [
        "dt.PointParticle(position=..., intensity=...)",
        "dt.Sphere(radius=..., position=..., intensity=...)",
        "dt.Ellipse(radius=(...), position=..., rotation=..., intensity=...)",
        "dt.MieSphere(radius=..., refractive_index=..., position=..., z=...)",
    ],
    "optics": [
        "dt.Fluorescence(NA=..., wavelength=..., magnification=..., resolution=..., output_region=...)",
        "dt.Brightfield(NA=..., wavelength=..., magnification=..., resolution=..., output_region=...)",
        "dt.Holography(..., return_field=False)",
    ],
}

PHYSICS = {
    "scatterers": "散射体模块定义样本的空间分布、尺寸、形状和折射率等参数，是成像前的物理对象。",
    "optics": "成像模块把样本场映射到探测面：荧光近似点扩散卷积，明场/全息考虑相位与干涉传播。",
}


def summarize(name: str, image: np.ndarray) -> None:
    """打印图像统计信息，便于判断成像链路是否符合预期。"""
    arr = np.asarray(image)
    print(f"[{name}] shape={arr.shape}, dtype={arr.dtype}, min={arr.min():.6f}, max={arr.max():.6f}")


def main() -> None:
    # 固定随机种子，保证每次演示结果可复现。
    np.random.seed(0)
    print("=== 00_scatterers_optics ===")
    print("[代码意图] 用最核心的散射体与成像器件组合，演示物理建模到成像输出的完整闭环。")
    print("[期望结果] 不同散射体在不同光学系统下输出统计明显不同，体现物理差异。")
    print("[运行逻辑] 定义散射体 -> 定义光学系统 -> 成像并输出统计。")
    print("\n[调用命令]")
    for key, cmds in COMMANDS.items():
        print(f"- {key}:")
        for cmd in cmds:
            print(f"  - {cmd}")

    print("\n[底层物理逻辑]")
    for key, text in PHYSICS.items():
        print(f"- {key}: {text}")

    # 荧光成像：近似以 PSF 卷积方式形成图像（非相干叠加）。
    fluorescence = dt.Fluorescence(
        NA=0.8,
        wavelength=680e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )
    # 明场成像：考虑相位传播与透射影响。
    brightfield = dt.Brightfield(
        NA=0.8,
        wavelength=550e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )
    # 全息成像：通过干涉场形成强度图，可用于三维信息恢复。
    holography = dt.Holography(
        NA=0.8,
        wavelength=550e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
        return_field=False,
    )

    # 定义从简单到复杂的散射体：点粒子 -> 球体 -> 椭圆体 -> Mie 球。
    point = dt.PointParticle(position=(32, 32), intensity=200)
    sphere = dt.Sphere(radius=1e-6, position=(32, 32), intensity=1)
    ellipse = dt.Ellipse(
        radius=(1.2e-6, 0.7e-6),
        position=(32, 32),
        rotation=np.pi / 6,
        intensity=1,
    )
    mie_sphere = dt.MieSphere(
        radius=0.5e-6,
        refractive_index=1.45 + 0.01j,
        position=(32, 32),
        z=2e-6,
    )

    # 执行成像并输出结果统计，便于快速对比不同物理设定。
    summarize("Fluorescence(PointParticle)", fluorescence(point).resolve())
    summarize("Fluorescence(Sphere)", fluorescence(sphere).resolve())
    summarize("Fluorescence(Ellipse)", fluorescence(ellipse).resolve())
    summarize("Brightfield(Sphere)", brightfield(sphere).resolve())
    summarize("Holography(MieSphere)", holography(mie_sphere).resolve())


if __name__ == "__main__":
    main()
