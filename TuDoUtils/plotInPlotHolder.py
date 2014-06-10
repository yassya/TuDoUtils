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


class plotInPlotHolder(plotBase):

    '''
    @brief A class for plotting a plot within another one

    an example for this can be found in examples/example_plotInPlot.py
    '''


    def __init__(self):
        '''
        Constructor
        Default values which should give decent results out of the box
        Make sure to change the values of xTitleMiddle and yTitleMiddle
        '''
        
        
        self.yTitleMiddle = "I'm still a lazy student"
        self.xTitleMiddle = "This plot is not actually correct"

        self.middlePositions = (0.65, 0.6)
        self.middleSize = (0.3, 0.3)
        plotBase.__init__(self)
                


        self.y_up_mult=1.3
        self.y_down_mult = 1.1
    def addPlot2D(self, thing, label, style):
        raise(AttributeError("No 2D with plots in plot (yet)"))
        

        

    def bookCanvas(self, xSize=1600, ySize=900):
        '''
        @brief book a ROOT TCanvas
        @param xSize: size (in pixels) in the horizontal direction 
        @param ySize: size (in pixels) in the vertical direction

        It is necessary to set self.middlePositions and self.middleSize to 
        the desired values before calling this as it sets up the middle pad
        '''

        if self.middlePositions[0]+self.middleSize[0] > 1:
            raise(ValueError("Inner plot exceeds right boundary!"))
        if self.middlePositions[1]+self.middleSize[1] > 1:
            raise(ValueError("Inner plot exceeds top boundary!"))
        
        self.canvas = TCanvas("TuDoUtils Canvas", "TuDoUtils Canvas", 10, 10, xSize, ySize)



        self.pad1 = TPad("pad1", "pad1", 0, 0, 1, 1, 0, 0, 0)
        self.pad2 = TPad("pad2", "pad2",  self.middlePositions[0], self.middlePositions[1], self.middlePositions[0]+self.middleSize[0], self.middlePositions[1]+self.middleSize[1])

        margin = 0.2
        # self.pad1.SetLeftMargin(margin)
        # self.pad1.SetRightMargin(margin)
        self.pad2.SetLeftMargin(0.15)
        self.pad2.SetBottomMargin(0.2)
        self.xRangeMiddle=self.xRange

            
    def addPlot1D(self, thing, label, style, middlePlot=False):
        '''
        @brief This adds a TH1*, THStack, TGraph, or TF1 to the drawList..
        @param thing: The object to be added
        @param label: Label for the legend
        @param style: ROOT-Draw() Style for that object  
        @middlePlot style: Does this belong to the pad in the middle?
        '''


        plotType = type(thing)
        if plotType not in [type(errorBarHist()), type(errorBarStack()), type(TGraph()), type(TGraphErrors()), type(TH1D()), type(TH1F()), type(THStack()), type(TF1())]:
            raise(TypeError(str(plotType) + "is not drawable (in 1D) :("))
        self.stuffToDraw.append(centerPlotToDraw(thing, label, style, middlePlot))


    def drawPlots(self, xPos=0.725, yPos=0.80,  xPosMiddle=0.725, yPosMiddle =0.80):
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
        return(self.drawPlots1D(xPos, yPos, xPosMiddle, yPosMiddle))
    def drawPlots1D(self, xPos=0.725, yPos=0.80, xPosMiddle=0.725, yPosMiddle =0.80):
        '''
        @brief: This draws all the objects which where added with addPlot and builds a legend.
        @param xPos: Fractional horziontal Position of the legend
        @param yPos: Fractional vertical Position of the legend
        @param xPosMiddle: Fractional horziontal Position of the legend for the smaller plot in the middle
        @param xPosMiddle: Fractional vertical Position of the legend for the smaller plot in the middle
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

        maximum_center = -9999999999.
        minimum_center = 9999999999.


        n_plots_left = 0
        n_plots_center = 0 # these two are needed for checking if each side gets at least one plot
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
                curr_maximum = curr_maximum + (self.y_up_mult - 1) * abs(curr_maximum)
                curr_minimum = plot.thingToDraw.GetHistogram().GetMinimum() 
                curr_minimum = curr_minimum - (self.y_down_mult - 1) * abs(curr_minimum)
            else:
                curr_maximum = plot.thingToDraw.GetMaximum() 
                curr_maximum = curr_maximum + (self.y_up_mult - 1) * abs(curr_maximum)
                curr_minimum = plot.thingToDraw.GetMinimum() 
                curr_minimum = curr_minimum - (self.y_down_mult - 1) * abs(curr_minimum)



            if plot.centerPlot==False:
                n_plots_center+=1
                if curr_maximum > maximum_center:
                    maximum_center = curr_maximum
                if curr_minimum < minimum_center:
                    minimum_center = curr_minimum
            else:
                n_plots_left+=1
                if curr_maximum > maximum:
                    maximum = curr_maximum
                if curr_minimum < minimum:
                    minimum = curr_minimum

        if n_plots_left == 0:
            raise(IndexError("No plot for the main pad."))
        if n_plots_center == 0:
            raise(IndexError("No plot for the center pad."))
        func_index=-1  #index of TF1 object, we want to draw that one last
        for plot in self.stuffToDraw:
        
            

            if plot.centerPlot==False:
                
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
            else:

                '''
                the standard calculation will not really work for the smaller plot
                keep the old default values there. 

                it should not be that critical as this plot will unlikely be
                close to the border of the canvas anyways
                '''
                if type(plot.thingToDraw) is not type(THStack()):
                    plot.thingToDraw.GetXaxis().SetTitle(self.xTitleMiddle)
                    plot.thingToDraw.GetXaxis().SetLabelFont(43)
                    plot.thingToDraw.GetXaxis().SetLabelSize(self.size*800)
                    plot.thingToDraw.GetXaxis().SetTitleFont(43)
                    plot.thingToDraw.GetXaxis().SetTitleSize(self.size*800)
                    plot.thingToDraw.GetXaxis().SetLabelOffset(0.016)
                    plot.thingToDraw.GetXaxis().SetTitleOffset(3.0)
                                   
                if type(plot.thingToDraw) is not type(THStack()) and type(plot.thingToDraw) is not type(errorBarStack()):
                    plot.thingToDraw.GetYaxis().SetTitle(self.yTitleMiddle)
                    plot.thingToDraw.GetYaxis().SetLabelFont(43)
                    plot.thingToDraw.GetYaxis().SetNdivisions(804,True)
                    plot.thingToDraw.GetYaxis().SetLabelSize(self.size*800)
                    plot.thingToDraw.GetYaxis().SetTitleFont(43)
                    plot.thingToDraw.GetYaxis().SetTitleSize(self.size*700)
                    
                
            if plot.centerPlot==False: 
                plot.thingToDraw.GetYaxis().SetTitleOffset(self.calcLeftTitleOffset())                        
                plot.thingToDraw.GetYaxis().SetLabelOffset(0.01)


                if self.xRange[0] is not self.xRange[1]:
                    plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0], self.xRange[1])
            else:

                '''
                this is not yet properly optimized. should still work decently
                '''
                if maximum_center <= 0:
                    plot.thingToDraw.GetYaxis().SetTitleOffset(1.0)
                elif log(maximum_center,10) > 4 or log(maximum_center,10) < -4:
                    plot.thingToDraw.GetYaxis().SetTitleOffset(3.5)
                else:
                    plot.thingToDraw.GetYaxis().SetTitleOffset(2.0)
                plot.thingToDraw.GetYaxis().SetLabelOffset(0.01)
                if self.xRange[0] is not self.xRange[1]:
                    plot.thingToDraw.GetXaxis().SetRangeUser(self.xRangeMiddle[0], self.xRangeMiddle[1])



            if type(plot.thingToDraw) is type(TF1()):
                plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0]-2, self.xRange[1]+10)
                func_index=self.stuffToDraw.index(plot)
            if not self.logy:
                if type(plot.thingToDraw) is not type(TGraph()) and type(plot.thingToDraw) is not type(TGraphErrors()):
                    if plot.centerPlot == True:
                        plot.thingToDraw.SetMinimum(minimum)
                        
                        plot.thingToDraw.SetMaximum(maximum)
                    else:
                        plot.thingToDraw.SetMinimum(minimum_center)
                        
                        plot.thingToDraw.SetMaximum(maximum_center)

                else:
                    if plot.centerPlot == True:
                        plot.thingToDraw.SetMinimum(minimum)
                        
                        plot.thingToDraw.SetMaximum(maximum)
                    else:
                        plot.thingToDraw.SetMinimum(minimum_center)
                        
                        plot.thingToDraw.SetMaximum(maximum_center)

        



        same = ""   # we do it a bit differently here. first draw all plots for the first pad (= left y axis)
        firstIndex = -1
        for plot in [x for x in self.stuffToDraw if x.centerPlot==False]:
            if firstIndex == -1:
                firstIndex=self.stuffToDraw.index(plot)
            plot.drawPlot(same)     
            same = "SAME"       

         
        
        #self.stuffToDraw[firstIndex].drawPlot(same)        
        if firstIndex==-1 and type(self.stuffToDraw[0].thingToDraw) is not type(TGraphErrors()) and  type(self.stuffToDraw[0].thingToDraw) is not type(TGraph()):
            self.stuffToDraw[0].drawPlot(same)
        elif firstIndex != -1:
            self.stuffToDraw[firstIndex].drawPlot(same)

        firstIndex = -1
        same = ""
       # and affterwards all the others
        
        
        self.pad2.Draw()    
        self.pad2.cd()
        for plot in [x for x in self.stuffToDraw if x.centerPlot==True]:
            if firstIndex == -1:
                firstIndex=self.stuffToDraw.index(plot)
            plot.drawPlot(same)     
            same = "SAME"      
        if firstIndex==-1 and type(self.stuffToDraw[0].thingToDraw) is not type(TGraphErrors()) and  type(self.stuffToDraw[0].thingToDraw) is not type(TGraph()):
            self.stuffToDraw[0].drawPlot(same)
        elif firstIndex != -1:
            self.stuffToDraw[firstIndex].drawPlot(same)


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


        self.pad1.cd()
        for plot in [x for x in self.stuffToDraw if x.centerPlot==False]:
            yPos = plot.drawLabel(self, xPos, yPos) # return value will be next free y value
        self.pad2.cd()


        actualYPos = yPosMiddle
        actualXPos = xPosMiddle
        
        for plot in [x for x in self.stuffToDraw if x.centerPlot==True]:
            actualYPos = plot.drawLabel(self, actualXPos, actualYPos) # return value will be next free y value
        

        self.pad1.RedrawAxis()
        self.pad2.RedrawAxis()
        
        self.canvas.RedrawAxis()


        self.pad1.cd()
        return None
    def __del__(self):
        del(self.pad1)
        del(self.pad2)

class centerPlotToDraw(toDraw): #if it quacks like a duck...
    """
    This class is basically the same as the toDraw object. The only
    functionality added is that the twoAxisPlotHolder can ask 
    if it belongs to the left axis
    """
    def __init__(self, thing, label, style, centerPlot):
        self.centerPlot=centerPlot
        toDraw.__init__(self,thing, label, style)