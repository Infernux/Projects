# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ContactsListButtonMeta(DAAPIModule):

    def as_setContactsCountS(self, num):
        if self._isDAAPIInited():
            return self.flashObject.as_setContactsCount(num)




+++ okay decompyling contactslistbuttonmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
