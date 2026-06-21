#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — Virtual Interface 代码生成器
#
# 【设计说明】
# - interface 内部信号使用 logic 类型（非 input/output 端口声明）
# - 生成两个 clocking block:
#   - dcb (driver clocking block): 驱动视角，output 为 output，input 为 input
#   - mcb (monitor clocking block): 监控视角，所有信号为 input（纯观察）
# - clocking block 使用 #step 避免竞争
#
# 【UVM 方法论要点】
# - logic 是 SystemVerilog 推荐的四值（0/1/X/Z）信号类型
# - clocking block 的 input #1step 采样和 output #0 驱动，
#   避免仿真中的 setup/hold 时序竞争
# - 每个 UVC 应有独立的 interface，不应共享
# ============================================================
import os
import re

from common_lib.parameters import Parameters
from common_lib.common_lib import GetDutSignalList

class gen_uvc_vif:

    def __init__(self):
        print("[gen_uvc_vif]:initial")
        uvc_name='aa'
        uvc_signals=    "            \
                        input a     ,\
                        input[1:0]b ,\
                        output c    ,\
                        output[2:0]d,\
                        "
        self.gen_uvc_vif_info(uvc_name,uvc_signals,PrintEnable=True)

    def gen_uvc_vif_info(self,name,SIGNALS,PrintEnable):
        signals=[]
        Signals0=SIGNALS.replace('\n','')
        Signals1=Signals0.replace(' ','')
        Signals2=Signals1.rstrip(',')
        Signals3=Signals2.split(',')

        # 解析信号方向
        for i in range(len(Signals3)):
            if "input" in Signals3[i]:
                direction = "input"
            elif "output" in Signals3[i]:
                direction = "output"
            elif "inout" in Signals3[i]:
                direction = "inout"
            else:
                direction = "inout"
            
            # 提取信号名和位宽
            signal_clean = Signals3[i].replace('input','').replace('output','').replace('inout','')
            # 分离位宽和信号名
            width_match = re.findall(r'\[(.*?)\]', signal_clean)
            signal_name = re.sub(r'\[.*?\]', '', signal_clean)
            
            if width_match:
                width = width_match[-1]
                signals.append({
                    'direction': direction,
                    'name': signal_name,
                    'width': width
                })
            else:
                signals.append({
                    'direction': direction,
                    'name': signal_name,
                    'width': '0'  # 1-bit
                })

        # ===== 生成 interface =====
        filename = open("%s_vif.sv"%name, "w+")
        filename.write("`ifndef _%s_VIF_SV_\n"%name.upper())
        filename.write("`define _%s_VIF_SV_\n")
        filename.write("\n")
        filename.write("//=========================================================================\n")
        filename.write("// %s_vif: %s UVC 的 virtual interface\n" % (name, name))
        filename.write("//   interface 端口：clk, rstn → 由 tb_top 传入\n")
        filename.write("//   内部信号：使用 logic 类型（非 input/output），由 DUT 和 driver 共驱\n")
        filename.write("//=========================================================================\n")
        filename.write("interface %s_vif(input logic clk, input logic rstn);\n"%name)
        filename.write("\n")
        filename.write("\t// ===== DUT 信号声明（logic 类型） =====\n")
        
        # 声明所有信号为 logic
        for sig in signals:
            if sig['width'] != '0':
                filename.write("\tlogic [%s-1:0] %s;\n"%(sig['width'], sig['name']))
            else:
                filename.write("\tlogic %s;\n"%sig['name'])
        
        filename.write("\n")
        filename.write("\t// ===== Clocking Blocks =====\n")
        filename.write("\t// dcb: Driver 视角的 clocking block\n")
        filename.write("\t//   驱动信号使用 output（相对于 driver），采样信号使用 input\n")
        filename.write("\t//   input #1step: 在时钟边沿前采样（避免竞争）\n")
        filename.write("\t//   output #0: 在时钟边沿后驱动（避免竞争）\n")
        filename.write("\tdefault clocking dcb @(posedge clk);\n")
        filename.write("\t\tdefault input #1step output #0;\n")
        # driver clocking: 方向反转
        for sig in signals:
            if sig['width'] != '0':
                if sig['direction'] == 'input':
                    filename.write("\t\toutput [%s-1:0] %s;\n"%(sig['width'], sig['name']))
                elif sig['direction'] == 'output':
                    filename.write("\t\tinput  [%s-1:0] %s;\n"%(sig['width'], sig['name']))
                else:
                    filename.write("\t\tinout  [%s-1:0] %s;\n"%(sig['width'], sig['name']))
            else:
                if sig['direction'] == 'input':
                    filename.write("\t\toutput %s;\n"%sig['name'])
                elif sig['direction'] == 'output':
                    filename.write("\t\tinput  %s;\n"%sig['name'])
                else:
                    filename.write("\t\tinout  %s;\n"%sig['name'])
        filename.write("\tendclocking : dcb\n")
        filename.write("\n")
        filename.write("\t// mcb: Monitor 视角的 clocking block（纯观察，全部 input）\n")
        filename.write("\tclocking mcb @(posedge clk);\n")
        filename.write("\t\tdefault input #1step;\n")
        for sig in signals:
            if sig['width'] != '0':
                filename.write("\t\tinput [%s-1:0] %s;\n"%(sig['width'], sig['name']))
            else:
                filename.write("\t\tinput %s;\n"%sig['name'])
        filename.write("\tendclocking : mcb\n")
        filename.write("\n")
        
        # ===== 可选的 modport =====
        filename.write("\t// ===== Modports（可选） =====\n")
        filename.write("\t// 用于 module 端口连接时指定方向\n")
        filename.write("\tmodport drv_mp (clocking dcb, input clk, input rstn);\n")
        filename.write("\tmodport mon_mp (clocking mcb, input clk, input rstn);\n")
        filename.write("\n")
        
        # ===== 电平检测宏 =====
        filename.write("\t// ===== UT/IT/ST 级宏定义 =====\n")
        filename.write("\t// 用于控制断言和覆盖率在不同验证级别的使能\n")
        filename.write("\t`ifndef CHK_%s\n"%name.upper())
        filename.write("\t\t`define CHK_%s 1\n"%name.upper())
        filename.write("\t`endif\n")
        filename.write("\n")
        filename.write("\t`ifndef COV_%s\n"%name.upper())
        filename.write("\t\t`define COV_%s 1\n"%name.upper())
        filename.write("\t`endif\n")
        filename.write("\n")
        filename.write("endinterface : %s_vif\n"%name)
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_uvc_vif] %s_vif.sv generated with:"%name)
            print("  - logic type for all signals (not input/output port)")
            print("  - dcb (driver view) clocking block with proper direction")
            print("  - mcb (monitor view) clocking block (pure observation)")
            print("  - modport drv_mp/mon_mp for module connection")

if __name__ == '__main__':
    gen=gen_uvc_vif()
