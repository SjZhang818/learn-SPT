# Advanced code pack（从浅到深的指令整理 + 实战整合）

本目录用于满足以下目标：

1. **整理主要公开指令**，并说明每个指令用途。
2. 对涉及物理建模的模块，**明确给出物理法则定义**。
3. 给出**可直接运行的实战代码**，并附中文注释、代码意图、期望结果、运行逻辑。
4. 最后提供**高级与进阶整合脚本**，把关键模块串成一条完整链路。

## 目录

- `00_api_catalog.py`：库内主要公开指令总表（按模块），含用途与物理法则映射
- `00_scatterers_optics.py`：散射体与成像模块（PointParticle/Sphere/Ellipse/MieSphere + Fluorescence/Brightfield/Holography）
- `01_noises.py`：噪声模块（Gaussian / Poisson）
- `02_math.py`：数学处理模块（Clip / NormalizeMinMax / NormalizeStandard）
- `03_augmentations.py`：增强模块（FlipLR / Affine / Crop / Pad）
- `04_sequences.py`：序列模块（to_sequential / Sequence）
- `05_sources.py`：数据源模块（Source / Product / random_split）
- `06_integrated_advanced.py`：高级与进阶整合（Source + MieSphere + Holography + Aberration + Noise + Math + Augmentation + Sequence + Statistics）
- `run_all.py`：一键串行运行全部脚本

## 运行方式

在仓库根目录下执行：

```bash
cd <repository-root>
python tutorials/4-advanced-code-pack/00_scatterers_optics.py
python tutorials/4-advanced-code-pack/01_noises.py
python tutorials/4-advanced-code-pack/02_math.py
python tutorials/4-advanced-code-pack/03_augmentations.py
python tutorials/4-advanced-code-pack/04_sequences.py
python tutorials/4-advanced-code-pack/05_sources.py
python tutorials/4-advanced-code-pack/06_integrated_advanced.py
```

或者一键运行：

```bash
python tutorials/4-advanced-code-pack/run_all.py
```

## 物理法则（本目录涉及）

- **Mie 散射理论**：用于 `MieSphere` 等球形粒子的电磁散射计算（球谐展开 + 边界条件）。
- **傅里叶光学 / 衍射理论**：用于 `Fluorescence`、`Brightfield`、`Holography` 的成像传播建模。
- **Zernike 像差模型**：用于 `Defocus` 等像差在孔径函数上的相位调制。
- **统计噪声模型**：`Gaussian` 对应读出噪声，`Poisson` 对应光子散粒噪声。

## 依赖

```bash
cd <repository-root>
python -m pip install -r requirements.txt
python -m pip install -e .
```
