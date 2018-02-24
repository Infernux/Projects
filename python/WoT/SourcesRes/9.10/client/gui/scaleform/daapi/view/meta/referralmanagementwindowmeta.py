# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ReferralManagementWindowMeta(DAAPIModule):

    def onInvitesManagementLinkClick(self):
        self._printOverrideError('onInvitesManagementLinkClick')



    def inviteIntoSquad(self, referralID):
        self._printOverrideError('inviteIntoSquad')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_setTableDataS(self, referrals):
        if self._isDAAPIInited():
            return self.flashObject.as_setTableData(referrals)



    def as_setProgressDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setProgressData(data)




+++ okay decompyling referralmanagementwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
