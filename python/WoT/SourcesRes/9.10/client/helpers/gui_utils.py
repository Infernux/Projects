# 2015.01.14 22:38:35 CET
import GUI
import Math

def setAnchor(component, hor, vert):
    component.horizontalAnchor = hor
    component.verticalAnchor = vert



def setPixMode(component):
    component.heightMode = 'PIXEL'
    component.widthMode = 'PIXEL'
    component.verticalPositionMode = 'PIXEL'
    component.horizontalPositionMode = 'PIXEL'



def pixToClipVector2(pixVector):
    scrRes = GUI.screenResolution()
    return Math.Vector2(2.0 * pixVector[0] / scrRes[0], -2.0 * pixVector[1] / scrRes[1])



def buildTexMapping(texCoords, texSize, fullTexSize):
    max = texCoords + texSize
    return ((texCoords[0] / fullTexSize[0], texCoords[1] / fullTexSize[1]),
     (texCoords[0] / fullTexSize[0], max[1] / fullTexSize[1]),
     (max[0] / fullTexSize[0], max[1] / fullTexSize[1]),
     (max[0] / fullTexSize[0], texCoords[1] / fullTexSize[1]))



+++ okay decompyling gui_utils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:38:35 CET
