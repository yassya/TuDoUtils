'''
This is an example for the usage of the TuDoUtils class
Author: Christian Jung <christian.jung@udo.edu>
'''
from TuDoUtils.plotClass import plotClass
import ROOT
from ROOT import TH2F, TF1, gStyle

def example():


    ROOT.gROOT.ProcessLine(".x ../2DAnalysis/Helper/styles.cxx")
    
    ROOT.gROOT.SetStyle("ATLAS");
    ROOT.gErrorIgnoreLevel = 1001
    ROOT.gStyle.SetPalette(1)

    # first we need to generate the object we are going to use
    myUtils = plotClass()
    
    #axis labels. I recommend setting them
    myUtils.xTitle = "some title for the x-axis"
    myUtils.yTitle = "something else for the y-axis"
    

    
    # we will need a canvas i guess..
    myUtils.bookCanvas(2000,1000) 
    
    
    #adjust the xrange/yrange
    myUtils.xRange = (-6,8) 
    myUtils.yRange = (-6,6)
    
    
    #now we need some stuff we actually want to draw
    #supported types so far are TH1D/TH1F, THStack and TF1.
    #
    #There are additional classes for uncertaintybands,
    # called errorBarHist/errorBarStack
    # which can also be used
    
    myFirstPlot = TH2F("myFirstPlot", "this is a 2D gaussian!", 200, -10 , 10,200,-10,10)
    myFirstPlot.SetFillColor(ROOT.kBlue)
    
    firstGaus=TF1("gaus1","gaus",-10,10)
    firstGaus.SetParameter(0,1)
    firstGaus.SetParameter(1,0)
    firstGaus.SetParameter(2,1)
    sndGaus=TF1("gaus2","gaus",-10,10)
    sndGaus.SetParameter(0,1)
    sndGaus.SetParameter(1,2)
    sndGaus.SetParameter(2,1)    

    for i_evt  in range(100000):
        x,y=firstGaus.GetRandom(), sndGaus.GetRandom()
#        print(x,y)
        myFirstPlot.Fill(x,y+x,0.00000001)
        
        
    mySndPlot = TH2F("mySecondPlot", "this is a 2D gaussian, too!",  200, -10 , 10,200,-10,10)
    mySndPlot.SetFillColor(ROOT.kRed)
    
    firstGaus=TF1("gaus1","gaus",-10,10)
    firstGaus.SetParameter(0,1)
    firstGaus.SetParameter(1,-2)
    firstGaus.SetParameter(2,1)
    sndGaus=TF1("gaus2","gaus",-10,10)
    sndGaus.SetParameter(0,1)
    sndGaus.SetParameter(1,-3)
    sndGaus.SetParameter(2,1)    


    for i_evt  in range(100000):
        x,y=firstGaus.GetRandom(), sndGaus.GetRandom()
#        print(x,y)
        mySndPlot.Fill(x,y)


    myThirdPlot = TH2F("myThirdPlot", "this is a 2D gaussian, too!",  200, -10 , 10,200,-10,10)
    myThirdPlot.SetFillColor(ROOT.kOrange)
    
    firstGaus=TF1("gaus1","gaus",-10,10)
    firstGaus.SetParameter(0,1)
    firstGaus.SetParameter(1,-1)
    firstGaus.SetParameter(2,0.5)
    sndGaus=TF1("gaus2","gaus",-10,10)
    sndGaus.SetParameter(0,1)
    sndGaus.SetParameter(1,-0.5)
    sndGaus.SetParameter(2,0.5)    

    for i_evt  in range(100000):
        x,y=firstGaus.GetRandom(), sndGaus.GetRandom()
#        print(x,y)
        myThirdPlot.Fill(x,y)
    
#    myUtils.addPlot2D(myFirstPlot, "A nice 2D Gaussian", "BOX")
#    myUtils.addPlot2D(mySndPlot, "Another nice 2D Gaussian", "BOX")
#    myUtils.addPlot2D(myThirdPlot, "Yet another 2D Gaussian", "BOX")
    myUtils.addPlot2D(myFirstPlot, "A nice 2D Gaussian", "COLZ")
    myUtils.addPlot2D(mySndPlot, "Another nice 2D Gaussian", "COL")
    myUtils.addPlot2D(myThirdPlot, "Yet another 2D Gaussian", "COL")
    
    #and now lets draw that stuff
    #first and second argument are xpos and ypos of the legend
    #third argument specifies the plot which is the reference for the ratio
    myUtils.drawPlots(0.65,0.4)
    

    
    
    myUtils.saveCanvas("example.pdf")
    
    
    
    
    
if __name__ == "__main__":
    import sys
    example()    
    
    
