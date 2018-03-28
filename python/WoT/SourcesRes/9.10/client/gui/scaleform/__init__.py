# 2015.01.14 22:35:47 CET
from nations import NAMES
SCALEFORM_SUPPORT = False
try:
    import _Scaleform
    SCALEFORM_SUPPORT = True
except ImportError:
    raise NotImplementedError, 'Client not support Scaleform'
SCALEFORM_SWF_PATH = 'gui/scaleform'
SCALEFORM_SWF_PATH_V3 = 'gui/flash'
SCALEFORM_STARTUP_VIDEO_PATH = 'gui/flash/video'
SCALEFORM_STARTUP_VIDEO_MASK = 'video/%s'
SCALEFORM_WALLPAPER_PATH = 'gui/maps/login'
SCALEFORM_FONT_LIB_PATH = 'gui/flash'
SCALEFORM_FONT_CONFIG_FILE = 'fontconfig.xml'
SCALEFORM_FONT_CONFIG_PATH = 'gui/flash/%s' % SCALEFORM_FONT_CONFIG_FILE
SCALEFORM_DEFAULT_CONFIG_NAME = 'All'
VEHICLE_TYPES_ICONS_DIR_PATH = '../maps/icons/filters/tanks/'
NATIONS_ICON_FILENAME = '../maps/icons/nations/%s_%s.%s'
NATION_ICON_PREFIX_131x31 = '131x31'

def getVehicleTypeAssetPath(vehicleType, extension = '.png'):
    return ''.join([VEHICLE_TYPES_ICONS_DIR_PATH, vehicleType, extension])



def getNationsAssetPath(nation, namePrefix = '', extension = 'png'):
    return NATIONS_ICON_FILENAME % (NAMES[nation], namePrefix, extension)



+++ okay decompyling __init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:35:47 CET
