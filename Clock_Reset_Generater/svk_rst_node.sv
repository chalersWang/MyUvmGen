/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_node (Abstract Virtual Class)
// 功能概述: 复位节点抽象基类
//           所有具体复位节点 (drv/cfg/and/sel/sync/wire) 的公共基类。
//           定义统一接口: get_expe_rst(), get_real_rst(), check_rst(),
//           check_glitch(), check_sync(), set_rst(), run_phase()。
// 纯虚方法 (子类必须实现):
//   get_expe_rst(rst)  — 计算期望复位值
// 公共方法 (基类实现):
//   get_real_rst(rst)  — 从物理接口读取实际复位值
//   check_rst()        — 对比期望复位值 vs 实际复位值, 不匹配报 UVM_ERROR
//   check_glitch()     — 监测复位毛刺 (高/低脉冲宽度 < glitch_high_th/glitch_low_th)
//   check_sync()       — 检测复位释放是否与时钟同步 (posedge rst 与 posedge clk 时间差)
//   set_rst(rst)       — 强制设置复位值
//   run_phase()        — UVM run_phase: 启动 drive + glitch_check + sync_check
// ============================================================================

`ifndef SVK_RST_NODE__SV
`define SVK_RST_NODE__SV

virtual class svk_rst_node extends uvm_component;

    svk_rst_node_cfg       cfg;

    // 构造函数: 实例化 cfg 配置对象 (svk_rst_node_cfg)
    extern function new(string name="svk_rst_node", uvm_component parent=null);
    // [纯虚方法] 计算期望复位值 (子类必须实现)
    // drv_node: ri.rst   cfg_node: pre_rst & cfg_bit   and_node: 多输入 AND
    // sel_node: 选择前驱   sync_node/wire_node: 透传
    pure virtual task get_expe_rst(output logic rst);
    // 读取实际复位值: 从物理接口 ri.rst 直接取值
    extern virtual task get_real_rst(output logic rst);
    // 复位值校验: 对比期望 vs 实际复位值, 不匹配 → UVM_ERROR
    extern task check_rst();
    // 毛刺检测: 监测高/低脉冲宽度是否小于 glitch_high_th/glitch_low_th
    // 检测到毛刺 → UVM_ERROR
    extern task check_glitch();
    // 同步校验: 检测复位释放沿 (posedge rst) 与时钟沿 (posedge clk) 的时间差
    // 时间差 > sync_ignore_th → UVM_ERROR (未同步)
    extern task check_sync();
    // 强制设置复位: 委托给 cfg.ri.set_rst()
    extern task set_rst(input logic rst);
    // UVM run_phase: fork 启动 drive + glitch_check + sync_check
    // is_active=1 → cfg.ri.drive()
    // glitch_check_en=1 → check_glitch()
    // sync_check_en=1 → check_sync()
    extern task run_phase(uvm_phase phase);

endclass

    // 构造函数实现: 调用 super.new() 并创建 cfg 配置对象
function svk_rst_node::new(string name="svk_rst_node", uvm_component parent=null);
    super.new(name, parent);

    cfg = new();
endfunction

    // 读取实际复位值实现: rst = cfg.ri.rst
task svk_rst_node::get_real_rst(output logic rst);
    rst = cfg.ri.rst;
endtask

    // 复位校验实现 (详见声明处注释)
task svk_rst_node::check_rst();
    logic expe_rst;
    logic real_rst;

    get_expe_rst(expe_rst);
    get_expe_rst(real_rst);

    if(expe_rst !== real_rst)begin
        `uvm_error("check_rst", $sformatf("%s is error expe_rst=%0b, real_rst=%0b", cfg.ri.rst_hire, expe_rst, real_rst))
    end
endtask

    // 毛刺检测实现: fork 两个 while(1) 分别监测高/低毛刺 (详见声明处注释)
task svk_rst_node::check_glitch();
    if(cfg.glitch_check_en)begin
        fork
            while(1)begin
                real t1,t2;
                @(posedge cfg.ri.rst);
                t1 = $realtime();
                @(negedge cfg.ri.rst);
                t2 = $realtime();
                if(t2 - t1 < cfg.glitch_high_th)
                    `uvm_error("check_glitch", $sformatf("%s has high glitch, glitch_time=%0fns", cfg.ri.rst_hire, t2-t1))
            end
            while(1)begin
                real t1,t2;
                @(negedge cfg.ri.rst);
                t1 = $realtime();
                @(posedge cfg.ri.rst);
                t2 = $realtime();
                if(t2 - t1 < cfg.glitch_low_th)
                    `uvm_error("check_glitch", $sformatf("%s has low glitch, glitch_time=%0fns", cfg.ri.rst_hire, t2-t1))
            end
        join
    end
endtask


    // 同步校验实现: fork 分别监测 clk posedge 和 rst posedge (详见声明处注释)
task svk_rst_node::check_sync();
    real t1,t2;
    if(cfg.sync_check_en)begin
        fork
            while(1)begin
                @(posedge cfg.ci.clk);
                t1 = $realtime();
            end
            while(1)begin
                @(posedge cfg.ri.rst);
                #0;
                t2 = $realtime();

                if(t2 - t1 > cfg.sync_ignore_th)
                    `uvm_error("check_sync", $sformatf("%s is not sync to %s,t1=%0f,t2=%0f,sync_ignore_th=%0f", cfg.ri.rst_hire, cfg.ci.clk_hire, t1, t2, cfg.sync_ignore_th))
            end
        join
    end
endtask


    // 设置复位实现: 委托 cfg.ri.set_rst()
task svk_rst_node::set_rst(input logic rst);
    cfg.ri.set_rst(rst);
endtask

    // run_phase 实现 (详见声明处注释)
task svk_rst_node::run_phase(uvm_phase phase);
    fork
        if(cfg.is_active)begin
            cfg.ri.up_time   = cfg.up_time;
            cfg.ri.down_time = cfg.down_time;
            cfg.ri.drive();
        end
        if(cfg.glitch_check_en)begin
            check_glitch();
        end
        if(cfg.sync_check_en)begin
            check_sync();
        end
    join
endtask

`endif
