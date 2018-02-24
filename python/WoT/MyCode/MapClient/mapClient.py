#!/usr/bin/python
from Tkinter import *
#import ImageTk, Image
from PIL import Image, ImageTk
from ttk import Frame, Button, Style
import socket

import threading

class UI(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)

        self.parent=parent
        self.initUI()
        self.initCode()

    def initUI(self):
        self.parent.title("Title")
        self.canvas = Canvas(self, bd=0)
        #canvas.pack()
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        #self.canvas.create_image(0,0,image=self.photo,anchor=NW,tags="MAP")
        self.canvas.grid(row=0, sticky=W+N+E+S)
        self.bind("<Configure>", self.resize)

        button = Button(self)
        button.bind("<Button-1>", self.changeMapAc)
        button.grid(row=1)

        self.pack(fill=BOTH, expand=1)

    def initCode(self):
        self.activeMapPath='maps/karelia.png'

        self.LT1 = Image.open('types/green/lightTank.png')
        self.LT1 = ImageTk.PhotoImage(self.LT1)
        self.MT1 = Image.open('types/green/mediumTank.png')
        self.MT1 = ImageTk.PhotoImage(self.MT1)
        self.HT1 = Image.open('types/green/heavyTank.png')
        self.HT1 = ImageTk.PhotoImage(self.HT1)
        self.SPG1= Image.open('types/green/spg.png')
        self.SPG1= ImageTk.PhotoImage(self.SPG1)
        self.TD1= Image.open('types/green/at-spg.png')
        self.TD1 = ImageTk.PhotoImage(self.TD1)

        self.LT2 = Image.open('types/red/lightTank.png')
        self.LT2 = ImageTk.PhotoImage(self.LT2)
        self.MT2 = Image.open('types/red/mediumTank.png')
        self.MT2 = ImageTk.PhotoImage(self.MT2)
        self.HT2 = Image.open('types/red/heavyTank.png')
        self.HT2 = ImageTk.PhotoImage(self.HT2)
        self.SPG2= Image.open('types/red/spg.png')
        self.SPG2= ImageTk.PhotoImage(self.SPG2)
        self.TD2= Image.open('types/red/at-spg.png')
        self.TD2 = ImageTk.PhotoImage(self.TD2)

        self.tanks = dict()

    def resize(self,event):
        print event.width
        print event.height
        self.size = event.width if event.width<event.height else event.height
        print self.size
        self.redrawMap(self.activeMapPath,self.size)
        self.scale = self.original.width/self.size
        self.square= self.size/10
        self.xOffset= self.square*5
        self.yOffset= self.square*5

    def redrawMap(self,mapName,size):
        self.original = Image.open(mapName)
        resized = self.original.resize((size, size),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.canvas.delete("MAP") 
        print self.canvas.create_image(0,0,image=self.image,anchor=NW,tags="MAP")

        index = self.canvas.find_withtag("MAP")
        self.canvas.tag_lower(index)

        for tank in self.tanks:
            self.displayOnMap(tank[0],tank[4],tank[1],tank[2],tank[3])

    def changeMapAc(self,event):
        self.changeMap('malinovka')

    def changeMap(self,mapName):
        self.activeMapPath='maps/'+mapName+'.png'
        self.redrawMap('maps/'+mapName+'.png',self.size)

    def displayOnMap(self,playerID,team,tankType,x,y):
        activeType = None
        print tankType
        if(tankType=='lightTank'):
            activeType = self.LT1 if team==0 else self.LT2
        elif(tankType=='mediumTank'):
            activeType = self.MT1 if team==0 else self.MT2
        elif(tankType=='heavyTank'):
            activeType = self.HT1 if team==0 else self.HT2
        elif(tankType=='mediumAT-SPG'):
            activeType = self.TD1 if team==0 else self.TD2
        elif(tankType=='SPG'):
            activeType = self.SPG1 if team==0 else self.SPG2
        elif(tankType=='mediumSPG'):
            activeType = self.SPG1 if team==0 else self.SPG2
            pass

        index = self.canvas.find_withtag('b'+str(playerID))
        actCoords = self.canvas.coords(index)

        if len(index) != 0:
            x=(float(x)-(actCoords[0]/self.size))*(self.size)
            y=(float(y)-(actCoords[1]/self.size))*(self.size)
            self.canvas.move(index,float(x),float(y))
        else:
            x=float(x)*(self.size)
            y=float(y)*(self.size)
            self.canvas.create_image(x,y,image=activeType,anchor=NW,tags='b'+str(playerID))
        #scaling

class InfosEater(threading.Thread):
    def __init__(self,UI):
        super(InfosEater,self).__init__()
        self.ui=UI
        pass

    #((-x, -y), (x, y))
    def extractBoundaries(self, boundaries):
        coords=[]
        boundaries=boundaries[2:-2] #remove surrounding parenthesis
        bounds=boundaries.split('), (').split(',')
        for b in bounds:
            for coord in b.split(','):
                coords.append(int(coord))
        if len(coords)==4:
            self.ui.boundaries=coords
            self.mapWidth=abs(coords[0])+abs(coords[2])
            self.mapHeight=abs(coords[1])+abs(coords[3])
            return 0

        return -1

    def run(self):
        HOST='192.168.0.182'
        PORT=8666
        while True:
            print 'new'
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((HOST,PORT))
            sock.listen(1)
            sockClient,infos=sock.accept()
            print "connected"
            mapInfos=sockClient.recv(1024)
            mi=mapInfos.split(':')
            mapName=mi[0]
            mapSize=mi[1]
            print "map:"+mapName
            print mapSize
            if self.extractBoundaries(mi[1])!=0: #parse and set values in ui
                print "Error while retrieving boundaries : "+mi[1]
                break

            self.ui.changeMap(mapName)
            while True:
                try:
                    data=sockClient.recv(2048)
                    #print data
                    #print '\n'
                except:
                    break
                if not data: break
                try:
                    self.eatInfos(data)
                except Exception,e:
                    print 'fail infos\n'
                    print e
                    pass
            sockClient.close()
            sock.close()

    def removeParenthesis(self,line):
        return line[1:len(line)-1]

    def eatInfos(self,allInfos):
        for tank in allInfos.split(';'):
            if len(tank)==0:
                continue
            print '('+tank+')'
            infos   = tank.split(':')
            playerId= infos[0]
            team    = 0 if infos[1]=='ally' else 1
            tankType= infos[2]
            position= infos[3]
            position= self.removeParenthesis(position)
            #print position
            position= position.split(',')
            name    = infos[4]
            tankX   = float(position[0]) + abs(self.ui.boundaries[0]) #abs(min)
            tankX   /= (self.ui.mapWidth + 10)
            #print 'name:'+name
            #print "Y0:"+str(position[2])
            tankY   = -float(position[2])
            tankY   += abs(self.ui.boundaries[3]) #max
            tankY   /= self.ui.mapWidth 

            #print "Y1:"+str(tankY)
            tankZ   = position[1]
            #print tankType+':'+tankX+':'+tankY
            self.ui.tanks[playerId]=(tankType,tankX,tankY,team)
            self.ui.displayOnMap(playerId,team,tankType,tankX,tankY)
            #for tank in infos:
            #    displayOnMap(tank)
            pass



root = Tk()

app = UI(root)

#thread eatInfos
eatThread=InfosEater(app)
eatThread.start()

root.mainloop()
