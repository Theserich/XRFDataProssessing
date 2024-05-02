import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand
from copy import copy
from dataManager import *
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from plotFunctions import setPlotParams
import os

class ringwithClass:
    def __init__(self, sampleName, dataPath='data', metadataPath='metadata', redo=False):
        self.sampleName = sampleName
        self.dataPath = dataPath
        self.metaPath = metadataPath
        self.rawdf = load_data(sampleName, folder=dataPath)
        self.path = join(dataPath, sampleName, metadataPath)
        self.figpath = join(dataPath, sampleName, 'Figures Raster')
        self.redo = redo
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.figpath):
            os.makedirs(self.figpath)

        self.fullimage = self.rawdf['Image']
        self.trimData()
        self.outlierElement = 'Si'
        self.maskOutliers()
        self.getRingData()
        self.calc_rings()


    def trimData(self):
        trimfile = 'trimindexes'
        #trimfile = join(self.dataPath, self.sampleName, self.metaPath, self.sampleName + 'trimindexes.txt')
        if os.path.isfile(join(self.path,trimfile+'.json')) and self.redo == False:
            savedf = read_settings(trimfile,path=self.path)
            self.yInd0 = savedf['yInd0']
            self.yInd1 = savedf['yInd1']
        else:
            self.savebool = False
            self.yInd0 = 0
            self.yInd1 = None
            self.firstclick = True
            self.fig, self.ax = plt.subplots()
            self.ax.imshow(self.fullimage, aspect='auto', cmap=plt.cm.gist_yarg)
            plt.gcf().canvas.mpl_connect('button_press_event', self.trimClick)
            plt.gcf().canvas.mpl_connect('key_press_event', self.trimKeyEvent)
            self.ax.set_title('Select slice of the image')
            plt.show()
            if self.savebool:
                savedf = {'yInd0':self.yInd0,'yInd1':self.yInd1}
                write_settings(savedf,file_name=trimfile,path=self.path)
        self.df = {}
        for element in self.rawdf:
            self.df[element] = copy(self.rawdf[element][self.yInd0:self.yInd1])
        self.image = self.df['Image']

    def trimKeyEvent(self, event):
        if event.key == 'enter':
            self.savebool = True
            plt.close()
        if event.key == 'backspace':
            self.ax.clear()
            self.ax.imshow(self.fullimage, aspect='auto', cmap=plt.cm.gist_yarg)
            if self.yInd1 is None:
                self.firstclick = True
                self.yInd0 = 0
            else:
                self.yInd1 = None
                self.ax.axhline(self.yInd0)
            self.ax.set_title('Select slice of the image')
            self.fig.canvas.draw()
    def trimClick(self, event):
        if self.fig.canvas.widgetlock.locked():
            return
        if event.inaxes:
            y = event.ydata
            # check if this is the first click
            if self.firstclick:
                self.yInd0 = int(y)
                self.ax.axhline(self.yInd0)
                self.fig.canvas.draw()
                self.firstclick = False
            else:
                if self.yInd1 is None:
                    if self.yInd0 == int(y):
                        return
                    self.yInd1 = int(y)
                    self.ax.axhline(self.yInd1)
                    if self.yInd0 > self.yInd1:
                        y0 = self.yInd0
                        self.yInd0 = self.yInd1
                        self.yInd1 = y0
                else:
                    if self.yInd0 == int(y):
                        return
                    self.yInd1 = int(y)
                    self.ax.clear()
                    self.ax.imshow(self.df[self.outlierElement], aspect='auto', cmap=plt.cm.jet)
                    self.ax.set_title('Click the rings')
                    self.ax.axhline(self.yInd0)
                    self.ax.axhline(self.yInd1)
                self.fig.canvas.draw()

    def maskOutliers(self):
        maskfile = 'maskindexes'
        if os.path.isfile(join(self.path,maskfile+'.json')) and self.redo == False:
            savedf = read_settings(maskfile,path=self.path)
            self.maskindexes = savedf['maskindexes']
            self.maskpoints = savedf['maskpoints']
        else:
            self.savebool = False
            self.maskpoints = []
            self.maskindexes = []
            self.firstclick = True
            self.fig, self.ax = plt.subplots()
            self.ax.imshow(self.df[self.outlierElement], aspect='auto', cmap=plt.cm.jet)
            plt.gcf().canvas.mpl_connect('button_press_event', self.maskClick)
            plt.gcf().canvas.mpl_connect('key_press_event', self.maskKeyEvent)
            self.ax.set_title('Mark where you want to ignore')
            plt.show()
            if self.savebool:
                savedf = {'maskpoints':self.maskpoints,'maskindexes':self.maskindexes}
                write_settings(savedf,file_name=maskfile,path=self.path)
        for element in self.df:
            if element == 'Image':
                continue
            for ind in self.maskindexes:
                self.df[element][ind[0],ind[1]] = np.nan
        self.image = self.df['Image']

    def maskClick(self, event):
        if self.fig.canvas.widgetlock.locked():
            return
        if event.inaxes:
            x = event.xdata
            y = event.ydata
            # check if this is the first click
            if self.firstclick:
                self.x1 = int(round(x,0))
                self.y1 = int(round(y,0))
                self.ax.plot(self.x1, self.y1, 'x', color='C1')
                self.fig.canvas.draw()
                self.firstclick = False
            else:
                self.x2 = int(round(x,0))
                self.y2 = int(round(y,0))
                if self.y1 == self.y2 or self.x1 == self.x2 :
                    return
                self.maskpoints.append([(self.x1, self.y1), (self.x2, self.y2)])
                xindexes = np.arange(min(self.x1,self.x2),max(self.x1,self.x2))
                yindexes = np.arange(min(self.y1,self.y2),max(self.y1,self.y2))
                for x in xindexes:
                    for y in yindexes:
                        self.maskindexes.append((int(y),int(x)))
                self.ax.plot(self.x2, self.y2, 'x', color='C1')
                rect = Rectangle((min(self.x1,self.x2), min(self.y1,self.y2)), abs(self.x1-self.x2), abs(self.y1-self.y2), linewidth=1, edgecolor='r', facecolor='none')
                self.ax.add_patch(rect)
                self.fig.canvas.draw()
                self.firstclick = True

    def maskKeyEvent(self, event):
        if event.key == 'enter':
            self.savebool = True
            plt.close()
        if event.key == 'backspace':
            try:
                del self.maskpoints[-1]
            except:
                pass
            try:
                del self.maskindexes[-1]
            except:
                pass
            self.ax.clear()
            self.ax.imshow(self.df[self.outlierElement], aspect='auto', cmap=plt.cm.jet)
            for points in self.maskpoints:
                (self.x1, self.y1), (self.x2, self.y2) = points
                rect = Rectangle((min(self.x1, self.x2), min(self.y1, self.y2)), abs(self.x1 - self.x2),
                                 abs(self.y1 - self.y2), linewidth=1, edgecolor='r', facecolor='none')
                self.ax.plot(self.x1, self.y1, 'x', color='C1')
                self.ax.plot(self.x2, self.y2, 'x', color='C1')
                self.ax.add_patch(rect)
            self.firstclick = True
            self.ax.set_title('Mark where you want to ignore')
            self.fig.canvas.draw()


    def getRingData(self):
        ringfile = 'ringindexes'
        if os.path.isfile(join(self.path, ringfile + '.json')) and self.redo == False:
            savedf = read_settings(ringfile, path=self.path)
            self.ringindexes = savedf['ringindexes']
            self.ringpoints = savedf['ringpoints']
            self.rings = savedf['rings']
            self.firstyear = savedf['firstyear']
        else:
            self.getYearInput()
            self.savebool = False
            self.firstclick = True
            self.yinds = np.arange(len(self.image))
            self.rings = []
            self.ringpoints = []
            self.fig, self.ax = plt.subplots()
            img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)
            plt.gcf().canvas.mpl_connect('button_press_event', self.ringClick)
            plt.gcf().canvas.mpl_connect('key_press_event', self.ringKeyEvent)
            self.ax.set_title('Click the rings')
            plt.show()
            ring0 = np.zeros(len(self.image))
            self.ringindexes = []
            for i,ring in enumerate(self.rings):
                self.ringindexes.append([])
                for yind in np.arange(len(self.image)):
                    xinds = np.arange(ring0[yind],ring[yind])
                    for xind in xinds:
                        self.ringindexes[i].append((int(yind),int(xind)))
                ring0=ring
            self.rings = np.array(self.rings)
            ringind = [ring[0] for ring in self.rings]
            sortind = np.argsort(ringind)
            ringsave = []
            self.rings = self.rings[sortind]
            for i, ring in enumerate(self.rings):
                listring = ring.tolist()
                ringsave.append(listring)
            self.rings = ringsave
            if self.savebool:
                #print(self.rings)
                savedf = {'rings':self.rings,'ringindexes':self.ringindexes,'ringpoints':self.ringpoints,'firstyear':self.firstyear}
                write_settings(savedf,file_name=ringfile,path=self.path)




    @timer
    def calc_rings(self):
        self.years = np.arange(self.firstyear, self.firstyear + len(self.rings))
        self.ringinds = []
        self.ringdata = {}
        ring0 = np.zeros(len(self.image))
        for ring in self.rings:
            meanind = sum(ring+ring0)/len(self.image)/2
            self.ringinds.append(meanind)
            ring0=ring
        self.ringdf = {}
        types = ['mean', 'median', 'max', 'min','std','std2']
        for element in self.df:
            self.ringdf[element] = {}
            self.ringdata[element] = []
            for type in types:
                self.ringdf[element][type] = np.full(len(self.rings), np.nan)
        for element in self.df:
            for j,ringinds in enumerate(self.ringindexes):
                lendat = len(ringinds)
                ringdata = np.full(lendat, np.nan)
                for i,index in enumerate(ringinds):
                    ringdata[i] = self.df[element][index[0],index[1]]
                ringdata = ringdata[~np.isnan(ringdata)]
                self.ringdata[element].append(ringdata)
                for type in types:

                    try:
                        if type == 'mean':
                            self.ringdf[element][type][j] = np.nanmean(ringdata)

                        elif type == 'median':
                            self.ringdf[element][type][j] = np.nanmedian(ringdata)
                        elif type == 'min':
                            self.ringdf[element][type][j] = np.nanmin(ringdata)
                        elif type == 'max':
                            self.ringdf[element][type][j] = np.nanmax(ringdata)
                        elif type == 'std':
                            self.ringdf[element][type][j] = np.nanstd(ringdata)
                        elif type == 'std2':
                            self.ringdf[element][type][j] = np.nanstd(ringdata)/len(ringdata)**0.5
                    except Exception as e:
                        pass
                        #print(e)
                        #print(ringdata)


    def getYearInput(self):
        print('Enter year of fist ring:')
        year = input()
        try:
            self.firstyear = int(year)
        except:
            print('Only integers are allowed:')
            self.getYearInput()

    def initialize_plot(self):
        self.fig,self.ax = plt.subplots()
        img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)
        plt.gcf().canvas.mpl_connect('button_press_event', self.ringClick)
        plt.gcf().canvas.mpl_connect('key_press_event', self.ringKeyEvent)
        plt.show()

    def ringClick(self, event):
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
                self.ringpoints.append([(self.x1,self.y1),(self.x2,self.y2)])
                self.ax.plot(x, y, 'x', color='C1')
                #self.ax.plot(indexes,self.yinds, color='C1')
                self.ax.axline((self.x1,self.y1),(self.x2,self.y2),color='C1')
                self.fig.canvas.draw()
                self.firstclick = True


    def ringKeyEvent(self, event):
        if event.key == 'enter':

            self.savebool = True
            plt.close()
        if event.key == 'backspace':
            try:
                del self.rings[-1]
            except:
                pass
            try:
                del self.ringpoints[-1]
            except:
                pass
            self.ax.clear()
            img = self.ax.imshow(self.image, aspect='auto', cmap=plt.cm.gist_yarg)

            for point in self.ringpoints:
                self.ax.plot(point[0][0], point[0][1], 'x', color='C1')
                self.ax.plot(point[1][0], point[1][1], 'x', color='C1')
                self.ax.axline(point[0],point[1],color='C1')
            self.fig.canvas.draw()

    def showDatapreparation(self,element='Si',block=True):
        setPlotParams(12, figsize=(20, 12))
        fig, ax = plt.subplots()
        ax.imshow(self.rawdf[element], aspect='auto', cmap=plt.cm.gist_yarg)
        ylim = ax.get_ylim()
        xlim = ax.get_xlim()
        # show trimmed region
        ax.axhspan(ymin=-1, ymax=self.yInd0, alpha=0.5)
        if self.yInd1 is not None:
            ax.axhspan(ymin=self.yInd1 - 1, ymax=len(self.fullimage), alpha=0.5)
        # show masked areas
        for points in self.maskpoints:
            (self.x1, self.y1), (self.x2, self.y2) = points
            self.y1 += self.yInd0
            self.y2 += self.yInd0
            rect = Rectangle((min(self.x1, self.x2), min(self.y1, self.y2)), abs(self.x1 - self.x2),
                             abs(self.y1 - self.y2), linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        # show rings
        yarr = np.arange(len(self.image)) + self.yInd0
        for ring in self.rings:
            ax.plot(ring, yarr, color='C1')

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title('Data preparation overview')
        plt.savefig(join(self.figpath,'1_DataOverview.png'))
        plt.show(block=block)
    def generateAllElementFigs(self):
        setPlotParams(12,figsize=(20,5))
        for element in self.df:
            fig, ax = plt.subplots()
            ax.imshow(self.df[element], aspect='auto', cmap=plt.cm.jet)
            ax.set_title(element)
            plt.savefig(join(self.figpath,f'{element}.png'))
            plt.close()

    def plotAnnualdata(self,elements=[],types=['mean','median','min','max']):
        setPlotParams(12, figsize=(20, 8))
        Nplots = len(elements)
        fig, ax = plt.subplots(len(elements))
        if Nplots == 1:
            ax = [ax]

        for i,element in enumerate(elements):
            if element in self.df:
                ax[i].set_ylabel(element)
                for type in types:
                    ax[i].plot(self.years,self.ringdf[element][type], label=type)
                ax[i].legend()
        plt.subplots_adjust(hspace=0)
        #plt.savefig(join(self.figpath, f'{element}.png'))
        plt.show()

    def plotAnnualboxplot(self,elements=[],types=['mean','median','min','max']):
        setPlotParams(12, figsize=(20, 8))
        Nplots = len(elements)
        fig, ax = plt.subplots(len(elements))
        if Nplots == 1:
            ax = [ax]
        for i,element in enumerate(elements):
            if element in self.df:
                ax[i].set_ylabel(element)
                ax[i].boxplot(self.ringdata[element],positions=self.years)
                #ax[i].legend()
        plt.subplots_adjust(hspace=0)
        #plt.savefig(join(self.figpath, f'{element}.png'))
        plt.show()



    def plotringdata(self,elements=[]):
        mediandf = getmedian(self.df)
        setPlotParams(12, figsize=(20, 8))
        Nplots = len(elements)
        Nplots = len(elements)
        fig, ax = plt.subplots(len(elements))
        if Nplots == 1:
            ax = [ax]

        for i,element in enumerate(elements):
            imax = ax[i]
            imax.set_yticks([])
            lineax = ax[i].twinx()
            imax.imshow(self.df[element], aspect='auto', cmap=plt.cm.jet)
            if element in self.df:
                lineax.plot(mediandf[element])
                lineax.set_ylabel(element)
                #for type in types:
                #    lineax.plot(self.ringinds,self.ringdf[element][type], label='Ring '+type)$

                lineax.errorbar(self.ringinds,self.ringdf[element]['median'],yerr=self.ringdf[element]['std'],capsize=3,fmt='x')
                #lineax.errorbar(self.ringinds,self.ringdf[element]['mean'],yerr=self.ringdf[element]['std'],capsize=3,fmt='x')
                #lineax.legend()
        plt.subplots_adjust(hspace=0)
        #plt.savefig(join(self.figpath, f'{element}.png'))
        plt.show()









