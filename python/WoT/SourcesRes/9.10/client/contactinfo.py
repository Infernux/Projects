# 2015.01.14 13:32:36 CET
import BigWorld
import Settings

class ContactInfo:
    KEY_USER = 'user'
    KEY_HOST = 'host'
    KEY_EMAIL = 'email'
    KEY_PASSWORD = 'password'
    KEY_REMEMBER = 'remember'

    def __init__(self):
        self.host = None
        self.user = None
        self.email = None
        self.password = None
        self.rememberPassword = False
        self.__checkLoginDataSection()
        self.readLocalLoginData()



    def readLocalLoginData(self):
        ds = self.getLoginDataSection()
        self.host = ds.readString(self.KEY_HOST)
        self.user = ds.readString(self.KEY_USER)
        self.email = ds.readString(self.KEY_EMAIL)
        self.password = ds.readString(self.KEY_PASSWORD)
        self.rememberPassword = bool(ds.readString(self.KEY_REMEMBER))



    def writeLocalLoginData(self):
        ds = self.getLoginDataSection()
        ds.writeString(self.KEY_HOST, self.host)
        ds.writeString(self.KEY_USER, self.user)
        ds.writeString(self.KEY_EMAIL, self.email)
        ds.writeString(self.KEY_PASSWORD, self.password)
        ds.writeString(self.KEY_REMEMBER, str(self.rememberPassword))



    def getLoginDataSection(self):
        return Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO]



    def __checkLoginDataSection(self):
        up = Settings.g_instance.userPrefs
        if not up.has_key(Settings.KEY_LOGIN_INFO):
            up.write(Settings.KEY_LOGIN_INFO, '')




+++ okay decompyling contactinfo.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:32:36 CET
