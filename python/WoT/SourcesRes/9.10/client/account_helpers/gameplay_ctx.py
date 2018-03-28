# 2015.01.14 13:53:27 CET
import ArenaType
import constants
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_WARNING
_ASSAULT2_GP_NAME = constants.ARENA_GAMEPLAY_NAMES[6]
ENABLED_ARENA_GAMEPLAY_NAMES = constants.ARENA_GAMEPLAY_NAMES[:3] + (_ASSAULT2_GP_NAME,)

def getDefaultMask():

    def getValue(name):
        return ArenaType.getVisibilityMask(ArenaType.getGameplayIDForName(name))


    return sum(map(getValue, ENABLED_ARENA_GAMEPLAY_NAMES))



def getMask():
    from account_helpers.settings_core.SettingsCore import g_settingsCore
    mask = g_settingsCore.serverSettings.getGameplaySetting('gameplayMask', getDefaultMask())
    ctfMask = 1 << constants.ARENA_GAMEPLAY_IDS['ctf']
    nationsMask = 1 << constants.ARENA_GAMEPLAY_IDS['nations']
    if not mask:
        LOG_WARNING('Gameplay is not defined', mask)
    elif mask & ctfMask == 0:
        LOG_WARNING('Gameplay "ctf" is not defined', mask)
    if mask & nationsMask:
        mask ^= nationsMask
        LOG_DEBUG('Nations battle mode currently unavailable')
    mask |= ctfMask
    return mask



def setMaskByNames(names):
    gameplayNames = {'ctf'}
    for name in names:
        if name in ArenaType.g_gameplayNames:
            gameplayNames.add(name)
        else:
            LOG_ERROR('Gameplay is not available', name)

    gameplayMask = ArenaType.getGameplaysMask(gameplayNames)
    LOG_DEBUG('Set gameplay (names, mask)', gameplayNames, gameplayMask)
    from account_helpers.settings_core.SettingsCore import g_settingsCore
    g_settingsCore.serverSettings.setGameplaySettings({'gameplayMask': gameplayMask})



def isCreationEnabled(gameplayName):
    return gameplayName in ENABLED_ARENA_GAMEPLAY_NAMES



+++ okay decompyling gameplay_ctx.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:27 CET
