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

samplename = 'Text Data MSH PF918'

if samplename in ['Text Data Newport_400DT_05TC_Focused_Thermal']:
    rotate = True

df = load_data(samplename)
df = normalizedata(df)
image = df['Ca']
mediandf = getmedian(df)
elements = ['Ca','Br']

setPlotParams(12,figsize=(20,3))
fig, ax = plt.subplots()
ax.set_title(samplename+f'{elements}')
dataax = ax.twinx()
dataax.plot(mediandf['Ca'])


#levls = np.linspace(0.0,0.15,50)

ax.contourf(np.log(df['Ca']/(df['Br']+1)), cmap=plt.cm.jet)#,levels=levls
#plt.show()

fig2, ax2 = plt.subplots(3,sharex=True)
#for i, data in enumerate(df['Ca']):
#    ax2[0].plot(data,label=i)
ax2[0].legend()



ax2[0].imshow(df['Cu'],aspect='auto')
#ax2[1].plot(df['Ca'])
#ax2[2].plot(df['Ca'])
plt.subplots_adjust(hspace=0)
plt.show()