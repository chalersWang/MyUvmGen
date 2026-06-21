# Clock_Reset_Generater 架构文档

> UVM 时钟与复位树验证组件库（CRG — Clock & Reset Generator）
>
> 版本: v2.0 | 作者: ChalersWang (19910619333@189.cn) | 日期: 2026-06

---

## 1. 概述

Clock_Reset_Generater 是一个基于 SystemVerilog/UVM 的**时钟与复位树建模与验证组件库**。它将 DUT 的时钟树和复位树抽象为有向图节点，支持：

- 多种时钟节点类型：驱动源、PLL、分频器、选择器、门控、直通
- 多种复位节点类型：驱动源、可配置、AND 门、选择器、同步器、直通
- 自动生成节点拓扑（从 Excel 配置文件读取）
- 时钟周期/占空比/jitter/ppm 校验、毛刺检测
- 复位值校验、同步校验、毛刺检测
- 寄存器域（reg_field）和 HDL 路径（hdl_path）双模式配置读取

---

## 2. 文件清单（27 个文件）

| # | 文件名 | 层 | 说明 |
|---|--------|----|------|
| 1 | `svk_crg_pkg.sv` | 包 | 顶层 package，`include` 所有类 |
| 2 | `svk_crg.sv` | 全局查找 | 全局 clock/retest 接口关联数组 + 通配符查找 |
| 3 | `svk_crg_if.sv` | 接口容器 | 参数化 clock/retest 接口组容器 |
| 4 | `crg_nodes.sv` | 拓扑编排 | UVM 组件，实例化并配置全部节点 |
| 5 | `crg_if_inst.sv` | 接口实例 | 具体 DUT 的 clk_if/rst_if 实例化（代码生成模板） |
| 6 | `crg_nodes.xlsm` | 配置文件 | Excel 配置表（CLK 页 + RST 页），定义节点拓扑 |
| 7 | `gen_crg_nodes.py` | 代码生成器 | 读取 .xlsm 自动生成 crg_nodes.sv 和 crg_if_inst.sv |
| 8 | `svk_clk_if.sv` | 接口层 | 时钟物理接口，force/release 驱动实际时钟线 |
| 9 | `svk_clk_node_cfg.sv` | 配置层 | 时钟节点配置对象 |
| 10 | `svk_clk_node.sv` | 基类层 | 时钟节点抽象基类（virtual class） |
| 11 | `svk_clk_drv_node.sv` | 时钟节点 | 时钟驱动源节点 |
| 12 | `svk_clk_pll_node.sv` | 时钟节点 | PLL 锁相环节点 |
| 13 | `svk_clk_div_node.sv` | 时钟节点 | 时钟分频器节点 |
| 14 | `svk_clk_sel_node.sv` | 时钟节点 | 时钟多路选择器节点 |
| 15 | `svk_clk_gate_node.sv` | 时钟节点 | 时钟门控节点 |
| 16 | `svk_clk_wire_node.sv` | 时钟节点 | 时钟直通节点 |
| 17 | `svk_clk_interface.sv` | 接口层(legacy) | 旧版时钟接口（含 check/glitch_check/close 等） |
| 18 | `svk_rst_if.sv` | 接口层 | 复位物理接口，force 驱动实际复位线 |
| 19 | `svk_rst_node_cfg.sv` | 配置层 | 复位节点配置对象 |
| 20 | `svk_rst_node.sv` | 基类层 | 复位节点抽象基类（virtual class） |
| 21 | `svk_rst_drv_node.sv` | 复位节点 | 复位驱动源节点 |
| 22 | `svk_rst_cfg_node.sv` | 复位节点 | 可配置复位节点（pre_rst & cfg_bit） |
| 23 | `svk_rst_and_node.sv` | 复位节点 | 复位与门节点（多输入 AND） |
| 24 | `svk_rst_sel_node.sv` | 复位节点 | 复位选择器节点（二选一 MUX） |
| 25 | `svk_rst_sync_node.sv` | 复位节点 | 同步复位节点（直通 + sync check） |
| 26 | `svk_rst_wire_node.sv` | 复位节点 | 复位直通节点 |
| 27 | `svk_rst_interface.sv` | 接口层(legacy) | 旧版复位接口（含 init/is_pull_up/sync 检测等） |

---

## 3. 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                    应用层 / 测试用例                        │
│   实例化 crg_nodes, 调用 check_clk() / check_rst()      │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│              拓扑编排层                                   │
│  svk_crg_pkg  ─── 顶层包，聚合所有类                      │
│  svk_crg      ─── 全局 clk_ifs[] / rst_ifs[] 接口查找      │
│  crg_nodes    ─── UVM组件，构建节点图并配置                 │
│  crg_if_inst  ─── 接口实例化（gen脚本输出）                 │
└─────────────────────────────────────────────────────────┘
                            │
┌──────────────────┬──────────────────────────────────────┐
│   时钟节点体系    │           复位节点体系                  │
│                  │                                      │
│  svk_clk_node    │    svk_rst_node                      │
│  (virtual class) │    (virtual class)                   │
│    ├─ drv_node   │      ├─ drv_node                     │
│    ├─ pll_node   │      ├─ cfg_node                     │
│    ├─ div_node   │      ├─ and_node                     │
│    ├─ sel_node   │      ├─ sel_node                     │
│    ├─ gate_node  │      ├─ sync_node                    │
│    └─ wire_node  │      └─ wire_node                    │
│                  │                                      │
│  svk_clk_node_cfg│    svk_rst_node_cfg                  │
└──────────────────┴──────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│              物理接口层                                   │
│  svk_clk_if  ── force/release 驱动时钟线                 │
│  svk_rst_if  ── force 驱动复位线                        │
│  svk_clk_interface / svk_rst_interface  (legacy)        │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│              代码生成层                                   │
│  crg_nodes.xlsm ──(xlwings)──▶ gen_crg_nodes.py        │
│                       │                                 │
│                ┌──────┴──────┐                          │
│           crg_nodes.sv  crg_if_inst.sv                  │
└─────────────────────────────────────────────────────────┘
```

---

## 4. 类层次结构

### 4.1 时钟节点体系

```
uvm_component
  └─ svk_clk_node (virtual abstract class)
       ├─ svk_clk_drv_node   — 驱动源（根节点/时钟发生器）
       ├─ svk_clk_pll_node   — PLL锁相环（从寄存器读取参数计算期望频率）
       ├─ svk_clk_div_node   — 分频器（period = pre_period × (div+1)）
       ├─ svk_clk_sel_node   — 选择器（根据 sel 位选择前驱节点）
       ├─ svk_clk_gate_node  — 门控（gate=0 则时钟关闭 period=0）
       └─ svk_clk_wire_node  — 直通（透传前一节点时钟）
```

### 4.2 复位节点体系

```
uvm_component
  └─ svk_rst_node (virtual abstract class)
       ├─ svk_rst_drv_node   — 驱动源（根节点/复位发生器）
       ├─ svk_rst_cfg_node   — 可配置复位（pre_rst & cfg_bit）
       ├─ svk_rst_and_node   — AND门（多前驱 & 多寄存器/HDL位 ALL AND）
       ├─ svk_rst_sel_node   — 选择器（根据 sel 位选择前驱节点）
       ├─ svk_rst_sync_node  — 同步器（直通 + 自动同步校验）
       └─ svk_rst_wire_node  — 直通（透传前一节点复位）
```

---

## 5. 节点图（有向图）

时钟和复位各自构成**有向无环图 (DAG)**：

- 每个节点通过 `cfg.node_numbers[]` (pre_nodes) 引用其前驱节点
- `cfg.is_end_point` 标记末端节点，`check_clk()`/`check_rst()` 从末端节点开始递归校验

```
示例时钟拓扑:

  clk_in1 ──▶ [drv_node1] ──────────────────────────────┐
                                              ┌──────────┤
  clk_in2 ──▶ [drv_node2] ──┐                 ▼
                              ├──▶ [sel_node4] ──▶ [div_node5] ──▶ [gate_node6] ──▶ [wire_node7] ──▶ clk_out
  [drv_node1] ──▶ [pll_node3] ─┘

示例复位拓扑:

  rst_in1 ──▶ [drv_node1] ──┐
                              ├──▶ [sel_node4] ──▶ [and_node5] ──▶ [sync_node6] ──▶ [cfg_node7] ──▶ [wire_node8] ──▶ rst_out
  rst_in2 ──▶ [drv_node2] ──┤
  rst_in3 ──▶ [drv_node3] ──┘
```

---

## 6. 核心机制

### 6.1 时钟驱动机制 (`svk_clk_if.drive()`)

```
  force clk=0 → delay(PERIOD_L) → force clk=1 → delay(PERIOD_H)
                                           ↓
  force clk=0 → delay(PERIOD_L-ppm-jitter) → force clk=1 → delay(PERIOD_H-ppm-jitter)
```

- 使用 `force/release` 语句物理驱动时钟线
- jitter 模拟：第 1 个半周期加 jitter，第 2 个半周期减 jitter
- ppm 模拟：每个半周期叠加 ppm 偏置
- 支持 `stop_clk` 停止时钟，`undrive()` 释放

### 6.2 期望值递归计算 (`get_expe_clk()`)

每个时钟节点根据**前驱节点**和**配置参数**递归计算期望周期和占空比：

| 节点类型 | 期望周期公式 |
|----------|------------|
| drv_node | `period = ci.period`（直接取配置值） |
| pll_node | `period = pre_period × refdiv / (fbdiv + frac/2^24)`（DSM 使能时） |
| div_node | `period = pre_period × (div + 1)` |
| sel_node | 取被选中的前驱节点值 |
| gate_node | gate=0 → period=0; gate=1 → 取前驱节点值 |
| wire_node | 直接透传前驱节点值 |

### 6.3 期望值递归计算 (`get_expe_rst()`)

| 节点类型 | 期望复位值公式 |
|----------|--------------|
| drv_node | `rst = ri.rst`（直接读取物理接口） |
| cfg_node | `rst = pre_rst & cfg_bit` |
| and_node | `rst = pre0 & pre1 & ... & reg0 & reg1 & ... & hdl0 & hdl1 & ...` |
| sel_node | 取被选中的前驱节点值 |
| sync_node | 直接透传前驱节点值 |
| wire_node | 直接透传前驱节点值 |

### 6.4 配置读取双模式

每个节点支持两种配置读取方式：
1. **reg_field 模式** — 通过 UVM 寄存器模型 `reg_fields[string]` 读取
2. **hdl_path 模式** — 通过 `uvm_hdl_read()` 直接读取 DUT 信号

优先级：`reg_fields.exists(key)` → reg_field，否则 → hdl_path

### 6.5 频率切换 (`set_next_freq()`)

时钟驱动源可在 `freqs[]` 列表中动态切换频率（模拟 DVFS/变频场景）。

---

## 7. 校验功能一览

| 功能 | 时钟 | 复位 | 说明 |
|------|:----:|:----:|------|
| 周期校验 | ✅ | — | 实测周期 vs 期望周期 (±jitter±ppm 容差) |
| 占空比校验 | ✅ | — | 实测占空比 vs 期望占空比 (±jitter 容差) |
| 毛刺检测 | ✅ | ✅ | 半周期低于阈值→报警 |
| 复位值校验 | — | ✅ | 期望复位值 vs 实测复位值 |
| 同步校验 | — | ✅ | 复位沿 vs 时钟沿时间差检测 |

---

## 8. 代码生成流程 (`gen_crg_nodes.py`)

```
┌─────────────────┐
│ crg_nodes.xlsm  │  Excel 配置文件
│  ├─ CLK sheet   │  时钟节点定义表
│  └─ RST sheet   │  复位节点定义表
└────────┬────────┘
         │ xlwings 读取
         ▼
┌─────────────────┐
│ gen_crg_nodes.py│  Python 代码生成器
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
crg_nodes.sv  crg_if_inst.sv
```

### Excel CLK 表列说明：
`node_type | node_number | pre_node | clk_hire | freqs | current_freq | duty_ratio | jetter | ppm | cfgs | is_active | is_end_point | glitch_check_en | gen_en`

### Excel RST 表列说明：
`node_type | node_number | pre_node | rst_hire | sync_check_en | sync_clk | up_time | down_time | cfgs | glitch_check_en | glitch_high_th | glitch_low_th | is_active | is_end_point | gen_en`

---

## 9. 使用示例

```systemverilog
// 1. 在 testbench 顶层 include 接口实例化模板
`include "crg_if_inst.sv"

// 2. 在 build_phase 创建 crg_nodes
crg_nodes crg;
crg = crg_nodes::type_id::create("crg", this);

// 3. 在合适时机校验时钟和复位
crg.check_clk();   // 递归校验所有 is_end_point=1 的时钟节点
crg.check_rst();   // 递归校验所有 is_end_point=1 的复位节点
```

---

## 10. 依赖关系

```
外部依赖:
  ├─ uvm_pkg       — UVM 1.2 标准库
  ├─ xlwings       — Python Excel 操作库（仅 gen_crg_nodes.py）
  └─ xxx_reg_block — 用户寄存器模型（需在 crg_nodes 中替换）

内部依赖链:
  svk_clk_if ← svk_clk_node_cfg ← svk_clk_node ← (各时钟子类)
  svk_rst_if ← svk_rst_node_cfg ← svk_rst_node ← (各复位子类)
  svk_crg_pkg ← 所有类
  crg_nodes ← svk_crg + 所有节点类 + 寄存器模型
```

---

## 11. Legacy 接口说明

`svk_clk_interface.sv` 和 `svk_rst_interface.sv` 为旧版接口实现：

| 新版 | 旧版 | 差异 |
|------|------|------|
| `svk_clk_if` | `svk_clk_interface` | 旧版 more features (is_closed, stop_check_glitch)，但接口更重 |
| `svk_rst_if` | `svk_rst_interface` | 旧版 more features (init, is_pull_up/down, is_syn_with)，但接口更重 |

建议新项目使用新版 `svk_clk_if` / `svk_rst_if` + 节点体系。
