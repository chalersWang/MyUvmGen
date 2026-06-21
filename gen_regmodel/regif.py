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

    nrows               = sh.nrows  # total rows number
    row_msg_idx         = {}        # store information of column
    row_msg             ={}        # store information of each row
    line_copy           = 0         # indicate copy line is in-progress
    line_replay         = 0         # indicate copied lines insertion is in-progress
    reg_list            = {}        # store information of each reg
    field_list          = {}        # store information of each field
    rst_list            = []        # store reset sigals

    copy_reg_list       = []        # store copy reg in order
    copy_reg_lines      = {}        # store lines of each copy reg
    copy_lines          = []        # store lines temporarily

    title_line          = 1         #indicate the line which contrains the title of columns 
    global excel_line_num           #indicate the current line number of excel table

    #scan excel table
    for row_num in range(0,nrows):

        excel_line_num = row_num
        row = sh.row_values(row_num)
       # print(row)
        if row[0].find('//') != -1: #comment line
            continue

        if title_line == 1: #decode info col
            
            row_msg_idx['reg_name_col']     = row.index('Register Name') 
            row_msg_idx['bits_col']         = row.index('Bits')
            row_msg_idx['field_name_col']   = row.index('Field Name')
            row_msg_idx['access_col']       = row.index('Access')
            row_msg_idx['rst_val_col']      = row.index('Reset Value')
            row_msg_idx['rst_ctl_col']      = row.index('Reset Ctl')
            row_msg_idx['des_col']          = row.index('Description')

            title_line = 0
            continue

        else:
            cap_row_msg(row=row, row_msg_idx=row_msg_idx, row_msg=row_msg)

        if title_line == 0:
            
            reg_name    = row_msg['reg_name']
            field_name  = row_msg['field_name']

            #copy/replay control
            if reg_name != '':

                if reg_name.find('[') != -1: #need to copy

                    line_copy = 1
                    copy_reg_list.append(reg_name)
                    copy_reg = reg_name
                    copy_lines = []
                
                else: #normal row where can start to replay

                    if line_copy == 1: #start to insert the copy lines of reg
                        next_row = row #save current new line
                        line_replay = 1
                        line_copy = 0
            
            if line_replay==1:
                
                row_replay(row_msg_idx=row_msg_idx,
                           row_msg=row_msg, 
                           reg_list=reg_list, 
                           field_list=field_list,
                            global_info=global_info,
                           rst_list=rst_list,
                           copy_reg_list=copy_reg_list,
                           copy_reg_lines=copy_reg_lines)

                line_replay = 0
                #clean copy lines
                copy_reg_list = []
                copy_reg_lines = {}
