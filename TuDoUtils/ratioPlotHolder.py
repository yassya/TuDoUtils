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

from TuDoUtils.plotBase import plotBase, toDraw
from TuDoUtils.errorBars import *


class ratioPlotHolder(plotBase):

    '''
    @brief Plot stuff with an additional ratio on the bottom
    '''


    def __init__(self):
        '''
        Constructor
        Default values which should give decent results out of the box
        Interesting parameters are 
            doMCoverData : flips the ratio if wanted
            centerUncertAtZero : centers systematic uncertainites (if present, see errorBars) at zero instead at the ratiopoints
        '''
        
        
        self.ratioRange = 0.25
        self.size=0.1
        self.ratioType = "EY"        
        self.doMCoverData=False
        self.centerUncertAtZero=True
        self.ratioRange = 0.25
        self.ratioType = "EY"
        self.ratioTitle="rel. difference"
        plotBase.__init__(self)

        self.area_first_pad_corr = 1. / 0.75
                

    def addPlot1D(self, thing, label, style):
        '''
        @brief This adds a TH1*, THStack, TGraph, or TF1 to the drawList..
        @param thing: The object to be added
        @param label: Label for the legend
        @param style: ROOT-Draw() Style for that object  
        '''

        plotType = type(thing)
        if plotType not in [type(errorBarHist()), type(errorBarStack()), type(TGraph()), type(TGraphErrors()), type(TH1D()), type(TH1F()), type(THStack()), type(TF1())]:
            print(plotType, "is not drawable (in 1D) :(")
            return None

        self.stuffToDraw.append(toDraw(thing, label, style))
        
        
    def addPlot2D(self, thing, label, style):
        raise(AttributeError("No 2D with ratio"))
        

        

    def bookCanvas(self, xSize=1600, ySize=900):
        '''
        @brief book a ROOT TCanvas
        @param xSize: size (in pixels) in the horizontal direction 
        @param ySize: size (in pixels) in the vertical direction
        '''
        self.canvas = TCanvas("TuDoUtils Canvas", "TuDoUtils Canvas", 10, 10, xSize, ySize)


        upheight=0.75
        dwcorr=1.32
        dwheight=(1-upheight)*dwcorr

        self.pad1 = TPad("pad1", "pad1",0.0,1-upheight,1.0,1.0)
#            self.pad1.SetTopMargin(0.05 * 20. / 13.)
        self.pad1.SetBottomMargin(-0.05)
        self.pad1.SetLeftMargin(0.12)
        self.pad1.SetRightMargin(0.05)#

        self.pad2 = TPad("pad2", "pad2", 0.0,0.0,1.0,dwheight)
        self.pad2.SetGridy(1)
#            self.pad2.SetTopMargin(0)
        self.pad2.SetBottomMargin(0.16*20/7)
        self.pad2.SetLeftMargin(0.12)
        self.pad2.SetRightMargin(0.05)
            
      
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
        
        @returns: list with chi2 residuals 
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
            raise(IndexError("Only one plot. Impossible to build a ratio"))
        
        if self.canvas is None: #redundant f one calls drawPlots() but someone might skip that and then this is necessary 
            print("You did not book a canvas. I will do that for you")
            self.bookCanvas()
        
        self.canvas.Clear() #just in case someone did not do that..

        
        
        
        self.pad2.Draw()    
        self.pad1.Draw()
        self.pad1.cd()
        maximum = 0
        minimum = 0
        
        for plot in self.stuffToDraw:
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
            
            
            if type(plot.thingToDraw) is not type(THStack()) and type(plot.thingToDraw) is not type(errorBarStack()):
                plot.thingToDraw.GetYaxis().SetTitle(self.yTitle)
                plot.thingToDraw.GetYaxis().SetLabelFont(43)
                
                plot.thingToDraw.GetXaxis().SetLabelSize(0)
                
                plot.thingToDraw.GetYaxis().SetNdivisions(804,True)
                plot.thingToDraw.GetYaxis().SetLabelSize(self.size*1000)
                plot.thingToDraw.GetYaxis().SetTitleFont(43)
                plot.thingToDraw.GetYaxis().SetTitleSize(self.size*1000)
                plot.thingToDraw.GetXaxis().SetTitleOffset(self.calcBottomTitleOffset())
                plot.thingToDraw.GetYaxis().SetTitleOffset(self.calcLeftTitleOffset())
    
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
            
#        self.addATLASLabel(0.16, 0.85)
        
        residualslist = []
        
        self.pad2.cd()
        self.pad2.SetFillStyle(4000)
        self.pad1.SetFillStyle(4000)
        isTF1 = False
        
        theRatio = self.stuffToDraw[index - 1]
        
        same = ""
        for ratioPlot in self.stuffToDraw:
            if theRatio == ratioPlot:
                continue
            thePlot = ratioPlot.thingToDraw
            isTF1 = type(thePlot)
            thePlot = self.divide(thePlot, theRatio.thingToDraw)
            residuals = []
            
            if thePlot is None:
                print("I failed to divide, skippin' that plot")
                continue
            if same is "":
                
                thePlot.GetYaxis().SetRangeUser(-self.ratioRange, self.ratioRange)
                thePlot.GetXaxis().SetTitle(self.xTitle)
                
                thePlot.GetXaxis().SetLabelFont(43)
                thePlot.GetXaxis().SetLabelSize(self.size*1000)
                thePlot.GetXaxis().SetTitleFont(43)
                thePlot.GetXaxis().SetTitleSize(self.size*1200)
                thePlot.GetXaxis().SetTitleOffset(self.calcBottomTitleOffset())
                thePlot.GetYaxis().SetTitleOffset(self.calcLeftTitleOffset())
            else:
                thePlot.GetYaxis().SetLabelSize(self.size*2)
                thePlot.GetYaxis().SetLabelSize(self.size*3.0)
                thePlot.GetYaxis().SetTitleSize(self.size*3.0)     
                thePlot.GetYaxis().SetTitle("rel. difference")
                thePlot.GetYaxis().SetTitleOffset(self.calcLeftTitleOffset())
                thePlot.GetYaxis().SetLabelOffset(0.025)  
                thePlot.GetYaxis().SetNdivisions(206, True);
                thePlot.SetMarkerSize(self.size * 50)
            if len(self.stuffToDraw) is 2:
                thePlot.SetMarkerSize(self.size * 50)

            thePlot.Draw(str(self.ratioType) + same)
            #print(str(self.ratioType) + same)
            #thePlot.Draw("EY" + same)
            same = "SAME"
            
            if isTF1 is type(TF1()):
                for i in range(thePlot.GetNbinsX()):
                    binCenter = thePlot.GetBinCenter(i)
                    if  self.xRange[0] is not self.xRange[1]:
                        if binCenter < self.xRange[0] or binCenter > self.xRange[1]:
                            continue
                    residuals.append(thePlot.GetBinContent(i))
#print(residuals)
                residualslist.append(residuals)
            
        if self.xRange[0] is not self.xRange[1]:
            lineAtZero = TLine(self.xRange[0], 0, self.xRange[1], 0)
        else:
            lineAtZero = TLine(theRatio.thingToDraw.GetXaxis().GetXmin(), 0, theRatio.thingToDraw.GetXaxis().GetXmax(), 0)
        lineAtZero.SetLineWidth(3)
        lineAtZero.Draw("SAME")
        self.stuffToKeep.Add(lineAtZero)
        self.pad2.RedrawAxis()
            
        

            
        self.pad1.cd()
        self.pad1.Draw()
        self.pad1.RedrawAxis()
        self.canvas.RedrawAxis()
        
        return residualslist
        
        
 

    def divide(self, numerator, denumerator):
        
        """
        @brief calculates ratio between numerator and denumerator, depending on tpye
        @param numerator: Numerator for the division
        @param denumerator: Denumerator for the division 
        
        @returns: Histogram with ratio
        """
        
        if type(denumerator) not in [type(TH1D()), type(TH1F())]:
            raise(TypeError("Can only compare with histograms right now, sorry :("))
            
        if type(numerator) is type(TH1D()) or type(numerator) is type(TH1F()):
            compare = numerator.Clone("newNumerator")
            

            compare.Divide(denumerator)
            
            for i in range(compare.GetNbinsX()+1):
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
                if self.doMCoverData ==False:
                    compare.SetBinContent(i, compare.GetBinContent(i) *- 1)
            self.stuffToKeep.Add(compare)
            compare.GetYaxis().SetTitle(self.ratioTitle)
            compare.SetMarkerStyle(20)
            return compare
        elif type(numerator) is type(errorBarHist()):
            compare = numerator.histo.Clone("newNumerator")
            compareError = numerator.errorHist.Clone("newErrorNumerator")
            
            if self.centerUncertAtZero == True:
                temp_denum = denumerator.Clone("zeroErrorDenum")
                for i in range(compare.GetNbinsX()+1):
#                    compareError.SetBinError(i,0)
#                    compare.SetBinError(i,0)
                    temp_denum.SetBinError(i,0)
                compare.Divide(denumerator)
                compareError.Divide(temp_denum) # to not add the statistical error of the denumerator to the error - it remains at the points

            else:
                
                compare.Divide(denumerator)
                compareError.Divide(denumerator)
            
            for i in range(compare.GetNbinsX()+1):
                if self.centerUncertAtZero == True:
                    compareError.SetBinContent(i, 0)
                else:
                    compareError.SetBinContent(i, compareError.GetBinContent(i) - 1)
#                compareError.SetBinError(i, compareError.GetBinError(i))#/denumerator.GetBinContent(i))
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
                if self.doMCoverData ==False:
                    compare.SetBinContent(i, compare.GetBinContent(i) *- 1)
                    compareError.SetBinContent(i, compareError.GetBinContent(i) *- 1)
            compare.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])
            compareError.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])

            compare.GetYaxis().SetTitle(self.ratioTitle)
            newCompare = errorBarHist()
            newCompare.histo = compare
            newCompare.errorHist = compareError
            self.stuffToKeep.Add(newCompare.histo)
            self.stuffToKeep.Add(newCompare.errorHist)
            newCompare.SetMarkerStyle(20)
            return newCompare
        elif type(numerator) is type(errorBarStack()):
#            compare = numerator.errorHist.Clone("newNumerator")
            compare = None
            for hist in numerator.histo.GetHists():
                if compare is None:
                    compare = hist.Clone("newNumerator")
                else:
                    compare.Add(hist)
            
            tempDenum=denumerator.Clone("tempDenum") #do not want to add the error of the data
            compareError = numerator.errorHist.Clone("newErrorNumerator")
            for i in range(denumerator.GetNbinsX()+1):
                tempDenum.SetBinError(i,0)
                
                
        
            compare.Divide(tempDenum)
            compareError.Divide(tempDenum)
            compare.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])
            compareError.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])
            for i in range(compare.GetNbinsX()+1):
                if self.centerUncertAtZero == True:
                    compareError.SetBinContent(i, 0)
                else:
                    compareError.SetBinContent(i, compareError.GetBinContent(i) - 1)

                compareError.SetBinError(i, compareError.GetBinError(i))#/denumerator.GetBinContent(i))
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
                if self.doMCoverData ==False:
                    compare.SetBinContent(i, compare.GetBinContent(i) *- 1)
                    compareError.SetBinContent(i, compareError.GetBinContent(i) *- 1)
                
            compare.GetYaxis().SetTitle(self.ratioTitle)    
            newCompare = errorBarStack()
            newCompare.histo = compare
            newCompare.errorHist = compareError
            compare.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])
            compareError.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])

            self.stuffToKeep.Add(newCompare.histo)
            self.stuffToKeep.Add(newCompare.errorHist)
            newCompare.SetMarkerStyle(20)
            return newCompare
        elif type(numerator) is type(THStack()):
            compare = denumerator.Clone("newNumerator")
            compare.Reset()
            for hist in numerator.GetHists():
                compare.Add(hist)
            compare.Divide(denumerator)
            for i in range(compare.GetNbinsX()+1):
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
                if self.doMCoverData ==False:
                    compare.SetBinContent(i, compare.GetBinContent(i) *- 1)
                    
            self.stuffToKeep.Add(compare)
            compare.GetYaxis().SetTitle(self.ratioTitle)
            compare.SetMarkerStyle(20)
            return compare
        elif type(numerator) is type(TF1()):
            
            compare = denumerator.Clone("newNumerator")
            compare.Reset()
            
            for i in range(compare.GetNbinsX()+1):
                binCenter = compare.GetBinCenter(i)
                if  self.xRange[0] is not self.xRange[1]:
                    if binCenter < self.xRange[0] or binCenter > self.xRange[1]:
                        compare.SetBinContent(i, 0)
                        continue
                val = denumerator.GetBinContent(i)
                err = denumerator.GetBinError(i)
                fit = numerator.Eval(binCenter)
                
                sign = 1
                if val > fit:
                    sign = -1
                if err != 0:
                    chi2 = ((val - fit) / err) ** 2
                else:
                    chi2 = 0
                
                
                compare.SetBinContent(i, sign * chi2)
                compare.SetBinError(i, 0)
            compare.GetXaxis().SetRangeUser(self.xRange[0],self.xRange[1])
            compare.SetFillColor(ROOT.kRed)
            compare.SetLineColor(ROOT.kBlack)
            compare.SetLineWidth(2)
            compare.GetYaxis().SetTitle("signed #chi^{2}")
            self.stuffToKeep.Add(compare)
            return compare
            
        else:
            raise(TypeError("You passed me a ", type(denumerator), "which I can't handle :("))
            return None


    def calcBottomTitleOffset(self):
        '''
        @brief calculates the label offset which depends on the margin size of the pad

        function needs to be changed due to the 2nd pad changing things
        '''
        if self.pad1 == None:
            raise(AttributeError("calcBottomTitleOffset: No pad exists (yet)"))

        bottom_margin = self.pad1.GetBottomMargin()

        '''
        This has been calculated by trial and error. Will unlikely
        give decent results if the margin size is less than 0.1 or more than 0.3
        '''
        target_offset = 2 + 4 * bottom_margin
        
        aspect_ratio = self.canvas.GetXsizeReal()/self.canvas.GetYsizeReal()

        aspect_corr = (2 - aspect_ratio) * 0.15


        # print(aspect_ratio, aspect_corr)

        target_offset += aspect_corr 
        return(target_offset)

        
    def __del__(self):
        del(self.pad1)
        del(self.pad2)

    