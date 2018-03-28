# 2015.01.14 22:14:47 CET
from gui.Scaleform.daapi.view.lobby.cyberSport.RosterSlotSettingsWindow import RosterSlotSettingsWindow
from gui.Scaleform.daapi.view.lobby.cyberSport.VehicleSelectorPopup import VehicleSelectorPopup
from gui.Scaleform.framework.managers.loaders import PackageBusinessHandler
from gui.Scaleform.framework import GroupedViewSettings, ViewTypes, ViewSettings, ScopeTemplates
from gui.Scaleform.genConsts.CYBER_SPORT_ALIASES import CYBER_SPORT_ALIASES
from gui.shared import EVENT_BUS_SCOPE
from gui.shared.events import ShowDialogEvent

def getViewSettings():
    from gui.Scaleform.daapi.view.lobby.cyberSport.CyberSportMainWindow import CyberSportMainWindow
    from gui.Scaleform.daapi.view.lobby.cyberSport.CyberSportIntroView import CyberSportIntroView
    from gui.Scaleform.daapi.view.lobby.cyberSport.CyberSportUnitsListView import CyberSportUnitsListView
    from gui.Scaleform.daapi.view.lobby.cyberSport.CyberSportUnitView import CyberSportUnitView
    from gui.Scaleform.daapi.view.dialogs.CyberSportDialog import CyberSportDialog
    return [GroupedViewSettings(CYBER_SPORT_ALIASES.CYBER_SPORT_WINDOW_PY, CyberSportMainWindow, CYBER_SPORT_ALIASES.CYBER_SPORT_WINDOW_UI, ViewTypes.WINDOW, '', CYBER_SPORT_ALIASES.CYBER_SPORT_WINDOW_PY, ScopeTemplates.DEFAULT_SCOPE),
     GroupedViewSettings(CYBER_SPORT_ALIASES.ROSTER_SLOT_SETTINGS_WINDOW_PY, RosterSlotSettingsWindow, CYBER_SPORT_ALIASES.ROSTER_SLOT_SETTINGS_WINDOW_UI, ViewTypes.TOP_WINDOW, '', None, ScopeTemplates.DEFAULT_SCOPE),
     GroupedViewSettings(CYBER_SPORT_ALIASES.VEHICLE_SELECTOR_POPUP_PY, VehicleSelectorPopup, CYBER_SPORT_ALIASES.VEHICLE_SELECTOR_POPUP_UI, ViewTypes.TOP_WINDOW, '', None, ScopeTemplates.DEFAULT_SCOPE),
     GroupedViewSettings(CYBER_SPORT_ALIASES.CYBER_SPORT_DIALOG_PY, CyberSportDialog, CYBER_SPORT_ALIASES.CYBER_SPORT_DIALOG_UI, ViewTypes.TOP_WINDOW, '', None, ScopeTemplates.DYNAMIC_SCOPE),
     ViewSettings(CYBER_SPORT_ALIASES.INTRO_VIEW_PY, CyberSportIntroView, None, ViewTypes.COMPONENT, None, ScopeTemplates.DEFAULT_SCOPE),
     ViewSettings(CYBER_SPORT_ALIASES.UNITS_LIST_VIEW_PY, CyberSportUnitsListView, None, ViewTypes.COMPONENT, None, ScopeTemplates.DEFAULT_SCOPE),
     ViewSettings(CYBER_SPORT_ALIASES.UNIT_VIEW_PY, CyberSportUnitView, None, ViewTypes.COMPONENT, None, ScopeTemplates.DEFAULT_SCOPE)]



def getBusinessHandlers():
    return [CyberSportBusinessHandler(), CyberSportDialogsHandler()]



class CyberSportBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        listeners = [(CYBER_SPORT_ALIASES.CYBER_SPORT_WINDOW_PY, self.__showSimpleWindow), (CYBER_SPORT_ALIASES.VEHICLE_SELECTOR_POPUP_PY, self.__showSimpleWindow), (CYBER_SPORT_ALIASES.ROSTER_SLOT_SETTINGS_WINDOW_PY, self.__showSimpleWindow)]
        super(CyberSportBusinessHandler, self).__init__(listeners, EVENT_BUS_SCOPE.LOBBY)



    def __showSimpleWindow(self, event):
        self.app.loadView(event.eventType, event.name, event.ctx)




class CyberSportDialogsHandler(PackageBusinessHandler):

    def __init__(self):
        super(CyberSportDialogsHandler, self).__init__([(ShowDialogEvent.SHOW_CYBER_SPORT_DIALOG, self.__showCyberSportDialog)], EVENT_BUS_SCOPE.DEFAULT)



    def __showCyberSportDialog(self, event):
        self._loadView(CYBER_SPORT_ALIASES.CYBER_SPORT_DIALOG_PY, event.meta, event.handler)




+++ okay decompyling sf_settings.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:47 CET
