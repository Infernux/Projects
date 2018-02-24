# 2015.01.18 14:20:44 CET
from messenger.m_constants import MESSENGER_SCOPE

def setGUIEntries(decorator):
    from messenger.gui.Scaleform.LobbyEntry import LobbyEntry
    from messenger.gui.Scaleform.BattleEntry import BattleEntry
    decorator.setEntry(MESSENGER_SCOPE.LOBBY, LobbyEntry())
    decorator.setEntry(MESSENGER_SCOPE.BATTLE, BattleEntry())



+++ okay decompyling __init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.18 14:20:44 CET
