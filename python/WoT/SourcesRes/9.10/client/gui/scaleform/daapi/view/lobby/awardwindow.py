# 2015.01.14 22:14:35 CET
from gui.Scaleform.daapi.view.meta.AwardWindowMeta import AwardWindowMeta
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework import AppRef
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class AwardAbstract(AppRef):

    def getWindowTitle(self):
        return ''



    def getBackgroundImage(self):
        return ''



    def getAwardImage(self):
        return None



    def getHeader(self):
        return ''



    def getDescription(self):
        return ''



    def getAdditionalText(self):
        return ''



    def getBottomText(self):
        return ''



    def getExtraFields(self):
        return {}



    def handleOkButton(self):
        pass




class AwardWindow(View, AbstractWindowView, AwardWindowMeta, AppRef):

    def __init__(self, ctx):
        super(AwardWindow, self).__init__()
        assert 'award' in ctx and isinstance(ctx['award'], AwardAbstract)
        self.__award = ctx['award']



    def onWindowClose(self):
        self.destroy()



    def onOKClick(self):
        self.onWindowClose()
        return self.__award.handleOkButton()



    def _populate(self):
        super(AwardWindow, self)._populate()
        data = {'windowTitle': self.__award.getWindowTitle(),
         'backImage': self.__award.getBackgroundImage(),
         'awardImage': self.__award.getAwardImage(),
         'header': self.__award.getHeader(),
         'description': self.__award.getDescription(),
         'additionalText': self.__award.getAdditionalText(),
         'buttonText': self.__award.getBottomText()}
        data.update(self.__award.getExtraFields())
        self.as_setDataS(data)




+++ okay decompyling awardwindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:14:35 CET
