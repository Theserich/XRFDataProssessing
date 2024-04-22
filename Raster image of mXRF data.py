from plotFunctions import *
from ringManager import *

redraw=True #Pick True to redraw rings, false to keep previous selected ring boundaries

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
samplename = 'Text Data WPT12'
samplename = 'Text Data WPT12C_1060_1110ish_400_RES016_2'
samplename = 'Text Data WPT9_1051_1093_400_RES013'
samplename = 'Text Data WPT19b'
samplename = 'Text Data WPT403'
samplename = 'Text Data WPT19b_HiRes' #No Bromine, need to reanalyze all elements
samplename = 'Text Data WPT 9'
samplename = 'Text Data WPT301'

if samplename in ['Text Data Newport_400DT_05TC_Focused_Thermal']: #Use sample file name if rings are oriented horizontally
    rotate = True

df = load_data(samplename)
#df = normalizedata(df)
df = zscore(df)
image = df['Image']
mediandf = getmedian(df)

setPlotParams(12,figsize=(20,6))
fig, ax = plt.subplots()
dataax = ax.twinx() #this draws the median data line along
#dataax.plot(mediandf['Ca'], color = 'r')
#Test change


levls = np.linspace(-3,3, 100)

#Below is how to greyscale, raster image
# ax.imshow(image,aspect='auto',cmap=plt.cm.gist_yarg)
# ax.imshow(image,aspect='auto', cmap=plt.cm.jet)
# ax.contourf(image, levels=levls, cmap=plt.cm.jet)

#Below shows the raster of elemental ratioing
elements = ['Ca','Image']
ax.contourf(df['Ca']/(df['Image']), levels=levls, cmap=plt.cm.jet) #for ratios
ax.set_title(samplename+f'{elements}')
plt.show()

#Show the median element line plots
# fig2, ax2 = plt.subplots(3,sharex=True)
# ax2[0].plot(df['Al'][1])
# ax2[1].plot(df['Fe'][1])
# ax2[2].plot(df['S'][1])
# plt.show()

elementlist = ['Image','Ca','Mg','Fe','Ta','Mo']
colormaplist=[plt.cm.Greys,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet]
#Show the raster images of the elements
#Do it automagically
#elementlist = df.keys()

fig2, ax2 = plt.subplots(len(elementlist),sharex=True)
for i, element in enumerate(elementlist):
    if element in df.keys():
        ax2[i].contourf(df[element],aspect='auto', levels= levls, cmap=colormaplist[i],label=element)
    ax2[i].text(0.0, 0.5, element, transform=ax2[i].transAxes)

# fig2, ax2 = plt.subplots(22)
# ax2[0].imshow(df['Image'],aspect='auto', cmap=plt.cm.Greys,label='Image')
# ax2[1].imshow(df['Na'],aspect='auto', cmap=plt.cm.jet)
# ax2[2].imshow(df['Mg'],aspect='auto', cmap=plt.cm.jet)
# ax2[3].imshow(df['Al'],aspect='auto', cmap=plt.cm.jet)
# ax2[4].imshow(df['Si'],aspect='auto', cmap=plt.cm.jet)
# ax2[5].imshow(df['P'],aspect='auto', cmap=plt.cm.jet)
# ax2[6].imshow(df['S'],aspect='auto', cmap=plt.cm.jet)
# ax2[7].imshow(df['Cl'],aspect='auto', cmap=plt.cm.jet)
# ax2[8].imshow(df['K'],aspect='auto', cmap=plt.cm.jet)
# ax2[9].imshow(df['Ca'],aspect='auto', cmap=plt.cm.jet)
# ax2[10].imshow(df['Mn'],aspect='auto', cmap=plt.cm.jet)
# ax2[11].imshow(df['Fe'],aspect='auto', cmap=plt.cm.jet)
# ax2[12].imshow(df['Ni'],aspect='auto', cmap=plt.cm.jet)
# ax2[13].imshow(df['Cu'],aspect='auto', cmap=plt.cm.jet)
# ax2[14].imshow(df['Zn'],aspect='auto', cmap=plt.cm.jet)
# ax2[15].imshow(df['Br'],aspect='auto', cmap=plt.cm.jet)
# ax2[16].imshow(df['Sr'],aspect='auto', cmap=plt.cm.jet)
# ax2[17].imshow(df['Y'],aspect='auto', cmap=plt.cm.jet)
# ax2[18].imshow(df['Mo'],aspect='auto', cmap=plt.cm.jet)
# ax2[19].imshow(df['I'],aspect='auto', cmap=plt.cm.jet)
# ax2[20].imshow(df['Ta'],aspect='auto', cmap=plt.cm.jet)
# ax2[21].imshow(df['Nd'],aspect='auto', cmap=plt.cm.jet)
# ax2[0].text(0.0, 0.5, 'Image', transform=ax2[0].transAxes)

plt.subplots_adjust(hspace=0)
plt.show()