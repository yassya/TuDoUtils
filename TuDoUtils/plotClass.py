'''
 <TuDoUtils --- A program for some nice plotting with ROOT.>
    Copyright (C) 2013  Christian Jung

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
from ROOT import TCanvas, TH1D, TH1F, THStack, TF1, TLatex, TPave, TMarker, TPad, TList, TLine, TGraph, TGraphErrors

from math import sqrt
import gc

from TuDoUtils.errorBars import *


class plotClass(object):
    '''
    Handle for all the functions, can hold plots and stuff
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.canvas = None
        self.doRatio = False
        self.ratioRange = 0.25
        self.pads = []
        self.stuffToDraw = []
        self.logy = False
        self.pad1 = self.pad2 = None
        self.stuffToKeep = TList()

        self.xRange = (0, 0)
        
        self.xTitle = "Every time you forget the title, god kills a Phd student"
        self.yTitle = "I am a lazy student"
        gc.disable() # this will make the python garbage collection stop trying to clean up root objects
    def bookCanvas(self, xSize=1600, ySize=900):
        self.canvas = TCanvas("TuDoUtils Canvas", "TuDoUtils Canvas", 10, 10, xSize, ySize)

        if self.doRatio == True:

            self.pad2 = TPad("pad2", "pad2", 0, 0, 1, 0.35, 0, 0, 0)
            self.pad2.SetGridy(1)
            self.pad2.SetTopMargin(0)
            self.pad2.SetBottomMargin(0.16 * 20. / 7.)
            self.pad2.SetLeftMargin(0.12)
            self.pad2.SetRightMargin(0.05)
            

            
            self.pad1 = TPad("pad1", "pad1", 0, 0.35, 1, 1, 0, 0, 0)
            self.pad1.SetTopMargin(0.05 * 20. / 13.)
            self.pad1.SetBottomMargin(0)
            self.pad1.SetLeftMargin(0.12)
            self.pad1.SetRightMargin(0.05)

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
        if self.canvas is None:
            print ("No canvas found, cannot save!")
            return None
        if type(fileName) != type(str()):
            print (fileName, "is not a string!")
            return None
        self.canvas.SaveAs(fileName)
        
    
    def addText(self, text, xPos, yPos, color=ROOT.kBlack, textsize=0.05):
        '''
        adds text at (xPos,yPos) in color and size on the canvas
        '''
        if self.canvas is None:
            print("No canvas to paint on!")
            return None
        l = TLatex()
        l.SetTextAlign(12)
        l.SetNDC()
        l.SetTextColor(color)
        l.SetTextSize(textsize)
        l.DrawLatex(xPos, yPos, text)
        return 0
        
    def addBoxText(self, text, xPos, yPos, boxsize, color, fillstyle=1001):
        '''
        adds a box with text at (xPos,yPos) in color and boxsize on the canvas
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
        adds a marker with text at (xPos,yPos) in color and size on the canvas
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
        
    def addATLASLabel(self, xPos, yPos, addText="Internal"):
        
        add = 0.12
        if self.doRatio:
            add /= 1.35
        if self.addText(str(addText), xPos + add, yPos, ROOT.kBlack) is None:
            print("Failed to print ATLAS extra text")
            return None
        
        l = TLatex()
        l.SetNDC()
        l.SetTextAlign(12)
        l.SetTextFont(72)
        l.SetTextColor(1)
        text = "ATLAS"
        l.DrawLatex(xPos, yPos, text)
        
    def addPlot1D(self, thing, label, style):
        '''
        This adds a TH1, THStack or TF1 to the drawList..
        '''
        plotType = type(thing)
        if plotType not in [type(errorBarHist()), type(errorBarStack()), type(TGraph()), type(TGraphErrors()), type(TH1D()), type(TH1F()), type(THStack()), type(TF1())]:
            print(plotType, "is not drawable :(")
            return None
        self.stuffToDraw.append(toDraw(thing, label, style))
        
        
    def resetPlots(self):
        '''
        This removes all plots and all other things from the lists
        '''
        
        self.stuffToDraw = []
        
        self.stuffToKeep = TList()
        
    def drawPlots(self, xPos=0.725, yPos=0.80, index=1):
        '''
        This draws all the objects which where added with addPlot 
        and builds a legend.
        
        if self.doRatio is True it will also draw the ratio of the things, w.r.t
        to the (index-1)'th element in the list it got to draw,
        which is the index'th elemtent which was added
        
        xPos and yPos are the position of the legend  
        '''
        if len(self.stuffToDraw) == 0:
            print("Nothing to draw!")
            return None
        if len(self.stuffToDraw) < 2 and self.doRatio == True:
            print("Too much stuff or to little stuff for a ratio...")
            return None
        
        if self.canvas is None:
            print("You did not book a canvas. I will do that for you")
            self.bookCanvas()
        
        self.canvas.Clear() #just in case someone did not do that..

        
        if self.pad2 is not None:
            self.pad2.Draw()
            
            self.pad1.Draw()
            self.pad1.cd()
        maximum = 0
        
        for plot in self.stuffToDraw:
            if plot.thingToDraw.GetMaximum() * 1.3 > maximum:
                maximum = plot.thingToDraw.GetMaximum() * 1.3
        
        same = ""
        for plot in self.stuffToDraw:
            
            if self.doRatio is True:
                pass
            else:
                
                if type(plot.thingToDraw) is not type(THStack()):
                    plot.thingToDraw.GetXaxis().SetTitle(self.xTitle)
                    plot.thingToDraw.GetXaxis().SetLabelFont(43)
                    plot.thingToDraw.GetXaxis().SetLabelSize(50)
                    plot.thingToDraw.GetXaxis().SetTitleFont(43)
                    plot.thingToDraw.GetXaxis().SetTitleSize(50)
                    plot.thingToDraw.GetXaxis().SetTitleOffset(1)                    
            if type(plot.thingToDraw) is not type(THStack()) and type(plot.thingToDraw) is not type(errorBarStack()):
                plot.thingToDraw.GetYaxis().SetTitle(self.yTitle)
                plot.thingToDraw.GetYaxis().SetLabelFont(43)
                plot.thingToDraw.GetYaxis().SetLabelSize(50)
                plot.thingToDraw.GetYaxis().SetTitleFont(43)
                plot.thingToDraw.GetYaxis().SetTitleSize(50)
                        
                plot.thingToDraw.GetYaxis().SetTitleOffset(1)
                plot.thingToDraw.GetYaxis().SetLabelOffset(0.01)
                if self.xRange[0] is not self.xRange[1]:
                    plot.thingToDraw.GetXaxis().SetRangeUser(self.xRange[0], self.xRange[1])
            if type(plot.thingToDraw is not type(TGraph())):
                plot.thingToDraw.SetMinimum(0)
                plot.thingToDraw.SetMaximum(maximum)
            plot.drawPlot(same)     # first time same will be "" after that "SAME" 
            same = "SAME"       # which is the wanted behaviour :)
        self.stuffToDraw[0].drawPlot(same)
        for plot in self.stuffToDraw:
            yPos = plot.drawLabel(self, xPos, yPos) # return value will be next free y value
            
#        self.addATLASLabel(0.16, 0.85)
        
        if self.doRatio == True:
            self.pad2.cd()

            
            theRatio = self.stuffToDraw[index - 1]
            
            same = ""
            for ratioPlot in self.stuffToDraw:
                if theRatio == ratioPlot:
                    continue
                thePlot = ratioPlot.thingToDraw
                thePlot = self.divide(thePlot, theRatio.thingToDraw)
                if thePlot is None:
                    print("I failed to divide, skippin' that plot")
                    continue
                if same is "":
                    
                    thePlot.GetYaxis().SetRangeUser(-self.ratioRange, self.ratioRange)
                    thePlot.GetXaxis().SetTitle(self.xTitle)
                    thePlot.GetXaxis().SetLabelFont(43)
                    thePlot.GetXaxis().SetLabelSize(50)
                    thePlot.GetXaxis().SetTitleFont(43)
                    thePlot.GetXaxis().SetTitleSize(50)
                    thePlot.GetXaxis().SetTitleOffset(2.5)
                    thePlot.GetXaxis().SetLabelOffset(0.01)
#                    

                    thePlot.GetYaxis().SetTitleSize(30)
                    if type(thePlot) is not type(errorBarStack()):
                        thePlot.GetYaxis().SetLabelSize(30)
                        thePlot.GetYaxis().SetTitleOffset(1.5)     
                    else:
                        thePlot.GetYaxis().SetLabelSize(0.1)
                        thePlot.GetYaxis().SetTitleSize(0.1)        
                        thePlot.GetYaxis().SetTitle("rel. difference")
                        thePlot.GetYaxis().SetTitleOffset(0.5)  
                        
                    
                    
                    thePlot.GetYaxis().SetLabelOffset(0.01)  
                    thePlot.GetYaxis().SetNdivisions(206, True);
                if len(self.stuffToDraw) is 2:
                    thePlot.SetMarkerSize(2)
                    thePlot.SetMarkerStyle(20)
                    thePlot.SetLineColor(ROOT.kBlack)
                thePlot.Draw("EY" + same)
                same = "SAME"
            if self.xRange[0] is not self.xRange[1]:
                lineAtZero = TLine(self.xRange[0], 0, self.xRange[1], 0)
            else:
                lineAtZero = TLine(theRatio.thingToDraw.GetXaxis().GetXmin(), 0, theRatio.thingToDraw.GetXaxis().GetXmax(), 0)
            lineAtZero.SetLineWidth(3)
            lineAtZero.Draw("SAME")
            self.stuffToKeep.Add(lineAtZero)
            self.pad2.RedrawAxis()
        self.pad1.cd()
        self.pad1.RedrawAxis()
        self.canvas.RedrawAxis()
        
        
    def divide(self, numerator, denumerator):
        
        """
        calculates ratio between numerator and denumerator, depending on tpye
        
        returns: Histogram with ratio
        """
        
        if type(denumerator) not in [type(TH1D()), type(TH1F())]:
            print("Can only compare with histograms right now, sorry :(")
            return None
        if type(numerator) is type(TH1D()) or type(numerator) is type(TH1F()):
            compare = numerator.Clone("newNumerator")
            

            compare.Divide(denumerator)
            for i in range(compare.GetNbinsX()):
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
            self.stuffToKeep.Add(compare)
            compare.GetYaxis().SetTitle("rel. difference")
            return compare
        elif type(numerator) is type(errorBarHist()):
            compare = numerator.histo.Clone("newNumerator")
            compareError = numerator.errorHist.Clone("newErrorNumerator")
            

            compare.Divide(denumerator)
            compareError.Divide(denumerator)
            for i in range(compare.GetNbinsX()):
                compareError.SetBinContent(i, compareError.GetBinContent(i) - 1)
                compareError.SetBinError(i, compareError.GetBinError(i))#/denumerator.GetBinContent(i))
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
                
            compare.GetYaxis().SetTitle("rel. difference")    
            newCompare = errorBarHist()
            newCompare.histo = compare
            newCompare.errorHist = compareError
            self.stuffToKeep.Add(newCompare.histo)
            self.stuffToKeep.Add(newCompare.errorHist)
            
            return newCompare
        elif type(numerator) is type(errorBarStack()):
#            compare = numerator.errorHist.Clone("newNumerator")
            compare = None
            for hist in numerator.histo.GetHists():
                if compare is None:
                    compare = hist.Clone("newNumerator")
                else:
                    compare.Add(hist)
            

            compareError = numerator.errorHist.Clone("newErrorNumerator")
            
            compare.Divide(denumerator)
            compareError.Divide(denumerator)
            for i in range(compare.GetNbinsX()):
                compareError.SetBinContent(i, compareError.GetBinContent(i) - 1)
                compareError.SetBinError(i, compareError.GetBinError(i))#/denumerator.GetBinContent(i))
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
                
            compare.GetYaxis().SetTitle("rel. difference")    
            newCompare = errorBarStack()
            newCompare.histo = compare
            newCompare.errorHist = compareError
            self.stuffToKeep.Add(newCompare.histo)
            self.stuffToKeep.Add(newCompare.errorHist)
            
            return newCompare
        elif type(numerator) is type(THStack()):
            compare = denumerator.Clone("newNumerator")
            compare.Reset()
            for hist in numerator.GetHists():
                compare.Add(hist)
            compare.Divide(denumerator)
            for i in range(compare.GetNbinsX()):
                compare.SetBinContent(i, compare.GetBinContent(i) - 1)
            self.stuffToKeep.Add(compare)
            compare.GetYaxis().SetTitle("rel. difference")
            return compare
        elif type(numerator) is type(TF1()):
            
            compare = denumerator.Clone("newNumerator")
            compare.Reset()
            
            for i in range(compare.GetNbinsX()):
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
                if err is not 0:
                    chi2 = ((val - fit) / err) ** 2
                else:
                    chi2 = 0
                
                
                compare.SetBinContent(i, sign * chi2)
                compare.SetBinError(i, 0)
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
        This is a handle for a thing to draw.. 
    '''
    def __init__(self, thing, label, style):
        self.thingToDraw = thing
        self.label = label
        self.style = style
        self.thingToDraw.SetTitle("")
    def drawPlot(self, opt):
        '''
        draw the plot with its one style 
        and opt (most of the time "SAME"
        '''
        
        self.thingToDraw.Draw(self.style + opt)
        
    def drawLabel(self, utils, xPos, yPos):
        '''
        draw the label, depending on type and linestyle
        '''
        if type(self.thingToDraw) == type(TH1D()) or type(self.thingToDraw) == type(TH1F()):
            if "E" in self.style: #lets see if this works as i want it too..
                
                if "E2" in self.style:
                    utils.addBoxText(self.label, xPos, yPos, 0.04, ROOT.kBlack, 3254)
                else:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.GetLineColor(), 0.04)
            elif "HIST" in self.style:
                if self.thingToDraw.GetFillColor() is ROOT.kWhite:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.GetLineColor(), 0.04)
                else:
                    utils.addBoxText(self.label, xPos, yPos, 0.04, self.thingToDraw.GetFillColor())
            return yPos - 0.04
        elif type(self.thingToDraw) == type(THStack()):
            yPos -= (len(self.thingToDraw.GetHists()) + 1) * 0.04
            for histo in self.thingToDraw.GetHists():
                if "nostack" in self.style:
                    utils.addBoxText(histo.GetTitle(), xPos, yPos, 0.04, histo.GetLineColor())
                else:
                    utils.addBoxText(histo.GetTitle(), xPos, yPos, 0.04, histo.GetFillColor())
                yPos += 0.05
            return yPos - (len(self.thingToDraw.GetHists()) + 1) * 0.05
        elif type(self.thingToDraw) == type(errorBarStack()):
            yPos -= (len(self.thingToDraw.histo.GetHists()) + 2) * 0.04
            utils.addBoxText("uncertainty", xPos, yPos, 0.04, ROOT.kBlack, self.thingToDraw.errorHist.GetFillStyle())
            yPos += 0.05
            for histo in self.thingToDraw.histo.GetHists():
                utils.addBoxText(histo.GetTitle(), xPos, yPos, 0.04, histo.GetFillColor())
                yPos += 0.05
            
            
            return yPos - (len(self.thingToDraw.histo.GetHists()) + 2) * 0.05
        elif type(self.thingToDraw) == type(errorBarHist()):
            if "E" in self.style: #lets see if this works as i want it too..
                
                if "E2" in self.style:
                    utils.addBoxText(self.label, xPos, yPos, 0.04, ROOT.kBlack, 3254)
                else:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.histo.GetLineColor(), 0.04)
            elif "HIST" in self.style:
                if self.thingToDraw.histo.GetFillColor() is ROOT.kWhite:
                    utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.histo.GetLineColor(), 0.04)
                else:
                    utils.addBoxText(self.label, xPos, yPos, 0.04, self.thingToDraw.histo.GetFillColor())
            return yPos - 0.04
            
        else: # its a tf1 then...
            utils.addMarkerText(self.label, xPos, yPos, 8, self.thingToDraw.GetLineColor(), 0.04)



