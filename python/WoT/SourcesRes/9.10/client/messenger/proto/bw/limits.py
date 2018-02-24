# 2015.01.14 21:21:02 CET
from constants import CHAT_MESSAGE_MAX_LENGTH, CHAT_MESSAGE_MAX_LENGTH_IN_BATTLE
from messenger.m_constants import MESSAGES_HISTORY_MAX_LEN
from messenger.proto.interfaces import IProtoLimits

class BattleLimits(IProtoLimits):

    def getMessageMaxLength(self):
        return CHAT_MESSAGE_MAX_LENGTH_IN_BATTLE



    def getHistoryMaxLength(self):
        return MESSAGES_HISTORY_MAX_LEN




class LobbyLimits(IProtoLimits):

    def getMessageMaxLength(self):
        return CHAT_MESSAGE_MAX_LENGTH



    def getHistoryMaxLength(self):
        return MESSAGES_HISTORY_MAX_LEN




+++ okay decompyling limits.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 21:21:02 CET
