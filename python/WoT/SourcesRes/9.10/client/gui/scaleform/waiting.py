# 2015.01.14 22:35:47 CET
import BigWorld
from helpers import i18n

class Waiting:
    __waitingStack = []
    __suspendStack = []
    __isVisible = False

    @classmethod
    def isVisible(cls):
        return cls.__isVisible



    @classmethod
    def isOpened(cls, msg):
        return msg in cls.__waitingStack



    @staticmethod
    def show(message, isSingle = False, interruptCallback = lambda : None):
        BigWorld.Screener.setEnabled(False)
        if not (isSingle and message in Waiting.__waitingStack):
            Waiting.__waitingStack.append(message)
        from gui.WindowsManager import g_windowsManager
        if g_windowsManager.window is not None:
            waitingView = g_windowsManager.window.waitingManager
            if waitingView is not None:
                waitingView.showS(i18n.makeString('#waiting:%s' % message))
                Waiting.__isVisible = True
                waitingView.setCallback(interruptCallback)



    @staticmethod
    def suspend():
        if Waiting.isSuspended():
            return 
        Waiting.__suspendStack = list(Waiting.__waitingStack)
        Waiting.close()



    @staticmethod
    def resume():
        if not Waiting.isSuspended():
            return 
        for id in Waiting.__suspendStack:
            Waiting.show(id)

        Waiting.__suspendStack = []



    @staticmethod
    def isSuspended():
        return len(Waiting.__suspendStack) > 0



    @staticmethod
    def hide(message):
        stack = Waiting.__suspendStack
        if message in stack:
            stack.remove(message)
        try:
            stack = Waiting.__waitingStack
            if message in stack:
                stack.remove(message)
        except:
            pass
        if len(Waiting.__waitingStack) == 0:
            Waiting.close()



    @staticmethod
    def close():
        BigWorld.Screener.setEnabled(True)
        from gui.WindowsManager import g_windowsManager
        if g_windowsManager.window is not None and g_windowsManager.window.waitingManager is not None:
            g_windowsManager.window.waitingManager.close()
        Waiting.__isVisible = False
        Waiting.__waitingStack = []



    @staticmethod
    def rollback():
        Waiting.__suspendStack = []
        Waiting.close()



    @staticmethod
    def cancelCallback():
        from gui.WindowsManager import g_windowsManager
        if g_windowsManager.window is not None:
            waitingView = g_windowsManager.window.waitingManager
            if waitingView is not None:
                waitingView.cancelCallback()




+++ okay decompyling waiting.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:35:47 CET
