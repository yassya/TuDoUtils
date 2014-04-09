'''
 <TuDoUtils --- A program for some nice plotting with ROOT.>
    Copyright (C) 2013-2014  Christian Jung

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import ROOT
from ROOT import TCanvas, TH1D, TH1F, THStack, TF1, TLatex, TPave, TMarker, TPad, TList, TLine, TGraph, TGraphErrors, gStyle, TH2F, TH2D

from math import sqrt,log,log10,floor, ceil
import gc

from TuDoUtils.bin.plotBase import plotBase
from TuDoUtils.bin.errorBars import *


class simplePlotHolder(plotBase):
    '''
    @brief A class for holding objects to be drawn and to draw them 
    Handle for all the functions, can hold plots and stuff
    '''


    def __init__(self):
        '''
        Constructor
        Default values which should give decent results out of the box
        Make sure to change the values of xTitle and yTitle
        '''
        self.yRange = (0, 0) #only used for 2D histograms
        self.is2D=-1 # -1 means unspecified
        super().__init__()

      

    def drawPlots(self, xPos=0.725, yPos=0.80, index=1):
        '''
        @brief: This draws all the objects which where added with addPlot and builds a legend.
        @param xPos: Fractional horziontal Position of the legend
        @param yPos: Fractional vertical Position of the legend
        @param index: Index of the object for the ratio. See below for details  
        
        if self.doRatio is True it will also draw the ratio of the things, w.r.t
        to the (index-1)'th element in the list it got to draw,
        which is the index'th elemtent which was added
        
        xPos and yPos are the position of the legend  
        
        @returns: list with chi2 residuals in 1D case. Otherwise None
        '''
        if len(self.stuffToDraw) == 0:
            print("Nothing to draw!")
            return None
        if self.canvas is None:
            print("You did not book a canvas. I will do that for you")
            self.bookCanvas()
            
        if self.is2D==0:
            return(self.drawPlots1D(xPos, yPos, index))
        elif self.is2D==1:
            return(self.drawPlots2D(xPos, yPos, index))
        else:
            print("Cannot decicde if 2D or 1D. Probably this means that you did not add anything too draw yet..")
            return None
    def drawPlots1D(self, xPos=0.725, yPos=0.80, index=1):
        '''
        @brief: This draws all the objects which where added with addPlot and builds a legend.
        @param xPos: Fractional horziontal Position of the legend
        @param yPos: Fractional vertical Position of the legend
        @param index: Index of the object for the ratio. See below for details  
        
        if self.doRatio is True it will also draw the ratio of the things, w.r.t
        to the (index-1)'th element in the list it got to draw,
        which is the index'th elemtent which was added
        
        xPos and yPos are the position of the legend  
        
        @returns: list with chi2 residuals 
        '''
        
        if self.is2D!=0:
            print("This instance does not have any 1D objects, aborting")
            return None
        if len(self.stuffToDraw) < 2 and self.doRatio == True:
            print("Too much stuff or to little stuff for a ratio...")
            return None
        
        if self.canvas is None: #redundant f one calls drawPlots() but someone might skip that and then this is necessary 
            print("You did not book a canvas. I will do that for you")
            self.bookCanvas()
        
        self.canvas.Clear() #just in case someone did not do that..

        

        maximum = 0
        minimum = 0
        
        for plot in self.stuffToDraw:

            """FIXME: Add Andreas Tgraph min/max calculation"""
            if type(plot.thingToDraw) == type(TF1()):
                continue
            if type(plot.thingToDraw) == type(errorBarHist()):
                continue
            #print(maximum)
            if plot.thingToDraw.GetMaximum() * self.y_up_mult > maximum:
                maximum = plot.thingToDraw.GetMaximum() * self.y_up_mult
            if plot.thingToDraw.GetMinimum() * self.y_down_mult < minimum:
                minimum = plot.thingToDraw.GetMinimum() * self.y_down_mult
                
        same = ""
        
        
        func_index=-1  #index of TF1 object, we want to draw that one last
        for plot in self.stuffToDraw:
            

                
            if type(plot.thingToDraw) is not type(THStack()):
                plot.thingToDraw.GetXaxis().SetTitle(self.xTitle)
                plot.thingToDraw.GetXaxis().SetLabelFont(43)
                plot.thingToDraw.GetXaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetXaxis().SetTitleFont(43)
                if self.doRatio is True:
                    plot.thingToDraw.GetXaxis().SetTitleSize(self.size*1000)
                    plot.thingToDraw.GetXaxis().SetTitleOffset(1.8)
                else:
                    plot.thingToDraw.GetXaxis().SetTitleSize(self.size*1200)
                    plot.thingToDraw.GetXaxis().SetTitleOffset(1.1)
                               
            if type(plot.thingToDraw) is not type(THStack()) and type(plot.thingToDraw) is not type(errorBarStack()):
                plot.thingToDraw.GetYaxis().SetTitle(self.yTitle)
                plot.thingToDraw.GetYaxis().SetLabelFont(43)
                if self.doRatio==True:
                    plot.thingToDraw.GetXaxis().SetLabelSize(0)
                
                plot.thingToDraw.GetYaxis().SetNdivisions(804,True)
                plot.thingToDraw.GetYaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetYaxis().SetTitleFont(43)
                plot.thingToDraw.GetYaxis().SetTitleSize(self.size*1000)



                
                if self.canvas.GetAspectRatio() > 1: #hochformat
                    #plot.thingToDraw.GetYaxis().SetTitleOffset(1.0)
                    if maximum <= 0:
                        plot.thingToDraw.GetYaxis().SetTitleOffset(1.2)
                    elif log(maximum,10) > 4 or log(maximum,10) < 4:
                        plot.thingToDraw.GetYaxis().SetTitleOffset(1.8)
                    else:
                        plot.thingToDraw.GetYaxis().SetTitleOffset(1.6)
                else:
                    #plot.thingToDraw.GetYaxis().SetTitleOffset(1.0)
                    if maximum <= 0:
                        plot.thingToDraw.GetYaxis().SetTitleOffset(1.0)
                    elif log(maximum,10) > 4 or log(maximum,10) < 4:
                        plot.thingToDraw.GetYaxis().SetTitleOffset(1.6)
                    else:
                        plot.thingToDraw.GetYaxis().SetTitleOffset(1.4)
                plot.thingToDraw.GetYaxis().SetLabelOffset(0.01)
                if self.xRange[0] is not self.xRange[1]:
                    plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0], self.xRange[1])
            if type(plot.thingToDraw) is type(TF1()):
                plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0]-2, self.xRange[1]+10)
                func_index=self.stuffToDraw.index(plot)
            if not self.logy:
                if type(plot.thingToDraw) is not type(TGraph()) and type(plot.thingToDraw) is not type(TGraphErrors()):
                    plot.thingToDraw.SetMinimum(0)
                    
                    plot.thingToDraw.SetMaximum(maximum)
                else:
                    plot.thingToDraw.SetMinimum(minimum)
                    plot.thingToDraw.SetMaximum(maximum)
               
#            if type(plot.thingToDraw is type(TF1())):
#                plot.thingToDraw.SetMaximum(0.05)
            plot.drawPlot(same)     # first time same will be "" after that "SAME" 
            
            same = "SAME"       # which is the wanted behaviour :)
        if func_index==-1 and type(self.stuffToDraw[0].thingToDraw) is not type(TGraphErrors()) and  type(self.stuffToDraw[0].thingToDraw) is not type(TGraph()):

            self.stuffToDraw[0].drawPlot(same)
        elif func_index != -1:
            self.stuffToDraw[func_index].drawPlot(same)
        if self.logy:
            self.canvas.SetLogy()
            
            self.pad1.SetLogy()
        for plot in self.stuffToDraw:
            yPos = plot.drawLabel(self, xPos, yPos) # return value will be next free y value
        self.pad1.RedrawAxis()
        self.canvas.RedrawAxis()
        
        return None
        
        
 
        


    def drawPlots2D(self, xPos=0.725, yPos=0.80, index=1):
        if self.is2D!=1:
            print("This instance does not have any 2D histograms, aborting")
            return None
        
        same = ""

        for plot in self.stuffToDraw:
            
            if same == "":
                plot.thingToDraw.GetXaxis().SetTitle(self.xTitle)
                plot.thingToDraw.GetXaxis().SetLabelFont(43)
                plot.thingToDraw.GetXaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetXaxis().SetTitleFont(43)
                plot.thingToDraw.GetXaxis().SetTitleSize(self.size*1000)
                
                
                plot.thingToDraw.GetYaxis().SetTitle(self.yTitle)
                plot.thingToDraw.GetYaxis().SetLabelFont(43)
                plot.thingToDraw.GetYaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetYaxis().SetTitleFont(43)
                plot.thingToDraw.GetYaxis().SetTitleSize(self.size*1000)
                
                if "COLZ" in plot.style:
                    base=0.08 #min width for color legend
                    
                    digits = floor(log10(plot.thingToDraw.GetMaximum()))
                    if digits < 0: # numbers lower than 0. 
                        digits = - digits + 1.5 # flip sign as printed number gets bigger as more zeroes appear after decimal point. Also add .5 space for that very point
                    if digits < 1:  # lower limit for digits
                        digits = 1 
                    if digits > 4.6: # upper limit. Here roots starts to print 10^{something}. Fix width for this
                        digits = 3
                    self.canvas.SetRightMargin(base+digits*0.01)
            
            
            if self.xRange[0] is not self.xRange[1]:
                plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0], self.xRange[1])
            if self.yRange[0] is not self.yRange[1]:
                plot.thingToDraw.GetYaxis().SetRangeUser(self.yRange[0], self.yRange[1])
            plot.drawPlot(same)     # first time same will be "" after that "SAME" 
            same = "SAME"       # which is the wanted behaviour :)
        for plot in self.stuffToDraw:
            yPos = plot.drawLabel(self, xPos, yPos) # return value will be next free y value
        self.canvas.RedrawAxis()
        
        return None
