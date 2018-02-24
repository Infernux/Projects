# 2015.01.14 22:10:02 CET
from adisp import process
from gui.shared.utils.functions import checkAmmoLevel

def vehicleAmmoCheck(func):

    @process
    def wrapper(*args, **kwargs):
        res = yield checkAmmoLevel()
        if res:
            func(*args, **kwargs)
        elif kwargs.get('callback') is not None:
            kwargs.get('callback')(False)


    return wrapper



+++ okay decompyling decorators.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:10:02 CET
