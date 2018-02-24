# 2015.01.14 23:59:34 CET
from debug_utils import LOG_DEBUG
from gui.Scaleform.framework.managers.loaders import PackageBusinessHandler
from gui.Scaleform.framework import ViewSettings, GroupedViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.shared import EVENT_BUS_SCOPE

def getViewSettings():
    from gui.Scaleform.daapi.view.lobby import trainings
    return [ViewSettings(PREBATTLE_ALIASES.TRAINING_LIST_VIEW_PY, trainings.Trainings, 'trainingForm.swf', ViewTypes.LOBBY_SUB, PREBATTLE_ALIASES.TRAINING_LIST_VIEW_PY, ScopeTemplates.DEFAULT_SCOPE), ViewSettings(PREBATTLE_ALIASES.TRAINING_ROOM_VIEW_PY, trainings.TrainingRoom, 'trainingRoom.swf', ViewTypes.LOBBY_SUB, PREBATTLE_ALIASES.TRAINING_ROOM_VIEW_PY, ScopeTemplates.DEFAULT_SCOPE), GroupedViewSettings(PREBATTLE_ALIASES.TRAINING_SETTINGS_WINDOW_PY, trainings.TrainingSettingsWindow, 'trainingWindow.swf', ViewTypes.WINDOW, PREBATTLE_ALIASES.TRAINING_SETTINGS_WINDOW_PY, None, ScopeTemplates.DEFAULT_SCOPE)]



def getBusinessHandlers():
    return [_TrainingPackageBusinessHandler()]



class _TrainingPackageBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        listeners = [(PREBATTLE_ALIASES.TRAINING_LIST_VIEW_PY, self.__showViewSimple), (PREBATTLE_ALIASES.TRAINING_ROOM_VIEW_PY, self.__showViewSimple), (PREBATTLE_ALIASES.TRAINING_SETTINGS_WINDOW_PY, self.__showViewSimple)]
        super(_TrainingPackageBusinessHandler, self).__init__(listeners, EVENT_BUS_SCOPE.LOBBY)



    def __showViewSimple(self, event):
        self.app.loadView(event.eventType, event.name, event.ctx)




+++ okay decompyling sf_settings.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:59:34 CET
