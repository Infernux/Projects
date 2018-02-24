CONNECT_REQ='\x00'
CONNECT_RESP='\x01'
DISCONNECT_REQ='\x02'
DISCONNECT_RESP='\x03'
DISCONNECT_IND='\x04'
TRANSFER_APDU_REQ='\x05'
TRANSFER_APDU_RESP='\x06'
TRANSFER_ATR_REQ='\x07'
TRANSFERT_ATR_RESP='\x08'
POWER_SIM_OFF_REQ='\x09'
POWER_SIM_OFF_RESP='\x0A'
POWER_SIM_ON_RESP='\x0B'
POWER_SIM_ON_RESP='\x0C'
RESET_SIM_REQ='\x0D'
RESET_SIM_RESP='\x0E'
TRANSFER_CARD_READER_STATUS_REQ='\x0F'
TRANSFER_CARD_READER_STATUS_REQ='\x10'
STATUS_IND='\x11'
ERROR_RESP='\x12'
SET_TRANSPORT_PROTOCOL_REQ='\x13'
SET_TRANSPORT_PROTOCOL_RESP='\x14'

#Params
MaxMsgSize='\x00'
ConnectionStatus='\x01'
ResultCode='\x02'
DisconnectionType='\x03'
CommandAPDU='\x04'
CommandAPDU7816='\x10'
ResponseAPDU='\x05'
ATR='\x06'
CardReaderStatus='\x07'
StatusChange='\x08'
TransportProtocol='\x09'

RESERVED='\x00'
RESERVED2='\x00\x00'

class Connect_Req():
    LEN='\x00\xff'
    def __init__(self):
        self.header=CONNECT_REQ+'\x01'+RESERVED2
        self.payload=MaxMsgSize+RESERVED+'\x00\x02'+self.LEN

    def changeLen(self,newLen):
        if(newLen>65535):
            print "Length too high"
            return
        firstDigit=newLen/256
        secDigit=newLen%256
        self.LEN=hex(firstDigit)+hex(secDigit)
        self.LEN=self.LEN.replace('0x0','0x00')
        self.LEN=self.LEN.replace('0x','\\x')

    def get(self):
        return self.header+self.payload

class APDU_Req():
    def __init__(self):
        self.header=TRANSFER_APDU_REQ+'\x01'+RESERVED2
        self.payload=CommandAPDU+RESERVED+'\x02'+'\x00\x00'

    def get(self):
        return self.header+self.payload

class ATR_Req():
    def __init__(self):
        self.header=TRANSFER_ATR_REQ+'\x00'+RESERVED2

    def get(self):
        return self.header
