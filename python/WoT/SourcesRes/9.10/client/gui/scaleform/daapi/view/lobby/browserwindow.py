# 2015.01.14 22:14:35 CET
from gui import game_control
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.meta.BrowserMeta import BrowserMeta
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.framework import AppRef
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework.managers.TextManager import TextIcons
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.WAITING import WAITING
from gui.shared.event_bus import EVENT_BUS_SCOPE
from helpers import i18n

class BrowserWindow(View, AbstractWindowView, BrowserMeta, AppRef):

    def __init__(self, ctx = None):
        super(BrowserWindow, self).__init__()
        self.__url = ctx.get('url')
        self.__customTitle = ctx.get('title')
        self.__showActionBtn = ctx.get('showActionBtn', True)
        self.__showWaiting = ctx.get('showWaiting', False)
        self.__browserID = ctx.get('browserID')
        self.__browser = game_control.g_instance.browser.getBrowser(self.__browserID)
        if not self.__browser is not None:
            raise AssertionError('Cannot find browser for browser window')
            self.__size = ctx.get('size', game_control.g_instance.browser.BROWSER_SIZE)
            self.__isDefault = ctx.get('isDefault', True)
            self.__isLoaded = True
            return 



    def onWindowClose(self):
        self.destroy()



    def browserAction(self, action):
        self.__browser.browserAction(action)



    def browserMove(self, x, y, z):
        self.__browser.browserMove(x, y, z)



    def browserDown(self, x, y, z):
        self.__browser.browserDown(x, y, z)



    def browserUp(self, x, y, z):
        self.__browser.browserUp(x, y, z)



    def browserFocusOut(self):
        self.__browser.browserFocusOut()



    def onBrowserShow(self, needRefresh = False):
        self.__browser.onBrowserShow(needRefresh)



    def onBrowserHide(self):
        self.__browser.onBrowserHide()



    def _populate(self):
        super(BrowserWindow, self)._populate()
        self.as_setBrowserSizeS(*self.__size)
        self.as_configureS(self.__isDefault, self.__customTitle, self.__showActionBtn)
        self.__browser.onLoadStart += self.__onLoadStart
        self.__browser.onLoadEnd += self.__onLoadEnd
        self.__browser.onNavigate += self.__onNavigate
        game_control.g_instance.browser.onBrowserDeleted += self.__onBrowserDeleted
        self.addListener(VIEW_ALIAS.BROWSER_WINDOW, self.__onShow, EVENT_BUS_SCOPE.LOBBY)



    def _dispose(self):
        self.__browser.onLoadStart -= self.__onLoadStart
        self.__browser.onLoadEnd -= self.__onLoadEnd
        self.__browser.onNavigate -= self.__onNavigate
        browser = game_control.g_instance.browser
        browser.onBrowserDeleted -= self.__onBrowserDeleted
        self.removeListener(VIEW_ALIAS.BROWSER_WINDOW, self.__onShow, EVENT_BUS_SCOPE.LOBBY)
        self.__browser = None
        browser.delBrowser(self.__browserID)
        super(BrowserWindow, self)._dispose()



    def __showDataUnavailableView(self):
        warningIcon = i18n.makeString(self.app.utilsManager.textManager.getIcon(TextIcons.ALERT_ICON))
        header = warningIcon + i18n.makeString(MENU.BROWSER_DATAUNAVAILABLE_HEADER)
        description = i18n.makeString(MENU.BROWSER_DATAUNAVAILABLE_DESCRIPTION)
        self.as_showServiceViewS(header, description)



    def __onLoadStart(self, url):
        self.as_loadingStartS()
        if self.__showWaiting:
            self.as_showWaitingS(WAITING.LOADCONTENT, {})



    def __onLoadEnd(self, url, isLoaded = True):
        self.as_loadingStopS()
        if self.__showWaiting:
            self.as_hideWaitingS()
            self.__isLoaded = self.__isLoaded and isLoaded
            if not self.__isLoaded:
                self.__showDataUnavailableView()



    def __onNavigate(self, url):
        self.as_hideServiceViewS()
        self.__isLoaded = True



    def __onShow(self, event):
        if self.__browserID == event.ctx.get('browserID'):
            self.__url = event.ctx.get('url')
            self.__customTitle = event.ctx.get('title', self.__customTitle)
            self.__showActionBtn = event.ctx.get('showActionBtn', self.__showActionBtn)
            self.as_configureS(self.__isDefault, self.__customTitle, self.__showActionBtn)
            if self.__url is not None and self.__url != self.__browser.url:
                self.__browser.navigate(self.__url)
            else:
                self.__browser.onBrowserShow(False)



    def __onBrowserDeleted(self, browserID):
        if self.__browserID == browserID:
            self.destroy()




+++ okay decompyling browserwindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:35 CET
