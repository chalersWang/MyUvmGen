#include {VERIFY_HOME}

export path_tb=${PWD}
###################################################
# switch on/off
###################################################
GATE_SIM        ?= off
COVERAGE        ?= off
FSDB_DUMP       ?= on

####################################################
# Compile options
####################################################
#<1> Base compile options
COMP_DIR        ?=
TIME_SCALE      ?= 1ns/1ps

#<2> RTL compile options
TB_TOP          ?= tb_top

#<3> C compile options
C_TEST          ?=
CC              = gcc
C_OPT           = -fPIC -std=c99 -g -w
C_INCLUDE       = -I{VCS_HOME}/include -I{path_tb}/c_dpi
C_DEF_ARGS      = -DVCS
#C_TEST_DIR     ?= $(path_tb)/fw/test
#INCLUDE_PATH   := ../include
#SRC_PATH       += $(C_TEST_DIR)/$(C_TEST)
#C_FLAGS        += $(foreach dir,$(INCLUDE_PATH),$(foreach sub_dir,$(wildcard $(dir)),-I$(sub_dir)))
#SRCS           += $(foreach dir,$(SRC_PATH),$(wildcard $(dir)/*.c))
#OBJ            = ${patsubst %.c, %.0, $(SRCS)}   

#<4> User compile options
SEED            ?= 1
TCL_FILE        ?= $(path)/tcl/wave.tcl
COVERAGE_TYPE   ?= line+tgl+branch+fsdm+cond+assert -cm_cond allops
COV_DIR         ?= $(path)/sim/cov
#COV_DIR        ?= $(path)/coverage

#<5> add compile options
TILE_ARGS       += -Marchive=2000
#TILE_ARGS      += -no_error ZONMCMIPY
TILE_ARGS       += -sverilog +v2k
TILE_ARGS       += +evalorder
TILE_ARGS       += +vcs+lic+wait
TILE_ARGS       += +libext+.sv+.v+.V+.vp+.vlib
#TILE_ARGS      += -ntb_opts uvm-1.2
#TILE_ARGS      += -assert dve -debug_all+nomemcbk+dmptf -debug_region+cell
TILE_ARGS       += +define+SYNOPSYS_SV+NTB +define+notiming
TILE_ARGS       += -P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX/pli.a
TILE_ARGS       += -cm line+cond+fsm+tgl+branch+assert -cm_tgl mda
TILE_ARGS       += -cm_line contassion
TILE_ARGS       += +systemverilogext+.svh
TILE_ARGS       += +warn=noIAVCVF-W
TILE_ARGS       += +warn=noDRTZ
TILE_ARGS       += +warn=noVCM-BSZEX
TILE_ARGS       += +incdir+${VCS_HOME}/etc/uvm-1.2
TILE_ARGS       += +incdir+${VCS_HOME}/packages/aip/AHB_AIP/scr

TILE_ARGS       += +define+PMU
TILE_ARGS       += +define+KCORE_SIM
TILE_ARGS       += +define+SCORE_SIM
TILE_ARGS       += +define+RUN_KCORE
TILE_ARGS       += +define+MULTINUCLEAR

TILE_ARGS       += -file ${VERIFY_HOME}/coverage/coverage_list/Coverage_define.lst
TILE_ARGS       += -cm_hier ${VERIFY_HOME}/coverage/coverage_list/Coverage.lst
TILE_ARGS       += -file ${VERIFY_HOME}/sva/sva_lst/Assertion_define.lst
TILE_ARGS       += -assert enable_hier

TILE_ARGS       += +define+XPROP_ENABLE
#TILE_ARGS      += -xprop=xmerge
TILE_ARGS       += -xprop=${VERIFY_HOME}/run/xprop_merge.cfg

####################################################
# Simulation options
####################################################
#<1> Base Simulation options
SIM_DIR         ?=
UVM_TIMEOUT     ?= "1000000000ps,YES"
UVM_VERBOSITY   =UVM_MEDIUM

SIM_ARGS        += -sv_lib libdpi
SIM_ARGS        += +vcs+ignorestop
SIM_ARGS        += +vcs+loopreport+2
SIM_ARGS        += +vcs+loopdetect
SIM_ARGS        += -report=xprop
SIM_ARGS        += -assert hier=Assertion_hierarchy.lst

####################################################################################################
export MY_FSDB_DUMP=${FSDB_DUMP}
.PHONY:comp elab sim c_comp regression env_check prepare_comp_dir pre_sim_dir help

ifeq ($(COVERAGE),on)
COM_COVERAGE_OPTS = -cm_dir $(COMP_DIR)/sim -cm $(COVERAGE_TYPE)
SIM_COVERAGE_OPTS = -cm_dir $(COV_DIR)/sim -cm $(COVERAGE_TYPE)
else
SIM_COVERAGE_OPTS =
endif

ifneq ($(QUITE_MODE),0)
QUITE_OPTS=
QUITE=
else
QUITE_OPTS=
QUITE=
endif

help:
    @echo "---------------------------------------------------------------------"
    @echo "         make clean              |   clean the compile directory     "
    @echo "---------------------------------------------------------------------"
    

env_check:
    @echo "---------------------------------------------------------------------"
    @echo "         check the environment                                       "


prepare_comp_dir:
    $(if $(wildcard $(COMP_DIR)),,mkdir -p $(COMP_DIR))

prepare_sim_dir:
    $(if $(wildcard $(SIM_DIR)),,mkdir -p $(SIM_DIR))

ifeq ($(GATE_SIM),on)
else
comp:prepare_comp_dir
    cd ${COMP_DIR};\
    vcs -full64 -error=noMPD -l comp.log -sverilog \
        -ntb_opts uvm-1.2 \
        +lint=TFIPOC-L +lint=PCWM \
        -j4 -kdb -lca -debug_all \
        +notimingcheck +nospecify \
        +Marchive=1000 \
        -reportstats \
        -file ${VERIFY_HOME}/filelist/c_filelist.lst \
        -CFLAGS "-I${VERIFY_HOME}/refrence" \
        -timescale=$(TIME_sCALE) \
        -top $(TB_TOP) \
        $(TB_DEF_OPTS) \
        $(COM_COVERAGE_OPTS) \
        $(TILE_ARGS) \
        -file $(DEFINE_FILELIST) -file $(RTL_FILELIST) -file $(VIP_FILELIST) -file $(TB_FILELIST) &
endif

ifeq ($(GATE_SIM),on)
else
ifeq ($(C_TEST), )
else
sim:pre_sim_dir
    $(QUITE)cd $(SIM_DIR);\
    $(COMP_DIR)/simv \
    -l sim.log \
    +UVM_VERBOSITY=$(UVM_VERBOSITY) \
    +UVM_TESTNAME=$(UVM_TEST) +(UVM_NO_RELNOTES) \
    +UVM_TIMEOUT=$(UVM_TIMEOUT) \
    +fsdb+all \
    +vcs+ignorestop \
    -reportstats \
    $(SIM_ARGS) \
    $(SIM_COVERAGE_OPTS) \
    +RANDOM_SEED=$(SEED) +ntb_random_seed=$(SEED) \
    $(TCL_FILE) -ucli -do $(TCL_FILE)
    $(QUITE_OPTS)
endif
endif

clean:
    rm -rf $(COMP_DIR)

cov_merge:
    urg -full64 -dir $(COMP_DIR)/simv.vbd -dir $(COV_DIR)/*.vdb -format both -dbname cov_merge

verdi_cov:
    dve -full64 -cov -dir cov_merge.vbd 
