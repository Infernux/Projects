# 2015.01.14 22:38:29 CET
import BigWorld
DRR_MIN_SCALE_VALUE = 0.5
DRR_MAX_SCALE_VALUE = 1.0
DRR_MAX_STEP_VALUE = 0.05
PERCENT_MODIFIER = 100.0

def normalizeScale(value):
    result = min(max(round(value, 2), DRR_MIN_SCALE_VALUE), DRR_MAX_SCALE_VALUE)
    modulo = result * PERCENT_MODIFIER % (DRR_MAX_STEP_VALUE * PERCENT_MODIFIER)
    if modulo:
        result = result - modulo / PERCENT_MODIFIER
    return result



def getPercent(value):
    return round(value, 3) * PERCENT_MODIFIER



def changeScaleByStep(offset):
    result = None
    scale = BigWorld.getDRRScale()
    newScale = normalizeScale(scale + offset)
    if scale != newScale:
        BigWorld.setDRRScale(newScale)
        if normalizeScale(BigWorld.getDRRScale()) == newScale:
            result = newScale
    return result



def stepUp():
    return changeScaleByStep(DRR_MAX_STEP_VALUE)



def stepDown():
    return changeScaleByStep(-DRR_MAX_STEP_VALUE)



+++ okay decompyling drr_scale.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:38:29 CET
