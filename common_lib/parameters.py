#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys

class Parameters:
    #--------------------------------------------------------------
    ############################################################################
    #EnvironmentGenCfg       ='../VerifyEnvironmentGenCfg.xlsx'
    EnvironmentGenCfg       ='../VerifyEnvironmentGenCfg_cclink.xlsx'
    # If you want to define the project name in excel, enter xx or None here. 
    # [For Example]:    tb_name='xx' or None 
    # If you want to define the project name here, enter the project name you want to create
    # [for Example]:    tb_name='sct_wx'  
    tb_name                 =None
    COMPANY                 ='WX'
    ############################################################################
    tb_level                ='UT'
    macro_name              ='TX82_CGRA_DV_%s'%tb_level
    Cfg_comp_base_file      ='comp_base.cfg'
    Cfg_sim_base_file       ='sim_base.cfg'
    Cfg_debug_file          ='debug.cfg'
    Cfg_xprop_file          ='xprop.cfg'
    Cfg_coverage_file       ='coverage.cfg'
    Cfg_assertion_file      ='assertion.cfg'
    Cfg_partitioncomp_file  ='partitioncompile_cfg.v'
    Filelist_define         ='define.f'
    Filelist_rtl            ='rtl.f'
    Filelist_netlist        ='netlist.f'
    Filelist_vip            ='vip.f'
    Filelist_tb             ='tb.f'
    Filelist_cmodel         ='cmodel.f'
    SvaVifDefine            ='VifMacroDefine.v'
    SvaHierarchyFile        ='AssertionHierarchy.lst'
    CoverageHierarchyFile   ='CoverageHierarchy.lst'
    readme                  ='readme'
    JsonSuffix              ='.json'
    slash                   = os.sep  # auto-detect platform separator
    PrintEnable             =True
    #--------------------------------------------------------------
    runscript               ="all"  #"run","xrun"
    #--------------------------------------------------------------
    #CPU:[None,'RISCV','A55','PowerPC','MIPS']
    TopCoreArch             =None
    TopCoreCluster          =0
    TopCoreNum              =0
    SubCoreArch             ='RISCV'
    TopCoreCluster          =2
    SubCoreNum              =[2,2]
    # #####################################################
    # pid                 =None
    # main_cpu            ="ca53"
    # assist_cpu          ="ck804"
    # cpu_option_group    =[main_cpu,assist_cpu]
    # asic_option_group   =['tsmc28npcp','tsmc12ffc','behavior']
    # sdf_option_group    =['WC','WCL','LT','ML','TC']
    # codemem_option_group=['shram','dpi','sram','ddr']
    # ddrtype_option_group=['ddr_model','lpddr2','ddr2','lpddr3','ddr3','lpddr4','ddr4','lpddr5','ddr5']
    # nocomp_option_group =['all','tb','rtl','all']
    # verbose_option_group=['NONE','LOW','MEDIUM','HIGH','DEBUG']
    # step_option_group   =['all','vivado']
    # gui_option_group    =['dve','verdi','spg']
    # spggoal_option_group=['designread','lint','cdc']
    # boot_option_group   =['spi','emmc','qspi','usb']

