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

    extern function new(string name="svk_rst_node", uvm_component parent=null);
    pure virtual task get_expe_rst(output logic rst);
    extern virtual task get_real_rst(output logic rst);
    extern task check_rst();
    extern task check_glitch();
    extern task check_sync();
    extern task set_rst(input logic rst);
    extern task run_phase(uvm_phase phase);

endclass

function svk_rst_node::new(string name="svk_rst_node", uvm_component parent=null);
    super.new(name, parent);

    cfg = new();
endfunction

task svk_rst_node::get_real_rst(output logic rst);
    rst = cfg.ri.rst;
endtask

task svk_rst_node::check_rst();
    logic expe_rst;
    logic real_rst;

    get_expe_rst(expe_rst);
    get_expe_rst(real_rst);

    if(expe_rst !== real_rst)begin
        `uvm_error("check_rst", $sformatf("%s is error expe_rst=%0b, real_rst=%0b", cfg.ri.rst_hire, expe_rst, real_rst))
    end
endtask

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


task svk_rst_node::set_rst(input logic rst);
    cfg.ri.set_rst(rst);
endtask

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
