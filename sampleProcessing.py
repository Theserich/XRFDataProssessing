#####  Code created by Nicolas Brehm May, 2024 at LTRR in collaboration with Nathan B English  #####

from ringManager import * #Imports all the functions used in the code below from "ringManager.py"

##### Crop and mask problem areas of the sample, and indicate ring years  ######
##### To redo ring years or the masks, open Metadata and delete the relevant file separately  #######

samplename = 'Text Data WPT301'  #Name of the folder the data is. Folder should include at least one .txt image (which is an matrix of values titled "... - Image.txt" and one with "... - Si.txt"
data = ringwithClass(samplename,redo=False) #This function calls the trim function, the mask function and the ring selection function
data.showDatapreparation(element='Image',block=False) #Shows the slice, and the masks selected above

#####  Generate the raster images  ######
data.generateAllElementFigs() #Creates the Raster images of all elements, leave this in

######  Generate the normalized and/or smoothed data  ######
data.df = smoothing(data.df,21,3) #Row by row smoothing of every row, smoothing(data.df,window size,polynomial)
data.df = normalizedata(data.df) #normalizes the element data, Min/max  over the whole element matrix for zero to one
data.calc_rings() #recalculate the value of each element for every annual ring. So this must occur after the smoothing and normalizing or it wont work...also includes the masks

#####  Data Plotting  ######
data.plotAnnualboxplot(elements=['Cu','Mo','Mn']) #generates the box plots.
data.plotAnnualdata(elements=['Cu'],types = ['max']) #line plot of the annual data.
data.plotringdata(elements=['Cu','Ca','Mo'])


