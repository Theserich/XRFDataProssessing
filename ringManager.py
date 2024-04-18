import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand
from copy import copy
from dataManager import *
import os

class ringwithClass:
    def __init__(self,sampleName, folder='data',ringfolder='ringdata',redraw=False):
        df = load_data(sampleName,folder=folder)
        self.sampleName = sampleName
        self.path = join(folder,sampleName, ringfolder)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.ringfile = join(folder,sampleName, ringfolder,sampleName+'.txt')
        if os.path.isfile(self.ringfile) and redraw==False:
            self.rings = np.loadtxt(self.ringfile)
        else:
            self.image = copy(df['Image'])
            self.rings = []
            self.initialize_plot()



    def initialize_plot(self):
        self.fig,self.ax = plt.subplots()
        img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)
        plt.gcf().canvas.mpl_connect('button_press_event', self.onclick)
        plt.gcf().canvas.mpl_connect('key_press_event', self.onkeypress)
        plt.show()

    def onclick(self,event):
        if event.inaxes:
            x = int(round(event.xdata, 0))
            self.rings.append(x)
            y = round(event.ydata, 0)
            self.ax.axvline(x,ls='-',color='C1')
            self.fig.canvas.draw()

    def onkeypress(self,event):
        if event.key == 'enter':
            self.rings = np.array(self.rings)
            sortind = np.argsort(self.rings)
            self.rings = self.rings[sortind]
            #self.rings = list(self.rings)
            np.savetxt(self.ringfile,self.rings)
            plt.close()
        if event.key == 'backspace':
            try:
                del self.rings[-1]
            except:
                pass
            self.ax.clear()
            img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)
            for ring in self.rings:
                self.ax.axvline(ring,ls='-',color='C1')
            self.fig.canvas.draw()









