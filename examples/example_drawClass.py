'''
This is an example for the usage of the ratioPlotHolder class.
Author: Christian Jung <christian.jung@udo.edu>
'''
from TuDoUtils.simplePlotHolder import simplePlotHolder
from TuDoUtils.ratioPlotHolder import ratioPlotHolder
import ROOT
from ROOT import TH1F

def example():


    ROOT.gROOT.ProcessLine(".x ../2DAnalysis/Helper/styles.cxx")
    
    ROOT.gROOT.SetStyle("ATLAS");
    ROOT.gErrorIgnoreLevel = 1001
    ROOT.gStyle.SetPalette(1)

    # first we need to generate the object we are going to use
    myUtils = ratioPlotHolder()
    # myUtils = simplePlotHolder()
    
    #axis labels. I recommend setting them
    myUtils.xTitle = "some title for the x-axis"
    myUtils.yTitle = "something else for the y-axis"
    
    #if its the ratioPlotHolder specify the ratio range

    myUtils.ratioRange = 0.5 # +- 50%
    
    # we will need a canvas i guess..
    # if you want a ratio you need to do this *after* doRatio is set to True!!
    myUtils.bookCanvas(1600,900) 
    
    
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
    myUtils.addPlot1D(myFirstPlot, "This will appear", "EY")
    myUtils.addPlot1D(mySecondPlot, "in the legend", "HIST")
    
    #and now lets draw that stuff
    #first and second argument are xpos and ypos of the legend
    #third argument specifies the plot which is the reference for the ratio
    myUtils.drawPlots(0.8,0.7)
    
    #you can add text like this
    #it will only work properly after drawPlots ..
    myUtils.addText("You can write stuff", 0.2,0.5, ROOT.kBlue)
    
    myUtils.addATLASLabel(0.2,0.8,"Internal")
    
    myUtils.saveCanvas("example.pdf")
    
    
    
    
    
if __name__ == "__main__":
    import sys
    example()    
    
    
