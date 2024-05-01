from ringManager import *

samplename = 'Text Data WPT301'
data = ringwithClass(samplename)
data.showDatapreparation(element='Image')
data.generateAllElementFigs()
data.plotringdata(elements=['Cu','Ca','Mo'])


