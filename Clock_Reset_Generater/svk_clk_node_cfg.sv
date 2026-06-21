/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_node_cfg
// 功能概述: 时钟节点配置对象 (Configuration Object)
//           定义时钟节点所有可配置属性，由 crg_nodes 在 build_phase 中
//           填充，在 run_phase 中使用。
// 关键字段:
//   pre_nodes[]      — 前驱时钟节点列表 (建立有向图边)
//   ci               — 绑定的 svk_clk_if 虚接口
//   reg_fields[]     — 寄存器模型域引用 (寄存器配置读取, 优先级高于 hdl_path)
//   hdl_paths[]      — HDL 路径字符串 (直接 uvm_hdl_read 读取, 备选方案)
//   freqs[]          — 支持的频率列表 (用于 set_next_freq 随机切换)
//   current_freq     — 当前工作频率
//   duty_ratio       — 占空比 (默认 0.5)
//   jetter           — 抖动百分比 (默认 0.01 = 1%)
//   ppm              — 频率偏差 ppm (默认 1)
//   is_active        — 是否激活时钟驱动 (1=drive, 0=仅监控)
//   is_end_point     — 是否末端节点 (1=校验检查点)
//   glitch_check_en  — 是否使能毛刺检测
//   node_type        — 字符串标记节点类型
// ============================================================================

`ifndef SVK_CLK_NODE_CFG__SV
`define SVK_CLK_NODE_CFG__SV

typedef class svk_clk_node;

class svk_clk_node_cfg;
    svk_clk_node                pre_nodes[];
    virtual svk_clk_if          ci;
    uvm_reg_field               reg_fields[string];
    string                      hdl_paths[string];
    real                        freqs[];
    real                        duty_ratio=0.5;
    real                        jetter=0.01;
    real                        ppm=1;
    bit                         is_active;
    bit                         glitch_check_en;
    bit                         is_end_point;
    real                        current_freq=-1;
    string                      node_type;

    function void print();








    endfunction


endclass

`endif