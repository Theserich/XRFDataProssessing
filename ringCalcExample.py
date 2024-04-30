from plotFunctions import *
from ringManager import *



samplenames = ['Text Data WPT301','Text Data WPT87C','Text Data WPT 9']

types = ['mean','median']

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