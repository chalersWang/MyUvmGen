#!/usr/bin/python2.7

import xlrd
import re
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import importlib,sys
importlib.reload(sys)
import string
import math
import os
import difflib
import filecmp

#global variables
excel_line_num = 0

#This function is used to capture info from excel table

def extract_reg(sh,global_info):
    nrows           =sh.nrows   #总的行号
    row_msg_idx     ={}         #存储列信息
    row_msg         ={}         #存储每行的信息
    line_copy       = 0         #表明进程中的复制行
    line_replay     = 0         #
    reg_list        ={}         #
    field_list      ={}         #
    rst_list        =[]         #

    copy_reg_list   =[]         #
    copy_reg_lines  ={}         #
    copy_lines      =[]         #

    title_line      =1
    global excel_line_num

    #扫描excel表
    for row_num in range(0,nrows):
        excel_line_num=row_num
        row=sh.row_values(row_num)
        
        if row[0].find('//')!=-1:
            continue

        if title_line ==1:
            row_msg_idx['reg_name_col']     =row.index('Register Name')
            row_msg_idx['bits_col']         =row.index('Bits')
            row_msg_idx['field_name_col']   =row.index('Field Name')
            row_msg_idx['access_col']       =row.index('Access')
            row_msg_idx['rst_val_col']      =row.index('Reset Value')
            row_msg_idx['rst_ctl_col']      =row.index('Reset Ctl')
            row_msg_idx['des_col']          =row.index('Destription')

            title_line=0
            continue

        else:
            cap_row_msg(row=row,row_msg_idx=row_msg_idx,row_msg=row_msg)

        if title_line==0:
            reg_name    =row_msg['reg_name']
            field_name  =row_msg['field_name']

            #复制/替换控制
            if reg_name!='':
                if reg_name.find('[')!=-1:#需要复制
                    line_copy=1
                    copy_reg_list.append(reg_name)
                    copy_reg=reg_name
                    copy_lines=[]
                else:
                    if line_copy==1:
                        next_row    =row
                        line_replay =1
                        line_copy   =0
            


