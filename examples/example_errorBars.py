'''
This is an example for the usage of the TuDoUtils package 
Author: Christian Jung <christian.jung@udo.edu>
'''
import TuDoUtils
from TuDoUtils.ratioPlotHolder import ratioPlotHolder
from TuDoUtils.errorBars import *
from ROOT import TH1F

from math import floor

# first we need to generate the object we are going to use
myUtils = ratioPlotHolder()

#axis labels. I recommend setting them
myUtils.xTitle = "some title for the x-axis"
myUtils.yTitle = "something else for the y-axis"

#plot a ratio at the bottom
myUtils.doRatio = True
myUtils.ratioRange = 0.5 # +- 50%

# we will need a canvas i guess..
myUtils.bookCanvas(2000,1000) 


#adjust the xrange
myUtils.xRange = (-4,4) 


#now we need some stuff we actually want to draw
# we will use an errorBarHist for simplicity. 
# The stack thing works the same way, just with a stack

# first a "data" thing which we want to compare to

myFirstPlot = TH1F("myFirstPlot", "this is a gaussian!", 100, -5 , 5)
myFirstPlot.Sumw2()
myFirstPlot.FillRandom("gaus",floor(80000/254.4));
myFirstPlot.SetMarkerStyle(20)
myFirstPlot.SetLineColor(ROOT.kBlack)

# this one will be the "simulation". We will scale it down a bit

mySecondPlot = TH1F("mySecondPlot", "this is another one!!", 100, -5, 5)
mySecondPlot.Sumw2()
mySecondPlot.FillRandom("gaus",floor(1000000000/254.4)) # to have something to see in the ratio 

mySecondPlot.Scale(0.00008*0.8) # and get them to almost the same area
mySecondPlot.SetLineColor(ROOT.kBlack)
mySecondPlot.SetFillColor(ROOT.kRed)



#ok, we will build a simple 10% uncertainty on the yield
mySecondPlotUncert = mySecondPlot.Clone("myUncertaintyBand")
mySecondPlotUncert.Scale(1.2) # difference will be 10% per bin


# now build an errorBarHist

myErrorBars = errorBarHist(mySecondPlot)

# and tell it about the uncertainty.
# it will take the difference between the put in histogram (mySecondPlotUncert) and 
# its "default" histogram (mySecondPlot) as the uncertainty, symmetric

myErrorBars.addUncertSingle(mySecondPlotUncert)

# you can also add with errorBarHist.addUncertUpDown(upHist, downHist)
# it will take half the difference between upHist and downHist
# and use it as the uncertainty

# If you add more than one uncertainty it will add them in quadrature
# even if you add only one it will have the statistical uncertainty
# added to that one in quadrature

#tell the utils about the plots
myUtils.addPlot1D(myFirstPlot, "\"Data\"", "EY")
myUtils.addPlot1D(myErrorBars, "Notice the error band?", "HIST")

#and now lets draw that stuff
#first and second argument are xpos and ypos of the legend
#third argument specifies the plot which is the reference for the ratio
myUtils.ratioTitle = "#frac{Data - Pred.}{Pred.}"
myUtils.drawPlots(0.8,0.7,1)

print(mySecondPlot.GetBinContent(50))

myUtils.saveCanvas("example.pdf")








