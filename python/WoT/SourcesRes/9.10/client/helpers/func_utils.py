# 2015.01.14 22:38:35 CET
import BigWorld
from functools import partial

def callback(delay, obj, methodName, *args):
    return BigWorld.callback(delay, partial(callMethod, obj, methodName, *args))



def callMethod(obj, methodName, *args):
    if hasattr(obj, methodName):
        getattr(obj, methodName)(*args)



+++ okay decompyling func_utils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:38:35 CET
