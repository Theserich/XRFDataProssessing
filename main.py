from plotFunctions import *
from ringManager import *

rotate = False
redraw=False
samplename = 'LMCKSPL24_1950_1990_400_RES027'
samplename = 'Text Data LMCKSPL24_1950_1990_400_RES027'
samplename = 'Text Data MSH PF918'
samplename = 'Text Data MSH PF931'
samplename = 'Text Data MSH PF953'
samplename = 'Text Data MSH PF957'
samplename = 'Text Data MSH PF984'
samplename = 'Text Data Newport_400DT_05TC_Focused_Thermal'
samplename = 'Text Data WPT 9'
samplename = 'Text Data WPT12'
samplename = 'Text Data WPT301'
samplename = 'Text Data WPT301'
samplename = 'Text Data WPT301'
samplename = 'Text Data WPT301'
samplename = 'Text Data WPT301'


samplename = 'Text Data WPT301'

if samplename in ['Text Data Newport_400DT_05TC_Focused_Thermal']:
    rotate = True


ringsClass = ringwithClass(samplename,redraw=redraw)
rings = ringsClass.rings
df = load_data(samplename,rotate=rotate)
image = copy(df['Image'])

df = smoothing(df,15,3)
#smootheddf = normalizedata(smootheddf)
df = normalizedata(df)
mediandf = getmedian(df)
mediandf = normalizedata(mediandf)
#print(rings)
#Annualdf = getAnnualData(mediandf,rings)







elements = ['Br', 'Cu', 'Mn', 'Nd', 'Ni','Hf','Ni','Zn','Image']#, 'Fe','Co'#negative correlation
#elements = ['Ca','Cl'] #possitive correlation?


#elements = ['Ce','La','Al','Mo','Nd', 'S', 'Si', 'Sr', 'Y'] #no good correlation
#,
#elements = []

#divelements = ['Br', 'Cu', 'Fe', 'Mn', 'Nd', 'Ni','Hf','Ni','Zn','Nd']


divele = 'Image'
divelements = np.full(len(elements),divele)



setPlotParams(11, figsize=(10, 6))


#fig, ax,ax0 = subplots(len(elements))
#labels = []
#colors = [f'C{i}' for i in range(10)]
#for i, element in enumerate(elements):
#    axis = ax[i]
#    divelemetn = divelements[i]
#    try:
#        plotdat = mediandf[element]
#    except:
#        continue
#    label = element
#    if divelemetn in df.keys():
#        label += f'/{divelemetn}'
#        plotdat /= (mediandf[divelemetn]+1)
#    axis.plot(plotdat)
#    x,xerr,ymax,yerr = getAnnualData(plotdat,rings,type='max')
#    axis.errorbar(x, ymax, xerr=xerr, fmt=' ', color='C1', capsize=0)
#    x, xerr, y, yerr = getAnnualData(plotdat,rings, type='min')
#    #axis.errorbar(x, y, xerr=xerr, fmt=' ', color='C2', capsize=0)
#    x, xerr, y, yerr = getAnnualData(plotdat,rings, type='integral')
#    #axis.errorbar(x, y, xerr=xerr, fmt=' ', color='C3', capsize=0)
#    labels.append(label)
#for p in rings:
#    axis.axvline(p,ls=':',color='k')
#separateSubplots(ax,overlap=0.3,ylabelx=(0.08,0.05),plotlabels=labels)
#ax0.imshow(image, aspect='auto', cmap=plt.cm.gist_yarg)#gist_yarg
#ax0.set_title(samplename)



#plt.savefig(f'Plots/{samplename}separated.png')
print(df.keys())
mean = np.zeros(len(rings))
fig,imax = plt.subplots()
ax2 = imax.twinx()
counter = 0
for i, element in enumerate(elements):
    print(element)
    divelemetn = divelements[i]
    try:
        plotdat = mediandf[element]
        counter +=1
    except:
        continue
    label = element
    if divelemetn in df.keys():
        label += f'/{divelemetn}'
        plotdat = 2*plotdat/(mediandf[divelemetn] + 1)
    x, xerr, ymax, yerr = getAnnualData(plotdat, rings, type='max')
    mean += ymax
    #ax2.plot(x[:], ymax[:], label=label)
    ax2.errorbar(x, ymax, xerr=xerr, fmt='o-', capsize=0,label=label)
ax2.set_title(samplename)

ax2.plot(x, mean/counter,label='Mean',lw=5,color='k')
imax.imshow(image, aspect='auto', cmap=plt.cm.gist_yarg)
#plt.savefig(f'Plots/{samplename}maxring.png')

#if divele in df.keys():
#    x, xerr, ymax, yerr = getAnnualData(mediandf[divele], rings, type='max')
#    ax2.errorbar(x, ymax, xerr=xerr, fmt='o-', capsize=0, label=label,color='w')
#    #ax2.plot(mediandf[divele],color='w',label=divele)
ax2.legend()
plt.show()





