# 2015.01.14 22:38:36 CET
import random
import re
from constants import ARENA_GUI_TYPE
from debug_utils import LOG_CURRENT_EXCEPTION
from helpers import i18n

def _readNumberOfTips():
    result = 0
    tipsPattern = re.compile('^tip(\\d+)$')
    try:
        translator = i18n.g_translators['tips']
    except IOError:
        LOG_CURRENT_EXCEPTION()
        return result
    for key in translator._catalog.iterkeys():
        if len(key) > 0:
            sreMatch = tipsPattern.match(key)
            if sreMatch is not None and len(sreMatch.groups()) > 0:
                number = int(sreMatch.groups()[0])
                result = max(number, result)

    return result



def getNextNumberOfTip():
    return random.randint(0, g_totalNumberOfTips)



def getTip(arenaGuiType = None):
    if arenaGuiType == ARENA_GUI_TYPE.EVENT_BATTLES:
        return i18n.makeString('#tips:eventTip')
    return i18n.makeString('#tips:tip{0:d}'.format(getNextNumberOfTip()))


g_totalNumberOfTips = _readNumberOfTips()

+++ okay decompyling tips.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:38:36 CET
