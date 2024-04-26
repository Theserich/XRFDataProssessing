from plotFunctions import *
from ringManager import *
from matplotlib.pyplot import cm
redraw=False #Pick True to redraw rings, false to keep previous selected ring boundaries
samplename = 'Text Data WPT403'

df = load_data(samplename)

mediandf = getmedianofLines(df,range=(1,15))
element = 'Si'
fig, ax = plt.subplots()
ax.set_title(samplename)
ax.plot(mediandf[element],label=element)
ax.legend()
plt.show()