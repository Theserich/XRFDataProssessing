import numpy as np
from os.path import join
import pathlib
from time import time
from scipy.signal import savgol_filter, find_peaks


def timer(func):
    def wrapper(*args, **kwargs):
        start = time()
        rtrn = func(*args, **kwargs)
        end = time()

        print("%r %.3f s" % (func.__name__, end - start))
        return rtrn
    return wrapper

def load_data(samplename, folder='data',rotate=False):
    file = join(folder, samplename)
    files = list(pathlib.Path(file).glob('*.txt'))
    df = {}
    for filename in files:
        ISO = str(filename).strip('.txt').strip(' ').split('-')[1].strip(' ')
        if ISO == 'Image':
            pass
        data = []
        with open(filename) as fp:
            for i, line in enumerate(fp):
                if i == 0:
                    infos = line
                else:
                    dat = line
                    if len(dat) == 1:
                        continue
                    dat = dat.strip('\n').split(',')
                    dat = [float(i) for i in dat]
                    data.append(dat)
        data = np.array(data)
        if rotate:
            data = data.transpose()
        df[ISO] = data
    return df

def normalizedata(df):

    for key in df:
        maximum = df[key].max()
        minimum = df[key].min()
        totrange = maximum - minimum
        df[key] = (df[key] - minimum) / totrange
    return df

def zscore(df):
    results = {}
    for key in df.keys():
        meadian = np.nanmedian(df[key])
        stddev = np.nanstd(df[key])
        results[key] = (df[key]-meadian)/stddev
    return results

def smoothing(df,a,b):
    for key in df:
        for i, dat in enumerate(df[key]):
            df[key][i] = savgol_filter(dat,a,b)
    return df

def getmedian(df):
    mediandf = {}
    for key in df:
        data = df[key]
        data = data.transpose()
        mediandf[key] = np.full(len(data),np.nan)
        for i,d in enumerate(data):
            med = np.median(d)
            mediandf[key][i] = med
    mediandf['dImage'] = mediandf['Image']
    mediandf['dImage'] = -np.diff(mediandf['dImage'])
    return mediandf

def getmedianofLines(df,range=(4,10)):
    mediandf = {}
    for key in df:
        data = df[key]
        data = data.transpose()
        mediandf[key] = np.full(len(data),np.nan)
        for i,d in enumerate(data):
            med = np.median(d[range[0]:range[1]])
            mediandf[key][i] = med
    mediandf['dImage'] = mediandf['Image']
    mediandf['dImage'] = -np.diff(mediandf['dImage'])
    return mediandf


def getAnnualDatadf(df,peaks,year0=2000,type='min'):
    years = []
    annualdf = {}
    for key in df:
        annualdf[key] = []
        annualdf[key+'xerr'] = []
        annualdf[key+'yerr'] = []
    t0 = 0
    for i,p in enumerate(peaks):
        years.append(t0+(p-t0)/2)
        inttime = int(p)-t0
        for key in df:
            if type == 'max':
                ringdata = np.nanmax(df[key][t0:t0+inttime])
            elif type == 'min':
                ringdata = np.nanmin(df[key][t0:t0 + inttime])
            elif type == 'integral':
                ringdata = sum(df[key][t0:t0 + inttime]) / inttime
            xrange = inttime / 2
            annualdf[key].append(ringdata)
            annualdf[key+'xerr'].append(xrange)
            annualdf[key+'yerr'].append(0)
        t0 = int(p)
    for key in df:
        annualdf[key] = np.array(annualdf[key])
        annualdf[key + 'xerr'] = np.array(annualdf[key+'xerr'])
        annualdf[key + 'yerr'] = np.array(annualdf[key+'yerr'])
    annualdf['Year'] = np.array(years)
    return annualdf

def getAnnualData(data,rings,year0=2000,type='min'):
    x = []
    xerr = []
    y = []
    yerr = []
    t0=0
    for i,p in enumerate(rings):
        x.append(t0+(p-t0)/2)
        inttime = int(p)-t0
        try:
            dat = data[t0:t0+inttime]
            dat = dat[dat != np.inf]
            dat = dat[dat != -np.inf]
            if type == 'max':
                ringdata = np.nanmax(dat)
            elif type == 'min':
                ringdata = np.nanmin(dat)
            elif type == 'integral':
                ringdata = np.nansum(dat) / len(dat)
        except:
            ringdata = np.nan
        xrange = inttime / 2
        y.append(ringdata)
        xerr.append(xrange)
        yerr.append(0)
        t0 = int(p)
    y = np.array(y)
    xerr = np.array(xerr)
    yerr = np.array(yerr)
    x = np.array(x)
    return x,xerr,y,yerr






