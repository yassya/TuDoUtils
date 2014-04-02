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

from TuDoUtils.errorBars import *

'''
 
'''


class plotClass(object):
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
        
        gStyle.SetHatchesSpacing(2.3)
        gStyle.SetHatchesLineWidth(1)
        
        self.canvas = None
        self.doRatio = False
        self.ratioRange = 0.25
        self.size=0.04
        self.ratioType = "EY"
        self.pads = []
        self.stuffToDraw = []
        self.logy = False
        self.pad1 = self.pad2 = None
        self.stuffToKeep = TList()
        self.y_up_mult=1.3
        self.y_down_mult = 0
        self.xRange = (0, 0)
        self.yRange = (0, 0) #only used for 2D histograms
        self.is2D=-1 # -1 means unspecified
        
        self.xTitle = "Every time you forget the title, god kills a Phd student"
        self.yTitle = "I am a lazy student"
        
        """
        The next flags only matter if doRatio is True
        """
        self.doMCoverData=False
        self.centerUncertAtZero=True
        self.ratioRange = 0.25
        self.ratioType = "EY"
        self.ratioTitle="rel. difference"
        
                
        gc.disable() # this will make the python garbage collection stop trying to clean up root objects
    def bookCanvas(self, xSize=1600, ySize=900):
        '''
        @brief book a ROOT TCanvas
        @param xSize: size (in pixels) in the horizontal direction 
        @param ySize: size (in pixels) in the vertical direction
        '''
        self.canvas = TCanvas("TuDoUtils Canvas", "TuDoUtils Canvas", 10, 10, xSize, ySize)

        if self.doRatio == True:
       
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
            

            



#            self.pad1 = pad1
#            self.pad1.Draw()

            

        else:
            self.pad1 = TPad("pad1", "pad1", 0, 0, 1, 1, 0, 0, 0)
#            self.pad1 = pad

#            self.pad1.Draw()

#            self.pad1.Draw()


#        if len(self.pads) > 0:
#            self.pads[0].Draw()
#            if self.logy == True:
#                self.pads[0].SetLogy()
        
            
        
    def saveCanvas(self, fileName):
        '''
        @brief: save the canvas to a file
        @param fileName: Target filename. ROOT will detect filetype by ending (e.g. .pdf will make a pdf) 
        '''
        if self.canvas is None:
            print ("No canvas found, cannot save!")
            return None
        if type(fileName) != type(str()):
            print (fileName, "is not a string!")
            return None
        self.canvas.SaveAs(fileName)
        
    
    def addText(self, text, xPos, yPos, color=ROOT.kBlack, textsize=0.05, angle=0):
        '''
        @brief: adds text at (xPos,yPos) in color and size on the canvas
        @param text: Text to be drawn
        @param xPos: Fractional horizontal poisition on the canvas (0 is leftmost, 1 is rightmost)  
        @param yPos: Fractional vertical poisition on the canvas (1 is topmost, 0 is bottommost)
        @param color: Color of the text. Default is black
        @param textsize: Size of the text
        @param angle: Angle of the text. The default, 0, is horizontal  
        '''
        if self.canvas is None:
            print("No canvas to paint on!")
            return None
        l = TLatex()
        l.SetTextAlign(12)
        l.SetNDC()
        l.SetTextColor(color)
        l.SetTextSize(textsize)
        l.SetTextAngle(angle)
        l.DrawLatex(xPos, yPos, text)
        return 0
        
    def addBoxText(self, text, xPos, yPos, boxsize, color, fillstyle=1001):
        '''
        @brief: adds a box with text at (xPos,yPos) in color and boxsize on the canvas
        @param text: Text to be added
        @param xPos: Fractional horizontal poisition on the canvas (0 is leftmost, 1 is rightmost)  
        @param yPos: Fractional vertical poisition on the canvas (1 is topmost, 0 is bottommost)
        @param boxsize: Size of the bpx
        @param color: Color of the box.
        @param fillstyle: Style of the box content. Default is fine.  
        
        '''        
        
        if self.addText(text, xPos, yPos, ROOT.kBlack, boxsize * 0.9) is None:
            print("Failed to add text for Box")
            return None
        
        y1 = yPos - boxsize * 0.5 
        y2 = yPos + boxsize * 0.5 
        x2 = xPos - boxsize * 0.4
        x1 = x2 - boxsize 


        mbox = TPave(x1, y1, x2, y2, 0, "NDC")
        mbox.SetFillColor(color)
        mbox.SetFillStyle(fillstyle)
        mbox.SetBorderSize(1)
        self.stuffToKeep.Add(mbox)

        mbox.Draw()
        
        
    def addMarkerText(self, text, xPos, yPos, style, color, size=0.04):
        '''
        @brief adds a marker with text at (xPos,yPos) in color and size on the canvas
        @param text: Text to be added
        @param xPos: Fractional horizontal poisition on the canvas (0 is leftmost, 1 is rightmost)  
        @param yPos: Fractional vertical poisition on the canvas (1 is topmost, 0 is bottommost)
        @param style: Style of the marker. See ROOT.TAttStyle for details
        @param color: Color of the marker
        @param size: Size of the object  
        '''
        
        if self.addText(text, xPos, yPos, ROOT.kBlack, size * 0.9) is None:
            print("Failed to add text for Marker")
            return None
        
        marker = TMarker(xPos - (0.035), yPos, 8)
        marker.SetMarkerColor(color)
        marker.SetNDC()
        marker.SetMarkerStyle(style)
        marker.SetMarkerSize(size * 50)
        self.stuffToKeep.Add(marker)
        marker.Draw()
        
    def addLineText(self, text, xPos, yPos, style, color, size=0.04):
        '''
        @brief adds a line with text at (xPos,yPos) in color and size on the canvas
        @param text: Text to be added
        @param xPos: Fractional horizontal poisition on the canvas (0 is leftmost, 1 is rightmost)  
        @param yPos: Fractional vertical poisition on the canvas (1 is topmost, 0 is bottommost)
        @param style: Style of the marker. See ROOT.TAttLine for details
        @param color: Color of the marker
        @param size: Size of the object  
        '''
        
        if self.addText(text, xPos, yPos, ROOT.kBlack, size * 0.9) is None:
            print("Failed to add text for Marker")
            return None
        
        line = TLine(xPos - (0.055), yPos,xPos - (0.015),yPos)
        #print(color)
        line.SetLineColor(color)
        line.SetNDC()
        line.SetLineStyle(style)
        line.SetLineWidth(2)
        self.stuffToKeep.Add(line)
        line.Draw()
        
    def addATLASLabel(self, xPos, yPos, addText="Internal", size=0.04):
        '''
        @brief adds a ATLAS label at (xPos,yPos) to the canvas
        @param xPos: Fractional horizontal poisition on the canvas (0 is leftmost, 1 is rightmost)  
        @param yPos: Fractional vertical poisition on the canvas (1 is topmost, 0 is bottommost)
        @param addYext: Text to be added next to the label
        @param size: Size of the text

        '''  
        add = 0.8/100./size
        
        if self.doRatio:
            add /= 1.35

        if self.addText(str(addText), xPos + add, yPos, ROOT.kBlack,size) is None:
            print("Failed to print ATLAS extra text")
            return None
        
        l = TLatex()
        l.SetNDC()
        l.SetTextAlign(12)
        l.SetTextFont(72)
        l.SetTextSize(size)
        l.SetTextColor(1)
        text = "ATLAS"
        l.DrawLatex(xPos, yPos, text)
        
    def addPlot1D(self, thing, label, style):
        '''
        @brief This adds a TH1*, THStack, TGraph, or TF1 to the drawList..
        @param thing: The object to be added
        @param label: Label for the legend
        @param style: ROOT-Draw() Style for that object  
        '''
        if self.is2D==1:
            print("This plotClass is configured to be 2D. Cannot add 1D Object")
            return None
        plotType = type(thing)
        if plotType not in [type(errorBarHist()), type(errorBarStack()), type(TGraph()), type(TGraphErrors()), type(TH1D()), type(TH1F()), type(THStack()), type(TF1())]:
            print(plotType, "is not drawable (in 1D) :(")
            return None
        self.is2D=0
        self.stuffToDraw.append(toDraw(thing, label, style))
        
        
    def addPlot2D(self, thing, label, style):
        '''
        @brief This adds a TH2* to the drawList..
        @param thing: The object to be added
        @param label: Label for the legend
        @param style: ROOT-Draw() Style for that object  
        '''
        if self.is2D==0:
            print("This plotClass is configured to be 1D. Cannot add 2D Object")
            return None
        plotType = type(thing)
        if plotType not in [type(TH2D()), type(TH2F())]:
            print(plotType, "is not drawable (in 2D) :(")
            return None
        self.is2D=1
        self.stuffToDraw.append(toDraw(thing, label, style))
        

        
    def resetPlots(self):
        '''
        @brief This removes all plots and all other things from the lists
        '''
        
        self.stuffToDraw = []
        
        self.stuffToKeep = TList()
        
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

        
        if self.pad2 is not None:
            self.pad1.Draw()
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
            
            if self.doRatio is True:
                pass
            else:
                
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
            
#        self.addATLASLabel(0.16, 0.85)
        
        residualslist = []
        if self.doRatio == True:
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
                    thePlot.GetXaxis().SetLabelSize(50)
                    thePlot.GetXaxis().SetTitleFont(43)
                    thePlot.GetXaxis().SetLabelSize(self.size*1000)
                    thePlot.GetXaxis().SetTitleSize(self.size*1600)
                    thePlot.GetXaxis().SetLabelOffset(0.01)
                    if self.canvas.GetAspectRatio() > 1:
                        thePlot.GetYaxis().SetTitleOffset(2.5)
                        thePlot.GetXaxis().SetTitleOffset(2.5)
                    else:
                        thePlot.GetYaxis().SetTitleOffset(1.8)
                        thePlot.GetXaxis().SetTitleOffset(2.5)
                    
#                    

                    thePlot.GetYaxis().SetTitleSize(self.size*1000)
                    if type(thePlot) is not type(errorBarStack()):
                        thePlot.GetYaxis().SetLabelSize(self.size*800)
                        if self.canvas.GetAspectRatio() > 1:
                            thePlot.GetYaxis().SetTitleOffset(2)
                        else:
                            thePlot.GetYaxis().SetTitleOffset(1.5)

#                        thePlot.GetYaxis().SetTitleOffset(2)     
                    else:
                        thePlot.GetYaxis().SetLabelSize(self.size*2)
                        
                        thePlot.GetYaxis().SetLabelSize(self.size*3.0)
                        thePlot.GetYaxis().SetTitleSize(self.size*3.0)     
                        
                        #thePlot.GetYaxis().SetTitleSize(labelsize)        
                        thePlot.GetYaxis().SetTitle("rel. difference")
                        if self.canvas.GetAspectRatio() > 1: #hochformat
                            thePlot.GetYaxis().SetTitleOffset(1.0)
                            #thePlot.GetYaxis().SetTitleOffset(0.75)
                        else: #querformat
                            #thePlot.GetYaxis().SetTitleOffset(0.8)
                            thePlot.GetYaxis().SetTitleOffset(0.55)
#thePlot.GetYaxis().SetTitleOffset(0.75)  
                        
                    
                    
                    thePlot.GetYaxis().SetLabelOffset(0.025)  
                    thePlot.GetYaxis().SetNdivisions(206, True);
                    thePlot.SetMarkerSize(self.size * 50)
                if len(self.stuffToDraw) is 2:

                    thePlot.SetMarkerSize(self.size * 50)

                    
                    
#                    thePlot.SetMarkerStyle(20)
                    
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
    def divide(self, numerator, denumerator):
        
        """
        @brief calculates ratio between numerator and denumerator, depending on tpye
        @param numerator: Numerator for the division
        @param denumerator: Denumerator for the division 
        
        @returns: Histogram with ratio
        """
        
        if type(denumerator) not in [type(TH1D()), type(TH1F())]:
            print("Can only compare with histograms right now, sorry :(")
            return None
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
            print("You passed me a ", type(denumerator), "which I can't handle :(")
            return None
        
        
        

    
        
class toDraw(object):
    '''
        @brief This is a handle for a thing to draw.. 
    '''
    def __init__(self, thing, label, style):
        self.size = 0.04
        self.thingToDraw = thing
        self.label = label
        self.style = style
        self.thingToDraw.SetTitle("")
        
        
    def drawPlot(self, opt):
        '''
        @brief draw the plot with its  style 
        @param opt:  Can add additional stuff to the drawstyle (most common is 'SAME')
        '''
        if type(self.thingToDraw) == type(TH1D()) or type(self.thingToDraw) == type(TH1F()):
            if "E" in self.style or "P" in self.style:
                self.thingToDraw.SetMarkerSize(self.size * 50)      
        self.thingToDraw.Draw(self.style + opt)
        
    def drawLabel(self, utils, xPos, yPos):
        '''
        @brief: draw the label, depending on type and linestyle
        @param utils: the plotClass object in use
        @param xPos: Fractional horziontal Position of the legend
        @param yPos: Fractional vertical Position of the legend
        '''
        labelsize = self.size*1.2
        if type(self.thingToDraw) == type(TH1D()) or type(self.thingToDraw) == type(TH1F()):
            if "E" in self.style or "P" in self.style: #lets see if this works as i want it too..
                
                if "E2" in self.style:
                    utils.addBoxText(self.label, xPos, yPos, labelsize, ROOT.kBlack, 3254)
                else:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.GetLineColor(), labelsize)
            elif "HIST" in self.style:
                if self.thingToDraw.GetFillColor() is ROOT.kWhite:
                    utils.addLineText(self.label, xPos, yPos, self.thingToDraw.GetLineStyle(), self.thingToDraw.GetLineColor(), labelsize)
                else:
                    utils.addBoxText(self.label, xPos, yPos, labelsize, self.thingToDraw.GetFillColor())
            return yPos - labelsize
        elif type(self.thingToDraw) == type(THStack()):
            yPos -= (len(self.thingToDraw.GetHists()) + 1) * labelsize
            for histo in self.thingToDraw.GetHists():
                if "nostack" in self.style:
                    utils.addBoxText(histo.GetTitle(), xPos, yPos, labelsize, histo.GetLineColor())
                else:
                    utils.addBoxText(histo.GetTitle(), xPos, yPos, labelsize, histo.GetFillColor())
                yPos += labelsize*1.05
            return yPos - (len(self.thingToDraw.GetHists()) + 1) * labelsize
        elif type(self.thingToDraw) == type(TGraph()) or type(self.thingToDraw) == type(TGraphErrors()):

            return(yPos - labelsize)
        elif type(self.thingToDraw) == type(errorBarStack()):
            yPos -= (len(self.thingToDraw.histo.GetHists()) + 1) * labelsize
            utils.addBoxText("uncertainty", xPos, yPos, labelsize, ROOT.kBlack, self.thingToDraw.errorHist.GetFillStyle())
            yPos += labelsize*1.1
            for histo in self.thingToDraw.histo.GetHists():
                utils.addBoxText(histo.GetTitle(), xPos, yPos, labelsize, histo.GetFillColor())
                yPos += labelsize*1.1
            
            
            return yPos - (len(self.thingToDraw.histo.GetHists()) + 2) * labelsize
        elif type(self.thingToDraw) == type(errorBarHist()):
            if "E" in self.style: #lets see if this works as i want it too..
                
                if "E2" in self.style:
                    utils.addBoxText(self.label, xPos, yPos, labelsize, ROOT.kBlack, 3254)
                else:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.histo.GetLineColor(), labelsize)
            elif "HIST" in self.style:
                if self.thingToDraw.histo.GetFillColor() is ROOT.kWhite:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.histo.GetLineColor(), labelsize)
                else:
                    utils.addBoxText(self.label, xPos, yPos, labelsize, self.thingToDraw.histo.GetFillColor())
            return yPos - labelsize
        elif  type(self.thingToDraw) == type(TH2D()) or type(self.thingToDraw) == type(TH2F()):
            if "BOX" in self.style:
                utils.addBoxText(self.label, xPos, yPos, labelsize, self.thingToDraw.GetFillColor())
                return yPos - labelsize
        else: # its a tf1 then...
            utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.GetLineColor(), labelsize)
            return yPos - labelsize



