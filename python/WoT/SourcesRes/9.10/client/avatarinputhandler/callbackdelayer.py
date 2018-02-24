# 2015.01.14 23:56:17 CET
import BigWorld
import functools

class CallbackDelayer:

    def __init__(self):
        self.__callbacks = {}



    def destroy(self):
        for (callbackFunc, callbackId,) in self.__callbacks.iteritems():
            if callbackId is not None:
                BigWorld.cancelCallback(callbackId)

        self.__callbacks = {}



    def __funcWrapper(self, func, *args, **kwargs):
        del self.__callbacks[func]
        desiredDelay = func(*args, **kwargs)
        if desiredDelay is not None and desiredDelay >= 0:
            curId = BigWorld.callback(desiredDelay, functools.partial(self.__funcWrapper, func, *args, **kwargs))
            self.__callbacks[func] = curId



    def delayCallback(self, seconds, func, *args, **kwargs):
        curId = self.__callbacks.get(func)
        if curId is not None:
            BigWorld.cancelCallback(curId)
            del self.__callbacks[func]
        curId = BigWorld.callback(seconds, functools.partial(self.__funcWrapper, func, *args, **kwargs))
        self.__callbacks[func] = curId



    def stopCallback(self, func):
        curId = self.__callbacks.get(func)
        if curId is not None:
            BigWorld.cancelCallback(curId)
            del self.__callbacks[func]



    def hasDelayedCallback(self, func):
        return func in self.__callbacks




class TimeDeltaMeter(object):

    def __init__(self):
        self.__prevTime = BigWorld.time()



    def measureDeltaTime(self):
        time = BigWorld.time()
        deltaTime = time - self.__prevTime
        self.__prevTime = time
        return deltaTime




+++ okay decompyling callbackdelayer.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:56:17 CET
