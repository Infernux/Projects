# 2015.01.17 21:49:49 CET
from collections import namedtuple
from gui.Scaleform.framework import ViewTypes
import gui.Scaleform.framework.ViewTypes
import gui.Scaleform.framework.ScopeTemplates
from gui.Scaleform.framework.factories import EntitiesFactories, DAAPIModuleFactory, ViewFactory

class COMMON_VIEW_ALIAS(object):
    LOGIN = 'login'
    INTRO_VIDEO = 'introVideo'
    LOBBY = 'lobby'
    CURSOR = 'cursor'
    WAITING = 'waiting'

ViewSettings = namedtuple('ViewSettings', ('alias', 'clazz', 'url', 'type', 'event', 'scope'))
GroupedViewSettings = namedtuple('GroupedViewSettings', ('alias', 'clazz', 'url', 'type', 'group', 'event', 'scope'))
g_entitiesFactories = EntitiesFactories((DAAPIModuleFactory((ViewTypes.COMPONENT,)), ViewFactory((ViewTypes.DEFAULT,
  ViewTypes.LOBBY_SUB,
  ViewTypes.CURSOR,
  ViewTypes.WAITING,
  ViewTypes.WINDOW,
  ViewTypes.BROWSER,
  ViewTypes.TOP_WINDOW,
  ViewTypes.SERVICE_LAYOUT))))

class AppRef(object):
    __reference = None

    @property
    def app(self):
        return AppRef.__reference



    @property
    def gfx(self):
        return AppRef.__reference.movie



    @classmethod
    def setReference(cls, app):
        cls.__reference = app



    @classmethod
    def clearReference(cls):
        cls.__reference = None




+++ okay decompyling __init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.17 21:49:49 CET
