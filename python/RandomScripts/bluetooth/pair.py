#!/usr/bin/python

import dbus, gobject
import dbus.mainloop.glib
import sys
import os
import time
import subprocess

def getList(bus,path):
    adapter = dbus.Interface(bus.get_object("org.bluez",
        path),
        "org.bluez.Adapter")
    for d in adapter.ListDevices():
        adapter.RemoveDevice(d)
        print d

def newDeviceHandler(path):
    colSepMac=str.join(':',path.split('/')[-1].split('_')[1:])
    underSepMac=str.join('_',path.split('/')[-1].split('_')[1:])
    print colSepMac
    pass

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    ######## get Bluez PID #########
    proc=subprocess.Popen(["ps","-e"], stdout=subprocess.PIPE)
    out, err = proc.communicate()

    pos=out.find('bluetoothd')
    startline=out.rfind('\n',0,pos)
    pid=out[startline+1:pos].strip().split(' ')[0]
    ######## END ##########

    bus = dbus.SystemBus()
    path="/org/bluez/"+str(pid)+"/hci0"
    
    getList(bus,path)

    #### Register Signal ####
    bus.add_signal_receiver(newDeviceHandler, dbus_interface="org.bluez.Adapter", signal_name="DeviceCreated")

    #### End ####

    #### Register agent #####
    network = dbus.Interface(bus.get_object("org.bluez",
        path),
        "org.bluez.Adapter")
    network.RegisterAgent("/tmp/test","NoInputNoOutput")
    #### END ####
    
    loop = gobject.MainLoop()
    loop.run()
