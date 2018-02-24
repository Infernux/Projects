# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class CalendarMeta(DAAPIModule):

    def onMonthChanged(self, rawDate):
        self._printOverrideError('onMonthChanged')



    def onDateSelected(self, rawDate):
        self._printOverrideError('onDateSelected')



    def formatYMHeader(self, rawDate):
        self._printOverrideError('formatYMHeader')



    def as_openMonthS(self, rawDate):
        if self._isDAAPIInited():
            return self.flashObject.as_openMonth(rawDate)



    def as_selectDateS(self, rawDate):
        if self._isDAAPIInited():
            return self.flashObject.as_selectDate(rawDate)



    def as_updateMonthEventsS(self, items):
        if self._isDAAPIInited():
            return self.flashObject.as_updateMonthEvents(items)



    def as_setCalendarMessageS(self, message):
        if self._isDAAPIInited():
            return self.flashObject.as_setCalendarMessage(message)



    def as_setMinAvailableDateS(self, rawDate):
        if self._isDAAPIInited():
            return self.flashObject.as_setMinAvailableDate(rawDate)



    def as_setMaxAvailableDateS(self, rawDate):
        if self._isDAAPIInited():
            return self.flashObject.as_setMaxAvailableDate(rawDate)




+++ okay decompyling calendarmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
