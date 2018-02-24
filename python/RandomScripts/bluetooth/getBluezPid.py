#!/usr/bin/python

import subprocess

proc=subprocess.Popen(["ps","-e"], stdout=subprocess.PIPE)
out, err = proc.communicate()

pos=out.find('bluetoothd')
startline=out.rfind('\n',0,pos)
print out[startline+1:pos].strip().split(' ')[0]
