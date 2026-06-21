/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_node_cfg
// 功能概述: 复位节点配置对象 (Configuration Object)
//           定义复位节点所有可配置属性，由 crg_nodes 在 build_phase 中填充。
// 关键字段:
//   pre_nodes[]      — 前驱复位节点列表 (建立有向图边)
//   ci               — 绑定的 svk_clk_if 虚接口 (用于 sync_check)
//   ri               — 绑定的 svk_rst_if 虚接口
//   reg_fields[]     — 寄存器模型域引用 (优先级高于 hdl_path)
//   hdl_paths[]      — HDL 路径字符串 (备选配置读取)
//   up_time          — 复位高电平时间
//   down_time        — 复位低电平时间
//   is_active        — 是否激活复位驱动
//   glitch_check_en  — 是否使能毛刺检测
//   glitch_high_th   — 高毛刺阈值 (默认 10ns)
//   glitch_low_th    — 低毛刺阈值 (默认 10ns)
//   sync_check_en    — 是否使能同步检测
//   sync_ignore_th   — 同步容差阈值 (默认 0.0011ns)
//   is_end_point     — 是否末端节点 (1=校验检查点)
//   node_type        — 字符串标记节点类型
// ============================================================================

`ifndef SVK_RST_NODE_CFG__SV
`define SVK_RST_NODE_CFG__SV

typedef class svk_rst_node;

class svk_rst_node_cfg;
    svk_rst_node                pre_nodes[];
    virtual svk_clk_if          ci;
    virtual svk_rst_if          ri;
    uvm_reg_field               reg_fields[string];
    string                      hdl_paths[string];
    real                        up_time;
    real                        down_time;
    bit                         is_active;
    bit                         glitch_check_en;
    real                        glitch_high_th=10;
    real                        glitch_low_th=10;
    bit                         sync_check_en;
    real                        sync_ignore_th=0.0011;
    bit                         is_end_point;
    string                      node_type;


endclass

`endif
