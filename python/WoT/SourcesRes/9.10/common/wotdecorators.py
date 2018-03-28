# 2015.01.14 22:43:05 CET
from debug_utils import LOG_WRAPPED_CURRENT_EXCEPTION, CRITICAL_ERROR
from time_tracking import LOG_TIME_WARNING
import time
import time_tracking

def noexcept(func):

    def wrapper(*args, **kwArgs):
        try:
            return func(*args, **kwArgs)
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)


    return wrapper



def nofail(func):

    def wrapper(*args, **kwArgs):
        try:
            return func(*args, **kwArgs)
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)
            CRITICAL_ERROR('Exception in no-fail code')


    return wrapper



def exposedtoclient(func):

    def wrapper(*args, **kwArgs):
        try:
            lastTick = time.time()
            result = func(*args, **kwArgs)
            timeSinceLastTick = time.time() - lastTick
            if timeSinceLastTick > time_tracking.DEFAULT_TIME_LIMIT:
                LOG_TIME_WARNING(timeSinceLastTick, context=(args[0].id,
                 func.__name__,
                 args,
                 kwArgs))
            return result
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)


    return wrapper



+++ okay decompyling wotdecorators.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:43:05 CET
