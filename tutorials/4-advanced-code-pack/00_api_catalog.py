#!/usr/bin/env python3
"""DeepTrack 指令总表（按模块自动整理，含用途与物理法则）。"""

# 说明：
# 1) 本脚本用于“先总览后实战”，自动扫描公开模块中的类与函数。
# 2) 输出内容包括：指令名、用途（doc 首行）、物理法则（若适用）。
# 3) 这是从浅到深整合的第 0 步：先建立完整 API 地图。

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass


# 物理模块法则映射：用于回答“设计物理规律计算的要给出定义法则”。
PHYSICS_LAWS = {
    "deeptrack.scatterers": "几何散射与 Mie 散射：球谐展开、电磁散射边界条件（Riccati-Bessel 递推）。",
    "deeptrack.optics": "傅里叶光学与衍射成像：NA 截止、点扩散函数（PSF）、相位传播与干涉。",
    "deeptrack.holography": "Fresnel/角谱传播：频域传播核与逆传播重建。",
    "deeptrack.aberrations": "Zernike 多项式像差建模：在孔径函数上施加相位调制。",
    "deeptrack.noises": "探测噪声统计：高斯读出噪声 + 泊松光子散粒噪声。",
}


# 按“浅 -> 深”组织模块。
MODULES_IN_ORDER = [
    "deeptrack.features",
    "deeptrack.properties",
    "deeptrack.sources.base",
    "deeptrack.scatterers",
    "deeptrack.optics",
    "deeptrack.aberrations",
    "deeptrack.noises",
    "deeptrack.augmentations",
    "deeptrack.math",
    "deeptrack.elementwise",
    "deeptrack.statistics",
    "deeptrack.sequences",
    "deeptrack.holography",
]


@dataclass
class SymbolItem:
    """用于承载单个公开指令信息。"""

    name: str
    command: str
    kind: str
    purpose: str


def build_command(module_name: str, symbol_name: str) -> str:
    """根据模块构造用户常见调用写法。"""
    # 源模块使用 dt.sources 前缀更符合仓库教程写法。
    if module_name.startswith("deeptrack.sources"):
        return f"dt.sources.{symbol_name}(...)"
    return f"dt.{symbol_name}(...)"


def collect_symbols(module_name: str) -> list[SymbolItem]:
    """收集模块内公开类/函数并附带用途说明。"""
    module = importlib.import_module(module_name)
    items: list[SymbolItem] = []

    for name, obj in vars(module).items():
        # 过滤私有符号。
        if name.startswith("_"):
            continue

        # 仅保留定义在本模块的类/函数，避免导入污染。
        obj_module = getattr(obj, "__module__", "")
        if not obj_module.startswith(module_name):
            continue

        # 仅统计可直接调用的公开类与函数。
        if inspect.isclass(obj):
            kind = "class"
        elif inspect.isfunction(obj):
            kind = "function"
        else:
            continue

        # 读取 doc 首行作为用途摘要。
        doc = inspect.getdoc(obj) or ""
        first_line = doc.splitlines()[0].strip() if doc else "（暂无文档说明）"
        items.append(
            SymbolItem(
                name=name,
                command=build_command(module_name, name),
                kind=kind,
                purpose=first_line,
            )
        )

    # 统一排序，保证输出稳定可复现。
    items.sort(key=lambda x: (x.kind, x.name.lower()))
    return items


def print_module_catalog(module_name: str) -> None:
    """打印单模块指令总表。"""
    print(f"\n=== 模块：{module_name} ===")

    # 打印模块对应物理法则（若定义）。
    law = PHYSICS_LAWS.get(module_name)
    if law:
        print(f"[物理法则] {law}")
    else:
        print("[物理法则] 本模块以数据流程/数值处理为主，不直接定义新的物理传播定律。")

    symbols = collect_symbols(module_name)
    print(f"[公开指令数量] {len(symbols)}")

    # 输出每个指令的用途。
    for idx, item in enumerate(symbols, start=1):
        print(f"{idx:03d}. {item.command}  ({item.kind})")
        print(f"     用途：{item.purpose}")


def print_overall_intent() -> None:
    """打印脚本意图、期望结果与运行逻辑。"""
    print("=== 00_api_catalog ===")
    print("[代码意图] 整理库中主要公开指令，按模块给出用途，并对物理模块给出法则定义。")
    print("[期望结果] 运行后得到从浅到深的 API 目录，可直接作为后续实战脚本索引。")
    print("[运行逻辑] 通过反射扫描模块 -> 过滤公开类/函数 -> 输出调用写法与用途摘要。")


def main() -> None:
    """脚本主流程。"""
    # 第一步：打印总体意图。
    print_overall_intent()

    # 第二步：按浅到深顺序打印每个模块目录。
    for module_name in MODULES_IN_ORDER:
        print_module_catalog(module_name)


if __name__ == "__main__":
    main()
