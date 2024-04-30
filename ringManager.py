import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand
from copy import copy
from dataManager import *
import os

class ringwithClass:
    def __init__(self,sampleName, folder='data',ringfolder='ringdataadvanced',imagekey = 'Image',redraw=False):
        self.df = load_data(sampleName,folder=folder)
        self.image = copy(self.df[imagekey])
        self.sampleName = sampleName
        self.path = join(folder,sampleName, ringfolder)
        self.firstclick = True
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.ringfile = join(folder,sampleName, ringfolder,sampleName+'.txt')
        self.yearfile = join(folder,sampleName, ringfolder,'FirstYear'+'.txt')
        self.points = []
        if os.path.isfile(self.yearfile):
            self.firstyear = np.loadtxt(self.yearfile)
        else:
            self.getYear()
        if os.path.isfile(self.ringfile) and redraw==False:
            self.rings = np.loadtxt(self.ringfile)
        else:

            self.yinds = np.arange(len(self.image))
            self.rings = []
            self.initialize_plot()

    @timer
    def calc_rings(self,df):
        types = ['mean','median','max','min']
        self.ringdf = {}
        self.years = np.arange(self.firstyear,self.firstyear+len(self.rings))

        for element in df:
            self.ringdf[element] = {}
            for type in types:
                self.ringdf[element][type] = np.full(len(self.rings),np.nan)
            ring0 = np.zeros(len(self.image))

            for i,ring in enumerate(self.rings):
                index = 0
                lendat = 0
                for d in ring-ring0:
                    lendat += max(0,int(d))
                ringdata = np.full(lendat,np.nan)
                for j, ind in enumerate(ring):
                    data = df[element][j][int(ring0[j]):int(ind)]
                    for dat in data:
                        ringdata[index] = dat
                        index+=1
                ring0=ring
                for type in types:
                    if type == 'mean':
                        self.ringdf[element][type][i] = np.nanmean(ringdata)
                    elif type == 'median':
                        self.ringdf[element][type][i] = np.nanmedian(ringdata)
                    elif type == 'min':
                        self.ringdf[element][type][i] = np.nanmin(ringdata)
                    elif type == 'max':
                        self.ringdf[element][type][i] = np.nanmax(ringdata)
    def getYear(self):
        print('Enter year of fist ring:')
        year = input()
        try:
            self.firstyear = int(year)
        except:
            print('Only integers are allowed:')
            self.getYear()
        np.savetxt(self.yearfile, [self.firstyear])


    def initialize_plot(self):
        self.fig,self.ax = plt.subplots()
        img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)
        plt.gcf().canvas.mpl_connect('button_press_event', self.onclick)
        plt.gcf().canvas.mpl_connect('key_press_event', self.onkeypress)
        plt.show()

    def onclick(self,event):
        if self.fig.canvas.widgetlock.locked():
            return
        if event.inaxes:
            x = event.xdata
            y = event.ydata
            #check if this is the first click
            if self.firstclick:
                self.x1 = x
                self.y1 = y
                self.ax.plot(x,y,'x',color='C1')
                self.fig.canvas.draw()
                self.firstclick=False
            else:
                self.x2 = x
                self.y2 = y
                if self.y1 == self.y2:
                    return
                a = (self.x2-self.x1)/(self.y2-self.y1)
                b = self.x1-a*self.y1
                line = lambda y: a*y + b
                indexes = np.floor(line(self.yinds))
                self.rings.append(indexes)
                self.points.append([(self.x1,self.y1),(self.x2,self.y2)])
                self.ax.plot(x, y, 'x', color='C1')
                #self.ax.plot(indexes,self.yinds, color='C1')
                self.ax.axline((self.x1,self.y1),(self.x2,self.y2),color='C1')
                self.fig.canvas.draw()
                self.firstclick = True


    def onkeypress(self,event):
        if event.key == 'enter':
            self.rings = np.array(self.rings)
            ringind = [ring[0] for ring in self.rings]
            sortind = np.argsort(ringind)
            self.rings = self.rings[sortind]
            self.rings = list(self.rings)
            np.savetxt(self.ringfile,self.rings)
            plt.close()




        if event.key == 'backspace':
            try:
                del self.rings[-1]
            except:
                pass
            try:
                del self.points[-1]
            except:
                pass
            self.ax.clear()
            img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)

            for point in self.points:
                self.ax.plot(point[0][0], point[0][1], 'x', color='C1')
                self.ax.plot(point[1][0], point[1][1], 'x', color='C1')
                self.ax.axline(point[0],point[1],color='C1')
            self.fig.canvas.draw()









