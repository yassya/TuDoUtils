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




class errorBarHist(object):
    '''
    This class is for storing systematic errors associated with a histogram
    This allows it to draw the statistical and systematic errors separately in the same figure

    It works by first creating an instance with the histogram. Afterwards one can add 
    systematic variations with the two functions addUncertSingle and addUncertUpDown

    The class propagates all calls to ROOT functions used by other TuDoUtils packages
    to the nominal histogram
    '''
    def __init__(self, theHist=None):
        import gc
        gc.disable
        self.keepList = TList()

        if theHist == None:
            self.histo=None
            self.errorHist=None
        elif type(theHist)!=type(TH1F()) and type(theHist)!=type(TH1D()):
            raise(TypeError("errorBarHist needs to be initalized with a TH1X. Maybe you want errorBarStack instead?"))        

        else:
            self.histo = theHist
            self.errorHist = theHist.Clone(theHist.GetName() + "errors")
            self.errorHist.SetFillColor(self.errorHist.GetLineColor())
            self.keepList.Add(self.histo)
            self.keepList.Add(self.errorHist)
        
            theColor = self.errorHist.GetFillColor()
        
            if theColor % 2 == 0:
                self.errorHist.SetFillStyle(3154 + (self.errorHist.GetFillColor() % 2) * 100);
            else:
                self.errorHist.SetFillStyle(3145 + ((self.errorHist.GetFillColor() + 1) % 2) * 100);

    def addUncertUpDown(self, upHist, downHist):
        '''
        Add a systematic variation with a upwards and a downwards shift
        The uncertainty is half the difference between the two provided histograms
        '''
        if self.errorHist is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        if type(upHist) != type(TH1F()) and type(upHist) != type(TH1D()):
            raise(TypeError("The upwards variation is not a histogram!"))
        if type(downHist) != type(TH1F()) and type(downHist) != type(TH1D()):
            raise(TypeError("The downwards variation is not a histogram!"))

        upHist.Add(downHist, -1)
        for x in range(self.errorHist.GetNbinsX()):
            oldError = self.errorHist.GetBinError(x)
            addError = upHist.GetBinContent(x) / 2.
            newError = sqrt(oldError * oldError + addError * addError) 

            self.errorHist.SetBinError(x, newError)
    
    def addUncertSingle(self, theHist):
        '''
        Add a systematic variation with a single shift
        The uncertainty is the *full* difference between the provided histogram
        and the nominal histogram
        '''
        if self.errorHist is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        if type(theHist) != type(TH1F()) and type(theHist) != type(TH1D()):
            raise(TypeError("The downwards variation is not a histogram!"))
        theHist.Add(self.histo, -1)
        for x in range(self.errorHist.GetNbinsX()):
            oldError = self.errorHist.GetBinError(x)
            addError = theHist.GetBinContent(x) # /2. ? its difficult
            newError = sqrt(oldError * oldError + addError * addError) 

            self.errorHist.SetBinError(x, newError)
    

    def Draw(self, drawOpt):
        
        if self.errorHist is None or self.histo is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        self.histo.Draw(drawOpt)    

        self.errorHist.Draw("E2SAME")
        
    def SetTitle(self, title):
        self.histo.SetTitle(title)

    def GetMaximum(self):
        return self.histo.GetMaximum()
    def GetMinimum(self):
        return self.histo.GetMinimum()
    def GetXaxis(self):
        return self.histo.GetXaxis()
    def GetYaxis(self):
        return self.histo.GetYaxis()
    
    def SetMinimum(self, minimum):
        self.histo.SetMinimum(minimum)
    def SetMaximum(self, maximum):
        self.histo.SetMaximum(maximum)
    def SetMarkerStyle(self, size):
        self.histo.SetMarkerStyle(size)
    def SetMarkerSize(self, size):
        self.histo.SetMarkerSize(size)
    def SetLineColor(self, size):
        self.histo.SetLineColor(size)
    
    
    def Add(self, addHist):
        if self.errorHist is None or self.histo is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        if addHist is None:
            raise(AttributeError("Got no histogram to add. Please be careful"))
        self.histo.Add(addHist.histo)
        for i in self.errorHist.GetNbinsX():
            oldError = self.errorHist.GetBinError(i)
            addError = addHist.errorHist.GetBinError(i) # /2. ? its difficult
            newError = sqrt(oldError * oldError + addError * addError) 
            self.errorHist.SetBinError(i, newError)
            self.errorHist.SetBinContent(i, self.errorHist.GetBinContent(i) + addHist.errorHist.GetBinContent(i))
        
class errorBarStack(object):
    def __init__(self, theHist=None):
        '''
        This class is for storing systematic errors associated with a histogram *stack*
        This allows it to draw the statistical and systematic errors separately in the same figure

        It works by first creating an instance with the stack. Afterwards one can add 
        systematic variations with the two functions addUncertSingle and addUncertUpDown

        ******************************************************************************************
        IMPORTANT: even though the constructor must be called with a THStack, the variations
        still must be TH1* objects!!!
        ******************************************************************************************
        
        The class propagates all calls to ROOT functions used by other TuDoUtils packages
        to the nominal histogram
        '''


        import gc
        gc.disable
        if theHist == None:
            self.histo=None
            self.errorHist=None
        elif type(theHist)!=type(THStack()):
            raise(TypeError("errorBarStack needs to be initalized with a THStack. Maybe you want errorBarHist instead?"))        
        else:
            self.histo = theHist
            self.errorHist = None
            for hist in self.histo.GetHists():
                if self.errorHist is None:
                    self.errorHist = hist.Clone("errors")
                else:
                    self.errorHist.Add(hist)
            self.errorHist.SetFillColor(ROOT.kBlack)
            theColor = self.errorHist.GetFillColor()
            
            if theColor % 2 == 0:
                self.errorHist.SetFillStyle(3154 + (self.errorHist.GetFillColor() % 2) * 100);
            else:
                self.errorHist.SetFillStyle(3145 + ((self.errorHist.GetFillColor() + 1) % 2) * 100);

    def addUncertUpDown(self, upHist, downHist):
        '''
        Add a systematic variation with a upwards and a downwards shift
        The uncertainty is half the difference between the two provided histograms
        '''
        if self.errorHist is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        if type(upHist) != type(TH1F()) and type(upHist) != type(TH1D()):
            raise(TypeError("The upwards variation is not a histogram!"))
        if type(downHist) != type(TH1F()) and type(downHist) != type(TH1D()):
            raise(TypeError("The downwards variation is not a histogram!"))
        upHist.Add(downHist, -1)
        for x in range(self.errorHist.GetNbinsX()):
            oldError = self.errorHist.GetBinError(x)
            addError = upHist.GetBinContent(x) / 2.
            newError = sqrt(oldError * oldError + addError * addError) 
#            if x == 0:
#                print(oldError, addError, newError)
            self.errorHist.SetBinError(x, newError)
    
    def addUncertSingle(self, theHist):
        '''
        Add a systematic variation with a single shift
        The uncertainty is the *full* difference between the provided histogram
        and the nominal histogram
        '''
        if self.errorHist is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        if type(theHist) != type(TH1F()) and type(theHist) != type(TH1D()):
            raise(TypeError("The downwards variation is not a histogram!"))
        theHist.Add(self.errorHist, -1)
        for x in range(self.errorHist.GetNbinsX()):
            oldError = self.errorHist.GetBinError(x)
            addError = theHist.GetBinContent(x) # /2. #? its difficult
            newError = sqrt(oldError * oldError + addError * addError) 
#            if x == 0:
#                print(oldError, addError, newError)
            self.errorHist.SetBinError(x, newError)
    

    def Draw(self, drawOpt):
        
        if self.errorHist is None or self.histo is None:
            raise(AttributeError("Got no histogram. Please be careful"))
        self.histo.Draw(drawOpt)    
        
        self.errorHist.GetXaxis().SetRangeUser(self.histo.GetXaxis().GetXmin(), self.histo.GetXaxis().GetXmax())
        
        
        self.errorHist.Draw("E2SAME")
        
    def SetTitle(self, title):
        
        self.histo.SetTitle(title)

    def GetMaximum(self):
        
        return self.histo.GetMaximum()
    def GetMinimum(self):
        
        return self.histo.GetMinimum()
    def GetXaxis(self):
        return self.histo.GetXaxis()
    def GetYaxis(self):
        return self.histo.GetYaxis()
    
    def SetMinimum(self, minimum):
        
        self.histo.SetMinimum(minimum)
    def SetMaximum(self, minimum):
        self.histo.SetMaximum(minimum)
    def SetMarkerStyle(self, size):
        self.histo.SetMarkerStyle(size)
    def SetMarkerSize(self, size):
        self.histo.SetMarkerSize(size)
    def SetLineColor(self, size):
        self.histo.SetLineColor(size)
    def Add(self, addHist):
        
        i = 0
        addHists = addHist.histo.GetHists()
        for h in self.histo.GetHists():
            h.Add(addHists[i])
            i += 1
        
        for x in range(self.errorHist.GetNbinsX()):
            oldError = self.errorHist.GetBinError(x)
            addError = addHist.errorHist.GetBinError(x) # /2. ? its difficult
            newError = sqrt(oldError * oldError + addError * addError) 
            self.errorHist.SetBinError(x, newError)
            self.errorHist.SetBinContent(x, self.errorHist.GetBinContent(x) + addHist.errorHist.GetBinContent(x))
