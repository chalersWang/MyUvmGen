#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP
from readexcel.readexcel_DutSignal import readexcel_DutSignal
from readexcel.readexcel_ClockRst import readexcel_ClockRst

from common_lib.parameters import Parameters

class gen_coverage_file:

    def __init__(self):
        print("[gen_coverage_file]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_coverage_file_info(PrintEnable=True)

    def gen_coverage_file_info(self,PrintEnable):
        Signals0=[]
        Signals1=[]
        Signals2=[]
        Signals3=[]
        Signals4=[]
        Signals5=[]
        Signals6=[]
        delaystrlst=[]
        #xx_function_coverage.sv
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename = open("%s_function_coverage.sv"%self.DUT_GroupName[i], "w+")
                filename.write("//CDV: Coverage Drive Verify\n")
                filename.write("covergroup FeatureListNum_%s with function sample(%s_trans %s_tr);\n"
                                            %(self.DUT_GroupName[i].upper(),self.DUT_GroupName[i],self.DUT_GroupName[i]))
                filename.write("\t//function code\n")
                #Signals
                Signals0=self.DUT_Signals[i].replace('\n','')
                Signals1=Signals0.replace('input','')
                Signals2=Signals1.replace('output','')
                Signals3=Signals2.replace(' ','')
                Signals4=Signals3.rstrip(',')
                Signals5=Signals4.split(',')
                for j in range(len(Signals5)):
                    delaystrlst=Signals5[j][Signals5[j].find('['):Signals5[j].find(']')+1]
                    if delaystrlst==None:
                        Signals6=Signals5[j]
                    else:
                        Signals6=Signals5[j].replace(delaystrlst,'')
                    # filename.write("\t%s_%s:coverpoint %s_tr.%s{bins zero={0};bins nonzero={['h1:$]};\n"
                    #                         %(self.DUT_GroupName[i],Signals6,self.DUT_GroupName[i],Signals6))
                    filename.write("\t%s_%s:coverpoint %s_tr.%s{bins zero={0};bins nonzero={['h1:$]};\n"
                                             %(self.DUT_GroupName[i].upper(),Signals6,self.DUT_GroupName[i],Signals6))
                filename.write("endgroup\n")
                filename.close()

        #Coverage Hierarchy  
        #filename = open("CoverageHierarchy.lst", "w+")
        filename = open(Parameters.CoverageHierarchyFile, "w+")
        filename.write("//+module tb_top.DUT.xx1\n")
        filename.write("//-module tb_top.DUT.xx2\n")
        filename.write("//+tree tb_top.DUT.xx3\n")
        filename.write("//-tree tb_top.DUT.xx4\n")
        filename.close()

        #覆盖率配置说明文件
        filename = open("Guide.Coverage_coding.sv", "w+",encoding="utf-8")
        filename.write("//=======================================================================================\n")
        filename.write("//覆盖组(Covergroup)选项\n")
        filename.write("1. option.per_instance\n")
        filename.write("  //含义：此选项决定覆盖组实例化时覆盖率数据的统计方式。当设置为 1 时，每个覆盖组实例会独立统计覆盖率；设置为 0 时，所有实例共享同一套覆盖率数据\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      option.per_instance = 1; // 每个实例独立统计覆盖率\n")
        filename.write("      // 覆盖点定义\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：当需要区分不同实例的覆盖情况，例如在验证多个相同模块的不同行为时，设置为 1 有助于分别评估每个实例的验证充分性。\n")
        filename.write("\n")
        filename.write("2. option.comment\n")
        filename.write("  //含义：为覆盖组添加注释信息，该注释会显示在覆盖率报告中，方便其他人员理解覆盖组的目的。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      option.comment = \"This covergroup is used to measure address access patterns.\";\n")
        filename.write("      // 覆盖点定义\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：提高代码的可读性和可维护性，特别是在大型项目中，便于团队成员快速了解每个覆盖组的功能。\n")
        filename.write("\n")
        filename.write("3. option.goal\n")
        filename.write("  //含义：设置覆盖组的覆盖率目标，以百分比表示。当覆盖率达到该目标时，可作为验证是否充分的一个参考指标。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      option.goal = 90; // 覆盖率目标为 90%\n")
        filename.write("      // 覆盖点定义\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：帮助验证团队设定明确的验证目标，当接近或达到目标时，可以决定是否停止测试或调整测试策略。\n")
        filename.write("\n")
        filename.write("4. option.at_least\n")
        filename.write("  //含义：指定每个覆盖点或交叉覆盖的每个 bin 至少需要被命中的次数，以确保覆盖的稳定性。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      option.at_least = 5; // 每个 bin 至少命中 5 次\n")
        filename.write("      // 覆盖点定义\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：避免由于偶然因素导致某些 bin 仅被命中一次就被认为已覆盖，提高覆盖率的可信度。\n")
        filename.write("\n")
        filename.write("//=======================================================================================\n")
        filename.write("//覆盖点(Coverpoint)选项和参数\n")
        filename.write("1. bins\n")
        filename.write("  //含义：用于定义覆盖点的取值区间或具体值集合。一个覆盖点可以有多个 bins，每个 bin 代表一个独立的覆盖范围。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("    coverpoint my_variable {\n")
        filename.write("        bins low_values = {[0:10]};\n")
        filename.write("        bins high_values = {[90:100]};\n")
        filename.write("    }\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：将变量的取值范围划分为不同的区间，分别统计每个区间的覆盖情况，有助于发现设计对不同输入值的处理能力\n")
        filename.write("\n")
        filename.write("2. ignore_bins\n")
        filename.write("  //含义：指定不需要统计覆盖率的取值区间或具体值。这些值在覆盖率计算中会被忽略。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("    coverpoint my_variable {\n")
        filename.write("        ignore_bins invalid_values = {255};\n")
        filename.write("        // 其他 bins 定义\n")
        filename.write("    }\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：排除无效或不需要关注的取值，使覆盖率数据更聚焦于设计的有效行为。\n")
        filename.write("\n")
        filename.write("3. illegal_bins\n")
        filename.write("  //含义：定义非法的取值区间或具体值。如果变量取到这些值，会触发仿真错误，提醒验证人员设计可能存在问题。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("    coverpoint my_variable {\n")
        filename.write("        illegal_bins illegal_values = {[101:254]};\n")
        filename.write("        // 其他 bins 定义\n")
        filename.write("    }\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：用于检查设计是否遵守特定的约束条件，防止非法输入导致的错误。\n")
        filename.write("\n")
        filename.write("4. wildcard_bins\n")
        filename.write("  //含义：使用通配符（如 ?）来定义覆盖区间，允许部分位的取值为任意值。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("    coverpoint my_variable {\n")
        filename.write("        wildcard_bins pattern = {8'b10??_11??};\n")
        filename.write("    }\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：当需要覆盖某些特定的位模式，但不关心部分位的具体取值时，使用通配符可以简化覆盖点的定义。\n")
        filename.write("\n")
        filename.write("5. binsof\n")
        filename.write("  //含义：用于引用其他覆盖点或变量的取值集合，方便复用已定义的覆盖范围。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("    coverpoint my_variable1;\n")
        filename.write("    coverpoint my_variable2 {\n")
        filename.write("        bins same_values = binsof(my_variable1);\n")
        filename.write("    }\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：避免重复定义相同的覆盖范围，提高代码的复用性。\n")
        filename.write("\n")
        filename.write("//=======================================================================================\n")
        filename.write("//交叉覆盖（Cross）选项和参数\n")
        filename.write("1. cross\n")
        filename.write("  //含义：用于定义多个覆盖点之间的交叉组合，统计不同覆盖点取值组合的覆盖率。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      cp1 : coverpoint var1;\n")
        filename.write("      cp2 : coverpoint var2;\n")
        filename.write("      cross cp1, cp2;\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：检查不同变量之间的取值组合对设计行为的影响，发现可能的交互错误。\n")
        filename.write("\n")
        filename.write("2. option.weight\n")
        filename.write("  //含义：设置交叉覆盖中每个组合的权重，权重越高，该组合对整体覆盖率的贡献越大。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      cp1 : coverpoint var1;\n")
        filename.write("      cp2 : coverpoint var2;\n")
        filename.write("      cross cp1, cp2 {\n")
        filename.write("          option.weight = 2;\n")
        filename.write("      }\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：在某些情况下，某些取值组合可能比其他组合更重要，通过设置权重可以更合理地评估覆盖率。\n")
        filename.write("\n")
        filename.write("3. if 条件\n")
        filename.write("  //含义：为交叉覆盖添加条件，只有当条件满足时，才会统计相应组合的覆盖率。\n")
        filename.write("  //示例：\n")
        filename.write("  covergroup my_covergroup;\n")
        filename.write("      cp1 : coverpoint var1;\n")
        filename.write("      cp2 : coverpoint var2;\n")
        filename.write("      cross cp1, cp2 if (condition);\n")
        filename.write("  endgroup\n")
        filename.write("  //用途：只关注在特定条件下的交叉覆盖情况，减少不必要的覆盖率统计。\n")
        filename.write("\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_coverage_file()