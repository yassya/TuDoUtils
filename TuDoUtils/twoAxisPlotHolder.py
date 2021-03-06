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
from ROOT import TCanvas, TH1D, TH1F, THStack, TF1, TLatex, TPave, TMarker, TPad, TList, TLine, TGraph, TGraphErrors, gStyle, TH2F, TH2D, TGaxis

from math import sqrt,log,log10,floor, ceil
import gc

from TuDoUtils.plotBase import plotBase, toDraw
from TuDoUtils.errorBars import *


class twoAxisPlotHolder(plotBase):

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
        
        
        self.yTitleRight = "I'm still a lazy student"
        plotBase.__init__(self)
                


        
    def addPlot2D(self, thing, label, style):
        raise(AttributeError("No 2D with two axes"))
        

        

    def bookCanvas(self, xSize=1600, ySize=900):
        '''
        @brief book a ROOT TCanvas
        @param xSize: size (in pixels) in the horizontal direction 
        @param ySize: size (in pixels) in the vertical direction
        '''
        self.canvas = TCanvas("TuDoUtils Canvas", "TuDoUtils Canvas", 10, 10, xSize, ySize)



        self.pad1 = TPad("pad1", "pad1", 0, 0, 1, 1, 0, 0, 0)
        self.pad2 = TPad("pad2", "pad2",  0, 0, 1, 1)


        margin = 0.08
        self.pad1.SetLeftMargin(margin)
        self.pad1.SetRightMargin(margin)
        self.pad2.SetLeftMargin(margin)
        self.pad2.SetRightMargin(margin)

            
    def addPlot1D(self, thing, label, style, leftAxis=True):
        '''
        @brief This adds a TH1*, THStack, TGraph, or TF1 to the drawList..
        @param thing: The object to be added
        @param label: Label for the legend
        @param style: ROOT-Draw() Style for that object  
        @leftAxis style: Does this belong to the left Y axis?
        '''


        plotType = type(thing)
        if plotType not in [type(errorBarHist()), type(errorBarStack()), type(TGraph()), type(TGraphErrors()), type(TH1D()), type(TH1F()), type(THStack()), type(TF1())]:
            raise(TypeError(str(plotType) + "is not drawable (in 1D) :("))
        self.stuffToDraw.append(twoAxesToDraw(thing, label, style, leftAxis))


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
        return(self.drawPlots1D(xPos, yPos, index))
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
        
        if len(self.stuffToDraw) < 2:
            raise(IndexError("Need at least two plots for supporting two axes"))

        
        if self.canvas is None: #redundant f one calls drawPlots() but someone might skip that and then this is necessary 
            print("You did not book a canvas. I will do that for you")
            self.bookCanvas()
        
        self.canvas.Clear() #just in case someone did not do that..

        # self.pad1.SetFillStyle(4000)
        self.pad2.SetFillStyle(4000)
        self.pad2.SetFillColor(0)
        self.pad2.SetFrameFillStyle(4000)

        self.pad1.SetTicky(0);
        self.pad1.Draw()
         
        
        
        # self.pad1.Draw()
        self.pad1.cd()


        maximum = -9999999999.
        minimum = 9999999999.

        maximum_right = -9999999999.
        minimum_right = 9999999999.


        n_plots_left = 0
        n_plots_right = 0 # these two are needed for checking if each side gets at least one plot
        for plot in self.stuffToDraw:

            if type(plot.thingToDraw) == type(TF1()):
                continue
            if type(plot.thingToDraw) == type(errorBarHist()):
                continue


            curr_maximum = 0
            curr_minimum = 0

            """
            The absolute values are needed in case that the max/min values are smaller than 0
            By doing it this way we can control the direction of the 'multiplication'
            """
            if type(plot.thingToDraw) == type(TGraph()) or type(plot.thingToDraw) == type(TGraphErrors()):
                curr_maximum = plot.thingToDraw.GetHistogram().GetMaximum() 
                curr_minimum = plot.thingToDraw.GetHistogram().GetMinimum() 
            else:
                curr_maximum = plot.thingToDraw.GetMaximum() 
                curr_minimum = plot.thingToDraw.GetMinimum() 


            if plot.leftAxis==False:
                n_plots_right+=1
                if curr_maximum > maximum_right:
                    maximum_right = curr_maximum
                if curr_minimum < minimum_right:
                    minimum_right = curr_minimum
            else:
                n_plots_left+=1
                if curr_maximum > maximum:
                    maximum = curr_maximum
                if curr_minimum < minimum:
                    minimum = curr_minimum
                    

        maximum = maximum + (self.y_up_mult - 1) * abs(maximum)
        minimum = minimum - (self.y_down_mult - 1) * abs(minimum)

        maximum_right = maximum_right + (self.y_up_mult - 1) * abs(maximum_right)
        minimum_right = minimum_right - (self.y_down_mult - 1) * abs(minimum_right)


        if n_plots_left == 0:
            raise(IndexError("No plot for the left Y axis."))
        if n_plots_right == 0:
            raise(IndexError("No plot for the right Y axis."))
        func_index=-1  #index of TF1 object, we want to draw that one last
        for plot in self.stuffToDraw:
        
            

                
            if type(plot.thingToDraw) is not type(THStack()):
                plot.thingToDraw.GetXaxis().SetTitle(self.xTitle)
                plot.thingToDraw.GetXaxis().SetLabelFont(43)
                plot.thingToDraw.GetXaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetXaxis().SetTitleFont(43)
                plot.thingToDraw.GetXaxis().SetTitleSize(self.size*1200)
                plot.thingToDraw.GetXaxis().SetTitleOffset(self.calcBottomTitleOffset())
                # plot.thingToDraw.GetXaxis().SetTitleOffset(2)
                pass
            if type(plot.thingToDraw) is not type(THStack()) and type(plot.thingToDraw) is not type(errorBarStack()):
                plot.thingToDraw.GetYaxis().SetTitle(self.yTitle)
                plot.thingToDraw.GetYaxis().SetLabelFont(43)     
                plot.thingToDraw.GetYaxis().SetNdivisions(804,True)
                plot.thingToDraw.GetYaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetYaxis().SetTitleFont(43)
                plot.thingToDraw.GetYaxis().SetTitleSize(self.size*1200)
                plot.thingToDraw.GetYaxis().SetTitleOffset(self.calcLeftTitleOffset())                        
                plot.thingToDraw.GetYaxis().SetLabelOffset(0.01)

                
                if self.xRange[0] is not self.xRange[1]:
                    plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0], self.xRange[1])
            if type(plot.thingToDraw) is type(TF1()):
                plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0]-2, self.xRange[1]+10)
                func_index=self.stuffToDraw.index(plot)
            if not self.logy:
                if type(plot.thingToDraw) is not type(TGraph()) and type(plot.thingToDraw) is not type(TGraphErrors()):
                    if plot.leftAxis == True:
                        plot.thingToDraw.SetMinimum(minimum)
                        
                        plot.thingToDraw.SetMaximum(maximum)
                    else:
                        plot.thingToDraw.SetMinimum(minimum_right)
                        
                        plot.thingToDraw.SetMaximum(maximum_right)
                        plot.thingToDraw.GetYaxis().SetTickLength(0)
                        plot.thingToDraw.GetYaxis().SetLabelOffset(99999.)
                else:
                    if plot.leftAxis == True:
                        plot.thingToDraw.SetMinimum(minimum)
                        
                        plot.thingToDraw.SetMaximum(maximum)
                    else:
                        plot.thingToDraw.SetMinimum(minimum_right)
                        
                        plot.thingToDraw.SetMaximum(maximum_right)
                        plot.thingToDraw.GetYaxis().SetTickLength(0)
                        plot.thingToDraw.GetYaxis().SetLabelOffset(99999.)
        



        same = ""   # we do it a bit differently here. first draw all plots for the first pad (= left y axis)
        firstIndex = -1
        for plot in [x for x in self.stuffToDraw if x.leftAxis==True]:
            if firstIndex == -1:
                firstIndex=self.stuffToDraw.index(plot)
            plot.drawPlot(same)     
            same = "SAME"       

         
        
        #self.stuffToDraw[firstIndex].drawPlot(same)        
        if type(self.stuffToDraw[firstIndex].thingToDraw) is not type(TGraphErrors()) and  type(self.stuffToDraw[firstIndex].thingToDraw) is not type(TGraph()):
            self.stuffToDraw[firstIndex].drawPlot(same)

        firstIndex = -1
        same = ""
       # and affterwards all the others
        
        
        self.pad2.Draw()    
        self.pad2.cd()
        for plot in [x for x in self.stuffToDraw if x.leftAxis==False]:
            if firstIndex == -1:
                firstIndex=self.stuffToDraw.index(plot)
            plot.drawPlot(same)     
            same = "SAME"      
        if type(self.stuffToDraw[firstIndex].thingToDraw) is not type(TGraphErrors()) and  type(self.stuffToDraw[firstIndex].thingToDraw) is not type(TGraph()):
            self.stuffToDraw[0].drawPlot(same)


        # self.stuffToDraw[firstIndex].drawPlot(same)        


        if func_index != -1:
            if self.stuffToDraw[func_index].leftAxis==True:
                self.pad1.cd()
            else:
                self.pad2.cd()
            self.stuffToDraw[func_index].drawPlot(same)
        if self.logy:
            self.canvas.SetLogy()
            
            self.pad1.SetLogy()
            self.pad2.SetLogy()
        
        self.pad2.cd()

        if self.xRange[0] == self.xRange[1]:
            xmax = self.stuffToDraw[0].thingToDraw.GetXaxis().GetXmax()
            axis = TGaxis(xmax, minimum_right,xmax, maximum_right, minimum_right, maximum_right, 804,"+L")
        else:
            axis = TGaxis(self.xRange[1], minimum_right, self.xRange[1], maximum_right, minimum_right, maximum_right, 804,"+L")
        axis.SetLabelColor(ROOT.kRed)
        axis.SetTitleColor(ROOT.kRed)

        axis.SetTitle(self.yTitleRight)
        axis.Draw() 
        self.stuffToKeep.append(axis)
        

        self.pad1.cd()
        for plot in self.stuffToDraw:
            yPos = plot.drawLabel(self, xPos, yPos) # return value will be next free y value


        self.pad1.RedrawAxis()
        # self.pad2.RedrawAxis()
        self.canvas.RedrawAxis()


        self.pad1.cd()
        return None
    def __del__(self):
        del(self.pad1)
        del(self.pad2)

class twoAxesToDraw(toDraw): #if it quacks like a duck...
    """
    This class is basically the same as the toDraw object. The only
    functionality added is that the twoAxisPlotHolder can ask 
    if it belongs to the left axis
    """
    def __init__(self, thing, label, style, leftAxis):
        self.leftAxis=leftAxis
        toDraw.__init__(self,thing, label, style)