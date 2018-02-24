# 2015.01.14 23:18:56 CET
from gui.Scaleform.managers.windows_stored_data import DATA_TYPE, TARGET_ID
from gui.Scaleform.managers.windows_stored_data import stored_window
from messenger.gui.Scaleform.view.SimpleChannelWindow import SimpleChannelWindow

@stored_window(DATA_TYPE.CAROUSEL_WINDOW, TARGET_ID.CHANNEL_CAROUSEL)
class LazyChannelWindow(SimpleChannelWindow):
    pass

+++ okay decompyling lazychannelwindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 23:18:56 CET
