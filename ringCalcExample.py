from plotFunctions import *
from ringManager import *

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

#RowTrim Function


types = ['mean','median','max','min']

ringclasses = {}
for samplename in samplenames:
    df = load_data(samplename)
    df = normalizedata(df)
    ringsClass = ringwithClass(samplename,redraw=False,imagekey='Image')
    ringsClass.calc_rings(df)
    ringclasses[samplename] = ringsClass

fig, ax = plt.subplots()
for samplename in ringclasses:
    for type in types:
        ax.plot(ringclasses[samplename].years,ringclasses[samplename].ringdf['Cu'][type],label=f'{samplename} {type}')
ax.legend()
plt.show()