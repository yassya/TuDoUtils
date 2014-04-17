'''
This is an example for the usage of the TuDoUtils class
Author: Christian Jung <christian.jung@udo.edu>
'''
from TuDoUtils.twoAxisPlotHolder import twoAxisPlotHolder

import ROOT
from ROOT import TH1F

def example():
    ROOT.gROOT.ProcessLine(".x ../2DAnalysis/Helper/styles.cxx")
    
    ROOT.gROOT.SetStyle("ATLAS");
    ROOT.gErrorIgnoreLevel = 1001
    # first we need to generate the object we are going to use
    myUtils = twoAxisPlotHolder()
    
    #axis labels. I recommend setting them
    myUtils.xTitle = "some title for the x-axis"
    myUtils.yTitle = "something else for the y-axis"
    

    # we will need a canvas i guess..
    # if you want a ratio you need to do this *after* doRatio is set to True!!
    myUtils.bookCanvas(2000,1000) 
    
    
    #adjust the xrange
    myUtils.xRange = (-4,4) 
    
    
    #now we need some stuff we actually want to draw
    #supported types so far are TH1D/TH1F, THStack and TF1.
    #
    #There are additional classes for uncertaintybands,
    # called errorBarHist/errorBarStack
    # which can also be used
    
    myFirstPlot = TH1F("myFirstPlot", "this is a gaussian!", 100, -5 , 5)
    myFirstPlot.FillRandom("gaus",500);
    myFirstPlot.SetMarkerStyle(20)
    myFirstPlot.SetLineColor(ROOT.kBlack)
    
    mySecondPlot = TH1F("mySecondPlot", "this is another one!!", 100, -5, 5)
    mySecondPlot.FillRandom("gaus",500000) # to have something to see in the ratio 
    mySecondPlot.Scale(0.001) # and get them to the same area
    mySecondPlot.SetLineColor(ROOT.kBlack)
    mySecondPlot.SetFillColor(ROOT.kRed)
    
    
    
    #tell the utils about the plots
    myUtils.addPlot1D(myFirstPlot, "This will appear", "EY", True)
    myUtils.addPlot1D(mySecondPlot, "in the legend", "HIST", True)
    myThirdPlot=mySecondPlot.Clone("dafq")
    myThirdPlot.Scale(2)
    myThirdPlot.SetFillColor(0)
    myThirdPlot.SetLineColor(ROOT.kBlue)
    myUtils.addPlot1D(myThirdPlot, "in the legend", "EY", False)
    
    #and now lets draw that stuff
    #first and second argument are xpos and ypos of the legend
    #third argument specifies the plot which is the reference for the ratio
    myUtils.drawPlots(0.75,0.7)
    
    #you can add text like this
    #it will only work properly after drawPlots ..
    myUtils.addText("You can write stuff", 0.2,0.5, ROOT.kBlue)
    
    
    myUtils.saveCanvas("example.pdf")
    
    
    
    
    
if __name__ == "__main__":
    import sys
    example()    
    
    
