# Advanced code pack（按模块整理的可运行代码）

本目录把常见模块按类别整理为**独立可运行脚本**，每个脚本都包含：

1. 模块调用命令（API 速查）
2. 底层物理/数值逻辑简介
3. 对应功能的可运行实例代码

## 目录

- `00_scatterers_optics.py`：散射体与成像模块（PointParticle/Sphere/Ellipse/MieSphere + Fluorescence/Brightfield/Holography）
- `01_noises.py`：噪声模块（Gaussian / Poisson）
- `02_math.py`：数学处理模块（Clip / NormalizeMinMax / NormalizeStandard）
- `03_augmentations.py`：增强模块（FlipLR / Affine / Crop / Pad）
- `04_sequences.py`：序列模块（to_sequential / Sequence）
- `05_sources.py`：数据源模块（Source / Product / random_split）
- `run_all.py`：一键串行运行全部脚本

## 运行方式

在仓库根目录下执行：

```bash
cd /home/runner/work/learn-SPT/learn-SPT
python tutorials/4-advanced-code-pack/00_scatterers_optics.py
python tutorials/4-advanced-code-pack/01_noises.py
python tutorials/4-advanced-code-pack/02_math.py
python tutorials/4-advanced-code-pack/03_augmentations.py
python tutorials/4-advanced-code-pack/04_sequences.py
python tutorials/4-advanced-code-pack/05_sources.py
```

或者一键运行：

```bash
python tutorials/4-advanced-code-pack/run_all.py
```

## 依赖

```bash
cd /home/runner/work/learn-SPT/learn-SPT
python -m pip install -r requirements.txt
python -m pip install -e .
```
