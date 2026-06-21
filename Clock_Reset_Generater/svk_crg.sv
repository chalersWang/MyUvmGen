/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_crg
// 功能概述: 全局时钟/复位接口管理器
//           维护两个全局关联数组 —— clk_ifs[string] 和 rst_ifs[string]，
//           通过 instance path 字符串索引所有已实例化的 clock/reset interface。
//           提供通配符匹配的查找函数 get_clk_if() / get_rst_if()，
//           支持 UVM 风格的层级路径模糊搜索。
// 关键函数:
//   get_clk_if(wildcard_path)  — 通配符匹配查找 svk_clk_if, 返回唯一匹配项
//   get_rst_if(wildcard_path)  — 通配符匹配查找 svk_rst_if, 返回唯一匹配项
//   匹配规则: uvm_is_match() 支持 * 和 ? 通配符
//   查找到多个匹配 → UVM_ERROR; 0个 → UVM_ERROR
// ============================================================================

`ifndef SVK_CRG__SV
`define SVK_CRG__SV

virtual svk_clk_if clk_ifs[string];
virtual svk_rst_if rst_ifs[string];

function virtual svk_clk_if get_clk_if(string wildcard_path);
    virtual svk_clk_if ci_q[$];

    foreach(clk_ifs[clk_hire])begin
        if(uvm_is_match(wildcard_path, clk_hire))begin
            ci_q.push_back(clk_ifs[clk_hire]);
        end
    end

    if(ci_q.size == 1)begin
        return ci_q[0];
    end
    else if(ci_q.size > 1)begin
        `uvm_error("get_clk_if", $sformatf("find more than one svk_clk_if with wildcard_path=%0s", wildcard_path))
        `uvm_info("get_clk_if", "all find svk_clk_if:", UVM_NONE)
        foreach(ci_q[i])begin
           `uvm_info("get_clk_if", $sformatf("clk_hire=%0s", ci_q[i].clk_hire), UVM_NONE)
        end
    end
    else begin
        `uvm_error("get_clk_if", $sformatf("not find any svk_clk_if with wildcard_path=%0s", wildcard_path))
        `uvm_info("get_clk_if", "all svk_clk_if:", UVM_NONE)
        foreach(clk_ifs[clk_hire])begin
            `uvm_info("get_clk_if", $sformatf("clk_hire=%0s", clk_hire), UVM_NONE)
        end
    end
endfunction

function virtual svk_rst_if get_rst_if(string wildcard_path);
    virtual svk_rst_if ri_q[$];

    foreach(rst_ifs[rst_hire])begin
        if(uvm_is_match(wildcard_path, rst_hire))begin
            ri_q.push_back(rst_ifs[rst_hire]);
        end
    end

    if(ri_q.size == 1)begin
        return ri_q[0];
    end
    else if(ri_q.size > 1)begin
        `uvm_error("get_rst_if", $sformatf("find more than one svk_rst_if with wildcard_path=%0s", wildcard_path))
        `uvm_info("get_rst_if", "all find svk_rst_if:", UVM_NONE)
        foreach(ri_q[i])begin
           `uvm_info("get_rst_if", $sformatf("rst_hire=%0s", ri_q[i].rst_hire), UVM_NONE)
        end
    end
    else begin
        `uvm_error("get_rst_if", $sformatf("not find any svk_rst_if with wildcard_path=%0s", wildcard_path))
        `uvm_info("get_rst_if", "all svk_rst_if:", UVM_NONE)
        foreach(rst_ifs[rst_hire])begin
            `uvm_info("get_rst_if", $sformatf("rst_hire=%0s", rst_hire), UVM_NONE)
        end
    end
endfunction

`endif
