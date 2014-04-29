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


class plotBase(object):
    '''
    @brief A class for holding objects to be drawn and to draw them 
    Handle for all the functions, can hold plots and stuff

    This class is kind of abstract. To do actual plotting look at the classes which actually inherit from this one like simplePlotHolder
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
        self.size=0.04


        self.stuffToDraw = []
        self.logy = False
        self.pad1 = self.pad2 = None
        self.stuffToKeep = TList()
        self.y_up_mult=1.1
        self.y_down_mult = 1.1
        self.xRange = (0, 0)
        self.yRange = (0, 0) #only used for 2D histograms
        
        
        self.xTitle = "Every time you forget the title, god kills a Phd student"
        self.yTitle = "I am a lazy student"

        self.area_first_pad_corr = 1 #this is to make the stuff on smaller pads appear the same size due to root nastyness FIXME: find a better explanation
        
                
        gc.disable() # this will make the python garbage collection stop trying to clean up root objects
    def bookCanvas(self, xSize=1600, ySize=900):
        '''
        @brief book a ROOT TCanvas
        @param xSize: size (in pixels) in the horizontal direction 
        @param ySize: size (in pixels) in the vertical direction
        '''
        self.canvas = TCanvas("TuDoUtils Canvas", "TuDoUtils Canvas", 10, 10, xSize, ySize)

        self.pad1 = TPad("pad1", "pad1", 0, 0, 1, 1, 0, 0, 0)
        
    def saveCanvas(self, fileName):
        '''
        @brief: save the canvas to a file
        @param fileName: Target filename. ROOT will detect filetype by ending (e.g. .pdf will make a pdf) 
        '''
        if self.canvas is None:
            raise(AttributeError("No canvas found, cannot save!"))
        if type(fileName) != type(str()):
            raise(TypeError(str(fileName)+"is not a string!"))
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
        # '''
        textsize*=self.area_first_pad_corr
        if self.canvas is None:
            raise(AttributeError("No canvas to paint on!"))
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
        add = 1.5*size + 0.015


        if self.addText(str(addText), xPos + add, yPos, ROOT.kBlack,size) is None:
            print("Failed to print ATLAS extra text")
            return None
        
        l = TLatex()
        l.SetNDC()
        l.SetTextAlign(12)
        l.SetTextFont(72)
        l.SetTextSize(size*self.area_first_pad_corr)
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
            raise(TypeError("This plotClass is configured to be 2D. Cannot add 1D Object"))
        plotType = type(thing)
        if plotType not in [type(errorBarHist()), type(errorBarStack()), type(TGraph()), type(TGraphErrors()), type(TH1D()), type(TH1F()), type(THStack()), type(TF1())]:
            raise(TypeError(plotType, "is not drawable (in 1D) :("))
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
            raise(TypeError("This plotClass is configured to be 1D. Cannot add 2D Object"))
        plotType = type(thing)
        if plotType not in [type(TH2D()), type(TH2F())]:
            raise(TypeError(plotType, "is not drawable (in 2D) :("))
        self.is2D=1
        self.stuffToDraw.append(toDraw(thing, label, style))
        

        
    def resetPlots(self):
        '''
        @brief This removes all plots and all other things from the lists
        '''
        
        self.stuffToDraw = []
        
        self.stuffToKeep = TList()
        
    def drawPlots(self, xPos=0.725, yPos=0.80, index=1):
        raise(NotImplementedError("This class is kind of abstract (the python way). To draw plots use a class which inherits from this one"))    

    
    def __del__(self):
        for stuff in self.stuffToKeep:
            del(stuff)
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
            utils.addMarkerText(self.label, xPos, yPos, self.thingToDraw.GetMarkerStyle(), self.thingToDraw.GetMarkerColor(), labelsize)
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



