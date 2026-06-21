#! /usr/bin/env python
import os


# os.system("fsdbreport wxx.fsdb -bt 0ns -et 1us -exp \"/tb_top/DUT/clk&&/tb_top/DUT/rvalid\" -s \"/tb_top/DUT/rdata[1023:0]\" -of h -w 256 -o rdata.txt")

fsdbname        ="wxx.fsdb"
begin_time      ="0ns"
end_time        ="1us"
sample_condition="/tb_top/DUT/clk&&/tb_top/DUT/rvalid"
sample_signal   ="/tb_top/DUT/rdata[1023:0]"
sample_charnum  =256
output_file     ="rdata.txt"
print("fsdbreport %s -bt %s -et %s -exp \"%s\" -s \"%s\" -of h -w %s -o %s"
      %(fsdbname,begin_time,end_time,sample_condition,sample_signal,sample_charnum,output_file))
# os.system("fsdbreport %s -bt %s -et %s -exp \"%s\" -s \"%s\" -of h -w %s -o %s"
#       %(fsdbname,begin_time,end_time,sample_condition,sample_signal,sample_charnum,output_file))