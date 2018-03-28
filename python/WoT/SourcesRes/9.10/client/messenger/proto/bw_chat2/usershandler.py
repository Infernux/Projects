# 2015.01.18 11:53:48 CET
from messenger.proto.bw.entities import BWUserEntity
from messenger.proto.bw_chat2 import provider, limits
from messenger.proto.events import g_messengerEvents
from messenger_common_chat2 import MESSENGER_ACTION_IDS as _ACTIONS, messageArgs
from debug_utils import LOG_WARNING
import cPickle
from messenger.storage import storage_getter

class UsersHandler(provider.ResponseDictHandler):

    def __init__(self, provider):
        super(UsersHandler, self).__init__(provider)
        self.__limits = limits.FindUserLimits()



    @storage_getter('users')
    def usersStorage(self):
        return None



    def _onResponseSuccess(self, ids, args):
        if not super(UsersHandler, self)._onResponseSuccess(ids, args):
            return 
        result = cPickle.loads(args['strArg1'])
        users = []
        for userData in result:
            (name, dbID, isOnline, clanAbbrev,) = userData
            dbID = long(dbID)
            if not len(name):
                continue
            received = BWUserEntity(dbID, name=name, isOnline=isOnline, clanAbbrev=clanAbbrev)
            user = self.usersStorage.getUser(dbID)
            if user:
                if user.isCurrentPlayer():
                    received = user
                else:
                    received.update(roster=user.getRoster())
            users.append(received)

        g_messengerEvents.users.onFindUsersComplete(ids[1], users)



    def _onResponseFailure(self, ids, args):
        actionID = super(UsersHandler, self)._onResponseFailure(ids, args)
        if actionID is None:
            return 
        if actionID == _ACTIONS.FIND_USERS_BY_NAME:
            g_messengerEvents.users.onFindUsersFailed(ids[1], args)
        else:
            LOG_WARNING('Error is not resolved on the client', ids, args)



    @storage_getter('users')
    def usersStorage(self):
        return None



    def findUsers(self, namePattern, searchOnlineOnly = None):
        provider = self.provider()
        if searchOnlineOnly is None:
            searchOnlineOnly = False
        (success, reqID,) = provider.doAction(_ACTIONS.FIND_USERS_BY_NAME, messageArgs(strArg1=namePattern, int32Arg1=self.__limits.getMaxResultSize(), int64Arg1=searchOnlineOnly), response=True)
        if reqID:
            self.pushRq(reqID, _ACTIONS.FIND_USERS_BY_NAME)
        if success:
            cooldown = self.__limits.getRequestCooldown()
            provider.setActionCoolDown(_ACTIONS.FIND_USERS_BY_NAME, cooldown)
        return (success, reqID)



    def clear(self):
        super(UsersHandler, self).clear()
        self.__limits = None




+++ okay decompyling usershandler.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.18 11:53:48 CET
