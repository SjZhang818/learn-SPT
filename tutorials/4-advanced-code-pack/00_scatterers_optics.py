#!/usr/bin/env python3
"""Scatterers + Optics: categorized runnable examples."""

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
    arr = np.asarray(image)
    print(f"[{name}] shape={arr.shape}, dtype={arr.dtype}, min={arr.min():.6f}, max={arr.max():.6f}")


def main() -> None:
    np.random.seed(0)
    print("=== 00_scatterers_optics ===")
    print("\n[调用命令]")
    for key, cmds in COMMANDS.items():
        print(f"- {key}:")
        for cmd in cmds:
            print(f"  - {cmd}")

    print("\n[底层物理逻辑]")
    for key, text in PHYSICS.items():
        print(f"- {key}: {text}")

    fluorescence = dt.Fluorescence(
        NA=0.8,
        wavelength=680e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )
    brightfield = dt.Brightfield(
        NA=0.8,
        wavelength=550e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
    )
    holography = dt.Holography(
        NA=0.8,
        wavelength=550e-9,
        magnification=10,
        resolution=1e-6,
        output_region=(0, 0, 64, 64),
        return_field=False,
    )

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

    summarize("Fluorescence(PointParticle)", fluorescence(point).resolve())
    summarize("Fluorescence(Sphere)", fluorescence(sphere).resolve())
    summarize("Fluorescence(Ellipse)", fluorescence(ellipse).resolve())
    summarize("Brightfield(Sphere)", brightfield(sphere).resolve())
    summarize("Holography(MieSphere)", holography(mie_sphere).resolve())


if __name__ == "__main__":
    main()
