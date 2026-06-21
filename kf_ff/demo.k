//=====case1==========================
-f ${VERIFY_HOME}/xx.f
${VERIFY_HOME}/xx.sv

//=====case2==========================
`ifdef AA
    -f ${VERIFY_HOME}/AA.f
    ${VERIFY_HOME}/AA.sv
`else
    -f ${VERIFY_HOME}/aa.f
    ${VERIFY_HOME}/aa.sv
`endif

//=====case3==========================
`ifdef BB
    -f ${VERIFY_HOME}/BB.f
    ${VERIFY_HOME}/BB.sv
    
    `ifdef CC
        -f ${VERIFY_HOME}/BB_CC.f
        ${VERIFY_HOME}/BB_CC.sv
    `else
        -f ${VERIFY_HOME}/BB_cc.f
        ${VERIFY_HOME}/BB_cc.sv
    `endif

    -f ${VERIFY_HOME}/yy.f
    ${VERIFY_HOME}/yy.sv
`else
    -f ${VERIFY_HOME}/bb.f
    ${VERIFY_HOME}/bb.sv

    `ifdef CC
        -f ${VERIFY_HOME}/bb_CC.f
        ${VERIFY_HOME}/bb_CC.sv
    `else
        -f ${VERIFY_HOME}/bb_cc.f
        ${VERIFY_HOME}/bb_cc.sv
    `endif
`endif

//=====case4==========================
`ifdef DD
    -f ${VERIFY_HOME}/DD.f
    ${VERIFY_HOME}/DD.sv
`endif

//=====case5==========================
`ifdef EE
    -f ${VERIFY_HOME}/EE.f
    ${VERIFY_HOME}/EE.sv
`else
`endif

//=====case6==========================
-f ${VERIFY_HOME}/zz.f
${VERIFY_HOME}/zz.sv

//=====case7==========================
`ifdef FF
    -f ${VERIFY_HOME}/FF.f
    ${VERIFY_HOME}/FF.sv
//`else GG
    -f ${VERIFY_HOME}/GG.f
    ${VERIFY_HOME}/GG.sv
`else
    -f ${VERIFY_HOME}/ffgg.f
    ${VERIFY_HOME}/ffgg.sv
`endif

//=====case8==========================
-f ${VERIFY_HOME}/vv.f
${VERIFY_HOME}/vv.sv

//=====case9==========================
`ifdef DUMMY_CT
    ${VERIFY_HOME}/ct_dummy.sv
`else
    -f ${VERIFY_HOME}/ct.f
`endif