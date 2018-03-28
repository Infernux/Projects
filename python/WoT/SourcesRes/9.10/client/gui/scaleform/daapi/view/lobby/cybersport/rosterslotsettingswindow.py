# 2015.01.14 22:14:47 CET
from account_helpers.AccountSettings import AccountSettings
from gui.Scaleform.daapi.view.lobby.cyberSport.VehicleSelectorBase import VehicleSelectorBase
from gui.Scaleform.daapi.view.lobby.rally.vo_converters import makeVehicleVO
from gui.Scaleform.daapi.view.meta.RosterSlotSettingsWindowMeta import RosterSlotSettingsWindowMeta
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.framework.entities.View import View
from gui.shared.ItemsCache import g_itemsCache, REQ_CRITERIA
from gui.shared.events import CSRosterSlotSettingsWindow
__author__ = 'd_savitski'

class RosterSlotSettingsWindow(View, RosterSlotSettingsWindowMeta, AbstractWindowView, VehicleSelectorBase):

    def __init__(self, ctx = None):
        super(RosterSlotSettingsWindow, self).__init__()
        if not 'section' in ctx:
            raise AssertionError('Section is required to show selector popup')
            self.__section = ctx.get('section')
            self.__levelsRange = ctx.get('levelsRange', (1, 10))
            self.currentSlot = self.__makeInitialSlotData(ctx.get('settings'))
            return 



    def _populate(self):
        super(RosterSlotSettingsWindow, self)._populate()
        self.as_setDefaultDataS(self.currentSlot)
        self.slotSettings = None



    def updateSlots(self, slots):
        self.as_setDefaultDataS(slots)



    def onFiltersUpdate(self, nation, vehicleType, isMain, level, compatibleOnly):
        self._updateFilter(nation, vehicleType, isMain, level, compatibleOnly)
        self.updateData()



    def updateData(self):
        result = self._updateData(g_itemsCache.items.getVehicles(~REQ_CRITERIA.SECRET), self.__levelsRange)
        self.as_setListDataS(result)



    def getFilterData(self):
        filters = AccountSettings.getFilter(self.__section)
        filters['isMain'] = False
        result = self._initFilter(**filters)
        return result



    def submitButtonHandler(self, value):
        self.currentSlot = self.__makeCurrentSlotData(value)
        self.fireEvent(CSRosterSlotSettingsWindow(CSRosterSlotSettingsWindow.APPLY_SLOT_SETTINGS, self.currentSlot))
        self.onWindowClose()



    def __makeInitialSlotData(self, slotSettings):
        if slotSettings[2] is None:
            levels = list(self.__levelsRange)
            slotSettings[2] = {'nationIDRange': [],
             'vTypeRange': [],
             'vLevelRange': levels[::(len(levels) - 1)]}
            return slotSettings
        return self.__makeCurrentSlotData(slotSettings)



    def __makeCurrentSlotData(self, value):
        currentSlot = [value[0], value[1]]
        data = value[2]
        if isinstance(data, long):
            currentSlot.append(makeVehicleVO(g_itemsCache.items.getItemByCD(int(data)), self.__levelsRange))
        elif data is not None:
            if len(data.nationIDRange) == 0 and len(data.vTypeRange) == 0 and len(data.vLevelRange) == 0:
                currentSlot.append(None)
            else:
                currentSlot.append({'nationIDRange': data.nationIDRange,
                 'vTypeRange': data.vTypeRange,
                 'vLevelRange': data.vLevelRange})
        else:
            currentSlot.append(None)
        return currentSlot



    def cancelButtonHandler(self):
        self.onWindowClose()



    def onWindowClose(self):
        self.destroy()



    def _dispose(self):
        currentFilters = self.getFilters()
        if currentFilters:
            filters = {'nation': currentFilters['nation'],
             'vehicleType': currentFilters['vehicleType'],
             'isMain': currentFilters['isMain'],
             'level': currentFilters['level'],
             'compatibleOnly': currentFilters['compatibleOnly']}
            AccountSettings.setFilter(self.__section, filters)
        super(RosterSlotSettingsWindow, self)._dispose()
        self.currentSlot = None
        self.slotSettings = None




+++ okay decompyling rosterslotsettingswindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:47 CET
