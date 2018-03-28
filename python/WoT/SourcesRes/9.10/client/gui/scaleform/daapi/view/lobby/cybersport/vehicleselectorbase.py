# 2015.01.14 22:14:47 CET
from gui.Scaleform.daapi.view.lobby.rally.vo_converters import makeVehicleVO
from gui.Scaleform.locale.CYBERSPORT import CYBERSPORT
from gui.shared.ItemsCache import REQ_CRITERIA
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from gui.Scaleform import getVehicleTypeAssetPath
from helpers import i18n

class VehicleSelectorBase(object):

    def __init__(self):
        self.__filters = None
        self.showNotReadyVehicles = True



    def getFilters(self):
        return self.__filters



    def _updateFilter(self, nation, vehicleType, isMain, level, compatibleOnly):
        self.__filters = {'nation': nation,
         'vehicleType': vehicleType,
         'isMain': isMain,
         'level': level,
         'compatibleOnly': compatibleOnly}



    def _updateData(self, allVehicles, levelsRange):
        criteria = REQ_CRITERIA.EMPTY
        criteria |= ~REQ_CRITERIA.VEHICLE.EXPIRED_IGR_RENT
        criteria |= ~REQ_CRITERIA.VEHICLE.DISABLED_IN_PREM_IGR
        if not self.showNotReadyVehicles:
            criteria |= REQ_CRITERIA.VEHICLE.READY
        if self.__filters:
            if self.__filters['nation'] != -1:
                criteria |= REQ_CRITERIA.NATIONS([self.__filters['nation']])
            if self.__filters['vehicleType'] != 'none':
                criteria |= REQ_CRITERIA.VEHICLE.CLASSES([self.__filters['vehicleType']])
            if self.__filters['isMain']:
                criteria |= REQ_CRITERIA.VEHICLE.FAVORITE
            if self.__filters['level'] != -1:
                criteria |= REQ_CRITERIA.VEHICLE.LEVELS([self.__filters['level']])
        filteredVehicles = allVehicles.filter(criteria)
        if self.__filters.get('compatibleOnly', True):
            return [ vo for vo in [ makeVehicleVO(v, levelsRange) for v in filteredVehicles.values() ] if vo.get('enabled', True) ]
        else:
            return [ makeVehicleVO(v, levelsRange) for v in filteredVehicles.values() ]



    def _initFilter(self, nation, vehicleType, isMain, level, compatibleOnly):
        filtersData = {'vehicleTypesDP': self.getVehicleTypeDP(),
         'levelsDP': self.getLevelsDP(),
         'nation': nation,
         'vehicleType': vehicleType,
         'isMain': isMain,
         'level': level,
         'compatibleOnly': compatibleOnly}
        return filtersData



    def getLevelsDP(self):
        result = []
        for index in range(11):
            itemIcon = 'level_' + ('all' if index == 0 else str(index)) + '.png'
            itemLabel = CYBERSPORT.WINDOW_VEHICLESELECTOR_FILTERS_ALLLEVELS if index == 0 else i18n.makeString(CYBERSPORT.WINDOW_VEHICLESELECTOR_FILTERS_LEVEL) % {'levelNum': index}
            result.append({'label': itemLabel,
             'icon': '../maps/icons/filters/levels/' + itemIcon,
             'data': -1 if index == 0 else index})

        return result



    def getVehicleTypeDP(self):
        all = self._getProviderObject('none')
        all['label'] = self._getVehicleTypeLabel('all')
        result = [all,
         self._getProviderObject(VEHICLE_CLASS_NAME.LIGHT_TANK),
         self._getProviderObject(VEHICLE_CLASS_NAME.MEDIUM_TANK),
         self._getProviderObject(VEHICLE_CLASS_NAME.HEAVY_TANK),
         self._getProviderObject(VEHICLE_CLASS_NAME.SPG),
         self._getProviderObject(VEHICLE_CLASS_NAME.AT_SPG)]
        return result



    def _getVehicleTypeLabel(self, vehicleType):
        return '#menu:carousel_tank_filter/' + vehicleType



    def _getProviderObject(self, vehicleType):
        assetPath = {'label': self._getVehicleTypeLabel(vehicleType),
         'data': vehicleType,
         'icon': getVehicleTypeAssetPath(vehicleType)}
        return assetPath




+++ okay decompyling vehicleselectorbase.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:47 CET
