# 2015.01.14 22:35:43 CET
from collections import defaultdict
import json
import constants
import GUI
import _Scaleform
import weakref
from gui.Scaleform import SCALEFORM_SWF_PATH
from debug_utils import LOG_DEBUG, LOG_CODEPOINT_WARNING, LOG_ERROR, LOG_GUI, _doLog

class Flash(object):

    def __init__(self, swf, className = 'Flash', args = None, path = SCALEFORM_SWF_PATH):
        if args is None:
            args = []
        self.__fsCbs = defaultdict(set)
        self.__exCbs = defaultdict(set)
        movieDefinition = _Scaleform.MovieDef(''.join([path, '/', swf]))
        movie = movieDefinition.createInstance()
        self.component = getattr(GUI, className)(movie, *args)
        self.component.focus = True
        self.component.moveFocus = True
        self.component.position.z = 0.5
        self.flashSize = (2, 2)
        self.isActive = False
        movie = self.component.movie
        movie.setFSCommandCallback(_FsCommandObj(self))
        movie.setExternalInterfaceCallback(_ExternalInterfaceObj(self))



    def __del__(self):
        LOG_DEBUG('Deleted: %s' % self)



    def __onLogGui(self, type, msg, *kargs):
        if type == 'DEBUG' and not constants.IS_DEVELOPMENT:
            return 
        _doLog('%s.GUI' % str(type), msg, kargs)



    def __onLogGuiFormat(self, type, msg, *kargs):
        if type == 'DEBUG' and not constants.IS_DEVELOPMENT:
            return 
        _doLog('%s.GUI' % str(type), msg % kargs, None)



    @property
    def movie(self):
        return self.component.movie



    def afterCreate(self):
        self.addExternalCallback('debug.LOG_GUI', self.__onLogGui)
        self.addExternalCallback('debug.LOG_GUI_FORMAT', self.__onLogGuiFormat)



    def beforeDelete(self):
        self.removeAllCallbacks()
        self.__fsCbs.clear()
        self.__exCbs.clear()
        self.flashSize = None
        del self.component



    def active(self, state):
        if self.isActive != state:
            self.isActive = state
            if state:
                GUI.addRoot(self.component)
                self.component.size = self.flashSize
            else:
                GUI.delRoot(self.component)



    def close(self):
        self.component.script = None
        self.active(False)
        self.beforeDelete()



    def setMovieVariable(self, path, value):
        if not isinstance(value, list):
            value = [value]
        try:
            self.movie.invoke(('_root._level0.' + path, value))
        except Exception:
            LOG_ERROR('Error to set movie variable "' + '_root._level0.' + path + '"')



    def getMember(self, path):
        return getattr(self.movie, path, None)



    def call(self, methodName, args = None):
        if args is None:
            args = []
        args.insert(0, methodName)
        self.movie.invoke(('call', args))



    def callNice(self, methodName, args = None):
        if args is None:
            args = []
        jsonArgs = [methodName, json.dumps(args)]
        self.movie.invoke(('callJson', jsonArgs))



    def respond(self, args = None):
        if args is None:
            args = []
        self.movie.invoke(('respond', args))



    def addFsCallback(self, command, function):
        self.__fsCbs[command].add(function)



    def removeFsCallback(self, command):
        try:
            self.__fsCbs.pop(command)
        except KeyError:
            pass



    def addFsCallbacks(self, commands):
        add = self.addFsCallback
        for (command, function,) in commands.items():
            add(command, function)




    def removeFsCallbacks(self, *args):
        remove = self.removeFsCallback
        for command in args:
            remove(command)




    def addExternalCallback(self, command, function):
        self.__exCbs[command].add(function)



    def removeExternalCallback(self, command, function = None):
        try:
            if function is None:
                self.__exCbs.pop(command)
            elif function in self.__exCbs[command]:
                self.__exCbs[command].remove(function)
        except KeyError:
            pass



    def addExternalCallbacks(self, commands):
        add = self.addExternalCallback
        for (command, function,) in commands.items():
            add(command, function)




    def removeExternalCallbacks(self, *args):
        remove = self.removeExternalCallback
        for command in args:
            remove(command)




    def removeAllCallbacks(self):
        self.__fsCbs.clear()
        self.__exCbs.clear()



    def handleFsCommandCallback(self, command, arg):
        result = False
        if command in self.__fsCbs:
            result = True
            callbacks = self.__fsCbs[command]
            for callback in callbacks:
                callback(arg)

        else:
            LOG_DEBUG('FsCommandCallback "%s" not found' % command, arg)
        return result



    def handleExternalInterfaceCallback(self, command, args):
        result = False
        if command == 'callNice':
            tmp = list(json.loads(args[0]))
            command = tmp.pop(0)
            args = tmp
        if command in self.__exCbs:
            result = True
            callbacks = self.__exCbs[command]
            for callback in callbacks:
                callback(*args)

        else:
            LOG_DEBUG('ExternalInterfaceCallback "%s" not found' % command, args)
        return result




class _FsCommandObj():

    def __init__(self, obj):
        self.__weakObj = weakref.ref(obj)



    def __call__(self, command, args):
        obj = self.__weakObj()
        if obj:
            obj.handleFsCommandCallback(command, args)
        else:
            LOG_CODEPOINT_WARNING('weak object has been already destroyed.')




class _ExternalInterfaceObj():

    def __init__(self, obj):
        self.__weakObj = weakref.ref(obj)



    def __call__(self, command, args):
        obj = self.__weakObj()
        if obj:
            obj.handleExternalInterfaceCallback(command, args)
        else:
            LOG_CODEPOINT_WARNING('weak object has been already destroyed.')




+++ okay decompyling flash.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:35:44 CET
