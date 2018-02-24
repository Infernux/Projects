#!/usr/bin/python
from Tkinter import *
#from Tkinter import Listbox
from ttk import Frame, Button, Style

import dbus

import sys
from final import MAP
from conversation import Conversation, SENT, RECEIVED

class UI(Frame):
    def __init__(self, parent, msg):
        Frame.__init__(self,parent)

        self.parent = parent
        self.msg = msg
        self.initUI()

    def initUI(self):
        self.parent.title("Dat title")
        #self.style = Style()
        #self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        button = Button(self, text="Quit", command=self.quit)
        button.grid(row=4, column=1)

        button = Button(self, text="New Conversation")
        button.grid(row=0, column=0)
        button.bind('<Button-1>', self.onClickNewConv)

        self.listConv = Listbox(self)
        self.listConv.grid(row=1,column=0,rowspan=3,sticky=W+S+N+E)
        self.listConv.bind('<<ListboxSelect>>',self.onClickConv)

        self.text = Text(self)
        self.text.config(takefocus=False,wrap=WORD)
        self.text.tag_configure("red", background="#6666FF", foreground="#FFFFFF")
        self.text.tag_configure("blue", background="#0000FF", foreground="#FFFFFF")
        self.text.insert(END,"Retest\n")
        self.text.grid(row=0,column=1,rowspan=2,sticky=W+E+N+S)
        self.text.config(state=DISABLED)

        self.entry = Entry(self)
        self.entry.grid(row=3,column=1,sticky=W+E)
        self.entry.bind('<Return>', self.onReturnPressed)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

    def createNewConversation(self,name,number):
        i=0
        found=False
        name=name if len(name)!=0 else str(number)
        for conv in conversations:
            if conv.name==name:
                found=True
                break
            i=i+1

        if not found:
            conv = Conversation(name,str(number),)
            conversations.append(conv)
            self.listConv.insert(END,name)
            self.listConv.itemconfig(END,foreground="#FF00FF")

        #self.listConv.selection_set(i,i)
        self.listConv.focus_force()
        self.listConv.activate(i)

        return conversations[i]

    def convertMsg(self, msg):
        finalMsg=""
        for c in msg:
            finalMsg+=c if ord(c)<65536 else '(smiley)'
        return finalMsg

    def onNewMsg(self, infos):
        #bold out on received message
        self.text.config(state=NORMAL)

        senderName=infos[1] if len(infos[1]) else str(infos[3])
        found=False

        infos[0]=self.convertMsg(infos[0])

        i=0
        for conv in conversations:
            if conv.name==senderName:
                # if selected -> add message to conversation
                # otherwise bold out the text (maybe add a unread counter)
                conv.msg.append([RECEIVED,infos[0]+'\n'])
                found=True
                try:
                    if senderName==self.listConv.selection_get():
                        self.text.mark_set("matchStart",END)
                        self.text.insert(END,infos[0]+'\n',("red"))
                        self.text.mark_set("matchEnd",END)
                    else:
                        #bold out
                        self.listConv.itemconfig(i,foreground="#FF00FF")
                except:
                    pass
                break
            i=i+1

        if not found:
            conv=self.createNewConversation(senderName,infos[3])
            conv.msg.append([RECEIVED,infos[0]+'\n'])

        self.text.config(state=DISABLED)
        self.text.see(END)

    def onClickNumber(self):
        number  = self.listNumbers.selection_get().split(':')[1]
        self.createNewConversation(self.activeName,number) #easily improvable
        self.top.destroy()

    def onClickContact(self, event):
        self.activeName=self.listContacts.selection_get()
        contact=pb[self.listContacts.curselection()[0]]
        #for contact in pb :
        #    if str(contact['FN'][0])==self.activeName:
        self.listNumbers.delete(0,END)
        for num in contact['TEL']:
            self.listNumbers.insert(END,num[0]+':'+num[1])

    def onClickNewConv(self, event):
        self.top = Toplevel()
        self.listContacts = Listbox(self.top)
        self.listNumbers = Listbox(self.top)
        for contact in pb:
            self.listContacts.insert(END,contact['FN'][0])

        self.listContacts.grid(row=0,column=0,sticky=W+S+N+E)
        self.listNumbers.grid(row=0,column=1,sticky=W+S+N+E)
        self.listContacts.bind('<<ListboxSelect>>',self.onClickContact)

        button = Button(self.top, text="Select",command=self.onClickNumber)
        button.grid(row=1,column=0)
        button = Button(self.top, text="Dismiss",command=self.top.destroy)
        button.grid(row=1,column=1)

        self.top.columnconfigure(0, weight=1)
        self.top.columnconfigure(1, weight=1)
        self.top.rowconfigure(0, weight=1)

    def onClickConv(self, event):
        #1)get person name
        #2)get conversation
        #3)iterate and add text to self.text

        #print self.listConv.get(0)

        self.text.config(state=NORMAL)

        self.activeConversationIndex= self.listConv.curselection()[0]
        activeConversation          = conversations[self.activeConversationIndex]
        self.currentNum             = activeConversation.num

        self.listConv.itemconfig(self.activeConversationIndex,foreground="#000000")

        self.text.delete(1.0,END) #clear
        for msg in activeConversation.msg:
            self.text.insert(END,msg[1],"blue" if msg[0]==SENT else "red")

        self.text.config(state=DISABLED)
        self.text.see(END)

    def onReturnPressed(self, event):
        #sendSMS
        msgContent = self.entry.get()
        self.text.config(state=NORMAL)

        self.text.mark_set("matchStart",END)
        self.text.insert(END,msgContent+'\n',("blue"))
        self.text.mark_set("matchEnd",END)

        conversations[self.activeConversationIndex].msg.append([SENT,msgContent+'\n'])

        self.entry.delete(0,END)
        self.text.see(END)

        self.text.config(state=DISABLED)

        message.sendSMS(self.currentNum, msgContent)
    
def handler(msg):
    infos=message.unpackMsg(msg)
    app.onNewMsg(infos)

def compareFunc(a,b):
    return 1 if a['FN']>b['FN'] else -1
    #return 0

root = Tk()

host = sys.argv[1]

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_signal_receiver(handler, dbus_interface="com.mrnux.bluetoothSMS",
    signal_name="newSMS")

conversations=[]

message=MAP(host)
app = UI(root,message)
app.currentNum='0'

pb = message.initPhonebook()
pb.sort(compareFunc)

root.mainloop()
