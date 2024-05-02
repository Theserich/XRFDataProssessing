from plotFunctions import *
from ringManager import *

rotate = False
redraw = True
#Lake Mackenzie, Tasmania Australia samples. 1961 fire deposited ash but not much more.
samplename = 'Text Data LMCKSPL24_1950_1990_400_RES027'
samplename = 'Text Data LMCKPJB8'
samplename = 'Text Data LMCKPJB7'
samplename = 'Text Data LMCK21B'
samplename = 'Text Data LMCKSPL32'

#Mt St Helens samples, look for 1479 eruption/suppression
samplename = 'Text Data MSH PF918'
samplename = 'Text Data MSH PF931'
samplename = 'Text Data MSH PF953'
samplename = 'Text Data MSH PF957'
samplename = 'Text Data MSH PF965'
samplename = 'Text Data MSH PF977 Full'
samplename = 'Text Data MSH PF984'

#Samples from coastal Oregon, possible tsunami inundation 1700, 1884, 1964. This one sample covers the 1700 decades
samplename = 'Text Data Newport_400DT_05TC_Focused_Thermal' #Requires rotation, collected in 2023
samplename = 'Text Data Newport_PSME_Focus_A'#Requires rotation, collected in 2023
samplename = 'Text Data Newport_PSME_1'#Requires rotation, collected in 2023
samplename = 'Text Data PSME_2024' #This is a rescan run in 2024, no rotation required

#These are samples from WApatki Ruins near sunset crater. Cunset crater erupted sometime between 1050 and 1100CE, suppression in late 1060's
samplename = 'Text Data WPT5B'
samplename = 'Text Data WPT 9'
samplename = 'Text Data WPT9_1051_1093_400_RES013'
samplename = 'Text Data WPT12'
samplename = 'Text Data WPT12C_1060_1110ish_400_RES016_2'
samplename = 'Text Data WPT19b_HiRes' #No Bromine, need to reanalyze all elements
samplename = 'Text Data WPT19b'
samplename = 'Text Data WPT25C_1056_1085'
samplename = 'Text Data WPT25C_960_1000'
samplename = 'Text Data WPT81b'
samplename = 'Text Data WPT87C'
samplename = 'Text Data WPT301'
samplename = 'Text Data WPT403'

samplename = 'Text Data Zoser'

samplename = 'Text Data WPT81b'

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

elements = ['Al','Si','P','I','Ca','Br','Cu','Mn','Ni','Zn','Image']#, 'Fe','Co'#negative correlation
#elements = ['Ca','Cl'] #possitive correlation?

#elements = ['Ce','La','Al','Mo','Nd', 'S', 'Si', 'Sr', 'Y'] #no good correlation
#,
#elements = []

#divelements = ['Br', 'Cu', 'Fe', 'Mn', 'Nd', 'Ni','Hf','Ni','Zn','Nd']

divele = 'Image'
divelements = np.full(len(elements),divele)

setPlotParams(11, figsize=(20, 6))

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
        #plotdat = 2*plotdat/(mediandf[divelemetn] + 1)
        plotdat = plotdat/(mediandf[divelemetn] + 1)
    x, xerr, ymax, yerr = getAnnualData(plotdat, rings, type='max')
    mean += ymax
    #ax2.plot(x[:], ymax[:], label=label)
    ax2.errorbar(x, ymax, xerr=xerr, fmt='o-', capsize=0,label=label) #set horiz error bar to equal ring width
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