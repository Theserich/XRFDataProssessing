from matplotlib import pyplot as plt
from matplotlib.axis import Axis

def setPlotParams(fontsize, figsize=(15, 10), auto=False, lw=1.5, inline=False):
    import matplotlib.pylab as pylab
    params = {'figure.autolayout': auto,
              'legend.fontsize': fontsize,
              'figure.figsize': figsize,
              'axes.labelsize': fontsize,
              'axes.titlesize': fontsize,
              'axes.linewidth': lw,
              'xtick.labelsize': fontsize,
              'xtick.major.size': 10,
              'xtick.minor.size': 5,
              'ytick.major.size': 10,
              'ytick.minor.size': 5,
              'xtick.major.width': lw,
              'xtick.minor.width': lw,
              'ytick.major.width': lw,
              'ytick.minor.width': lw,
              'ytick.labelsize': fontsize}
    if inline:
        params['ytick.direction'] = 'in'
        params['ytick.direction'] = 'in'
    pylab.rcParams.update(params)


def plotElements(df, elements):
    setPlotParams(11,figsize=(15,10))
    fig, ax = plt.subplots(len(elements), sharex=True)
    for i, element in enumerate(elements):
        ax[i].set_title(element)
        ax[i].imshow(df[element], aspect='auto')
    plt.show()


def linePlot(df, elements, index=0):
    setPlotParams(11, figsize=(15, 10))
    fig, ax = plt.subplots(len(elements), sharex=True)
    for i, element in enumerate(elements):
        ax[i].plot(df[element][index])
        ax[i].set_title(element)
        ax[i].text(0.03, 0.9, element, horizontalalignment='left', verticalalignment='center',
                   transform=ax[i].transAxes)
    plt.subplots_adjust(hspace=0)
    plt.show()


def ratiolinePlot(df, elements,dividelements, index=0):
    setPlotParams(11, figsize=(15, 10))
    fig, ax = plt.subplots(len(elements), sharex=True)
    for i, element in enumerate(elements):
        axis = ax[i].twinx()
        bx = ax[i]
        divelemetn = dividelements[i]
        plotdat = df[element][index]
        label = element
        if divelemetn in df.keys():
            label += f'/{divelemetn}'
            plotdat /= df[divelemetn][index]
        axis.plot(df[element][index])
        axis.text(0.03, 0.9, label, horizontalalignment='left', verticalalignment='center',
                   transform=ax[i].transAxes)
        bx.imshow(df['Image'], aspect='auto', cmap=plt.cm.gist_yarg)
        bx.axhline(index,ls='--',color='k')

    plt.subplots_adjust(hspace=0)
    plt.show()

def ratiomedianlinePlot(df, elements,dividelements,imdf):
    setPlotParams(11, figsize=(15, 10))
    fig, ax = plt.subplots(len(elements), sharex=True)
    for i, element in enumerate(elements):
        axis = ax[i].twinx()
        bx = ax[i]
        divelemetn = dividelements[i]
        plotdat = df[element]
        label = element
        if divelemetn in df.keys():
            label += f'/{divelemetn}'
            plotdat /= df[divelemetn]
        axis.plot(df[element])
        axis.text(0.03, 0.9, label, horizontalalignment='left', verticalalignment='center',
                   transform=ax[i].transAxes)
        bx.imshow(imdf['Image'], aspect='auto', cmap=plt.cm.gist_yarg)
        #bx.axhline(index,ls='--',color='k')

    plt.subplots_adjust(hspace=0)
    plt.show()

def subplots(nplots):
    fig, firstax = plt.subplots()
    firstax.spines['bottom'].set_visible(False)
    firstax.spines['top'].set_visible(False)
    firstax.spines['left'].set_visible(False)
    firstax.spines['right'].set_visible(False)
    #firstax.set_xticks([])
    firstax.set_yticks([])
    ax = []
    for i in range(nplots):
        ax.append(firstax.twinx())
    return fig, ax,firstax

def separateSubplots(ax,overlap = 0.2,ylabelx = (0.08,0.05),fontsize=18,plotlabels=None,starlabelind = 0):
    if plotlabels is None:
        labels = ['a)', 'b)', 'c)', 'd)','e)','f)','g)','h)','i)','j)','k)']
    else:
        labels = plotlabels
    n = len(ax)
    xlim = ax[0].get_xlim()
    xticks = ax[0].get_xticks()[::1]
    for i, x in enumerate(ax):
        ticks = x.get_yticks()
        dticks = ticks[1]-ticks[0]
        maxy = max(ticks)
        miny = min(ticks)
        dy = maxy - miny
        nonscaletotheight = n * dy
        totheight = nonscaletotheight - (n - 1) * overlap * dy
        top = maxy + i * (1 - overlap) * dy
        bottom = top - totheight
        ylabelheight = (miny - bottom+dy/2) / totheight
        labelheight = (miny+0.8*dy - bottom) / totheight
        if i % 2 == 0:
            x.yaxis.tick_left()
            x.spines['left'].set_bounds((ticks[1], ticks[-2]))
            x.spines['right'].set_visible(False)
            Axis.set_label_coords(x.yaxis,-ylabelx[0],ylabelheight)
        else:
            x.yaxis.tick_right()
            #x.yaxis.ylabel_right()
            #x.axvline(xlim[1], ymin=(miny - bottom+dticks) / totheight, ymax=(maxy - bottom-dticks) / totheight, color='k',
            #          linewidth=3, solid_capstyle="butt")
            x.spines['right'].set_bounds((ticks[1], ticks[-2]))
            x.spines['left'].set_visible(False)
            Axis.set_label_coords(x.yaxis,1+ylabelx[1],ylabelheight)
        x.set_ylim(top=top, bottom=bottom)
        x.set_yticks(ticks[1:-1])
        #x.set_ylabel('')
        x.spines['top'].set_visible(False)
        try:
            x.text(0.03, labelheight, labels[i+starlabelind], fontsize=fontsize, horizontalalignment='left', verticalalignment='center',transform=x.transAxes)
        except:
            pass
        if i ==0:
            x.spines['bottom'].set_bounds((xticks[1],xticks[-2]))
        else:
            x.spines['bottom'].set_visible(False)
