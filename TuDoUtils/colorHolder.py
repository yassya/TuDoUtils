import ROOT
class colorHolder(object):
    def __init__(self):
        self.colorList = [ROOT.kRed, ROOT.kBlue,ROOT.kBlack, ROOT.kGreen - 6, ROOT.kMagenta+2, ROOT.kOrange, ROOT.kAzure+4] * 10
        self.index=0
        
    def getColor(self):
        col = self.colorList[self.index]
        self.index+=1
        return col
