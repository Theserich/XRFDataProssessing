from ringManager import *

samplename = 'Text Data WPT301'
data = ringwithClass(samplename,redo=False)
data.showDatapreparation(element='Image',block=False)



data.df = normalizedata(data.df)

#data.df = smoothing(data.df,21,3)
data.calc_rings()

data.plotAnnualboxplot(elements=['Cu','Mo','Mn'])
#data.plotAnnualdata(elements=['Cu'],types = ['median'])


#data.generateAllElementFigs()
#df = data.df = smoothing(data.df,13,3)

#data.plotringdata(elements=['Cu','Ca','Mo'])


